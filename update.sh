#!/usr/bin/env bash
# Skill Base — Update Script
# Wird täglich um 8:00 Uhr per launchd ausgeführt und kann jederzeit manuell laufen.
#
# Verwendung:
#   ~/.skill-base/repos/skill-base/update.sh

set -euo pipefail

# ── Konfiguration ──────────────────────────────────────────────────────────────
GITHUB_USER="sd624"
BOOTSTRAP_REPO="skill-base"
SKILL_REPOS=("skill-base-dozenten" "skill-base-admins")
SKILL_BASE_HOME="$HOME/.skill-base"
REPOS_DIR="$SKILL_BASE_HOME/repos"
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
LOG_FILE="$SKILL_BASE_HOME/update.log"

mkdir -p "$SKILL_BASE_HOME" "$CLAUDE_SKILLS_DIR"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "─── Update gestartet ───"

# ── 1. Voraussetzungen prüfen ──────────────────────────────────────────────────
if ! command -v gh &>/dev/null; then
  log "FEHLER: gh ist nicht installiert. Update wird abgebrochen."
  exit 1
fi

if ! gh auth status &>/dev/null; then
  log "FEHLER: gh ist nicht authentifiziert. Bitte 'gh auth login' ausführen."
  exit 1
fi

# ── 2. Alle Repos aktualisieren (Bootstrap + Skill-Repos) ──────────────────────
update_repo() {
  local repo="$1"
  local repo_path="$REPOS_DIR/$repo"

  if [[ ! -d "$repo_path/.git" ]]; then
    # Repo noch nicht da — versuche zu klonen, wenn zugreifbar
    if gh repo view "$GITHUB_USER/$repo" &>/dev/null; then
      log "Klone neues Repo: $repo"
      gh repo clone "$GITHUB_USER/$repo" "$repo_path" -- --quiet 2>>"$LOG_FILE"
      return 0
    else
      log "Kein Zugriff auf $repo — überspringe (okay, wenn diese Rolle nicht zutrifft)"
      return 1
    fi
  fi

  # Vorhanden — git pull
  local before after
  before="$(git -C "$repo_path" rev-parse HEAD 2>/dev/null || echo unknown)"

  if git -C "$repo_path" pull --ff-only --quiet 2>>"$LOG_FILE"; then
    after="$(git -C "$repo_path" rev-parse HEAD)"
    if [[ "$before" == "$after" ]]; then
      log "$repo: keine Änderungen"
    else
      log "$repo: aktualisiert ($before → $after)"
    fi
    return 0
  else
    log "$repo: git pull fehlgeschlagen (möglicher Konflikt — bitte manuell prüfen)"
    return 1
  fi
}

update_repo "$BOOTSTRAP_REPO" || true

declare -a ACTIVE_REPOS=()
for repo in "${SKILL_REPOS[@]}"; do
  if update_repo "$repo"; then
    ACTIVE_REPOS+=("$repo")
  fi
done

# ── 3. Symlinks resynchronisieren ──────────────────────────────────────────────
# Schritt 3a: Symlinks aufräumen, die auf nicht mehr existierende Repo-Skills zeigen
removed=0
if [[ -d "$CLAUDE_SKILLS_DIR" ]]; then
  for link in "$CLAUDE_SKILLS_DIR"/*; do
    [[ -L "$link" ]] || continue
    target="$(readlink "$link")"
    # nur Symlinks anfassen, die in unser Repo-Verzeichnis zeigen
    case "$target" in
      "$REPOS_DIR"/*)
        if [[ ! -e "$target" ]]; then
          rm "$link"
          log "Symlink entfernt (Ziel weg): $(basename "$link")"
          ((removed++)) || true
        fi
        ;;
    esac
  done
fi

# Schritt 3b: Symlinks für alle aktuellen Skills anlegen/aktualisieren
added=0
updated=0
conflicts=0

for repo in "${ACTIVE_REPOS[@]}"; do
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
        continue  # bereits korrekt
      fi
      if [[ "$current" == "$REPOS_DIR"/* ]]; then
        # alter Symlink aus unserem Repo-System — sicher zu aktualisieren
        ln -sfn "$src" "$target"
        log "Symlink aktualisiert: $skill_name"
        ((updated++)) || true
      else
        log "KONFLIKT (fremder Symlink): $skill_name → $current — übersprungen, bitte manuell klären"
        ((conflicts++)) || true
      fi
    elif [[ -e "$target" ]]; then
      log "KONFLIKT (vorhandener Ordner): $skill_name — übersprungen, bitte manuell klären"
      ((conflicts++)) || true
    else
      ln -sfn "$src" "$target"
      log "Symlink angelegt: $skill_name"
      ((added++)) || true
    fi
  done
done

log "Symlink-Sync: $added neu, $updated aktualisiert, $removed entfernt, $conflicts Konflikte"
log "─── Update beendet ───"
