#!/usr/bin/env bash
# Skill Base — Installer für Empfänger
# Lädt geteilte Claude Skills herunter und richtet täglich automatisches Update ein.
#
# Verwendung:
#   bash <(curl -fsSL https://raw.githubusercontent.com/sd624/skill-base/main/install.sh)

set -euo pipefail

# ── Konfiguration ──────────────────────────────────────────────────────────────
GITHUB_USER="sd624"
BOOTSTRAP_REPO="skill-base"
SKILL_REPOS=("skill-base-dozenten" "skill-base-admins")
SKILL_BASE_HOME="$HOME/.skill-base"
REPOS_DIR="$SKILL_BASE_HOME/repos"
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
LAUNCHD_LABEL="com.skillbase.update"
LAUNCHD_PLIST="$HOME/Library/LaunchAgents/${LAUNCHD_LABEL}.plist"
INSTALL_LOG="$SKILL_BASE_HOME/install.log"

# ── Optik ──────────────────────────────────────────────────────────────────────
RED=$'\033[0;31m'; GREEN=$'\033[0;32m'; YELLOW=$'\033[1;33m'
BLUE=$'\033[0;34m'; BOLD=$'\033[1m'; NC=$'\033[0m'

step() { printf "\n${BLUE}▶${NC} ${BOLD}%s${NC}\n" "$1"; }
ok()   { printf "  ${GREEN}✓${NC} %s\n" "$1"; }
warn() { printf "  ${YELLOW}⚠${NC} %s\n" "$1"; }
err()  { printf "  ${RED}✗${NC} %s\n" "$1" >&2; }
log()  { mkdir -p "$SKILL_BASE_HOME"; echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$INSTALL_LOG"; }

# ── Header ─────────────────────────────────────────────────────────────────────
cat <<'BANNER'

  ╭─────────────────────────────────────╮
  │    Skill Base — Installation        │
  ╰─────────────────────────────────────╯

BANNER

# ── 1. macOS-Check ─────────────────────────────────────────────────────────────
step "Prüfe System"
if [[ "$(uname -s)" != "Darwin" ]]; then
  err "Skill Base läuft aktuell nur auf macOS."
  exit 1
fi
ok "macOS $(sw_vers -productVersion)"

# ── 2. Homebrew-Check (nicht auto-installieren) ────────────────────────────────
if ! command -v brew &>/dev/null; then
  err "Homebrew ist nicht installiert."
  echo
  echo "  Bitte installiere Homebrew zuerst, indem du diesen Befehl ausführst:"
  echo
  echo "    /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
  echo
  echo "  Komme dann hierher zurück und führe den Skill-Base-Installer erneut aus."
  exit 1
fi
ok "Homebrew gefunden ($(brew --version | head -1))"

# ── 3. gh (GitHub CLI) installieren falls nötig ────────────────────────────────
if ! command -v gh &>/dev/null; then
  step "Installiere GitHub CLI (gh)"
  brew install gh
fi
ok "gh $(gh --version | head -1 | awk '{print $3}')"

# ── 4. GitHub-Login ────────────────────────────────────────────────────────────
if ! gh auth status &>/dev/null; then
  step "GitHub-Login"
  echo "  Gleich öffnet sich dein Browser zum Einloggen."
  echo "  Bitte folge den Anweisungen — der Installer wartet."
  echo
  read -r -p "  Drücke Enter, um fortzufahren..." _ </dev/tty
  gh auth login -h github.com -p https -w
fi
GH_USER="$(gh api user --jq .login)"
ok "Eingeloggt als ${BOLD}$GH_USER${NC}"

# ── 5. Verzeichnisstruktur ─────────────────────────────────────────────────────
step "Lege Verzeichnisstruktur an"
mkdir -p "$REPOS_DIR" "$CLAUDE_SKILLS_DIR"
ok "$SKILL_BASE_HOME"
ok "$CLAUDE_SKILLS_DIR"
log "Install gestartet (user=$GH_USER)"

# ── 6. Bootstrap-Repo klonen oder aktualisieren ────────────────────────────────
step "Hole Skill-Base-Tooling"
if [[ -d "$REPOS_DIR/$BOOTSTRAP_REPO/.git" ]]; then
  git -C "$REPOS_DIR/$BOOTSTRAP_REPO" pull --ff-only --quiet
  ok "$BOOTSTRAP_REPO aktualisiert"
else
  gh repo clone "$GITHUB_USER/$BOOTSTRAP_REPO" "$REPOS_DIR/$BOOTSTRAP_REPO" -- --quiet
  ok "$BOOTSTRAP_REPO geklont"
fi

# ── 7. Skill-Repos klonen (nur zugängliche) ────────────────────────────────────
step "Prüfe Zugriff auf Skill-Repos und klone"
declare -a ACCESSIBLE_REPOS=()
for repo in "${SKILL_REPOS[@]}"; do
  if gh repo view "$GITHUB_USER/$repo" &>/dev/null; then
    ACCESSIBLE_REPOS+=("$repo")
    if [[ -d "$REPOS_DIR/$repo/.git" ]]; then
      git -C "$REPOS_DIR/$repo" pull --ff-only --quiet
      ok "$repo aktualisiert"
    else
      gh repo clone "$GITHUB_USER/$repo" "$REPOS_DIR/$repo" -- --quiet
      ok "$repo geklont"
    fi
  else
    warn "$repo: kein Zugriff (überspringe — okay so, wenn du diese Rolle nicht hast)"
  fi
done

if [[ ${#ACCESSIBLE_REPOS[@]} -eq 0 ]]; then
  err "Du hast auf keines der Skill-Repos Zugriff."
  echo "  Bitte bei Simon (sd@kissconcepts.de) melden — du musst als"
  echo "  Collaborator eingeladen werden."
  exit 1
fi

# ── 8. Symlinks aufbauen (interaktiv bei Konflikten) ───────────────────────────
step "Verlinke Skills nach $CLAUDE_SKILLS_DIR"

handle_conflict() {
  local skill_name="$1" target="$2" src="$3" reason="$4"
  echo
  printf "  ${YELLOW}⚠ Konflikt:${NC} Skill '${BOLD}%s${NC}' (%s)\n" "$skill_name" "$reason"
  echo "    [s] Skip (vorhandenes belassen, Skill-Base-Version nicht verlinken)"
  echo "    [b] Vorhandenes als .backup umbenennen und Skill-Base-Version verlinken"
  echo "    [a] Abbruch"
  local choice=""
  while [[ ! "$choice" =~ ^[sba]$ ]]; do
    read -r -p "  Wahl (s/b/a): " choice </dev/tty
    choice="${choice,,}"
  done
  case "$choice" in
    s) log "Konflikt $skill_name: skip ($reason)"; warn "Skip: $skill_name" ;;
    b)
      local backup="${target}.backup-$(date +%Y%m%d-%H%M%S)"
      mv "$target" "$backup"
      ln -sfn "$src" "$target"
      log "Konflikt $skill_name: umbenannt zu $backup, neu verlinkt"
      ok "Verlinkt: $skill_name (Original als ${backup##*/})"
      ;;
    a) err "Abbruch durch User"; exit 1 ;;
  esac
}

for repo in "${ACCESSIBLE_REPOS[@]}"; do
  skills_src="$REPOS_DIR/$repo/skills"
  [[ -d "$skills_src" ]] || continue
  for skill_dir in "$skills_src"/*/; do
    [[ -d "$skill_dir" ]] || continue
    skill_name="$(basename "$skill_dir")"
    target="$CLAUDE_SKILLS_DIR/$skill_name"
    src="${skill_dir%/}"

    if [[ -L "$target" ]]; then
      current="$(readlink "$target")"
      if [[ "$current" == "$src" ]]; then
        ok "$skill_name (aktuell)"
      elif [[ "$current" == "$REPOS_DIR"/* ]]; then
        ln -sfn "$src" "$target"
        ok "$skill_name (Symlink aktualisiert)"
        log "Symlink aktualisiert: $skill_name"
      else
        handle_conflict "$skill_name" "$target" "$src" "fremder Symlink"
      fi
    elif [[ -e "$target" ]]; then
      handle_conflict "$skill_name" "$target" "$src" "vorhandener Ordner"
    else
      ln -sfn "$src" "$target"
      ok "$skill_name (neu verlinkt)"
      log "Symlink angelegt: $skill_name"
    fi
  done
done

# ── 9. LaunchAgent für tägliches Update ────────────────────────────────────────
step "Richte tägliches Auto-Update um 8:00 Uhr ein"
mkdir -p "$HOME/Library/LaunchAgents"
update_script="$REPOS_DIR/$BOOTSTRAP_REPO/update.sh"
chmod +x "$update_script"

plist_template="$REPOS_DIR/$BOOTSTRAP_REPO/launchagent/${LAUNCHD_LABEL}.plist.template"
if [[ ! -f "$plist_template" ]]; then
  err "Plist-Template fehlt: $plist_template"
  exit 1
fi

# Falls schon geladen: erst entladen
if launchctl print "gui/$UID/$LAUNCHD_LABEL" &>/dev/null; then
  launchctl bootout "gui/$UID/$LAUNCHD_LABEL" 2>/dev/null || true
fi

sed -e "s|{{LABEL}}|$LAUNCHD_LABEL|g" \
    -e "s|{{UPDATE_SCRIPT}}|$update_script|g" \
    -e "s|{{LOG_FILE}}|$SKILL_BASE_HOME/update.log|g" \
    "$plist_template" > "$LAUNCHD_PLIST"

launchctl bootstrap "gui/$UID" "$LAUNCHD_PLIST"
ok "LaunchAgent geladen — läuft täglich 8:00 + bei jedem Login"

# ── 10. Fertig ─────────────────────────────────────────────────────────────────
log "Install erfolgreich abgeschlossen"

cat <<SUCCESS

${GREEN}${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}
${GREEN}${BOLD}║  Skill Base ist eingerichtet!                                 ║${NC}
${GREEN}${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}

  ${BOLD}Aktive Repos:${NC}     ${ACCESSIBLE_REPOS[*]}
  ${BOLD}Repo-Clones:${NC}      $REPOS_DIR
  ${BOLD}Skill-Symlinks:${NC}   $CLAUDE_SKILLS_DIR
  ${BOLD}Auto-Update:${NC}      täglich 8:00 Uhr (per launchd)
  ${BOLD}Log:${NC}              $SKILL_BASE_HOME/update.log

  ${BOLD}Manuelles Update:${NC}
    $update_script

  ${BOLD}Test:${NC}
    Frage Claude einfach: "${BOLD}funktioniert hello-world?${NC}"

SUCCESS
