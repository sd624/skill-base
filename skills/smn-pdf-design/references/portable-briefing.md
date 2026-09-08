# Skill Me Now — Dokumentendesign (systemneutral)

Diese Fassung ist so geschrieben, dass sie sich in jedes KI-System einfügen lässt, das HTML
oder CSS erzeugen kann: ChatGPT, Codex, Gemini, Cursor. Sie enthält alles Nötige als Text —
keine Abhängigkeit von Claude-Skills, keine lokalen Dateien außer dem Logo.

**Einsatz:** Als Projektanweisung, Custom Instruction oder einfach als Nachricht vor dem
eigentlichen Auftrag. Danach genügt: „Erstelle daraus ein Dokument im Skill-Me-Now-Design."

---

## Marke

Skill Me Now ist die Weiterbildungsmarke der KISSconcepts GmbH (Pfronten, Allgäu),
AZAV-zertifizierter Bildungsträger für digitales Marketing und KI. Die Dokumente gehen an
Teilnehmende, Betriebe, Zertifizierungsstellen und Prüfer. Sie sollen freundlich und
zugänglich wirken, aber unmissverständlich seriös — die Marke tritt gegenüber Behörden auf.

## Farben

| Rolle | Hex |
|---|---|
| Dunkelblau (Primär) | `#0B3A8E` |
| Magenta (Akzent) | `#E926C8` |
| Blau | `#2C6FE0` |
| Hellblau | `#5BC0F8` |
| Grau (Sekundärtext) | `#5c6470` |
| Linien | `#c7d3e8` |
| Zeilenraster hell | `#f7f9fd` |
| Hinweiskasten | `#f2f6fd` |
| Offene Stelle | `#fff2cc` |

Dunkelblau trägt alle Überschriften und Tabellenköpfe. Magenta ist ausschließlich Akzent —
nie für Flächen oder Text, nur für Kanten und den Verlauf. Der Farbverlauf im Seitenkopf
läuft immer von Magenta links über Blau zu Hellblau rechts; er stammt aus dem Play-Dreieck
des Logos und ist das stärkste Wiedererkennungsmerkmal.

## Schrift

**Fredoka**, eine Google Font, in den Schnitten 400 (Fließtext), 500 (Unterüberschriften),
600 (Titel und Abschnitte), 700 (Reserve).

```css
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&display=swap');
```

Fredoka ist rund und freundlich, für lange Fließtexte aber grenzwertig. Deshalb 10,5 pt mit
Zeilenhöhe 1,55 — mehr Luft als bei einer Serifenschrift nötig wäre. Wird ein Dokument sehr
textlastig, ist das ein Hinweis auf fehlende Gliederung, nicht auf die falsche Schrift.

## Logo

Waagerechte Fassung, transparenter Hintergrund, im Seitenkopf 44 px hoch, links oben.
Rechts daneben auf gleicher Grundlinie ein kleiner grauer Kontexttext (9 pt), der das
Dokument einordnet, etwa „QM-Dokumentation AZAV · KISSconcepts GmbH".

## Stylesheet

Vollständig einsetzbar, nur `Fredoka` per Google Fonts einbinden.

```css
@page { size: A4; margin: 18mm 16mm 16mm 16mm; }
body { font-family:'Fredoka',sans-serif; font-size:10.5pt; line-height:1.55;
       color:#1c1c1c; margin:0; }

.kopf { display:flex; align-items:flex-end; justify-content:space-between;
        border-bottom:3px solid #0B3A8E; padding-bottom:9px; }
.kopf img { height:44px; }
.kontext { font-size:9pt; color:#5c6470; text-align:right; letter-spacing:.04em; }
.balken { height:4px; margin-bottom:20px;
          background:linear-gradient(90deg,#E926C8 0%,#2C6FE0 55%,#5BC0F8 100%); }

h1 { font-weight:600; font-size:19pt; color:#0B3A8E; margin:0 0 3px 0; line-height:1.2; }
.untertitel { color:#5c6470; font-size:10.5pt; margin:0 0 18px 0; }
h2 { font-weight:600; font-size:13pt; color:#0B3A8E; margin:22px 0 8px 0;
     border-left:4px solid #E926C8; padding-left:9px; page-break-after:avoid; }
h3 { font-weight:500; font-size:11.5pt; color:#0B3A8E; margin:18px 0 6px 0; }
p { margin:0 0 9px 0; }
strong,b { font-weight:600; color:#111; }

blockquote { margin:12px 0; padding:10px 14px; background:#f2f6fd;
             border-left:4px solid #2C6FE0; color:#333; font-size:10pt; }

table { border-collapse:collapse; width:100%; margin:10px 0 14px 0; font-size:9pt; }
th { background:#0B3A8E; color:#fff; font-weight:600; padding:6px 8px;
     border:1px solid #0B3A8E; text-align:left; }
td { border:1px solid #c7d3e8; padding:6px 8px; vertical-align:top; }
tr:nth-child(even) td { background:#f7f9fd; }
tr { page-break-inside:avoid; }

ul,ol { margin:6px 0 12px 0; padding-left:20px; }
li { margin-bottom:4px; }
mark { background:#fff2cc; padding:0 3px; }
```

## Aufbau eines Dokuments

1. **Kopf** mit Logo, Kontexttext, Linie, Farbverlauf
2. **Titel** (h1) und optional eine graue Unterzeile, etwa die Rechtsgrundlage
3. **Versionsblock** als zweispaltige Tabelle: Dokument, Version, Stand, Erstellt von.
   Bei Nachweisdokumenten unverzichtbar — ohne Version lässt sich ein Dokument später
   keiner Freigabe zuordnen.
4. **Inhalt** in Abschnitten mit h2
5. **Freigabefeld** am Ende, wo unterschrieben wird: Datum und Unterschriftslinie

## Regeln, die aus der Praxis kommen

**Offene Stellen gelb markieren.** In Prüfdokumenten muss sofort sichtbar sein, was fehlt.
Unauffällige Platzhalter werden übersehen und landen ungefüllt beim Auditor.

**Ab sechs Tabellenspalten Querformat.** Sonst brechen die Spalten so schmal um, dass nur
zwei Zeichen pro Zeile stehen. Erkennungszeichen beim Korrekturlesen.

**Echte Umlaute.** Immer ä, ö, ü, ß — nie ae, oe, ue, ss. Die Schrift enthält alle Zeichen.

**Deutsche Ansprache, sachlicher Ton.** Diese Dokumente gehen an Behörden und Betriebe.
Keine Werbesprache, keine Ausrufezeichen, keine Superlative.

**Eine Aussage pro Abschnitt.** Wird ein Abschnitt länger als eine Seite, prüfen, ob er in
zwei zerfällt. Gestaltung trägt lange Dokumente nur bei sauberer Gliederung.
