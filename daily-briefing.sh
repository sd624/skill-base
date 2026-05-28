#!/usr/bin/env bash
# Skill Base — Skill-Übersicht (für SessionStart-Hook)
# Zeigt höchstens alle 2 Tage eine Übersicht der verfügbaren Skills + Status.
# Die Beschreibungen werden automatisch aus den SKILL.md gezogen — immer aktuell.

set -uo pipefail  # nicht -e, damit der Hook auch bei kleineren Problemen weiterläuft

SKILL_BASE_HOME="$HOME/.skill-base"
LAST_BRIEFING="$SKILL_BASE_HOME/last-briefing"
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
REPOS_DIR="$SKILL_BASE_HOME/repos"
INTERVAL_SECONDS=172800   # 2 Tage

# Skill Base ist evtl. noch nicht installiert — dann still beenden
[[ -d "$REPOS_DIR" ]] || exit 0

# Höchstens alle 2 Tage zeigen
now_epoch="$(date +%s)"
if [[ -f "$LAST_BRIEFING" ]]; then
  last_epoch="$(cat "$LAST_BRIEFING" 2>/dev/null || echo 0)"
  # last_epoch muss eine reine Zahl sein (ältere Versionen speicherten ein Datum → dann neu zeigen)
  if [[ "$last_epoch" =~ ^[0-9]+$ ]] && (( now_epoch - last_epoch < INTERVAL_SECONDS )); then
    exit 0
  fi
fi

# Ersten Satz der description aus einer SKILL.md ziehen.
# Versteht sowohl einzeilige (description: text) als auch mehrzeilige
# YAML-Formate (description: > bzw. | mit eingerückten Folgezeilen).
skill_description() {
  local md="$1"
  [[ -f "$md" ]] || { echo ""; return; }
  local desc
  desc="$(awk '
    /^description:/ {
      rest=$0
      sub(/^description:[ \t]*/, "", rest)
      if (rest=="" || rest==">" || rest=="|" || rest==">-" || rest=="|-") { collecting=1; next }
      print rest; exit
    }
    collecting==1 {
      if ($0 ~ /^[ \t]+/) {                            # eingerückte Folgezeile
        line=$0; sub(/^[ \t]+/, "", line)
        buf = buf (buf==""?"":" ") line
      } else { print buf; exit }                       # Block zu Ende (nächster Key / ---)
    }
    END { if (collecting==1 && buf!="") print buf }
  ' "$md")"
  desc="${desc%%. *}"                                  # ersten Satz (bis zum ersten ". ")
  if [[ ${#desc} -gt 120 ]]; then desc="${desc:0:117}..."; fi
  echo "$desc"
}

# Skill-Liste mit Kurzbeschreibung (alle Symlinks, die in unser Repo-Verzeichnis zeigen)
declare -a skill_lines=()
if [[ -d "$CLAUDE_SKILLS_DIR" ]]; then
  for link in "$CLAUDE_SKILLS_DIR"/*; do
    [[ -L "$link" ]] || continue
    target="$(readlink "$link")"
    case "$target" in
      "$REPOS_DIR"/*)
        name="$(basename "$link")"
        desc="$(skill_description "$target/SKILL.md")"
        if [[ -n "$desc" ]]; then
          skill_lines+=("- ${name} — ${desc}")
        else
          skill_lines+=("- ${name}")
        fi
        ;;
    esac
  done
fi

# Updates-Check (best effort)
updates_text="unbekannt"
if command -v git &>/dev/null; then
  total_behind=0
  for repo_dir in "$REPOS_DIR"/*/; do
    [[ -d "$repo_dir/.git" ]] || continue
    behind="$(git -C "$repo_dir" rev-list HEAD..@{u} --count 2>/dev/null || echo 0)"
    total_behind=$((total_behind + behind))
  done
  if [[ "$total_behind" -gt 0 ]]; then
    updates_text="ja ($total_behind neue Commits — sag \"update meine skills\")"
  else
    updates_text="nein, alles aktuell"
  fi
fi

count="${#skill_lines[@]}"

# Output (geht als Context an Claude — Claude soll es dem User zeigen)
{
  echo "[SKILL_BASE_BRIEFING]"
  echo
  echo "Skill-Base-Übersicht — bitte dem User zu Beginn dieser Session zeigen."
  echo "Falls der User direkt eine Aufgabe stellt, die Übersicht knapp ans Ende der ersten Antwort hängen."
  echo
  echo "Aktuell ${count} Skills aus Skill Base verfügbar:"
  echo
  for line in "${skill_lines[@]}"; do
    echo "$line"
  done
  echo
  echo "Updates verfügbar: ${updates_text}"
  echo
  echo "Befehle: \"update meine skills\" (sofort aktualisieren) · \"feedback zu <skill>: …\" (Rückmeldung an Simon)"
  echo
  echo "[/SKILL_BASE_BRIEFING]"
}

# Zeitstempel (Epoch) speichern
mkdir -p "$SKILL_BASE_HOME"
echo "$now_epoch" > "$LAST_BRIEFING"
