#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut aus einer Markdown-Datei ein PDF im Skill-Me-Now-Markendesign.

    python3 build_pdf.py dokument.md ausgabe.pdf [--landscape]

Steuerung über YAML-Frontmatter am Anfang der Markdown-Datei (alles optional):

    ---
    title: Zusammenarbeit mit Akteuren
    subtitle: Nachweis nach § 178 SGB III
    header: QM-Dokumentation AZAV
    version: "1.3"
    stand: 08.09.2026
    author: Simon Doser, Geschäftsführung
    signature: true          # erzeugt Freigabe-/Unterschriftenfeld am Ende
    landscape: true          # Querformat, sinnvoll ab etwa 6 Tabellenspalten
    ---

Logo und Schriften liegen im Skill und werden eingebettet — das PDF ist damit
auf jedem Rechner identisch, auch ohne installierte Fredoka.
"""
import argparse, base64, os, re, subprocess, sys, tempfile, shutil

HIER   = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HIER), "assets")
LOGO   = os.path.join(ASSETS, "smn-logo.png")
FONTS  = os.path.join(ASSETS, "fonts")

# --- Markenfarben (aus dem Originallogo) ---------------------------------
BLAU    = "#0B3A8E"   # Primärfarbe, Schriftzug im Logo
MAGENTA = "#E926C8"   # Akzent, linke Kante der Abschnittsüberschriften
MITTEL  = "#2C6FE0"
HELL    = "#5BC0F8"
GRAU    = "#5c6470"
LINIE   = "#c7d3e8"
ZEBRA   = "#f7f9fd"
KASTEN  = "#f2f6fd"

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def font_face(datei, gewicht):
    pfad = os.path.join(FONTS, datei)
    if not os.path.exists(pfad):
        return ""
    b64 = base64.b64encode(open(pfad, "rb").read()).decode()
    return (f"@font-face{{font-family:'FredokaSMN';font-weight:{gewicht};font-style:normal;"
            f"src:url(data:font/ttf;base64,{b64}) format('truetype');}}\n")


def css(landscape=False):
    faces = (font_face("Fredoka-Regular.ttf", 400)
             + font_face("Fredoka-Medium.ttf", 500)
             + font_face("Fredoka-SemiBold.ttf", 600)
             + font_face("Fredoka-Bold.ttf", 700))
    groesse = "A4 landscape" if landscape else "A4"
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


def bauen(md_pfad, pdf_pfad, landscape=False):
    roh = open(md_pfad, encoding="utf-8").read()
    meta, md = frontmatter_lesen(roh)
    landscape = landscape or str(meta.get("landscape", "")).lower() in ("true", "ja", "yes", "1")

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

    logo_b64 = base64.b64encode(open(LOGO, "rb").read()).decode()
    untertitel = f'<p class="smn-untertitel">{meta["subtitle"]}</p>' if meta.get("subtitle") else ""
    kontext = meta.get("header", "Skill Me Now · KISSconcepts GmbH")
    signatur = unterschriftsblock() if str(meta.get("signature", "")).lower() in ("true", "ja", "yes", "1") else ""

    html = f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<title>{titel}</title><style>{css(landscape)}</style></head><body>
<div class="smn-kopf">
  <img src="data:image/png;base64,{logo_b64}" alt="Skill Me Now">
  <div class="smn-kontext">{kontext}</div>
</div>
<div class="smn-balken"></div>
{f'<h1>{titel}</h1>' if titel else ''}
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
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={ziel}", "--virtual-time-budget=9000",
                    f"file://{hp}"], capture_output=True)
    shutil.rmtree(tmp, ignore_errors=True)
    if not os.path.exists(ziel):
        sys.exit("PDF konnte nicht erzeugt werden — läuft Chrome unter dem erwarteten Pfad?")
    print(f"✅ {os.path.basename(ziel)}  ({os.path.getsize(ziel)//1024} KB"
          f"{', Querformat' if landscape else ''})")
    return ziel


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="PDF im Skill-Me-Now-Design bauen")
    p.add_argument("markdown"); p.add_argument("pdf")
    p.add_argument("--landscape", action="store_true", help="Querformat für breite Tabellen")
    a = p.parse_args()
    bauen(a.markdown, a.pdf, a.landscape)
