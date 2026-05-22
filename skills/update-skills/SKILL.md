---
name: update-skills
description: Aktualisiert die geteilten Skills aus Skill Base manuell — zieht die neuesten Versionen aus GitHub. Nutze diesen Skill, wenn der User sagt "update meine skills", "neue skills holen", "skill base aktualisieren", "skills updaten", "/update-skills" oder ähnliches. Auch wenn der User fragt, ob es Updates gibt.
---

# Update Skills

Aktualisiert alle Skill-Base-Repos und resynchronisiert Symlinks.

## Ablauf

1. **Update-Skript ausführen:**

   ```bash
   ~/.skill-base/repos/skill-base/update.sh
   ```

2. **Antwort dem User zusammenfassen** (auf Basis der Skript-Ausgabe):
   - Welche Repos aktualisiert wurden (oder ob nichts neues kam)
   - Welche Symlinks neu angelegt, aktualisiert oder entfernt wurden
   - Falls Konflikte gemeldet wurden: dem User sagen, dass er sich bei Simon ([sd@kissconcepts.de](mailto:sd@kissconcepts.de)) melden soll

3. **Bei Erfolg ohne Änderungen:** Kurz bestätigen, dass alles aktuell ist.

4. **Bei Fehlern (z.B. gh nicht authentifiziert):** Dem User die nötigen Schritte zeigen, idealerweise mit konkretem Befehl.

## Stil

Halte die Antwort kurz und ergebnisorientiert. Wenn nichts Neues kam, eine Zeile reicht. Bei Änderungen: stichpunktartig auflisten was neu/geändert ist.
