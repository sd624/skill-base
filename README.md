# Skill Base

Private Sammlung von Claude Skills, betrieben von [Simon](mailto:sd@kissconcepts.de). Diese Repo enthält nur den Installer und die Tooling-Scripts — die eigentlichen Skill-Inhalte liegen in privaten Repos und werden nach deiner Einladung automatisch geladen.

---

## Was ist das?

**Skill Base** liefert dir kuratierte [Claude Skills](https://docs.anthropic.com/en/docs/claude-code/skills) direkt in dein Claude — z. B. für Audio-Transkription, AZAV-Kursmodule oder Angebots-Standardisierung. Einmal installiert, aktualisieren sich deine Skills jeden Morgen um 8:00 Uhr automatisch.

---

## Voraussetzungen

1. **macOS** (aktuell ist nur Mac unterstützt)
2. **Homebrew** — falls nicht vorhanden, installierst du es vorher einmalig:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. **GitHub-Konto** — falls noch nicht vorhanden, registriere dich gratis bei [github.com](https://github.com). Dauert ca. 2 Minuten.
4. **Einladung von Simon** — schicke deinen GitHub-Username an [sd@kissconcepts.de](mailto:sd@kissconcepts.de). Simon lädt dich dann als Collaborator zu einem oder beiden privaten Skill-Repos ein. Die Einladung kommt per E-Mail von GitHub — bitte annehmen.

---

## Installation

Sobald die Einladung angenommen ist, öffne **Terminal** (Spotlight → "Terminal") und führe diesen einen Befehl aus:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/sd624/skill-base/main/install.sh)
```

Der Installer:
- prüft deine Voraussetzungen
- installiert die GitHub CLI (`gh`) falls nötig
- loggt dich bei GitHub ein (Browser öffnet sich automatisch)
- lädt die für dich freigeschalteten Skills herunter
- richtet automatisches tägliches Update um 8:00 Uhr ein

Bei Konflikten (z. B. du hast schon einen Skill mit gleichem Namen) fragt der Installer interaktiv, was er tun soll.

---

## Testen

Frage nach der Installation einfach Claude:

> funktioniert hello-world?

Wenn Claude dir antwortet, dass Skill Base läuft, ist alles okay.

---

## Was wird wo abgelegt?

| Pfad | Inhalt |
|------|--------|
| `~/.skill-base/repos/` | Geklonte Skill-Repos |
| `~/.claude/skills/` | Symlinks auf die Skills (von hier lädt Claude sie) |
| `~/.skill-base/update.log` | Log des Auto-Updaters |
| `~/Library/LaunchAgents/com.skillbase.update.plist` | LaunchAgent für tägliches Update |

Nichts liegt versteckt herum — du kannst alles inspizieren und jederzeit manuell aufräumen.

---

## Manuelles Update

Falls du nicht bis morgen warten willst:

```bash
~/.skill-base/repos/skill-base/update.sh
```

---

## Eigene Skills beisteuern

Du darfst Skills vorschlagen — der Workflow ist:

1. **Branch erstellen:**
   ```bash
   cd ~/.skill-base/repos/skill-base-dozenten   # oder -admins, je nachdem wo es hingehört
   git checkout -b mein-neuer-skill
   ```

2. **Skill anlegen:** Erstelle einen neuen Ordner unter `skills/<dein-skill-name>/` mit einer `SKILL.md`. Schau dir `hello-world/SKILL.md` als Vorlage an.

3. **Commit & Push:**
   ```bash
   git add skills/<dein-skill-name>
   git commit -m "Neuer Skill: <kurzbeschreibung>"
   git push -u origin mein-neuer-skill
   ```

4. **Pull Request öffnen:** Im Terminal:
   ```bash
   gh pr create --fill
   ```
   Oder auf github.com im Repo den Button "Compare & pull request" klicken.

5. **Warten:** Simon reviewt deinen PR und merged ihn — danach landet dein Skill beim nächsten Update bei allen Berechtigten.

Wenn du dir unsicher bist: einfach kurz Simon fragen.

---

## Deinstallation

```bash
# LaunchAgent stoppen
launchctl bootout "gui/$UID/com.skillbase.update" 2>/dev/null || true
rm -f ~/Library/LaunchAgents/com.skillbase.update.plist

# Symlinks aufräumen (entfernt nur die von Skill Base verlinkten)
for link in ~/.claude/skills/*; do
  [[ -L "$link" ]] && [[ "$(readlink "$link")" == "$HOME/.skill-base/repos/"* ]] && rm "$link"
done

# Daten löschen
rm -rf ~/.skill-base
```

---

## Hilfe

Bei Problemen oder Fragen: [sd@kissconcepts.de](mailto:sd@kissconcepts.de) — gerne mit Inhalt aus `~/.skill-base/update.log` als Anhang.
