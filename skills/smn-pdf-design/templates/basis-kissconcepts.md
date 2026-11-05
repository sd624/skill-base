---
marke: kissconcepts
title: Musterbogen Dokumentendesign KISSconcepts
subtitle: Zeigt alle Gestaltungselemente der Dachmarke einmal im Zusammenhang
header: Designvorlage · KISSconcepts GmbH
version: "1.0"
stand: 05.11.2026
author: Simon Doser, Geschäftsführung
signature: true
---

## Fließtext und Hervorhebungen

So sieht ein normaler Absatz aus. Er steht in Inter mit 9,8 Punkt und einer Zeilenhöhe von
1,5. **Fett** hebt einzelne Begriffe hervor, *kursiv* setzt leichte Betonungen, und
`technische Werte` erscheinen in einem grauen Feld. Der Titel oben endet automatisch mit
dem cyanfarbenen Punkt aus dem Logo.

Offene Stellen werden gelb markiert, damit sie beim Durchblättern auffallen:
<mark>Angabe fehlt noch</mark>.

> Ein Hinweiskasten eignet sich für Rechtsgrundlagen, Vorbehalte oder wörtliche Aussagen
> aus Gesprächen. Die cyanfarbene Kante ist neben dem Kopf der einzige Farbakzent.

## Aufzählungen

- Erster Punkt einer einfachen Liste
- Zweiter Punkt, etwas länger formuliert, damit man den Umbruch innerhalb eines
  Listenpunkts beurteilen kann

1. Nummerierte Liste für Abläufe
2. Zweiter Schritt

### Unterüberschrift dritter Ebene

Unterhalb der Abschnittsüberschriften gliedert diese Ebene längere Kapitel. Sie trägt
keine Linie; die kräftige Linie gehört nur den Abschnitten.

## Tabellen

| Thema | Zuständig | Frist | Stand |
|---|---|---|---|
| Jahresabschluss | Steuerberater | 31.07. | in Arbeit |
| Gesellschafterliste | Notar | nach Beschluss | erledigt |
| Bankvollmachten | Geschäftsführung | sofort | offen |

## Ampel

Für Abstimmungs- und Prüfdokumente, die Punkt für Punkt gemeinsam durchgegangen werden,
zeigt die Ampel den Stand: <span class="ampel rot">offen</span>
<span class="ampel gelb">Details offen</span> <span class="ampel gruen">geklärt</span>

<div class="zeile-rot"><b>1 · Beispielthema A</b> — muss noch entschieden werden. ☐ besprochen</div>
<div class="zeile-gelb"><b>2 · Beispielthema B</b> — Richtung klar, Formulierung offen. ☐ besprochen</div>
<div class="zeile-gruen"><b>3 · Beispielthema C</b> — geklärt. ☐ besprochen</div>

## Abschluss

Der Freigabeblock unten entsteht durch `signature: true` im Frontmatter. Er gehört in alle
Dokumente, die unterschrieben werden.
