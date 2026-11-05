# Markenreferenz

Inhalt: Skill Me Now (Farben, Schrift, Logo) · KISSconcepts (Farben, Schrift, Logo, Ampel) ·
HTML-Bausteine · Freigabeliste

# Skill Me Now

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

# KISSconcepts

Dachmarke der KISSconcepts GmbH, Pfronten. „KISS — Keep It Short and Simple“: sachlich,
schwarz auf weiß, ein einziger Farbakzent. Die Website kissconcepts.de ist dunkel; im
Druck wird daraus Schwarz auf Weiß.

## Farben

| Rolle | Hex | Einsatz |
|---|---|---|
| Tinte | `#0a0a0b` | Text, Überschriften, Tabellenköpfe, Kopflinie |
| Cyan | `#00BCD4` | einziger Akzent: Punkt im Logo, Strich unter dem Kopf, Titelpunkt, Kante der Hinweiskästen |
| Petrol | `#007f8c` | Links und kleine Akzenttexte (Cyan ist als Schrift auf Weiß zu blass) |
| Cyan hell | `#e8f8fa` | Hintergrund der Hinweiskästen |
| Grau | `#5f6168` | Untertitel, Kontexttext, Fußnoten |
| Linien | `#d9dcdf` | Tabellenrahmen, Trennlinien |
| Zebra | `#f5f6f7` | jede zweite Tabellenzeile, Kästen |

`#00BCD4` ist der exakte Wert aus dem Logo-SVG; das PNG zeigt durch Kantenglättung
`#13B8C7`. Gold `#e8c84a` (STARSCAN) und Hellblau `#5bc8f5` (Skill Me Now) gehören den
Töchtern — in Dokumenten der Dachmarke nicht verwenden.

## Schrift

Inter als variable Schrift (`assets/fonts/Inter-latin.woff2` und `Inter-latin-ext.woff2`),
eingebettet als `InterKISS`, Gewichte frei wählbar. Fließtext 9,8 pt / 1,5, Titel 700,
Abschnitte 700, Unterabschnitte 650, Hervorhebungen 620.

## Logo

`assets/kissconcepts-logo.png`, 951 × 354 px, schwarz mit cyanfarbenem Punkt, transparent,
Ränder beschnitten. Wird mit 36 px Höhe im Kopf eingesetzt.

Original: `Geteilte Ablagen/KISSconcepts/Logo/KISSconcepts Logo s_trans.png`. Im selben
Ordner liegen die weiße Fassung für dunkle Hintergründe (`w_trans`) und Varianten mit
Hintergrund (`s_w`, `w_schwarz`).

## Ampel (nur KISSconcepts)

Die Klassen sind nur im KISSconcepts-Stil definiert; Skill-Me-Now-Dokumente bleiben ohne
Ampel.

| Stand | Etikett | Kante / Hintergrund |
|---|---|---|
| offen, muss entschieden werden | `#b42318` auf `#fcebe8` | `#b42318` / `#fcebe8` |
| Details offen | `#8a5100` auf `#fcecc8` | `#d99a2b` / `#fdf5e4` |
| geklärt | `#1b6b44` auf `#e3f2e9` | `#1b6b44` / weiß |

```html
<span class="ampel rot">offen</span> <span class="ampel gelb">Details offen</span> <span class="ampel gruen">geklärt</span>

<div class="zeile-rot"><b>4 · Beispielthema</b> — muss noch entschieden werden. ☐ besprochen</div>

<tr class="gelb"><td>…</td></tr>
```

Rot nur für das, was wirklich noch entschieden werden muss. Ist alles rot, sieht man nichts
mehr.

# Allgemein

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
