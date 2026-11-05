#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut aus einer Markdown-Datei ein PDF im Markendesign von Skill Me Now (Standard)
oder der KISSconcepts GmbH.

    python3 build_pdf.py dokument.md ausgabe.pdf [--landscape] [--marke kissconcepts]

Steuerung über YAML-Frontmatter am Anfang der Markdown-Datei (alles optional):

    ---
    marke: kissconcepts      # smn (Standard) oder kissconcepts
    title: Zusammenarbeit mit Akteuren
    subtitle: Nachweis nach § 178 SGB III
    header: QM-Dokumentation AZAV
    version: "1.3"
    stand: 08.09.2026
    author: Simon Doser, Geschäftsführung
    signature: true          # erzeugt Freigabe-/Unterschriftenfeld am Ende
    landscape: true          # Querformat, sinnvoll ab etwa 6 Tabellenspalten
    ---

Logos und Schriften liegen im Skill und werden eingebettet — das PDF ist damit
auf jedem Rechner identisch, auch ohne installierte Schriften.
"""
import argparse, base64, os, re, subprocess, sys, tempfile, shutil

HIER   = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HIER), "assets")
FONTS  = os.path.join(ASSETS, "fonts")

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Welche Schreibweisen im Frontmatter oder auf der Kommandozeile welche Marke meinen
MARKEN = {"smn": "smn", "skillmenow": "smn", "skill-me-now": "smn", "skill me now": "smn",
          "kissconcepts": "kissconcepts", "kiss": "kissconcepts", "kiss-concepts": "kissconcepts",
          "kiss concepts": "kissconcepts"}


def b64(pfad):
    return base64.b64encode(open(pfad, "rb").read()).decode()


# --- Ampel (nur KISSconcepts) ----------------------------------------------
# Für Prüf- und Abstimmungsdokumente der GmbH. Skill-Me-Now-Dokumente bleiben bewusst
# unverändert — dort gibt es nur die gelbe Markierung offener Stellen.
AMPEL = """
*{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }
.ampel { display:inline-block; font-weight:600; font-size:8pt; padding:1px 8px; border-radius:9px;
         white-space:nowrap; line-height:1.55; }
.ampel::before { content:""; display:inline-block; width:6px; height:6px; border-radius:50%;
                 background:currentColor; margin-right:5px; vertical-align:1px; }
.ampel.rot { color:#b42318; background:#fcebe8; }
.ampel.gelb { color:#8a5100; background:#fcecc8; }
.ampel.gruen { color:#1b6b44; background:#e3f2e9; }
.zeile-rot, .zeile-gelb, .zeile-gruen { padding:6px 10px; margin:6px 0; break-inside:avoid;
                                        border-left:4px solid; }
.zeile-rot { border-left-color:#b42318; background:#fcebe8; }
.zeile-gelb { border-left-color:#d99a2b; background:#fdf5e4; }
.zeile-gruen { border-left-color:#1b6b44; }
.zeile-rot p:last-child, .zeile-gelb p:last-child, .zeile-gruen p:last-child { margin-bottom:0; }
table tr.rot td { background:#fcebe8; }
table tr.gelb td { background:#fdf5e4; }
"""


# --- Skill Me Now ----------------------------------------------------------
def css_smn(groesse):
    BLAU, MAGENTA, MITTEL, HELL = "#0B3A8E", "#E926C8", "#2C6FE0", "#5BC0F8"
    GRAU, LINIE, ZEBRA, KASTEN = "#5c6470", "#c7d3e8", "#f7f9fd", "#f2f6fd"
    faces = ""
    for datei, gewicht in (("Fredoka-Regular.ttf", 400), ("Fredoka-Medium.ttf", 500),
                           ("Fredoka-SemiBold.ttf", 600), ("Fredoka-Bold.ttf", 700)):
        pfad = os.path.join(FONTS, datei)
        if os.path.exists(pfad):
            faces += (f"@font-face{{font-family:'FredokaSMN';font-weight:{gewicht};font-style:normal;"
                      f"src:url(data:font/ttf;base64,{b64(pfad)}) format('truetype');}}\n")
    return faces + f"""
@page {{ size: {groesse}; margin: 18mm 16mm 16mm 16mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family:'FredokaSMN','Fredoka',sans-serif; font-size:10.5pt; line-height:1.55;
        color:#1c1c1c; margin:0; }}

/* Kopf: Logo links, Kontext rechts, darunter der Markenverlauf */
.smn-kopf {{ display:flex; align-items:flex-end; justify-content:space-between;
             border-bottom:3px solid {BLAU}; padding-bottom:9px; }}
.smn-kopf img {{ height:44px; }}
.smn-kontext {{ font-size:9pt; color:{GRAU}; text-align:right; letter-spacing:.04em; }}
.smn-balken {{ height:4px; margin-bottom:20px;
               background:linear-gradient(90deg,{MAGENTA} 0%,{MITTEL} 55%,{HELL} 100%); }}

h1 {{ font-weight:600; font-size:19pt; color:{BLAU}; margin:0 0 3px 0; line-height:1.2; }}
.smn-untertitel {{ color:{GRAU}; font-size:10.5pt; margin:0 0 18px 0; }}
h2 {{ font-weight:600; font-size:13pt; color:{BLAU}; margin:22px 0 8px 0;
      border-left:4px solid {MAGENTA}; padding-left:9px; page-break-after:avoid; }}
h3 {{ font-weight:500; font-size:11.5pt; color:{BLAU}; margin:18px 0 6px 0;
      page-break-after:avoid; }}
h4 {{ font-weight:600; font-size:10.5pt; color:#111; margin:14px 0 4px 0; }}
p {{ margin:0 0 9px 0; }}
strong, b {{ font-weight:600; color:#111; }}
a {{ color:{MITTEL}; text-decoration:none; }}

blockquote {{ margin:12px 0; padding:10px 14px; background:{KASTEN};
              border-left:4px solid {MITTEL}; color:#333; font-size:10pt; }}
blockquote p {{ margin:0; }}

table {{ border-collapse:collapse; width:100%; margin:10px 0 14px 0; font-size:9pt; }}
th {{ background:{BLAU}; color:#fff; font-weight:600; padding:6px 8px;
      border:1px solid {BLAU}; text-align:left; }}
td {{ border:1px solid {LINIE}; padding:6px 8px; vertical-align:top; }}
tr:nth-child(even) td {{ background:{ZEBRA}; }}
tr {{ page-break-inside:avoid; }}

ul, ol {{ margin:6px 0 12px 0; padding-left:20px; }}
li {{ margin-bottom:4px; }}
hr {{ border:none; border-top:1px solid {LINIE}; margin:20px 0; }}
code {{ background:#eef2f9; padding:1px 5px; border-radius:3px; font-size:9.5pt;
        font-family:'SF Mono',Menlo,monospace; }}

/* Kennzeichnung offener Stellen — im Audit muss sofort sichtbar sein, was fehlt */
.offen, mark {{ background:#fff2cc; padding:0 3px; }}

.smn-meta td:first-child {{ background:{BLAU}; color:#fff; font-weight:600; width:22%; }}
.smn-unterschrift {{ margin-top:34px; page-break-inside:avoid; }}
.smn-unterschrift div {{ margin-bottom:26px; }}
.smn-linie {{ border-bottom:1px solid #333; width:62%; margin-top:22px; }}
.smn-fuss {{ margin-top:26px; padding-top:8px; border-top:1px solid {LINIE};
             font-size:8pt; color:{GRAU}; }}
"""


def kopf_smn(kontext):
    return f"""<div class="smn-kopf">
  <img src="data:image/png;base64,{b64(os.path.join(ASSETS, 'smn-logo.png'))}" alt="Skill Me Now">
  <div class="smn-kontext">{kontext}</div>
</div>
<div class="smn-balken"></div>"""


# --- KISSconcepts ----------------------------------------------------------
# Dachmarke: sachlich, schwarz auf weiß, Cyan nur als Akzent (wie der Punkt im Logo).
# Cyan als Textfarbe ist auf Weiß zu blass (Kontrast ~2,3:1) — Links daher im dunkleren Petrol.
def css_kiss(groesse):
    INK, GRAU, LINIE, ZEBRA = "#0a0a0b", "#5f6168", "#d9dcdf", "#f5f6f7"
    CYAN, PETROL, CYAN_HELL = "#00BCD4", "#007f8c", "#e8f8fa"
    latin = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,"
             "U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD")
    latin_ext = ("U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+1D00-1DBF,"
                 "U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF")
    faces = ""
    for datei, bereich in (("Inter-latin.woff2", latin), ("Inter-latin-ext.woff2", latin_ext)):
        pfad = os.path.join(FONTS, datei)
        if os.path.exists(pfad):
            faces += (f"@font-face{{font-family:'InterKISS';font-weight:100 900;font-style:normal;"
                      f"src:url(data:font/woff2;base64,{b64(pfad)}) format('woff2');"
                      f"unicode-range:{bereich};}}\n")
    return faces + f"""
@page {{ size: {groesse}; margin: 16mm 15mm 15mm 15mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family:'InterKISS','Inter','Helvetica Neue',Arial,sans-serif; font-size:9.8pt;
        line-height:1.5; color:{INK}; margin:0; }}

/* Kopf: Logo links, Kontext rechts, schwarze Linie, kurzer Cyan-Akzent */
.kiss-kopf {{ display:flex; align-items:flex-end; justify-content:space-between;
              border-bottom:2px solid {INK}; padding-bottom:10px; }}
.kiss-kopf img {{ height:36px; display:block; }}
.kiss-kontext {{ font-size:7.5pt; color:{GRAU}; text-align:right; letter-spacing:.08em;
                 text-transform:uppercase; line-height:1.6; }}
.kiss-akzent {{ height:3px; width:56px; background:{CYAN}; margin-bottom:22px; }}

h1 {{ font-weight:700; font-size:22pt; letter-spacing:-.02em; color:{INK}; margin:0 0 5px 0;
      line-height:1.15; }}
h1 .kiss-punkt {{ color:{CYAN}; }}
.smn-untertitel {{ color:{GRAU}; font-size:10pt; margin:0 0 16px 0; }}
h2 {{ font-weight:700; font-size:14pt; letter-spacing:-.01em; color:{INK}; margin:24px 0 8px 0;
      padding-top:7px; border-top:2px solid {INK}; page-break-after:avoid; }}
h3 {{ font-weight:650; font-size:11pt; color:{INK}; margin:16px 0 6px 0; page-break-after:avoid; }}
h4 {{ font-weight:600; font-size:9.8pt; color:{INK}; margin:12px 0 4px 0; }}
p {{ margin:0 0 8px 0; }}
strong, b {{ font-weight:620; }}
a {{ color:{PETROL}; text-decoration:none; }}

blockquote {{ margin:12px 0; padding:10px 14px; background:{CYAN_HELL};
              border-left:3px solid {CYAN}; font-size:9.4pt; }}
blockquote p {{ margin:0; }}

table {{ border-collapse:collapse; width:100%; margin:10px 0 14px 0; font-size:8.8pt; }}
th {{ background:{INK}; color:#fff; font-weight:600; padding:6px 8px;
      border:1px solid {INK}; text-align:left; }}
td {{ border:1px solid {LINIE}; padding:6px 8px; vertical-align:top; }}
tr:nth-child(even) td {{ background:{ZEBRA}; }}
tr {{ page-break-inside:avoid; }}

ul, ol {{ margin:6px 0 12px 0; padding-left:20px; }}
li {{ margin-bottom:3px; }}
hr {{ border:none; border-top:1px solid {LINIE}; margin:20px 0; }}
code {{ background:#f0f2f3; padding:1px 5px; border-radius:3px; font-size:9pt;
        font-family:'SF Mono',Menlo,monospace; }}

.offen, mark {{ background:#fff2cc; padding:0 3px; }}

table.smn-meta tr td {{ background:#fff; }}
table.smn-meta tr td:first-child {{ background:{ZEBRA}; font-weight:600; width:22%; }}
.smn-unterschrift {{ margin-top:34px; page-break-inside:avoid; }}
.smn-unterschrift div {{ margin-bottom:26px; }}
.smn-linie {{ border-bottom:1px solid {INK}; width:62%; margin-top:22px; }}
.smn-fuss {{ margin-top:26px; padding-top:8px; border-top:1px solid {LINIE};
             font-size:7.6pt; color:{GRAU}; }}
"""


def kopf_kiss(kontext):
    return f"""<div class="kiss-kopf">
  <img src="data:image/png;base64,{b64(os.path.join(ASSETS, 'kissconcepts-logo.png'))}" alt="KISSconcepts">
  <div class="kiss-kontext">{kontext}</div>
</div>
<div class="kiss-akzent"></div>"""


MARKEN_STIL = {
    "smn": {"name": "Skill Me Now", "css": css_smn, "kopf": kopf_smn,
            "kontext": "Skill Me Now · KISSconcepts GmbH"},
    "kissconcepts": {"name": "KISSconcepts", "css": css_kiss, "kopf": kopf_kiss,
                     "kontext": "KISSconcepts GmbH · Pfronten"},
}


def frontmatter_lesen(text):
    meta = {}
    if text.startswith("---"):
        ende = text.find("\n---", 3)
        if ende > 0:
            for zeile in text[3:ende].strip().splitlines():
                if ":" in zeile:
                    k, v = zeile.split(":", 1)
                    meta[k.strip().lower()] = v.strip().strip('"').strip("'")
            text = text[ende + 4:].lstrip("\n")
    return meta, text


def metablock(meta):
    zeilen = [("Dokument", meta.get("title", "")),
              ("Version", meta.get("version", "")),
              ("Stand", meta.get("stand", "")),
              ("Erstellt von", meta.get("author", ""))]
    zeilen = [(k, v) for k, v in zeilen if v]
    if len(zeilen) < 2:
        return ""
    tr = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in zeilen)
    return f'<table class="smn-meta">{tr}</table>'


def unterschriftsblock():
    return """<div class="smn-unterschrift">
<div><b>Freigabe</b></div>
<div>Datum<div class="smn-linie"></div></div>
<div>Unterschrift Geschäftsführung<div class="smn-linie"></div></div>
</div>"""


def marke_bestimmen(wert):
    schluessel = MARKEN.get((wert or "smn").strip().lower())
    if not schluessel:
        sys.exit(f"Unbekannte Marke „{wert}“ — erlaubt sind: smn, kissconcepts")
    return schluessel


def bauen(md_pfad, pdf_pfad, landscape=False, marke=None):
    roh = open(md_pfad, encoding="utf-8").read()
    meta, md = frontmatter_lesen(roh)
    landscape = landscape or str(meta.get("landscape", "")).lower() in ("true", "ja", "yes", "1")
    marke = marke_bestimmen(marke or meta.get("marke"))
    stil = MARKEN_STIL[marke]

    md = md.replace("- [ ] ", "- ☐ ").replace("- [x] ", "- ☑ ")
    körper = subprocess.run(
        ["pandoc", "-f", "markdown+hard_line_breaks+pipe_tables+raw_html+mark",
         "-t", "html5", "--wrap=none"],
        input=md, capture_output=True, text=True, check=True).stdout

    titel = meta.get("title", "")
    if not titel:                                   # sonst erste H1 als Titel übernehmen
        m = re.search(r"<h1[^>]*>(.*?)</h1>", körper, re.S)
        if m:
            titel = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            körper = körper.replace(m.group(0), "", 1)
    else:
        körper = re.sub(r"<h1[^>]*>.*?</h1>", "", körper, count=1, flags=re.S)

    titel_html = titel
    if marke == "kissconcepts" and titel and not titel.rstrip().endswith((".", "!", "?", "…", ":")):
        titel_html = f'{titel}<span class="kiss-punkt">.</span>'   # Punkt wie im Logo

    groesse = "A4 landscape" if landscape else "A4"
    untertitel = f'<p class="smn-untertitel">{meta["subtitle"]}</p>' if meta.get("subtitle") else ""
    kontext = meta.get("header", stil["kontext"])
    signatur = unterschriftsblock() if str(meta.get("signature", "")).lower() in ("true", "ja", "yes", "1") else ""

    html = f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<title>{titel}</title><style>{stil['css'](groesse)}{AMPEL if marke == 'kissconcepts' else ''}</style></head><body>
{stil['kopf'](kontext)}
{f'<h1>{titel_html}</h1>' if titel else ''}
{untertitel}
{metablock(meta)}
{körper}
{signatur}
</body></html>"""

    tmp = tempfile.mkdtemp()
    hp = os.path.join(tmp, "dok.html")
    open(hp, "w", encoding="utf-8").write(html)
    ziel = os.path.abspath(pdf_pfad)
    os.makedirs(os.path.dirname(ziel) or ".", exist_ok=True)
    if os.path.exists(ziel):
        os.remove(ziel)                             # sonst meldet ein alter Stand fälschlich Erfolg
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={ziel}", "--virtual-time-budget=9000",
                    f"file://{hp}"], capture_output=True)
    shutil.rmtree(tmp, ignore_errors=True)
    if not os.path.exists(ziel):
        sys.exit("PDF konnte nicht erzeugt werden — läuft Chrome unter dem erwarteten Pfad?")
    print(f"✅ {os.path.basename(ziel)}  ({os.path.getsize(ziel)//1024} KB, Marke {stil['name']}"
          f"{', Querformat' if landscape else ''})")
    return ziel


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="PDF im Markendesign (Skill Me Now oder KISSconcepts) bauen")
    p.add_argument("markdown"); p.add_argument("pdf")
    p.add_argument("--landscape", action="store_true", help="Querformat für breite Tabellen")
    p.add_argument("--marke", help="smn (Standard) oder kissconcepts; überschreibt das Frontmatter")
    a = p.parse_args()
    bauen(a.markdown, a.pdf, a.landscape, a.marke)
