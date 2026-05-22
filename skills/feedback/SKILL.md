---
name: feedback
description: Sendet Feedback oder Verbesserungswünsche zu einem Skill an Simon (den Maintainer) — erstellt ein GitHub-Issue im passenden Repo. Nutze diesen Skill, wenn der User Feedback, Verbesserungsvorschläge, Fehler oder Wünsche zu einem Skill äußert. Triggert bei "feedback zu <skill>", "ich hätte eine idee für <skill>", "<skill> hat einen bug", "verbesserung für <skill>", "/feedback" oder ähnlichen Formulierungen.
---

# Feedback an Simon

Empfänger geben über diesen Skill Feedback, das als GitHub-Issue im passenden Repo landet. Simon sieht alle Issues an einem Ort und kann reagieren.

## Ablauf

1. **Inhalt klären** — falls der User noch nicht alles genannt hat, frag nach:
   - Welcher Skill betrifft das Feedback? (Wenn klar aus Kontext, übernehmen.)
   - Was genau ist die Rückmeldung? (Idee, Bug, Verbesserungswunsch?)
   - Optional: Wie reproduziert man das (bei Bugs)?

2. **Repo bestimmen** — anhand des Symlink-Ziels des betroffenen Skills:

   ```bash
   readlink ~/.claude/skills/<skill-name>
   ```

   - Endet mit `skill-base-dozenten/skills/...` → Issue ins Repo `sd624/skill-base-dozenten`
   - Endet mit `skill-base-admins/skills/...` → Issue ins Repo `sd624/skill-base-admins`
   - Endet mit `skill-base/skills/...` → Issue ins Repo `sd624/skill-base`
   - Wenn der Skill kein Symlink ist oder woanders hinzeigt: dem User sagen, dass das offenbar kein Skill-Base-Skill ist und das Feedback direkt an Simon ([sd@kissconcepts.de](mailto:sd@kissconcepts.de)) gehen sollte.

3. **Issue erstellen** mit `gh`:

   ```bash
   gh issue create \
     --repo sd624/<repo-name> \
     --title "Feedback: <skill-name> — <kurz-titel>" \
     --body "<ausführlicher-body>"
   ```

   **Body-Format:**
   ```
   ## Feedback von @<github-username>

   **Skill:** <skill-name>
   **Typ:** <Idee | Bug | Verbesserung>

   <eigentlicher Feedback-Text>

   ---
   _Erstellt via /feedback Skill aus Skill Base._
   ```

   GitHub-Username via `gh api user --jq .login` ermitteln.

4. **Bestätigung** an den User mit der Issue-URL.

## Fehlerfälle

- **`gh` nicht authentifiziert:** Dem User sagen, dass er `gh auth login` ausführen muss (Schritte aus dem Skill-Base-README erklären).
- **Repo nicht zugreifbar (HTTP 403/404):** Dem User sagen, dass er offenbar keinen Issue-Schreibzugriff hat — Feedback dann direkt an Simon per E-Mail.

## Stil

Bestätige knapp und freundlich. Beispiel: "Danke! Habe ein Issue dazu aufgemacht: <URL>. Simon sieht es im Repo-Dashboard."
