---
name: smn-pdf-design
description: Erzeugt PDF-Dokumente im Markendesign von Skill Me Now (KISSconcepts GmbH) — Originallogo, Schriftart Fredoka, Markenfarben, einheitlicher Kopf mit Verlaufsbalken, Versionsblock und Unterschriftenfeld. Nutze diesen Skill immer, wenn ein PDF entstehen soll oder ein Dokument ausgedruckt, unterschrieben, abgehakt oder weitergegeben wird — auch bei Formulierungen wie "mach daraus ein PDF", "als PDF exportieren", "zum Ausdrucken", "schön aufbereiten", "im Brand", "zum Unterschreiben", "Checkliste zum Abhaken", "Übersicht für den Auditor", "Handout für die Teilnehmer". Gilt für QM- und AZAV-Dokumente, Protokolle, Gesprächsvermerke, Berichte, Konzepte, Verträge, Nachweise, Übersichten und Schulungsunterlagen. Nicht für Angebote und Rechnungen — die laufen über lexoffice (Skill angebot-erstellen). Kommuniziere immer auf Deutsch.
---

# PDF-Design Skill Me Now

Dieser Skill sorgt dafür, dass jedes PDF, das für Skill Me Now oder die KISSconcepts GmbH
entsteht, gleich aussieht: gleicher Kopf, gleiche Schrift, gleiche Farben. Das ist kein
Selbstzweck — bei AZAV-Prüfungen, gegenüber Teilnehmenden und gegenüber Kunden wirkt eine
einheitliche Dokumentenfamilie professionell und erspart jedes Mal die Frage, wie man es
diesmal formatiert.

## Der Weg zum PDF

Schreibe den Inhalt als Markdown mit einem Frontmatter-Kopf, dann baue das PDF mit dem
mitgelieferten Skript. Alles Gestalterische steckt im Skript — im Markdown geht es nur um
Inhalt und Struktur.

```bash
python3 ~/.claude/skills/smn-pdf-design/scripts/build_pdf.py dokument.md ausgabe.pdf
```

Logo und Schriften sind im Skill gebündelt und werden ins PDF eingebettet. Das Ergebnis
sieht auf jedem Rechner gleich aus, auch ohne installierte Fredoka — wichtig, weil diese
Dokumente im Team weitergegeben werden.

Voraussetzungen: `pandoc` und Google Chrome. Beides ist auf Simons Rechner vorhanden.

## Frontmatter

Alle Felder sind optional. Was fehlt, wird weggelassen — es entstehen keine leeren Zeilen
oder Platzhalter.

```markdown
---
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
| `title` | Große Überschrift unter dem Kopf. Fehlt sie, wird die erste `#`-Zeile des Markdown genommen |
| `subtitle` | Graue Zeile darunter, gut für Rechtsgrundlagen oder Einordnungen |
| `header` | Kleiner Text oben rechts neben dem Logo, nennt den Kontext des Dokuments |
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
- **Gelbe Markierung** über `<mark>Text</mark>` oder `<span class="offen">…</span>` für
  offene Stellen. Bei Prüfdokumenten muss auf einen Blick sichtbar sein, was noch fehlt —
  unauffällige Platzhalter werden übersehen und landen ungefüllt beim Auditor.

Details, Farbwerte und Beispielschnipsel stehen in `references/brand.md`. Lies die Datei,
wenn du eigene HTML-Bausteine ergänzen willst oder Farbwerte brauchst.

## Vorlage

`templates/basis.md` ist ein Musterbogen, der alle Elemente einmal zeigt. Nutze ihn als
Ausgangspunkt für neue Dokumente oder um nach einer Änderung am Design zu prüfen, ob noch
alles stimmt.

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

## Bekannte Grenzen

Seitenzahlen fügt Chrome im Headless-Modus nicht ein. Bei Dokumenten über etwa zehn Seiten
lohnt es sich, eine Kopfzeile über `header` zu setzen, damit einzelne ausgedruckte Blätter
zuordenbar bleiben. Eine echte Seitennummerierung wäre der nächste Ausbauschritt.
