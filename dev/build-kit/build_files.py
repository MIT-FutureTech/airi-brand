#!/usr/bin/env python3
"""Generate the binary starter files in skill/templates/files/ from skill/tokens.json.

    python3 dev/build-kit/build_files.py           write the files
    python3 dev/build-kit/build_files.py --check   change nothing; fail if a file's theme
                                                   colours or fonts differ from tokens.json

Writes:
  airi-slides.pptx      PowerPoint deck: AIRI theme, layouts and sample slides
  airi-document.docx    Word document: named styles, page furniture, sample table
  airi-sheet.xlsx       Excel workbook: AIRI theme, Figtree, palette sheet, sample chart
  airi-og-image.html    Open Graph / social card source (1200 x 630)
  airi-og-image.png     the card, rendered with headless Chrome

Each file is also the starting point for Google Slides, Docs and Sheets: upload it to
Drive and open it with the Google app. Needs python-pptx, python-docx, openpyxl and
pillow, plus google-chrome for the two images. The files are not byte-stable (Office
stamps dates), so build.py --check compares their theme colours and fonts, not bytes.
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
FONT_FILE = SKILL / "templates" / "video" / "fonts" / "Figtree-wght.ttf"
T = json.loads((SKILL / "tokens.json").read_text())
C, D, SLOTS, TY = T["color"], T["data"], T["theme"]["slots"], T["typography"]
CATS = D["categorical"]
URL = T["video"]["end-card"]["url"]
FONT = "Figtree"
GEN = f"AIRI brand kit {T['version']}. Generated from tokens.json by dev/build-kit/build_files.py."

SCHEME_ORDER = [("dk1", "dark1"), ("lt1", "light1"), ("dk2", "dark2"), ("lt2", "light2"),
                ("accent1", "accent1"), ("accent2", "accent2"), ("accent3", "accent3"),
                ("accent4", "accent4"), ("accent5", "accent5"), ("accent6", "accent6"),
                ("hlink", "hyperlink"), ("folHlink", "followed-hyperlink")]

# Sample data shared by the slide and sheet charts. Illustrative, not data.
DOMAINS = ["Discrimination", "Privacy", "Misinformation", "Misuse", "Human-AI", "Socioeconomic", "AI safety"]
HIGHLIGHT = [41, 68, 37, 52, 29, 33, 47]
SUBJECT = 1   # Privacy: the bar the chart is about
ACTORS = [("Developers", [62, 71, 48, 66, 30, 22, 74]), ("Deployers", [41, 58, 27, 35, 24, 18, 39]),
          ("Governments", [55, 63, 52, 47, 15, 41, 33]), ("Investors", [12, 20, 8, 15, 6, 29, 10])]


def bare(h):
    return h.lstrip("#").upper()


# ---------------------------------------------------------------- theme XML (shared by all three Office files)

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

def svg_png(svg: Path, height_px: int, dest: Path):
    """Render an SVG to a transparent PNG with headless Chrome, cropped to the drawing."""
    from PIL import Image
    vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', svg.read_text()).group(1).split()]
    w = round(height_px * vb[2] / vb[3])
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "p.html"
        page.write_text(f'<html><body style="margin:0;background:transparent">'
                        f'<img src="{svg.as_uri()}" style="display:block;width:{w}px;height:{height_px}px"></body></html>')
        shot = Path(tmp) / "s.png"
        chrome(page, shot, w, height_px, transparent=True)
        Image.open(shot).convert("RGBA").save(dest)


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

def build_pptx(dest: Path, tmp: Path):
    from lxml import etree
    from pptx import Presentation
    from pptx.chart.data import CategoryChartData
    from pptx.dml.color import RGBColor
    from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT
    from pptx.oxml.ns import qn
    from pptx.util import Emu, Pt

    rgb = lambda h: RGBColor.from_string(bare(h))
    sp = TY["slides-pt-960"]
    prs = Presentation()
    old_w = prs.slide_width
    prs.slide_width, prs.slide_height = Pt(960), Pt(540)
    master = prs.slide_master

    # Theme colours and fonts.
    theme = master.part.part_related_by(RT.THEME)
    theme._blob = theme_xml(theme.blob)

    # Stretch the 4:3 master and layouts to 16:9, then set the kit's margins.
    kx = prs.slide_width / old_w
    for holder in [master] + list(master.slide_layouts):
        for shp in holder.shapes:
            if shp.left is not None:
                shp.left, shp.width = Emu(int(shp.left * kx)), Emu(int(shp.width * kx))
    M = {"top": Pt(48), "side": Pt(64), "bottom": Pt(72)}
    body_w = prs.slide_width - 2 * M["side"]
    title_h = Pt(72)

    def place(shp, top, height):
        shp.left, shp.top, shp.width, shp.height = M["side"], top, body_w, height

    from pptx.enum.shapes import PP_PLACEHOLDER as PH
    TITLES, BODIES = (PH.TITLE, PH.CENTER_TITLE), (PH.BODY, PH.OBJECT)
    body_top = M["top"] + title_h + Pt(24)
    body_h = prs.slide_height - body_top - M["bottom"]
    # Master and the plain one-column layouts: title band at the top margin, body under it.
    plain = ("Title and Content", "Title Only")
    for holder in [master] + [l for l in master.slide_layouts if l.name in plain]:
        for shp in holder.placeholders:
            t = shp.placeholder_format.type
            if t in TITLES:
                place(shp, M["top"], title_h)
                shp.text_frame.vertical_anchor = MSO_ANCHOR.TOP
            elif t in BODIES:
                place(shp, body_top, body_h)
            elif t in (PH.FOOTER, PH.DATE, PH.SLIDE_NUMBER):
                shp.top = prs.slide_height - Pt(48)
    master.background.fill.solid()
    master.background.fill.fore_color.rgb = rgb(C["background"])

    # Master text styles: titles red bold, body ink, red square list markers.
    A = "http://schemas.openxmlformats.org/drawingml/2006/main"
    tx = master.element.find(qn("p:txStyles"))

    def set_level(lvl, size, colour_scheme=None, bold=False, bullet=False, indent=0):
        for tag in ("a:buNone", "a:buChar", "a:buAutoNum", "a:buClr", "a:buSzPct", "a:buFont"):
            for e in lvl.findall(qn(tag)):
                lvl.remove(e)
        d = lvl.find(qn("a:defRPr"))
        if d is None:
            d = etree.SubElement(lvl, qn("a:defRPr"))
        d.set("sz", str(int(size * 100)))
        d.set("b", "1" if bold else "0")
        for e in list(d):
            if e.tag in (qn("a:solidFill"), qn("a:latin")):
                d.remove(e)
        fill = etree.Element(qn("a:solidFill"))
        etree.SubElement(fill, qn("a:schemeClr")).set("val", colour_scheme or "tx1")
        d.insert(0, fill)
        latin = etree.Element(qn("a:latin"))
        latin.set("typeface", "+mj-lt" if bold else "+mn-lt")
        d.append(latin)
        idx = list(lvl).index(d)
        if bullet:
            bc = etree.Element(qn("a:buClr"))
            etree.SubElement(bc, qn("a:schemeClr")).set("val", "accent1")
            bs = etree.Element(qn("a:buSzPct")); bs.set("val", "60000")
            bf = etree.Element(qn("a:buFont")); bf.set("typeface", "Arial")
            ch = etree.Element(qn("a:buChar")); ch.set("char", "■")
            for k, e in enumerate((bc, bs, bf, ch)):
                lvl.insert(idx + k, e)
            lvl.set("marL", str(Pt(18 + indent)))
            lvl.set("indent", str(-Pt(18)))
        else:
            lvl.insert(idx, etree.Element(qn("a:buNone")))
            lvl.set("marL", str(Pt(indent)))
            lvl.set("indent", "0")
        lvl.set("algn", "l")
        ln = lvl.find(qn("a:lnSpc"))
        if ln is None:
            ln = etree.Element(qn("a:lnSpc")); lvl.insert(0, ln)
        for e in list(ln):
            ln.remove(e)
        etree.SubElement(ln, qn("a:spcPct")).set("val", "100000" if bold else "120000")

    title_lvl = tx.find(qn("p:titleStyle")).find(qn("a:lvl1pPr"))
    set_level(title_lvl, sp["title"], "accent1", bold=True)
    body = tx.find(qn("p:bodyStyle"))
    for n in range(1, 10):
        lvl = body.find(qn(f"a:lvl{n}pPr"))
        if lvl is not None:
            set_level(lvl, sp["body"] if n <= 2 else sp["small"], "tx1", bullet=True, indent=18 * (n - 1))
    title_ph = master.placeholders[0]
    title_ph.text_frame.vertical_anchor = MSO_ANCHOR.TOP

    # Red layouts: Title Slide (cover) and Section Header (divider).
    layouts = {l.name: l for l in master.slide_layouts}

    def red_layout(layout, title_size, title_top, title_h_, sub_top=None):
        layout.background.fill.solid()
        layout.background.fill.fore_color.rgb = rgb(C["primary"])
        for shp in layout.placeholders:
            t = shp.placeholder_format.type
            if t in TITLES:
                shp.left, shp.top, shp.width, shp.height = M["side"], title_top, body_w, title_h_
                shp.text_frame.vertical_anchor = MSO_ANCHOR.BOTTOM
                style_ph(shp, title_size, C["white"], True)
            elif sub_top is not None and t in (PH.SUBTITLE, PH.BODY):
                shp.left, shp.top, shp.width, shp.height = M["side"], sub_top, body_w, Pt(64)
                shp.text_frame.vertical_anchor = MSO_ANCHOR.TOP
                style_ph(shp, sp["body"], C["white"], False)

    def style_ph(shp, size, colour, bold):
        """Formatting held in a layout placeholder's list style, so new slides inherit it."""
        txb = shp.text_frame._txBody
        lst = txb.find(qn("a:lstStyle"))
        if lst is None:
            lst = etree.Element(qn("a:lstStyle")); txb.insert(1, lst)
        for e in list(lst):
            lst.remove(e)
        lvl = etree.SubElement(lst, qn("a:lvl1pPr"))
        lvl.set("algn", "l"); lvl.set("marL", "0"); lvl.set("indent", "0")
        etree.SubElement(lvl, qn("a:buNone"))
        d = etree.SubElement(lvl, qn("a:defRPr"))
        d.set("sz", str(int(size * 100))); d.set("b", "1" if bold else "0")
        f = etree.SubElement(d, qn("a:solidFill"))
        etree.SubElement(f, qn("a:srgbClr")).set("val", bare(colour))

    red_layout(layouts["Title Slide"], sp["cover"], Pt(150), Pt(130), Pt(296))
    red_layout(layouts["Section Header"], sp["title"], Pt(160), Pt(120), Pt(296))

    # Logos for the red slides.
    airi_png = LOGOS / "initiative" / "horizontal-on-red.png"
    ft_png = tmp / "futuretech-white.png"
    svg_png(LOGOS / "futuretech" / "futuretech-on-dark.svg", 160, ft_png)

    def text_box(slide, x, y, w, h, runs, size, colour=C["text"], anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT):
        """runs: list of paragraphs; each a list of (text, bold, colour or None)."""
        tb = slide.shapes.add_textbox(x, y, w, h)
        tf = tb.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = anchor
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        for i, para in enumerate(runs):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            for text, bold, col in para:
                r = p.add_run()
                r.text = text
                r.font.size, r.font.bold, r.font.name = Pt(size), bold, FONT
                r.font.color.rgb = rgb(col or colour)
        return tb

    def source(slide, text):
        text_box(slide, M["side"], prs.slide_height - Pt(56), body_w, Pt(20), [[(text, False, C["text-muted"])]], sp["small"])

    def notes(slide, text):
        slide.notes_slide.notes_text_frame.text = text

    # 1. Cover.
    s = prs.slides.add_slide(layouts["Title Slide"])
    s.shapes.title.text = "The title says what the work is"
    s.placeholders[1].text = "One sentence on what the work is.\nMonth Year"
    s.shapes.add_picture(str(ft_png), M["side"], prs.slide_height - Pt(48) - Pt(36), height=Pt(36))
    s.shapes.add_picture(str(airi_png), prs.slide_width - M["side"] - Pt(120), prs.slide_height - Pt(48) - Pt(36), height=Pt(36))
    notes(s, f"{GEN}\nCover: title, one sentence on what the work is, the date. FutureTech logo bottom left, AIRI bottom right. "
             "New slides: Home > New Slide picks up the AIRI layouts. Body slides carry no logo.")

    # 2. Section divider.
    s = prs.slides.add_slide(layouts["Section Header"])
    s.shapes.title.text = "Section title"
    for ph in s.placeholders:
        if ph.placeholder_format.idx != 0:
            ph.text = "Optional line under the section title"
    notes(s, "Section divider: full red, white title. Use the Section Header layout.")

    # 3. Title and body.
    s = prs.slides.add_slide(layouts["Title and Content"])
    s.shapes.title.text = "A slide title states the slide's point"
    tf = s.placeholders[1].text_frame
    lines = ["Titles are red, bold and make sense read alone. No eyebrow line, no subtitle.",
             "Body text is ink, at 14 pt on this page. Sources and footers are muted, 11 pt.",
             "Use only five sizes: cover 36, title 28, outcome 18, body 14, small 11.",
             "Charts: grey for context, red for the one thing the chart is about."]
    tf.text = lines[0]
    for line in lines[1:]:
        tf.add_paragraph().text = line
    notes(s, "Title and body layout. Lists use the small red square; use numbers only when order matters.")

    # 4. Main point.
    s = prs.slides.add_slide(layouts["Title Only"])
    s.shapes.title.text = "One main point, set large"
    text_box(s, M["side"], Pt(190), body_w, Pt(140),
             [[("The outcome sits at the outcome size, in muted text, with ", False, None),
               ("the key words in bold red", True, C["link"]), (".", False, None)]],
             sp["outcome"], C["text-muted"])

    # 5. Stat cards.
    s = prs.slides.add_slide(layouts["Title Only"])
    s.shapes.title.text = "Stat cards: the number is the outcome"
    gap, n = Pt(24), 3
    cw = int((body_w - gap * (n - 1)) / n)
    stats = [("74%", "of entries name at least one risk domain", "Base: 1,600 entries"),
             ("7", "risk domains in the AI Risk Repository", "Source: AI Risk Repository"),
             ("24", "subdomains below the seven domains", "Source: AI Risk Repository")]
    from pptx.enum.shapes import MSO_SHAPE
    for i, (num, what, note) in enumerate(stats):
        x = M["side"] + i * (cw + gap)
        card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Pt(160), cw, Pt(150))
        card.adjustments[0] = 0.04
        card.fill.solid(); card.fill.fore_color.rgb = rgb(C["surface"])
        card.line.color.rgb = rgb(C["rule"]); card.line.width = Pt(1)
        card.shadow.inherit = False
        text_box(s, x + Pt(12), Pt(172), cw - Pt(24), Pt(126),
                 [[(num, True, C["link"])], [(what, False, C["text"])], [(note, False, C["text-muted"])]], sp["body"])
        tb = s.shapes[-1].text_frame
        tb.paragraphs[0].runs[0].font.size = Pt(sp["cover"])
        tb.paragraphs[2].runs[0].font.size = Pt(sp["small"])
        tb.paragraphs[1].space_before = Pt(8); tb.paragraphs[2].space_before = Pt(8)
    source(s, "Numbers are placeholders.")

    def style_chart(chart):
        chart.font.name, chart.font.size = FONT, Pt(sp["small"])
        chart.font.color.rgb = rgb(C["text-muted"])
        chart.has_title = False

    def axis_lines(ax, show=True):
        ax.format.line.color.rgb = rgb(C["rule"])
        if not show:
            ax.format.line.fill.background()
        ax.tick_labels.font.color.rgb = rgb(C["text-muted"])
        ax.tick_labels.font.size = Pt(sp["small"])

    # 6. Chart: grey bars, the subject in red.
    s = prs.slides.add_slide(layouts["Title Only"])
    s.shapes.title.text = "Privacy and security is the risk named most often"
    cd = CategoryChartData()
    cd.categories = DOMAINS[::-1]
    cd.add_series("Share of documents (%)", HIGHLIGHT[::-1])
    gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, M["side"], Pt(132), body_w, Pt(320), cd)
    ch = gf.chart
    style_chart(ch)
    ch.has_legend = False
    plot = ch.plots[0]
    plot.gap_width = 60
    ser = plot.series[0]
    ser.format.fill.solid(); ser.format.fill.fore_color.rgb = rgb(C["gray"])
    subject = len(DOMAINS) - 1 - SUBJECT
    pt = ser.points[subject]
    pt.format.fill.solid(); pt.format.fill.fore_color.rgb = rgb(C["primary"])
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    dl.font.size, dl.font.color.rgb = Pt(sp["small"]), rgb(C["text"])
    va = ch.value_axis
    va.visible = False
    va.has_major_gridlines = False
    axis_lines(ch.category_axis)
    ch.category_axis.tick_labels.font.size = Pt(sp["small"])
    source(s, "Share of documents that name each domain (%). Source: illustrative data.")
    notes(s, "Chart slide: every bar grey, the one the title is about red. Bars that compare groups are one colour. "
             "The title states the finding; the source sits in the footer. Edit the data: right-click the chart > Edit Data.")

    # 7. Category example: one line per group, slots 1 to 4 in order.
    s = prs.slides.add_slide(layouts["Title Only"])
    s.shapes.title.text = "Developers disclose most, except on socioeconomic risk"
    cd = CategoryChartData()
    cd.categories = DOMAINS
    for name, vals in ACTORS:
        cd.add_series(name, vals)
    gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, M["side"], Pt(132), body_w, Pt(320), cd)
    ch = gf.chart
    style_chart(ch)
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.RIGHT
    ch.legend.include_in_layout = False
    ch.legend.font.size, ch.legend.font.color.rgb = Pt(sp["small"]), rgb(C["text"])
    from pptx.enum.chart import XL_MARKER_STYLE
    for ser, c in zip(ch.plots[0].series, CATS):
        ser.smooth = False
        ser.format.line.color.rgb = rgb(c["fill"]); ser.format.line.width = Pt(2.25)
        ser.marker.style = XL_MARKER_STYLE.CIRCLE; ser.marker.size = 6
        ser.marker.format.fill.solid(); ser.marker.format.fill.fore_color.rgb = rgb(c["fill"])
        ser.marker.format.line.color.rgb = rgb(c["fill"])
    va = ch.value_axis
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = rgb(C["border"])
    va.format.line.fill.background()
    va.maximum_scale, va.minimum_scale, va.major_unit = 80, 0, 20
    axis_lines(va)
    axis_lines(ch.category_axis)
    source(s, "Share of organisations that disclose each risk, by type of actor (%). Source: illustrative data.")
    notes(s, "Category colours: one line per group, in slot order from 1 (blue, sky, violet, mauve ...). "
             "Use them only when each group needs its own mark. More than eight groups: grey with direct labels.")

    # 8. Closing.
    s = prs.slides.add_slide(layouts["Section Header"])
    s.shapes.title.text = "Next steps"
    for ph in s.placeholders:
        if ph.placeholder_format.idx != 0:
            ph.text = URL
    s.shapes.add_picture(str(airi_png), M["side"], M["top"], height=Pt(60))
    notes(s, "Closing: next steps and the on-red logo as a banner.")

    prs.core_properties.title = "AIRI slide template"
    prs.core_properties.subject = GEN
    prs.save(dest)


# ---------------------------------------------------------------- Word

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

def build_xlsx(dest: Path):
    from openpyxl import Workbook
    from openpyxl.chart import BarChart, Reference
    from openpyxl.chart.label import DataLabelList
    from openpyxl.chart.marker import DataPoint
    from openpyxl.chart.shapes import GraphicalProperties
    from openpyxl.chart.text import RichText
    from openpyxl.drawing.text import CharacterProperties, Paragraph, ParagraphProperties, Font as DFont
    from openpyxl.styles import Alignment, Border, Font, NamedStyle, PatternFill, Side
    from openpyxl.writer.theme import theme_xml as default_theme

    wb = Workbook()
    wb.loaded_theme = theme_xml(default_theme.encode("utf-8"))
    # Default font for every cell: Figtree 11, ink.
    wb._fonts[0] = Font(name=FONT, sz=11, color=bare(C["text"]))
    normal = wb._named_styles["Normal"]
    normal.font = Font(name=FONT, sz=11, color=bare(C["text"]))

    ink, muted = bare(C["text"]), bare(C["text-muted"])
    fill = lambda h: PatternFill("solid", fgColor=bare(h))
    rule = Side(style="thin", color=bare(C["rule"]))
    header = NamedStyle(name="AIRI header", font=Font(name=FONT, sz=11, bold=True, color=ink),
                        fill=fill(C["fill"]), border=Border(bottom=rule), alignment=Alignment(vertical="center"))
    wb.add_named_style(header)
    title = NamedStyle(name="AIRI title", font=Font(name=FONT, sz=16, bold=True, color=bare(C["link"])))
    wb.add_named_style(title)
    note = NamedStyle(name="AIRI note", font=Font(name=FONT, sz=9, color=muted))
    wb.add_named_style(note)

    # Example sheet with a bar chart: grey bars, the subject red.
    ws = wb.active
    ws.title = "Example"
    ws["A1"] = "Privacy and security is the risk named most often"; ws["A1"].style = "AIRI title"
    ws["A2"] = "Share of documents that name each domain (%). Source: illustrative data."; ws["A2"].style = "AIRI note"
    ws.append([])
    ws.append(["Risk domain", "Share (%)"])
    for c in ws[4]:
        c.style = "AIRI header"
    for name, v in zip(DOMAINS, HIGHLIGHT):
        ws.append([name, v])
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 12
    ch = BarChart()
    ch.type = "bar"
    ch.style = 10
    ch.title = None
    ch.legend = None
    ch.gapWidth = 60
    data = Reference(ws, min_col=2, min_row=4, max_row=4 + len(DOMAINS))
    cats = Reference(ws, min_col=1, min_row=5, max_row=4 + len(DOMAINS))
    ch.add_data(data, titles_from_data=True)
    ch.set_categories(cats)
    ch.y_axis.scaling.orientation = "minMax"
    ch.x_axis.scaling.orientation = "maxMin"     # first domain at the top
    ch.y_axis.majorGridlines = None
    ch.y_axis.delete = True
    ch.x_axis.delete = False
    s = ch.series[0]
    s.graphicalProperties = GraphicalProperties(solidFill=bare(C["gray"]))
    s.graphicalProperties.line.noFill = True
    pt = DataPoint(idx=SUBJECT)
    pt.graphicalProperties = GraphicalProperties(solidFill=bare(C["primary"]))
    pt.graphicalProperties.line.noFill = True
    s.dPt.append(pt)
    s.dLbls = DataLabelList(); s.dLbls.showVal = True
    for k in ("showSerName", "showCatName", "showLegendKey", "showPercent"):
        setattr(s.dLbls, k, False)
    cp = CharacterProperties(latin=DFont(typeface=FONT), sz=1000, solidFill=muted)
    ch.txPr = RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=cp), endParaRPr=cp)])
    ch.height, ch.width = 8, 14
    ch.y_axis.scaling.min = 0
    ws.add_chart(ch, "A15")
    ws["A13"] = ("Bars that compare groups are one colour: grey, with the one the title is about in red. "
                 "Select a single bar and set its fill to Accent 1 (red) to move the highlight.")
    ws["A13"].style = "AIRI note"

    # Palette sheet.
    p = wb.create_sheet("Palette")
    p["A1"] = "AIRI colours for charts and tables"; p["A1"].style = "AIRI title"
    p["A2"] = f"{GEN} Fill the swatch column, then copy a cell's colour with the format painter."; p["A2"].style = "AIRI note"
    row = 4

    def head(cols):
        nonlocal row
        p.append([]) if row > p.max_row else None
        for j, h in enumerate(cols, 1):
            c = p.cell(row=row, column=j, value=h); c.style = "AIRI header"
        row += 1

    def section(name, sub):
        nonlocal row
        row += 1
        c = p.cell(row=row, column=1, value=name); c.font = Font(name=FONT, sz=12, bold=True, color=ink)
        p.cell(row=row + 1, column=1, value=sub).style = "AIRI note"
        row += 2

    section("Categories", "Any grouping takes the slots in order from 1. Colour a grouping only when the colour says something.")
    head(["Slot", "Name", "Swatch", "Fill", "Text", "Tint", "Label on fill", "Risk domain"])
    for c in CATS + [dict(slot="", name="other", fill=D["other"]["fill"], ink=D["other"]["ink"], tint=D["other"]["tint"],
                          label="text", domain="Other, folded groups, context")]:
        lab = C["white"] if c["label"] == "white" else C["text"]
        vals = [c["slot"], c["name"].capitalize(), "Aa 123", c["fill"], c["ink"], c["tint"],
                "white" if c["label"] == "white" else "ink", c["domain"]]
        for j, v in enumerate(vals, 1):
            cell = p.cell(row=row, column=j, value=v)
        sw = p.cell(row=row, column=3)
        sw.fill = fill(c["fill"]); sw.font = Font(name=FONT, sz=11, bold=True, color=bare(lab))
        tint = p.cell(row=row, column=6)
        tint.fill = fill(c["tint"]); tint.font = Font(name=FONT, sz=11, color=bare(c["ink"]))
        row += 1

    def scale(name, sub, hexes, labels):
        nonlocal row
        section(name, sub)
        head(["Step", "Swatch", "Hex", "Label"])
        for i, (h, lab) in enumerate(zip(hexes, labels), 1):
            p.cell(row=row, column=1, value=i)
            sw = p.cell(row=row, column=2, value=i)
            col = C["white"] if lab == "white" else C["text"]
            sw.fill = fill(h); sw.font = Font(name=FONT, sz=11, bold=True, color=bare(col))
            sw.alignment = Alignment(horizontal="center")
            p.cell(row=row, column=3, value=h)
            p.cell(row=row, column=4, value="white" if lab == "white" else "ink")
            row += 1

    L = D["labels"]
    scale("Severity", "Ordered levels where higher is worse.", D["severity"], L["severity"])
    scale("Blue scale", "Counts and coverage: more is only more.", D["blue-sequential"], L["blue-sequential"])
    scale("Two-sided", "Two directions from a real midpoint. Red is the worse side.", D["diverging-7"], L["diverging-7"])
    for col, w in zip("ABCDEFGH", (7, 10, 10, 10, 10, 10, 13, 40)):
        p.column_dimensions[col].width = w

    wb.properties.title = "AIRI sheet template"
    wb.properties.subject = GEN
    wb.save(dest)


# ---------------------------------------------------------------- Open Graph card

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
    for name in ("airi-slides.pptx", "airi-document.docx", "airi-sheet.xlsx"):
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
    with tempfile.TemporaryDirectory() as tmp:
        build_pptx(OUT / "airi-slides.pptx", Path(tmp))
    build_docx(OUT / "airi-document.docx")
    build_xlsx(OUT / "airi-sheet.xlsx")
    build_og(OUT / "airi-og-image.html", OUT / "airi-og-image.png")
    for p in sorted(OUT.iterdir()):
        print("wrote", p.relative_to(ROOT))


if __name__ == "__main__":
    main()
