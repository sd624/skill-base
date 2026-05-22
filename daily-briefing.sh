#!/usr/bin/env bash
# Skill Base — Daily Briefing (für SessionStart-Hook)
# Gibt einen kurzen Tagesstatus auf stdout aus. Wird einmal pro Tag gezeigt.

set -uo pipefail  # nicht -e, damit der Hook auch bei kleineren Problemen weiterläuft

SKILL_BASE_HOME="$HOME/.skill-base"
LAST_BRIEFING="$SKILL_BASE_HOME/last-briefing"
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
REPOS_DIR="$SKILL_BASE_HOME/repos"

# Skill Base ist evtl. noch nicht installiert — dann still beenden
[[ -d "$REPOS_DIR" ]] || exit 0

# Einmal pro Tag
today="$(date +%Y-%m-%d)"
if [[ -f "$LAST_BRIEFING" ]] && [[ "$(cat "$LAST_BRIEFING" 2>/dev/null)" == "$today" ]]; then
  exit 0
fi

# Skill-Liste (alle Symlinks, die in unser Repo-Verzeichnis zeigen)
declare -a skills=()
if [[ -d "$CLAUDE_SKILLS_DIR" ]]; then
  for link in "$CLAUDE_SKILLS_DIR"/*; do
    [[ -L "$link" ]] || continue
    target="$(readlink "$link")"
    case "$target" in
      "$REPOS_DIR"/*) skills+=("$(basename "$link")") ;;
    esac
  done
fi

# Updates-Check (best effort, schnell, ohne Auth-Refresh)
updates_text="unbekannt"
if command -v git &>/dev/null; then
  total_behind=0
  for repo_dir in "$REPOS_DIR"/*/; do
    [[ -d "$repo_dir/.git" ]] || continue
    behind="$(git -C "$repo_dir" rev-list HEAD..@{u} --count 2>/dev/null || echo 0)"
    total_behind=$((total_behind + behind))
  done
  if [[ "$total_behind" -gt 0 ]]; then
    updates_text="**ja** ($total_behind neue Commits seit letztem Update — sag \"update meine skills\")"
  else
    updates_text="nein, alles aktuell"
  fi
fi

# Letztes erfolgreiches Update (aus Log)
last_update="unbekannt"
if [[ -f "$SKILL_BASE_HOME/update.log" ]]; then
  last_update="$(grep -E "^\[.*\] ─── Update beendet ───$" "$SKILL_BASE_HOME/update.log" 2>/dev/null | tail -1 | sed -E 's/^\[(.{19})\].*/\1/')"
  [[ -z "$last_update" ]] && last_update="noch nie"
fi

# Output (geht als Context an Claude — Claude soll es dem User zeigen)
cat <<EOF
[SKILL_BASE_DAILY_BRIEFING $today]

Tagesstatus für Skill Base — bitte am Anfang dieser Session dem User mitteilen,
falls er noch keine andere Anfrage gestellt hat. Wenn er direkt eine Aufgabe stellt,
das Briefing knapp am Ende der ersten Antwort anhängen.

Verfügbare Skills (${#skills[@]}): ${skills[*]:-keine}
Letztes erfolgreiches Update: $last_update
Updates verfügbar: $updates_text

Verfügbare Skill-Base-Befehle für den User:
- "update meine skills" → manuell aktualisieren
- "feedback zu <skill-name>: <text>" → Feedback als GitHub-Issue an Simon

[/SKILL_BASE_DAILY_BRIEFING]
EOF

# Datum speichern
mkdir -p "$SKILL_BASE_HOME"
echo "$today" > "$LAST_BRIEFING"
