#!/usr/bin/env python3
"""Generate the binary starter files in skill/templates/files/ from skill/tokens.json.

    python3 dev/build-kit/build_files.py           write the files
    python3 dev/build-kit/build_files.py --check   change nothing; fail if a file's theme
                                                   colours or fonts differ from tokens.json

Writes:
  airi-document.docx    Word document: named styles, page furniture, sample table
  airi-og-image.html    Open Graph / social card source (1200 x 630)
  airi-og-image.png     the card, rendered with headless Chrome

The document is also the starting point for Google Docs: upload it to Drive and open it
with Docs. Needs python-docx and pillow, plus google-chrome for the images. The .docx is not byte-stable (Word
stamps dates), so build.py --check compares its theme colours and fonts, not bytes.

There is no slide deck or workbook here on purpose: a generated deck was tried in November
2026 and was not good enough. Decks start from a recent AIRI deck or a Claude slide artifact.
"""
import copy
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skill"
OUT = SKILL / "templates" / "files"
LOGOS = SKILL / "logos"
T = json.loads((SKILL / "tokens.json").read_text())
C, D, SLOTS, TY = T["color"], T["data"], T["theme"]["slots"], T["typography"]
URL = T["video"]["end-card"]["url"]
FONT = "Figtree"
GEN = f"AIRI brand kit {T['version']}. Generated from tokens.json by dev/build-kit/build_files.py."

SCHEME_ORDER = [("dk1", "dark1"), ("lt1", "light1"), ("dk2", "dark2"), ("lt2", "light2"),
                ("accent1", "accent1"), ("accent2", "accent2"), ("accent3", "accent3"),
                ("accent4", "accent4"), ("accent5", "accent5"), ("accent6", "accent6"),
                ("hlink", "hyperlink"), ("folHlink", "followed-hyperlink")]

def bare(h):
    return h.lstrip("#").upper()


# ---------------------------------------------------------------- theme XML (the Office theme in the .docx)

def theme_xml(xml: bytes) -> bytes:
    """Put the kit's 12 colours and Figtree into an Office theme part."""
    s = xml.decode("utf-8")
    slots = "".join(f'<a:{tag}><a:srgbClr val="{bare(SLOTS[key])}"/></a:{tag}>' for tag, key in SCHEME_ORDER)
    s = re.sub(r"<a:clrScheme\b[^>]*>.*?</a:clrScheme>", f'<a:clrScheme name="AIRI">{slots}</a:clrScheme>', s, count=1, flags=re.S)
    for kind in ("majorFont", "minorFont"):
        s = re.sub(rf'(<a:{kind}>\s*<a:latin typeface=")[^"]*(")', rf"\g<1>{FONT}\g<2>", s, count=1)
    s = re.sub(r'(<a:fontScheme name=")[^"]*(")', r"\g<1>AIRI\g<2>", s, count=1)
    return s.encode("utf-8")


def read_theme(path: Path):
    """(colour scheme, major font, minor font) from the theme part inside an Office file."""
    with zipfile.ZipFile(path) as z:
        name = next(n for n in z.namelist() if re.search(r"theme/theme1\.xml$", n))
        s = z.read(name).decode("utf-8")
    scheme = {}
    for tag, key in SCHEME_ORDER:
        m = re.search(rf"<a:{tag}>\s*<a:srgbClr val=\"([0-9A-Fa-f]{{6}})\"", s)
        scheme[key] = "#" + m.group(1).upper() if m else None
    fonts = [re.search(rf'<a:{k}>\s*<a:latin typeface="([^"]*)"', s) for k in ("majorFont", "minorFont")]
    return scheme, [f.group(1) if f else None for f in fonts]


# ---------------------------------------------------------------- logos as PNG

def chrome(page: Path, shot: Path, w: int, h: int, transparent=False):
    exe = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if not exe:
        sys.exit("needs google-chrome or chromium for the images")
    args = [exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
            f"--window-size={w},{h}", f"--screenshot={shot}", "--allow-file-access-from-files"]
    if transparent:
        args.append("--default-background-color=00000000")
    subprocess.run(args + [page.as_uri()], check=True, capture_output=True, timeout=60)


# ---------------------------------------------------------------- PowerPoint

def build_docx(dest: Path):
    from docx import Document
    from docx.enum.section import WD_SECTION
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor

    rgb = lambda h: RGBColor.from_string(bare(h))
    dp = TY["docs-pt"]
    doc = Document()
    theme = doc.part.part_related_by(RT.THEME)
    theme._blob = theme_xml(theme.blob)

    def font(style_or_run, size=None, colour=None, bold=None):
        f = style_or_run.font
        f.name = FONT
        rpr = style_or_run.element.get_or_add_rPr() if hasattr(style_or_run.element, "get_or_add_rPr") else None
        if rpr is not None:
            rf = rpr.find(qn("w:rFonts"))
            if rf is None:
                rf = OxmlElement("w:rFonts"); rpr.insert(0, rf)
            for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
                if rf.get(qn(a)) is not None:
                    del rf.attrib[qn(a)]
            for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
                rf.set(qn(a), FONT)
        if size:
            f.size = Pt(size)
        if colour:
            f.color.rgb = rgb(colour)
        if bold is not None:
            f.bold = bold

    st = doc.styles
    spec = {"Normal": (dp["body"], C["text"], False), "Title": (dp["title"], C["link"], True),
            "Subtitle": (dp["subtitle"] if "subtitle" in dp else 14, C["text-muted"], False),
            "Heading 1": (dp["h1"] if "h1" in dp else 18, C["link"], True),
            "Heading 2": (dp["h2"] if "h2" in dp else 14, C["text"], True),
            "Heading 3": (dp["h3"] if "h3" in dp else 12, C["text"], True),
            "Caption": (dp["caption"] if "caption" in dp else 9, C["text-muted"], False)}
    for name, (size, colour, bold) in spec.items():
        s = st[name]
        font(s, size, colour, bold)
        s.font.italic = False
        rpr = s.element.get_or_add_rPr()
        for e in rpr.findall(qn("w:spacing")) + rpr.findall(qn("w:caps")):   # no letter-spacing, no all-caps
            rpr.remove(e)
        pf = s.paragraph_format
        if name == "Normal":
            pf.line_spacing = 1.15
            pf.space_after = Pt(8)
        elif name.startswith("Heading"):
            pf.space_before, pf.space_after = Pt(18 if name == "Heading 1" else 12), Pt(6)
            pf.keep_with_next = True
        elif name == "Title":
            pf.space_after = Pt(4)
            # Word's Title has a bottom border; the kit puts rules above blocks, never under headings.
            ppr = s.element.get_or_add_pPr()
            for e in ppr.findall(qn("w:pBdr")):
                ppr.remove(e)
        elif name == "Subtitle":
            pf.space_after = Pt(16)
    # Links are red and underlined.
    try:
        link = st["Hyperlink"]
    except KeyError:
        from docx.enum.style import WD_STYLE_TYPE
        link = st.add_style("Hyperlink", WD_STYLE_TYPE.CHARACTER)
    link.font.color.rgb = rgb(C["link"]); link.font.underline = True

    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2.5)
    sec.top_margin, sec.bottom_margin = Cm(2.8), Cm(2.5)
    sec.header_distance = sec.footer_distance = Cm(0)
    text_w = sec.page_width - sec.left_margin - sec.right_margin

    def bar(par):
        """A full-width red bar, 7 pt tall: a shaded empty paragraph pulled out to the page edges."""
        pf = par.paragraph_format
        pf.left_indent, pf.right_indent = -sec.left_margin, -sec.right_margin
        pf.space_before = pf.space_after = Pt(0)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pf.line_spacing = Pt(7)
        ppr = par._p.get_or_add_pPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), bare(C["primary"]))
        ppr.append(shd)
        r = par.add_run("​"); r.font.size = Pt(2)

    hdr = sec.header
    bar(hdr.paragraphs[0])
    logo_p = hdr.add_paragraph()
    logo_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    logo_p.paragraph_format.space_before = Pt(10)
    logo_p.add_run().add_picture(str(LOGOS / "initiative" / "horizontal-on-light.png"), width=Cm(3.2))

    ftr = sec.footer
    fp = ftr.paragraphs[0]
    from docx.enum.text import WD_TAB_ALIGNMENT
    fp.style.paragraph_format.tab_stops.clear_all()  # Word's Footer style has its own centre and right stops
    fp.paragraph_format.tab_stops.clear_all()
    fp.paragraph_format.tab_stops.add_tab_stop(text_w, alignment=WD_TAB_ALIGNMENT.RIGHT)
    fp.paragraph_format.space_after = Pt(10)

    def muted(par, text):
        r = par.add_run(text); font(r, 9, C["text-muted"]); return r
    muted(fp, f"{URL}  ·  Contact: name@mit.edu\t")
    r = fp.add_run()
    for kind, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if kind:
            e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), kind); r._r.append(e)
        else:
            e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = text; r._r.append(e)
    font(r, 9, C["text-muted"])
    bar(ftr.add_paragraph())

    # Body.
    doc.add_paragraph("Document title", style="Title")
    doc.add_paragraph("A subtitle, in muted text, says what this document is for", style="Subtitle")
    meta = doc.add_table(rows=3, cols=2)
    for row, (k, v) in zip(meta.rows, (("Last update", "Day Month Year"), ("Contact", "Name, name@mit.edu"),
                                       ("Sharing", "Internal / shareable / public"))):
        for cell, text, b in ((row.cells[0], k, True), (row.cells[1], v, False)):
            p = cell.paragraphs[0]; p.paragraph_format.space_after = Pt(0)
            font(p.add_run(text), 9, C["text"], b)
    meta.columns[0].width = Cm(3)
    for row in meta.rows:
        row.cells[0].width = Cm(3)
    doc.add_paragraph()

    doc.add_paragraph("How to use this template", style="Heading 1")
    lead = doc.add_paragraph()
    r = lead.add_run("Start each new AIRI document from a copy of this file, then replace the text.")
    shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), bare(C["red-tint"]))
    r._r.get_or_add_rPr().append(shd)
    lead.add_run(" The look lives in the named styles, so pick a style from the style list instead of "
                 "formatting text by hand. New headings then come out right.")
    doc.add_paragraph("What each style is for", style="Heading 2")
    for item in ("Title and Heading 1 are the only red text. Heading 2 and below are near-black.",
                 "Normal text is Figtree 11 pt. Notes and captions use the Caption style, 9 pt and muted.",
                 "Links are red and underlined. Paste text without formatting to keep the styles.",
                 "The red bars, the logo and the footer are in the header and footer. Edit the footer's contact line once."):
        doc.add_paragraph(item, style="List Bullet")
    doc.add_paragraph("Tables", style="Heading 2")
    doc.add_paragraph("Header rows are bold on light grey. Keep tables plain: thin rules, no colour in the body cells "
                      "unless a scale from the kit carries meaning.")

    rows = [("Risk domain", "Entries", "Share"), ("Discrimination & toxicity", "182", "11%"),
            ("Privacy & security", "246", "15%"), ("Misinformation", "131", "8%")]
    t = doc.add_table(rows=len(rows), cols=3)
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "bottom", "insideH"):
        e = OxmlElement(f"w:{side}"); e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "4"); e.set(qn("w:color"), bare(C["rule"]))
        borders.append(e)
    t._tbl.tblPr.append(borders)
    for i, row in enumerate(rows):
        for j, text in enumerate(row):
            cell = t.rows[i].cells[j]
            p = cell.paragraphs[0]; p.paragraph_format.space_after = Pt(2); p.paragraph_format.space_before = Pt(2)
            if j:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            font(p.add_run(text), dp["body"], C["text"], i == 0)
            if i == 0:
                tcpr = cell._tc.get_or_add_tcPr()
                sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:fill"), bare(C["fill"]))
                tcpr.append(sh)
    doc.add_paragraph("Table 1. Entries by risk domain. Source: illustrative data.", style="Caption")
    doc.add_paragraph("A third-level heading", style="Heading 3")
    doc.add_paragraph("Body text continues here. Mark draft or AI-written passages with the pale yellow highlight "
                      "until someone has checked them.")
    doc.core_properties.title = "AIRI document template"
    doc.core_properties.subject = GEN
    doc.save(dest)


# ---------------------------------------------------------------- Excel

def og_html():
    f = "../video/fonts/Figtree-wght.ttf"
    logo = "../../logos/initiative/horizontal-on-red.svg"
    return f"""<!doctype html>
<!-- {GEN}
     Open Graph / social share card, 1200 x 630. The gap rule applies: it reuses the video title card
     (red ground, white logo, white bold title). Change the title and the line under it, then render:
     google-chrome --headless=new --hide-scrollbars --window-size=1200,630 --screenshot=card.png airi-og-image.html -->
<html lang="en">
<head>
<meta charset="utf-8">
<title>AIRI social card</title>
<style>
  @font-face {{ font-family: "Figtree"; font-weight: 300 900; src: url("{f}") format("truetype"), local("Figtree"); }}
  html, body {{ margin: 0; width: 1200px; height: 630px; overflow: hidden; }}
  body {{ background: {C["primary"]}; color: {C["white"]}; font-family: Figtree, Arial, sans-serif; }}
  .card {{ box-sizing: border-box; width: 1200px; height: 630px; padding: 64px 80px;
          display: flex; flex-direction: column; justify-content: space-between; }}
  .logo {{ height: 72px; width: auto; align-self: flex-start; }}
  h1 {{ margin: 0; font-size: 64px; line-height: 1.12; font-weight: 700; max-width: 960px; }}
  p {{ margin: 16px 0 0; font-size: 28px; line-height: 1.3; font-weight: 400; }}
  .url {{ font-size: 24px; font-weight: 700; }}
</style>
</head>
<body>
<div class="card">
  <img class="logo" src="{logo}" alt="MIT AI Risk Initiative">
  <div>
    <h1>The title says what the page is about</h1>
    <p>One line under it, in plain words.</p>
  </div>
  <div class="url">{URL}</div>
</div>
</body>
</html>
"""


def build_og(html: Path, png: Path):
    html.write_text(og_html())
    chrome(html, png, 1200, 630)


# ---------------------------------------------------------------- check and main

def check():
    problems = []
    want = {k: SLOTS[k].upper() for _, k in SCHEME_ORDER}
    for name in ("airi-document.docx",):
        path = OUT / name
        if not path.exists():
            problems.append(f"skill/templates/files/{name} is missing: run dev/build-kit/build_files.py")
            continue
        scheme, fonts = read_theme(path)
        if scheme != want or fonts != [FONT, FONT]:
            problems.append(f"skill/templates/files/{name}: theme colours or fonts differ from tokens.json: run dev/build-kit/build_files.py")
    for name in ("airi-og-image.html", "airi-og-image.png"):
        if not (OUT / name).exists():
            problems.append(f"skill/templates/files/{name} is missing: run dev/build-kit/build_files.py")
    if (OUT / "airi-og-image.html").exists() and (OUT / "airi-og-image.html").read_text() != og_html():
        problems.append("skill/templates/files/airi-og-image.html is out of date: run dev/build-kit/build_files.py")
    return problems


def main():
    if "--check" in sys.argv:
        problems = check()
        for p in problems:
            print("FAIL", p)
        print("ok: template files agree with tokens.json" if not problems else f"{len(problems)} problem(s)")
        sys.exit(1 if problems else 0)
    OUT.mkdir(parents=True, exist_ok=True)
    build_docx(OUT / "airi-document.docx")
    build_og(OUT / "airi-og-image.html", OUT / "airi-og-image.png")
    for p in sorted(OUT.iterdir()):
        print("wrote", p.relative_to(ROOT))


if __name__ == "__main__":
    main()
