---
name: smn-pdf-design
description: Erzeugt PDF-Dokumente im Markendesign von Skill Me Now oder der Dachmarke KISSconcepts GmbH — Originallogo, Markenschrift und -farben, einheitlicher Kopf, Versionsblock und Unterschriftenfeld; bei KISSconcepts zusätzlich Ampel-Markierung (rot/gelb/grün). Nutze diesen Skill immer, wenn ein PDF entstehen soll oder ein Dokument ausgedruckt, unterschrieben, abgehakt oder weitergegeben wird — auch bei Formulierungen wie "mach daraus ein PDF", "als PDF exportieren", "zum Ausdrucken", "schön aufbereiten", "im Brand", "zum Unterschreiben", "Checkliste zum Abhaken", "farblich markieren", "Übersicht für den Auditor", "Handout für die Teilnehmer", "für den Steuerberater", "für den Notar". Skill Me Now für Kurse, AZAV/QM, Teilnehmende und Schulungsunterlagen; KISSconcepts für die GmbH selbst: Gesellschafter, Gesellschaftervertrag und -beschlüsse, Unterlagen für Steuerberater, Notar oder Bank. Nicht für Angebote und Rechnungen — die laufen über lexoffice (Skill angebot-erstellen). Kommuniziere immer auf Deutsch.
---

# PDF-Design Skill Me Now und KISSconcepts

Dieser Skill sorgt dafür, dass jedes PDF, das für Skill Me Now oder die KISSconcepts GmbH
entsteht, gleich aussieht: gleicher Kopf, gleiche Schrift, gleiche Farben. Das ist kein
Selbstzweck — bei AZAV-Prüfungen, gegenüber Teilnehmenden und gegenüber Kunden wirkt eine
einheitliche Dokumentenfamilie professionell und erspart jedes Mal die Frage, wie man es
diesmal formatiert.

## Welche Marke?

Der Skill kennt zwei Marken. Skill Me Now ist Standard; KISSconcepts wird mit einer Zeile
im Frontmatter gewählt.

| Marke | Wofür | Frontmatter |
|---|---|---|
| **Skill Me Now** (Standard) | alles rund ums Bildungsangebot: Kurse, AZAV- und QM-Dokumente, Teilnehmende, Betriebe, Agentur für Arbeit, Schulungsunterlagen | nichts nötig |
| **KISSconcepts** | die GmbH als Firma: Gesellschafter, Gesellschaftervertrag und -beschlüsse, Unterlagen für Steuerberater, Notar oder Bank, interne Firmenpapiere | `marke: kissconcepts` |

Warum die Unterscheidung wichtig ist: Skill Me Now ist die Kursmarke. Ein Firmenpapier für
Gesellschafter, Notar oder Bank im runden Fredoka-Look mit Magenta-Verlauf liest sich wie
Kursmaterial und wirkt dort fehl am Platz. Umgekehrt bleiben AZAV- und QM-Dokumente bei
Skill Me Now, auch wenn formal die GmbH der Träger ist: Freigabeliste und Auditor kennen
diese Dokumentenfamilie. Alles, was für KISSconcepts dazugekommen ist, gilt nur dort —
Skill-Me-Now-Dokumente sehen genauso aus wie bisher.

Ist die Zuordnung unklar, frag kurz nach. Für STARSCAN gibt es im Skill noch keine Marke —
nimm dann nicht ersatzweise eine der beiden, sondern sag das.

## Der Weg zum PDF

Schreibe den Inhalt als Markdown mit einem Frontmatter-Kopf, dann baue das PDF mit dem
mitgelieferten Skript. Alles Gestalterische steckt im Skript — im Markdown geht es nur um
Inhalt und Struktur.

```bash
python3 ~/.claude/skills/smn-pdf-design/scripts/build_pdf.py dokument.md ausgabe.pdf
```

Die Marke kommt aus dem Frontmatter (`marke: kissconcepts`) oder als Schalter
`--marke kissconcepts`; der Schalter gewinnt. Die Ausgabezeile des Skripts nennt die
verwendete Marke — kurz hinsehen, bevor du das PDF weitergibst.

Logos und Schriften sind im Skill gebündelt und werden ins PDF eingebettet. Das Ergebnis
sieht auf jedem Rechner gleich aus, auch ohne installierte Fredoka oder Inter — wichtig,
weil diese Dokumente im Team weitergegeben werden.

**Voraussetzungen:** `pandoc` und Google Chrome. Chrome ist meist vorhanden, pandoc oft
nicht. Prüfe es vor dem ersten Lauf und installiere es bei Bedarf — das dauert unter einer
Minute:

```bash
which pandoc || brew install pandoc
```

Fehlt Homebrew, verweise auf die Installationsanleitung im Skill-Base-README. Die Schriften
müssen nicht installiert werden, sie stecken im Skill.

## Frontmatter

Alle Felder sind optional. Was fehlt, wird weggelassen — es entstehen keine leeren Zeilen
oder Platzhalter.

```markdown
---
marke: smn
title: Zusammenarbeit mit Akteuren des Arbeits- und Bildungsmarktes
subtitle: Nachweis nach § 178 SGB III
header: QM-Dokumentation AZAV · KISSconcepts GmbH
version: "1.3"
stand: 08.09.2026
author: Simon Doser, Geschäftsführung
signature: true
landscape: false
---
```

| Feld | Wirkung |
|---|---|
| `marke` | `smn` (Standard) oder `kissconcepts`, siehe „Welche Marke?“ |
| `title` | Große Überschrift unter dem Kopf. Fehlt sie, wird die erste `#`-Zeile des Markdown genommen. Bei KISSconcepts bekommt sie automatisch den cyanfarbenen Punkt aus dem Logo |
| `subtitle` | Graue Zeile darunter, gut für Rechtsgrundlagen oder Einordnungen |
| `header` | Kleiner Text oben rechts neben dem Logo, nennt den Kontext des Dokuments. Bei vertraulichen Papieren gehört „Vertraulich“ und der Empfängerkreis hinein |
| `version`, `stand`, `author` | Erzeugen zusammen den Versionsblock. Ab zwei gefüllten Feldern erscheint die Tabelle |
| `signature: true` | Fügt am Ende ein Freigabefeld mit Datum und Unterschriftslinie an |
| `landscape: true` | Querformat |

Bei QM-Dokumenten gehören `version` und `stand` immer hinein, weil die Freigabeliste
darauf verweist. Ein PDF ohne Versionsangabe lässt sich später keiner Freigabe zuordnen.

## Querformat

Ab etwa sechs Tabellenspalten wird Hochformat unlesbar: Die Spalten werden so schmal, dass
jedes Wort einzeln umbricht. Setze dann `landscape: true`. Erkennungsmerkmal beim
Korrekturlesen — wenn in einer Zelle nur noch zwei bis drei Zeichen pro Zeile stehen, ist
das Format falsch gewählt.

## Was das Design ausmacht

### Skill Me Now

- **Kopf**: Logo links, Kontexttext rechts, darunter eine dünne Linie und der Farbverlauf
  von Magenta über Blau nach Hellblau. Der Verlauf ist das Wiedererkennungsmerkmal und
  stammt aus dem Play-Dreieck des Logos.
- **Überschriften** in Dunkelblau `#0B3A8E`, Abschnittsüberschriften mit magentafarbener
  Kante links. Die Kante macht die Gliederung beim Durchblättern sichtbar, ohne dass man
  lesen muss.
- **Tabellen** mit dunkelblauem Kopf, weißer Schrift und zartem Zebra-Muster. In
  QM-Dokumenten sind Tabellen der Hauptinhalt, deshalb sind sie kräftiger gestaltet als
  der Fließtext.
- **Zitatblöcke** als hellblaue Kästen, gut für Hinweise, Rechtsgrundlagen oder
  wörtliche Aussagen aus Gesprächen.
### KISSconcepts

Die Dachmarke ist sachlich: schwarz auf weiß, viel Luft, ein einziger Farbakzent.

- **Kopf**: dunkles Logo links, Kontext in kleinen Versalien rechts, darunter eine schwarze
  Linie und ein kurzer Strich in Cyan `#00BCD4` — der Farbton des Punkts im Logo.
- **Titel** in Inter Bold mit cyanfarbenem Schlusspunkt, wie im Logo „concepts.“
- **Abschnittsüberschriften** schwarz mit kräftiger Linie darüber, wie ein Aktenvermerk.
- **Tabellen** mit schwarzem Kopf und hellgrauem Zebra, **Hinweiskästen** zart cyan.
- **Cyan sparsam**: nur Akzente, nie Fließtext — als Schriftfarbe ist es auf Weiß zu blass.
  Links stehen deshalb in dunklerem Petrol. Gold und Hellblau gehören den Töchtern STARSCAN
  und Skill Me Now und haben in KISSconcepts-Dokumenten nichts zu suchen.

- **Ampel** für Abstimmungs- und Prüfdokumente der GmbH, wenn mehrere Punkte nach Stand
  sortiert gemeinsam durchgegangen werden: `<span class="ampel rot">offen</span>`,
  `ampel gelb`, `ampel gruen` als Etikett, `<div class="zeile-rot">…</div>` (bzw.
  `zeile-gelb`, `zeile-gruen`) als farbig umrandeter Absatz, `<tr class="rot">` für
  Tabellenzeilen. Für ein gemeinsames Durchgehen hilft ein „☐ besprochen“ bei jedem Punkt.
  Die Ampel gibt es nur im KISSconcepts-Stil; in Skill-Me-Now-Dokumenten greifen diese
  Klassen nicht.

### Für beide Marken

- **Gelbe Markierung** über `<mark>Text</mark>` oder `<span class="offen">…</span>` für
  offene Stellen. Bei Prüfdokumenten muss auf einen Blick sichtbar sein, was noch fehlt —
  unauffällige Platzhalter werden übersehen und landen ungefüllt beim Auditor.

Details, Farbwerte und Beispielschnipsel stehen in `references/brand.md`. Lies die Datei,
wenn du eigene HTML-Bausteine ergänzen willst oder Farbwerte brauchst.

## Vorlage

`templates/basis.md` ist ein Musterbogen, der alle Elemente einmal zeigt. Nutze ihn als
Ausgangspunkt für neue Dokumente oder um nach einer Änderung am Design zu prüfen, ob noch
alles stimmt. `templates/basis-kissconcepts.md` ist das Gegenstück für KISSconcepts,
einschließlich Ampel.

## Erfahrungen, die Zeit sparen

**Direkt in Markdown arbeiten, nicht in Google Docs.** Der Versuch, formatierte Inhalte per
Zwischenablage in ein Google Doc zu bekommen, endet regelmäßig in Doppelungen und
verschachtelten Absätzen: Docs verarbeitet große Einfügungen unzuverlässig, und
„Alles auswählen" erfasst Tabellen nicht vollständig. Markdown plus dieses Skript ist
schneller und das Ergebnis sieht besser aus.

**Umlaute gehören hinein.** Die Schriften enthalten alle deutschen Zeichen. Weiche nie auf
ae/oe/ue aus.

**Ein Dokument, eine Aussage pro Abschnitt.** Die Gestaltung trägt lange Dokumente nur,
wenn die Gliederung stimmt. Wenn ein Abschnitt länger als eine Seite wird, prüfe, ob er
in zwei zerfällt.

**Eigene Layouts als Rohblock.** Braucht ein Dokument Bausteine, die Markdown nicht kennt
(Kacheln, Karten, farbige Punktlisten), schreib sie als HTML in einen Block
```` ```{=html} ```` — samt eigenem `<style>`. pandoc reicht den Block unverändert durch.
Rohes HTML ohne diesen Block wird dagegen teilweise als Markdown gelesen: Eingerückte
Zeilen werden zu Codeblöcken und das Layout zerfällt. Farben für eigene Bausteine immer
aus `references/brand.md` nehmen, damit sie zur gewählten Marke passen.

**Seitenumbrüche gezielt setzen.** Große Abschnitte mit `break-before:page` auf eine neue
Seite legen und kleine Tabellen oder Kachelgruppen mit `break-inside:avoid` zusammenhalten.
Sonst steht schnell eine einzelne Tabellenzeile allein auf einer Seite. Beim Durchsehen die
Seiten verkleinert als Bild ansehen (`pdftoppm -r 60`) — so fallen Waisen sofort auf.

## Bekannte Grenzen

Seitenzahlen fügt Chrome im Headless-Modus nicht ein. Bei Dokumenten über etwa zehn Seiten
lohnt es sich, eine Kopfzeile über `header` zu setzen, damit einzelne ausgedruckte Blätter
zuordenbar bleiben. Eine echte Seitennummerierung wäre der nächste Ausbauschritt.
