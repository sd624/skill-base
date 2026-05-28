# Skill Base — Einrichtung in 10 Minuten

Willkommen! Diese Anleitung richtet **Skill Base** auf deinem Mac ein. Danach hast du die geteilten Claude-Skills automatisch in deinem Claude, und sie aktualisieren sich jeden Morgen von selbst.

Du brauchst dafür **keine Programmierkenntnisse** — einfach Schritt für Schritt folgen.

---

## Voraussetzungen

- Ein **Mac** (macOS)
- **Claude Code** ist bei dir installiert und eingerichtet
- **Homebrew** (ein Helfer-Programm) — falls noch nicht vorhanden, installierst du es in Schritt 3
- Ca. 10 Minuten Zeit

---

## Schritt 1 — GitHub-Account anlegen (falls noch keiner)

GitHub ist die Plattform, über die die Skills sicher geteilt werden.

1. Gehe auf **[github.com](https://github.com)**
2. Klicke oben rechts auf **Sign up**
3. **Wichtig:** Verwende **genau die E-Mail-Adresse, an die Simon dir die Einladung geschickt hat** (z. B. deine `@kissconcepts.de`-Adresse). Nur dann wird die Einladung automatisch mit deinem neuen Account verknüpft.
4. Passwort wählen, Benutzernamen festlegen, E-Mail-Bestätigung von GitHub anklicken

> Schon einen Account mit deiner Firmen-Mail? Dann diesen Schritt überspringen.

### Reihenfolge spielt keine Rolle

Du kannst den Account **auch erst dann anlegen, wenn die Einladung schon da ist** — dann führt dich die Einladungs-E-Mail direkt durch die Registrierung (siehe Schritt 2). Wichtig ist nur: immer dieselbe E-Mail-Adresse verwenden.

---

## Schritt 2 — Einladung annehmen

Simon lädt dich zu den Skill-Repos ein. Du bekommst eine **E-Mail von GitHub** mit dem Betreff „… invited you to collaborate".

1. E-Mail öffnen
2. Auf **View invitation** (Einladung ansehen) klicken
3. Auf der GitHub-Seite **Accept invitation** (Einladung annehmen) klicken

Fertig — du hast jetzt Zugriff.

---

## Schritt 3 — Homebrew installieren (einmalig, nur falls noch nicht vorhanden)

**Homebrew** ist ein kleines Helfer-Programm, über das der Installer die nötigen Werkzeuge nachlädt. Viele Macs haben es schon — viele aber auch nicht.

**So prüfst du, ob es schon da ist:** Terminal öffnen (`Cmd` + `Leertaste` → „Terminal" → Enter) und eingeben:

```bash
brew --version
```

- Erscheint eine Versionsnummer (z. B. `Homebrew 4.x`) → alles gut, **weiter mit Schritt 4**.
- Kommt „command not found" → Homebrew fehlt. Dann diesen Befehl ausführen:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

   Hinweise dazu:
   - Du wirst nach deinem **Mac-Passwort** gefragt (das, mit dem du dich am Mac anmeldest) — das ist normal.
   - Die Installation dauert **ein paar Minuten**.
   - Am Ende zeigt Homebrew evtl. zwei „Next steps"-Zeilen mit `echo …` an — **die bitte ausführen** (kopieren, Enter), damit `brew` sofort funktioniert. Danach `brew --version` nochmal testen.

> Bei Problemen mit Homebrew: kurz Simon melden, das ist schnell gelöst.

---

## Schritt 4 — Skill Base installieren

1. **Terminal öffnen** (falls noch nicht offen): `Cmd` + `Leertaste`, „Terminal", Enter.
2. **Diesen einen Befehl** hineinkopieren und Enter drücken:

   ```bash
   bash <(curl -fsSL https://raw.githubusercontent.com/sd624/skill-base/main/install.sh)
   ```

3. Der Installer führt dich durch:
   - Er prüft Homebrew (hast du in Schritt 3 erledigt) und installiert die **GitHub CLI** (`gh`) automatisch
   - Er öffnet den **Browser zum GitHub-Login** — dort einfach einloggen und bestätigen
   - Er lädt die für dich freigeschalteten Skills herunter
   - Er richtet das **tägliche Auto-Update um 8:00 Uhr** ein

Wenn am Ende eine grüne Box „Skill Base ist eingerichtet!" erscheint: geschafft! ✅

---

## Schritt 5 — Testen

Öffne Claude Code und frag einfach:

> funktioniert hello-world?

Wenn Claude mit „Skill Base läuft" antwortet, ist alles korrekt eingerichtet.

---

## Was du jetzt hast

Deine Skills tauchen automatisch in Claude auf. Ein paar Beispiele:

- **audio-transcribe** — Audiodateien in Text umwandeln
- **youtube-transcript** — YouTube-Videos transkribieren
- *(und weitere, je nachdem wofür du freigeschaltet bist)*

Manche Skills brauchen zusätzliche Zugänge (z. B. zu lexoffice oder unserem Server). Falls so ein Skill bei dir eine Fehlermeldung bringt, melde dich bei Simon — dann richten wir den Zugang ein.

---

## Praktische Befehle

| Was | Wie |
|---|---|
| Skills sofort aktualisieren (statt bis morgen warten) | Sag Claude: **„update meine skills"** |
| Feedback / Idee / Bug zu einem Skill melden | Sag Claude: **„feedback zu \<skill\>: …"** |
| Tagesübersicht deiner Skills | Erscheint automatisch beim ersten Claude-Start am Tag |

---

## Hilfe

Klappt etwas nicht? Schreib Simon ([sd@kissconcepts.de](mailto:sd@kissconcepts.de)) — am besten mit dem Inhalt der Datei `~/.skill-base/update.log` (die zeigt, was zuletzt passiert ist).

---

## Eigenen Skill beitragen (für Fortgeschrittene)

Du kannst eigene Skills vorschlagen. Der Weg läuft über einen sogenannten Pull Request — die Details stehen in der [README](README.md). Wenn du unsicher bist: einfach Simon fragen, er hilft beim ersten Mal.
