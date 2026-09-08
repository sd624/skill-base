# Markenreferenz Skill Me Now

## Farben

Alle Werte stammen aus dem Originallogo.

| Rolle | Hex | Einsatz |
|---|---|---|
| Dunkelblau | `#0B3A8E` | Primärfarbe: Überschriften, Tabellenköpfe, Kopflinie |
| Magenta | `#E926C8` | Akzent: linke Kante der Abschnittsüberschriften, Verlaufsanfang |
| Blau | `#2C6FE0` | Verlaufsmitte, Links, Kante der Zitatblöcke |
| Hellblau | `#5BC0F8` | Verlaufsende |
| Grau | `#5c6470` | Untertitel, Kontexttext, Fußnoten |
| Linien | `#c7d3e8` | Tabellenrahmen, Trennlinien |
| Zebra | `#f7f9fd` | jede zweite Tabellenzeile |
| Kasten | `#f2f6fd` | Hintergrund der Zitatblöcke |
| Offen | `#fff2cc` | gelbe Markierung offener Stellen |

Der Verlauf im Kopf läuft immer in dieser Richtung: Magenta links, Hellblau rechts. Das
entspricht dem Play-Dreieck im Logo und ist das stärkste Wiedererkennungsmerkmal der Marke.

## Schrift

Fredoka in vier Schnitten, eingebettet als `FredokaSMN`:

| Schnitt | Gewicht | Einsatz |
|---|---|---|
| Regular | 400 | Fließtext |
| Medium | 500 | Unterüberschriften (h3) |
| SemiBold | 600 | Titel, Abschnittsüberschriften, Hervorhebungen |
| Bold | 700 | Reserve |

Fredoka ist eine runde Displayschrift. Damit längere Texte lesbar bleiben, arbeitet das
Stylesheet mit 10,5 pt und einer Zeilenhöhe von 1,55 — mehr Luft als bei einer klassischen
Serifenschrift nötig wäre. Wenn ein Dokument sehr textlastig wird, ist das ein Hinweis auf
zu wenig Struktur, nicht auf eine falsche Schrift.

## Logo

`assets/smn-logo.png`, 1452 × 782 px, transparenter Hintergrund, Ränder beschnitten.
Wird mit 44 px Höhe im Kopf eingesetzt.

Das Original liegt unter
`Geteilte Ablagen/Skill Me Now/Logo/Skill Me Now Logo_dunkel_trans.png   .png`
(der doppelte Suffix im Dateinamen stammt aus dem Drive und ist kein Tippfehler hier).
Weitere Varianten im selben Ordner: helle Fassung für dunkle Hintergründe, Dreieck allein
als Profilbild, vertikale Anordnung.

Falls das Logo neu beschnitten werden muss:

```python
from PIL import Image
im = Image.open(quelle).convert("RGBA")
im.crop(im.split()[3].getbbox()).save(ziel)   # Alphakanal liefert die Bounding-Box
```

## HTML-Bausteine

Das Skript reicht rohes HTML durch, du kannst also im Markdown direkt gestalten.

**Gelbe Markierung für offene Stellen**

```html
<mark>zu ergänzen</mark>
```

**Zweispaltige Gegenüberstellung**

```html
<table><tr>
<td style="width:50%;border:none;padding-right:12px;"><b>Vorher</b><br>…</td>
<td style="width:50%;border:none;"><b>Nachher</b><br>…</td>
</tr></table>
```

**Hinweiskasten** — im Markdown genügt ein Zitat:

```markdown
> Wichtig: Diese Fassung ersetzt die Version 1.2 vom 08.07.2026.
```

**Ankreuzfeld für Checklisten**

```markdown
- [ ] noch offen
- [x] erledigt
```

## Zusammenspiel mit der Freigabeliste

QM-Dokumente sind mit der Freigabeliste `Freigabeliste AZAV Dokumentation` verknüpft. Wenn
ein Dokument als PDF neu gebaut wird, gehört in die Liste ein Eintrag mit Versionsnummer,
Datum und einer Beschreibung der Änderung. Die Spalten für freigebende Person und
Freigabedatum bleiben leer — die Freigabe ist ein Akt der Geschäftsführung und wird von
Simon selbst eingetragen.
