#!/usr/bin/env python3
"""Generate brand.css, skill/templates/ and guide/index.html from skill/tokens.json.

    python3 dev/build-kit/build.py           write the generated files
    python3 dev/build-kit/build.py --check   change nothing; fail if anything is out of sync

--check also reads the hand-written files (BRAND.md, SKILL.md, the guide) and
fails if they name a colour that is not a token, or pair a token with the
wrong hex. Standard library only.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import guide  # noqa: E402  (the one-page visual guide)

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skill"
TPL = SKILL / "templates"
T = json.loads((SKILL / "tokens.json").read_text())

C = T["color"]
DARK = {k: v for k, v in T["color-dark"].items() if k != "note"}
D = T["data"]
CATS = D["categorical"]
S = T["status"]
SLOTS = T["theme"]["slots"]
TY = T["typography"]
VERSION = T["version"]
FONT_URL = "https://fonts.googleapis.com/css2?family=Figtree:wght@400;600;700&display=swap"
GEN = f"AIRI brand kit {VERSION}. Generated from tokens.json by dev/build-kit/build.py. Do not edit by hand."


def bare(h):
    return h.lstrip("#")


def css_family(fam):
    parts = [p.strip() for p in fam.split(",")]
    return ", ".join(f"'{p}'" if p == "Figtree" else p for p in parts)


# ---------------------------------------------------------------- brand.css

def css_color_lines(colors, indent="  "):
    return [f"{indent}--color-{k}: {v};" for k, v in colors.items()]


def css_data_lines(indent="  ", dark=False):
    out = []
    if dark:
        for c in CATS:
            if "fill-dark" in c:
                out.append(f"{indent}--color-cat-{c['slot']}: {c['fill-dark']};")
        return out
    for c in CATS:
        n = c["slot"]
        out.append(f"{indent}--color-cat-{n}: {c['fill']}; --color-cat-{n}-ink: {c['ink']}; --color-cat-{n}-tint: {c['tint']};  /* {c['name']} */")
    o = D["other"]
    out.append(f"{indent}--color-cat-other: {o['fill']}; --color-cat-other-ink: {o['ink']}; --color-cat-other-tint: {o['tint']};")
    out.append("")
    out.append(indent + " ".join(f"--color-sev-{i}: {h};" for i, h in enumerate(D["severity"], 1)))
    out.append(f"{indent}--color-sev-none: {D['severity-none']};")
    out.append(indent + " ".join(f"--color-seq-blue-{i}: {h};" for i, h in enumerate(D["blue-sequential"], 1)))
    out.append(indent + " ".join(f"--color-div-{i}: {h};" for i, h in enumerate(D["diverging-7"], 1)))
    return out


def brand_css():
    L = [f"/* {GEN}", "   Import this file, or copy the variables into any project.", "   Dark mode is opt-in: set data-theme=\"dark\" on <html> or any container. */", "",
         f"@import url('{FONT_URL}');", "", ":root {", "  /* Colour: core, neutrals, links, status */"]
    L += css_color_lines(C)
    alias = ["  --color-poor: var(--color-primary);", "  --color-poor-ink: var(--color-link);", "  --color-poor-tint: var(--color-red-tint);",
             "  --color-info-tint: var(--color-blue-tint);"]
    L += alias + ["", "  /* Colour in data: categories (never red), severity, counts, two-sided */"]
    L += css_data_lines()
    L += ["", "  /* Type */",
          f"  --font-family: {css_family(TY['family'])};",
          f"  --font-family-mono: {TY['family-mono']};"]
    L += [f"  --font-weight-{k}: {v};" for k, v in TY["weight"].items()]
    L += [f"  --font-size-{k}: {v};" for k, v in TY["size"].items()]
    L += [f"  --line-height-{k}: {v};" for k, v in TY["line-height"].items()]
    L += ["", "  /* Spacing and radius */"]
    L += [f"  --space-{i}: {v};" for i, v in enumerate(T["spacing"]["scale"], 1)]
    L += [f"  --radius-{k}: {v};" for k, v in T["radius"].items()]
    L += ["  --focus-ring: 2px solid var(--color-focus);", "", "  /* Deprecated names from kit 1.x. Kept so old code still works. */"]
    L += [f"  --{old}: var(--{new});" for old, new in T["deprecated"].items() if old != "note"]
    L += ["}", "", '[data-theme="dark"] {']
    L += css_color_lines(DARK)
    L += alias[1:] + css_data_lines(dark=True)
    L += ["}", ""]
    return "\n".join(L)


# ---------------------------------------------------------------- Office

OFFICE_ORDER = [("dk1", "dark1"), ("lt1", "light1"), ("dk2", "dark2"), ("lt2", "light2"),
                ("accent1", "accent1"), ("accent2", "accent2"), ("accent3", "accent3"),
                ("accent4", "accent4"), ("accent5", "accent5"), ("accent6", "accent6"),
                ("hlink", "hyperlink"), ("folHlink", "followed-hyperlink")]


def office_colors():
    rows = "\n".join(f'  <a:{tag}><a:srgbClr val="{bare(SLOTS[slot])}"/></a:{tag}>' for tag, slot in OFFICE_ORDER)
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<a:clrScheme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="AIRI">\n'
            f"{rows}\n</a:clrScheme>\n")


def office_fonts():
    face = TY["family"].split(",")[0].strip()
    block = f'<a:latin typeface="{face}"/><a:ea typeface=""/><a:cs typeface=""/>'
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<a:fontScheme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="AIRI">\n'
            f"  <a:majorFont>{block}</a:majorFont>\n  <a:minorFont>{block}</a:minorFont>\n</a:fontScheme>\n")


def office_md():
    d = TY["docs-pt"]
    sw = " ".join(f"`{h}`" for h in T["theme"]["custom-swatches"])
    rows = "\n".join(f"| {tag} | {name} | `{SLOTS[slot]}` |" for (tag, slot), name in zip(OFFICE_ORDER, [
        "Text/Background: Dark 1", "Text/Background: Light 1", "Text/Background: Dark 2", "Text/Background: Light 2",
        "Accent 1", "Accent 2", "Accent 3", "Accent 4", "Accent 5", "Accent 6", "Hyperlink", "Followed Hyperlink"]))
    return f"""# AIRI theme for PowerPoint, Word and Excel

Two small files set the theme colours and fonts for every Office app:
`office-theme-colors.xml` and `office-theme-fonts.xml`. Once installed, "AIRI"
appears in the Colors and Fonts menus, and a default chart starts with AIRI red.

## Install

Copy `office-theme-colors.xml` into the Theme Colors folder and
`office-theme-fonts.xml` into the Theme Fonts folder, then restart the app.
Rename them `AIRI.xml` if you like; the menu shows the name inside the file.

| System | Folder |
|---|---|
| Windows | `%AppData%\\Microsoft\\Templates\\Document Themes\\Theme Colors` and `...\\Theme Fonts` |
| macOS | `~/Library/Group Containers/UBF8T346G9.Office/User Content/Themes/Theme Colors` and `.../Theme Fonts` |

Then choose the theme:

- PowerPoint: Design > Variants > Colors > AIRI, and Fonts > AIRI.
- Word: Design > Colors > AIRI, and Fonts > AIRI.
- Excel: Page Layout > Colors > AIRI, and Fonts > AIRI.

To make a template, apply both, set the styles below, and save as `.potx` or `.dotx`.
Figtree must be installed on the computer (it is free from Google Fonts).

## The 12 slots

If you would rather type them: Colors > Customize Colors.

| Slot | Name in the dialog | Hex |
|---|---|---|
{rows}

## PowerPoint

- Slide size 13.333 x 7.5 in (960 x 540 pt, the widescreen default).
- Master background `{C['background']}`. Section divider background `{C['primary']}` with white text.
- Sizes in pt: cover {TY['slides-pt-960']['cover']}, slide title {TY['slides-pt-960']['title']}, outcome {TY['slides-pt-960']['outcome']}, body {TY['slides-pt-960']['body']}, small {TY['slides-pt-960']['small']}. Nothing smaller than {TY['slides-pt-960']['small']}.
- Slide titles are Figtree Bold in Accent 1. Everything else is Dark 1, or Dark 2 for small text.

## Word styles

| Style | Font | Size | Colour |
|---|---|---|---|
| Title | Figtree Bold | {d['title']} pt | `{C['primary']}` (Accent 1) |
| Subtitle | Figtree Regular | {d['subtitle']} pt | `{C['text-muted']}` (Dark 2) |
| Heading 1 | Figtree Bold | {d['h1']} pt | `{C['primary']}` (Accent 1) |
| Heading 2 | Figtree Bold | {d['h2']} pt | `{C['text']}` (Dark 1) |
| Heading 3 | Figtree Bold | {d['h3']} pt | `{C['text']}` (Dark 1) |
| Normal | Figtree Regular | {d['body']} pt | `{C['text']}` (Dark 1) |
| Caption, table and figure notes | Figtree Regular | {d['caption']} pt | `{C['text-muted']}` (Dark 2) |
| Hyperlink | underlined | | `{C['link']}` |

Tables: header row bold on `{C['fill']}` (Light 2), or white on `{C['primary']}` for short tables.
Body rows alternate white and `{C['fill']}`. Rules `{C['rule']}`.

## Colours outside the theme

Office builds its own lighter and darker rows from each accent. Those are not AIRI
tints. When you need a tint or a chart colour that is not one of the 12 slots,
type one of these under More Colors (they then stay in Recent Colors):

{sw}
"""


# ---------------------------------------------------------------- Google

def rgb01(h):
    h = bare(h)
    return {k: round(int(h[i:i + 2], 16) / 255, 4) for k, i in (("red", 0), ("green", 2), ("blue", 4))}


GOOGLE_ORDER = [("DARK1", "dark1", "Text and background 1"), ("LIGHT1", "light1", "Text and background 2"),
                ("DARK2", "dark2", "Text and background 3"), ("LIGHT2", "light2", "Text and background 4"),
                ("ACCENT1", "accent1", "Accent 1"), ("ACCENT2", "accent2", "Accent 2"), ("ACCENT3", "accent3", "Accent 3"),
                ("ACCENT4", "accent4", "Accent 4"), ("ACCENT5", "accent5", "Accent 5"), ("ACCENT6", "accent6", "Accent 6"),
                ("HYPERLINK", "hyperlink", "Link"), ("FOLLOWED_HYPERLINK", "followed-hyperlink", "(API only)")]


def google_slides_md():
    s = TY["slides-pt-960"]
    rows = "\n".join(f"| {name} | `{api}` | `{SLOTS[slot]}` |" for api, slot, name in GOOGLE_ORDER)
    req = {"requests": [{"updatePageProperties": {
        "objectId": "MASTER_OBJECT_ID",
        "pageProperties": {"colorScheme": {"colors": [{"type": api, "color": rgb01(SLOTS[slot])} for api, slot, _ in GOOGLE_ORDER]}},
        "fields": "colorScheme.colors"}}]}
    sheets = "\n".join(f"| {n} | `{h}` |" for n, h in [
        ("Text", SLOTS["dark1"]), ("Background", SLOTS["light1"]), ("Accent 1", SLOTS["accent1"]), ("Accent 2", SLOTS["accent2"]),
        ("Accent 3", SLOTS["accent3"]), ("Accent 4", SLOTS["accent4"]), ("Accent 5", SLOTS["accent5"]), ("Accent 6", SLOTS["accent6"]),
        ("Hyperlink", SLOTS["hyperlink"])])
    sw = " ".join(f"`{h}`" for h in T["theme"]["custom-swatches"])
    return f"""# AIRI theme for Google Slides and Sheets

Set these once in a deck and every new slide, link and chart starts on brand.
Do it in a template deck, then start new decks with File > Make a copy.

## Slides: by hand

1. Slide > Edit theme. Click **Colors** in the toolbar.
2. Open the "Choose a theme color" list. Set each entry to the hex below.
3. Still in the theme editor, select the master slide. Set its background to `{C['background']}`.
   Select all text placeholders and set the font to Figtree.
4. Set the title placeholder to Figtree Bold, Accent 1.

| Entry in the list | API name | Hex |
|---|---|---|
{rows}

Sizes for a 960 x 540 pt page (File > Page setup > Custom > 13.333 x 7.5 in): cover {s['cover']} pt,
slide title {s['title']} pt, outcome {s['outcome']} pt, body {s['body']} pt, small {s['small']} pt.
Nothing smaller than {s['small']} pt. On Google's default 720 x 405 pt page, multiply by 0.75.

## Slides: by API

The same change as one `presentations.batchUpdate` request. Replace `MASTER_OBJECT_ID`
with the id of the deck's master page (`masters[0].objectId` from `presentations.get`).
The API needs all 12 colours in one request.

```json
{json.dumps(req, indent=1)}
```

## Colours outside the theme

Google lists custom colours under "Custom" in the colour picker. Add these there,
and keep a small strip of them on the template's last slide so they travel with copies:

{sw}

## Sheets

Format > Theme > Customize. Font: Figtree.

| Entry | Hex |
|---|---|
{sheets}

Charts then take series colours from Accent 1 to 6 in order.

## Do not click

- The dark red in the toolbar grid ("dark red berry 1", `{T['avoid']['google-toolbar-dark-red']}`) or any other toolbar red. AIRI red is the Accent 1 theme colour.
- The default link colours: teal `{T['avoid']['google-slides-teal-link']}` in Slides, blue `{T['avoid']['google-link-blue']}` in Docs. Links are `{C['link']}` and underlined.
- The greys are safe to click. They are Google presets: {', '.join(f'`{h}` ({n})' for h, n in T['theme']['google-presets'].items())}.
"""


def google_docs_md():
    d = TY["docs-pt"]
    return f"""# AIRI styles for Google Docs

Google Docs has no theme colours. The look lives in the named styles, so set
them once in a template document and start new documents from a copy of it.

## Set the named styles

For each row: format one paragraph as shown, then Format > Paragraph styles >
(style name) > "Update to match". When all are done, Format > Paragraph styles >
Options > "Save as my default styles" if you want them in your own new documents.

| Style | Font | Size | Colour |
|---|---|---|---|
| Title | Figtree Bold | {d['title']} pt | `{C['primary']}` |
| Subtitle | Figtree Regular | {d['subtitle']} pt | `{C['text-muted']}` |
| Heading 1 | Figtree Bold | {d['h1']} pt | `{C['primary']}` |
| Heading 2 | Figtree Bold | {d['h2']} pt | `{C['text']}` |
| Heading 3 | Figtree Bold | {d['h3']} pt | `{C['text']}` |
| Normal text | Figtree Regular | {d['body']} pt, line spacing 1.15 | `{C['text']}` |
| Notes and captions (use Normal text) | Figtree Regular | {d['caption']} pt | `{C['text-muted']}` |

Only the Title and Heading 1 are red. Heading 2 and below are near-black, so
there is never a reason to pick a second red.

## Links

Docs colours links one by one. Set each link to `{C['link']}` and keep the underline.
Pasting text with "Paste without formatting" keeps the template's styles.

## Page furniture

- Header: a full-width bar in `{C['primary']}`, 7 pt tall, at the top edge. The AIRI logo
  (`logos/initiative/horizontal-on-light.png`) top right, about 2.5 cm wide.
- Footer: site address and contact address in `{C['text-muted']}` at {d['caption']} pt, page number on the right,
  and a matching `{C['primary']}` bar at the bottom edge.
- Lead-sentence highlight: `{C['red-tint']}`. Marked or draft text: `{C['highlight']}`.

## Tables and callouts

- Header row: bold on `{C['fill']}`. For a short table, white bold on `{C['primary']}`.
- Body rows alternate white and `{C['fill']}`. Borders `{C['rule']}`, 0.5 pt.
- Callout: a one-cell table filled `{C['fill']}` (or `{C['red-wash']}` on screen-only documents), no border.

## Colours to paste

Add these under "Custom" in the colour picker:

`{C['primary']}` `{C['text']}` `{C['red-tint']}` `{C['red-wash']}` `{C['blue']}` `{C['highlight']}`

The greys are Google presets, so they can be clicked:
{', '.join(f'`{h}` ({n})' for h, n in T['theme']['google-presets'].items())}.

## Do not click

- "Dark red berry 1" (`{T['avoid']['google-toolbar-dark-red']}`) or any other red in the toolbar grid.
- The default link blue (`{T['avoid']['google-link-blue']}`).
- Pure red (`{T['avoid']['pure-red']}`) for emphasis. Emphasis is bold, or bold in `{C['primary']}`.
"""


# ---------------------------------------------------------------- charts

def default_cycle():
    """Subject, context, second colour, then the remaining theme accents."""
    return [C["primary"], C["gray"], C["blue"], SLOTS["accent3"], SLOTS["accent4"], SLOTS["accent5"], SLOTS["accent6"]]


def mplstyle():
    ch = D["chrome"]
    fam = [p.strip() for p in TY["family"].split(",") if p.strip() != "sans-serif"] + ["DejaVu Sans"]
    cyc = ", ".join(f"'{bare(h)}'" for h in default_cycle())
    f = TY["figure-pt"]
    return f"""# {GEN}
# Use: plt.style.use("airi.mplstyle"). For colour maps and the category cycle, import airi_mpl.
# Default cycle: red (the subject), grey (context), blue, then the theme accents.
# For named categories use airi_mpl.use_categorical(); categories never use red.

font.family: sans-serif
font.sans-serif: {', '.join(fam)}
font.size: {f['label']}
axes.titlesize: {f['panel-title']}
axes.titleweight: bold
axes.titlelocation: left
axes.labelsize: {f['label']}
xtick.labelsize: {f['label']}
ytick.labelsize: {f['label']}
legend.fontsize: {f['label']}

text.color: {bare(ch['text'])}
axes.titlecolor: {bare(ch['text'])}
axes.labelcolor: {bare(ch['axis-label'])}
xtick.color: {bare(ch['axis-label'])}
ytick.color: {bare(ch['axis-label'])}
axes.edgecolor: {bare(ch['axis-line'])}
grid.color: {bare(ch['grid'])}
grid.linewidth: 0.6
axes.linewidth: 0.8
axes.grid: True
axes.grid.axis: y
axes.axisbelow: True
axes.spines.top: False
axes.spines.right: False
axes.facecolor: {bare(ch['background'])}
figure.facecolor: {bare(ch['background'])}
savefig.facecolor: {bare(ch['background'])}
legend.frameon: False
lines.linewidth: 1.8
patch.linewidth: 0

axes.prop_cycle: cycler('color', [{cyc}])
"""


def mpl_py():
    cats = {c["name"]: c["fill"] for c in CATS}
    return f'''"""{GEN}

AIRI colours for matplotlib. Put this file next to airi.mplstyle.

    import matplotlib.pyplot as plt
    import airi_mpl                      # registers the colour maps
    plt.style.use(airi_mpl.STYLE)

    ax.bar(x, y, color=airi_mpl.CONTEXT)             # everything else
    ax.bar(x[3], y[3], color=airi_mpl.RED)           # the finding
    ax.imshow(m, cmap="airi_red")                    # more means more risk
    ax.imshow(m, cmap="airi_blue")                   # more is only more
    airi_mpl.use_categorical()                       # named categories, no red
"""
from pathlib import Path

import matplotlib as mpl
from cycler import cycler
from matplotlib.colors import ListedColormap, to_rgb

STYLE = str(Path(__file__).with_name("airi.mplstyle"))

RED = "{C['primary']}"
RED_PALE = "{C['red-300']}"       # the second condition beside RED
CONTEXT = "{C['gray']}"
BLUE = "{C['blue']}"
INK = "{C['text']}"
MUTED = "{C['text-muted']}"
NO_DATA = "{D['severity-none']}"

CATEGORICAL = {json.dumps(cats)}
OTHER = "{D['other']['fill']}"
SEVERITY = {json.dumps(D['severity'])}
GOOD, PARTIAL, POOR = "{S['good']['mark']}", "{S['partial']['mark']}", "{S['poor']['mark']}"

_STOPS = {{
    "airi_red": {json.dumps(D['red-continuous'])},
    "airi_blue": {json.dumps(D['blue-sequential'])},
    "airi_div": {json.dumps(D['diverging-7'])},
}}


def _to_oklab(c):
    r, g, b = [(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in to_rgb(c)]
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def _from_oklab(L, a, b):
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    rgb = (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
           -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
           -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)
    return tuple(min(1.0, max(0.0, 12.92 * v if v <= 0.0031308 else 1.055 * max(v, 0) ** (1 / 2.4) - 0.055)) for v in rgb)


def _ramp(stops, n=256):
    """Interpolate between the stops in OKLab, so steps look even."""
    lab = [_to_oklab(c) for c in stops]
    out = []
    for i in range(n):
        t = i / (n - 1) * (len(lab) - 1)
        k = min(int(t), len(lab) - 2)
        f = t - k
        out.append(_from_oklab(*[lab[k][j] + (lab[k + 1][j] - lab[k][j]) * f for j in range(3)]))
    return out


def register():
    for name, stops in _STOPS.items():
        for cmap in (ListedColormap(_ramp(stops), name=name), ListedColormap(_ramp(stops)[::-1], name=name + "_r")):
            if cmap.name not in mpl.colormaps:
                mpl.colormaps.register(cmap)
    if "airi_severity" not in mpl.colormaps:
        mpl.colormaps.register(ListedColormap(SEVERITY, name="airi_severity"))


def use_categorical():
    """Colour cycle for named categories: the seven slots in order, then grey for Other."""
    mpl.rcParams["axes.prop_cycle"] = cycler(color=list(CATEGORICAL.values()) + [OTHER])


register()
'''


def plotly_template():
    ch = D["chrome"]
    fam = TY["family"]

    def scale(stops):
        n = len(stops) - 1
        return [[round(i / n, 4), h] for i, h in enumerate(stops)]

    axis = {"gridcolor": ch["grid"], "linecolor": ch["axis-line"], "zerolinecolor": ch["axis-line"],
            "tickfont": {"color": ch["axis-label"]}, "title": {"font": {"color": ch["axis-label"]}},
            "ticks": "", "automargin": True}
    t = {"layout": {
        "font": {"family": fam, "color": ch["text"], "size": 14},
        "title": {"font": {"family": fam, "color": ch["text"], "size": 20}, "x": 0, "xanchor": "left"},
        "colorway": default_cycle(),
        "paper_bgcolor": ch["background"], "plot_bgcolor": ch["background"],
        "xaxis": dict(axis, showgrid=False), "yaxis": dict(axis, showline=False),
        "legend": {"font": {"color": ch["axis-label"]}, "bgcolor": "rgba(0,0,0,0)"},
        "hoverlabel": {"font": {"family": fam}, "bgcolor": C["white"], "bordercolor": C["rule"]},
        "colorscale": {"sequential": scale(D["blue-sequential"]),
                       "sequentialminus": scale(D["blue-sequential"][::-1]),
                       "diverging": scale(D["diverging-7"])},
        "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": "", "tickfont": {"color": ch["axis-label"]}}},
        "annotationdefaults": {"font": {"color": ch["text"]}, "arrowcolor": ch["axis-label"]},
        "shapedefaults": {"line": {"color": ch["axis-line"]}},
    }, "data": {
        "bar": [{"marker": {"line": {"width": 0}}}],
        "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}}],
    }}
    return json.dumps(t, indent=1) + "\n"


def r_palette():
    def vec(name, items):
        body = ", ".join(f'{k} = "{v}"' if k else f'"{v}"' for k, v in items)
        return f"  {name} = c({body})"

    cats = [(c["name"], c["fill"]) for c in CATS] + [("other", D["other"]["fill"])]
    inks = [(c["name"], c["ink"]) for c in CATS] + [("other", D["other"]["ink"])]
    tints = [(c["name"], c["tint"]) for c in CATS] + [("other", D["other"]["tint"])]
    core = [(k.replace("-", "_"), v) for k, v in C.items()]
    parts = [
        vec("color", core),
        vec("highlight", [("subject", C["primary"]), ("context", C["gray"])]),
        vec("pair", [("", h) for h in D["pair"]]),
        vec("categorical", cats), vec("categorical_ink", inks), vec("categorical_tint", tints),
        vec("severity", [("", h) for h in D["severity"]]),
        f'  severity_none = "{D["severity-none"]}"',
        vec("red", [("", h) for h in D["red-continuous"]]),
        vec("blue", [("", h) for h in D["blue-sequential"]]),
        vec("diverging", [("", h) for h in D["diverging-7"]]),
        vec("status", [("good", S["good"]["mark"]), ("partial", S["partial"]["mark"]), ("poor", S["poor"]["mark"]), ("none", S["none"]["mark"])]),
        vec("chrome", [(k.replace("-", "_"), v) for k, v in D["chrome"].items()]),
        f'  font = "{TY["family"].split(",")[0].strip()}"',
    ]
    f = TY["figure-pt"]
    return f"""# {GEN}
#
# AIRI colours for R figures. One shared file, so every paper uses the same values.
#   source("airi_palette.R")
#   ggplot(d, aes(x, y, fill = is_finding)) + geom_col() +
#     scale_fill_manual(values = c(`TRUE` = airi$color[["primary"]], `FALSE` = airi$color[["gray"]])) +
#     theme_airi()
#   scale_fill_gradientn(colours = airi_ramp("red"))    # more means more risk
#   scale_fill_gradientn(colours = airi_ramp("blue"))   # more is only more
#   scale_fill_manual(values = airi$categorical)         # named categories, never red

airi <- list(
{(',' + chr(10)).join(parts)}
)

# n colours along a named ramp ("red", "blue" or "diverging").
airi_ramp <- function(name = c("red", "blue", "diverging"), n = 256) {{
  name <- match.arg(name)
  grDevices::colorRampPalette(unname(airi[[name]]))(n)
}}

# ggplot2 theme. Sizes are for print figures at final size.
theme_airi <- function(base_size = {f['label']}, base_family = airi$font) {{
  ggplot2::theme_minimal(base_size = base_size, base_family = base_family) +
    ggplot2::theme(
      text = ggplot2::element_text(colour = airi$chrome[["text"]]),
      plot.title = ggplot2::element_text(size = {f['panel-title']}, face = "bold", hjust = 0),
      plot.title.position = "plot",
      axis.text = ggplot2::element_text(colour = airi$chrome[["axis_label"]]),
      axis.title = ggplot2::element_text(colour = airi$chrome[["axis_label"]]),
      axis.line.x = ggplot2::element_line(colour = airi$chrome[["axis_line"]]),
      panel.grid.major = ggplot2::element_line(colour = airi$chrome[["grid"]], linewidth = 0.3),
      panel.grid.major.x = ggplot2::element_blank(),
      panel.grid.minor = ggplot2::element_blank(),
      legend.position = "top",
      legend.justification = "left"
    )
}}
"""


# ---------------------------------------------------------------- web

TW_NAMES = {"text": "ink", "text-muted": "muted", "border": "line"}


def tailwind_css():
    L = [f"/* {GEN}", "   Tailwind CSS v4. Paste after @import \"tailwindcss\";",
         "   The first line removes Tailwind's own colours, so only AIRI colours can be used:",
         "   bg-primary, text-ink, text-muted, border-line, bg-fill, bg-cat-1, text-cat-1-ink ...",
         "   For Tailwind v3, copy the same names and values into theme.colors in tailwind.config.js. */", "",
         "@theme {", "  --color-*: initial;"]
    for k, v in C.items():
        L.append(f"  --color-{TW_NAMES.get(k, k)}: {v};")
    L.append(f"  --color-poor: {S['poor']['mark']};")
    for c in CATS:
        n = c["slot"]
        L.append(f"  --color-cat-{n}: {c['fill']}; --color-cat-{n}-ink: {c['ink']}; --color-cat-{n}-tint: {c['tint']};")
    L.append(f"  --color-cat-other: {D['other']['fill']};")
    L += [f"  --color-sev-{i}: {h};" for i, h in enumerate(D["severity"], 1)]
    L += ["", f"  --font-sans: {css_family(TY['family'])};", f"  --font-mono: {TY['family-mono']};",
          "", "  --radius-*: initial;"]
    L += [f"  --radius-{k}: {v};" for k, v in T["radius"].items()]
    L += ["}", ""]
    return "\n".join(L)


ALIASES = [("ink", "text"), ("body", "text"), ("muted", "text-muted"), ("faint", "gray"), ("rule", "rule"),
           ("line", "border"), ("empty", "fill"), ("red", "primary"), ("red-dark", "primary-dark"),
           ("red-pale", "red-300"), ("red-tint", "red-wash"), ("axis", "blue-tint"), ("gap", "partial")]


def aliases_css():
    L = [f"/* {GEN}", "   Short names used by some AIRI apps, mapped onto the kit tokens.",
         "   Load after brand.css. Keep the short names in existing code; write new code with the --color-* names. */", "", ":root {"]
    L += [f"  --{a}: var(--color-{k});" for a, k in ALIASES]
    L += ["}", ""]
    return "\n".join(L)


def artifact_html():
    light = "\n".join(css_color_lines(C, "    "))
    cats = "\n".join(f"    --color-cat-{c['slot']}: {c['fill']}; --color-cat-{c['slot']}-ink: {c['ink']}; --color-cat-{c['slot']}-tint: {c['tint']};" for c in CATS)
    sev = "    " + " ".join(f"--color-sev-{i}: {h};" for i, h in enumerate(D["severity"], 1))
    dark = "\n".join(css_color_lines(DARK, "      ") + css_data_lines("      ", dark=True))
    dark2 = "\n".join(css_color_lines(DARK, "    ") + css_data_lines("    ", dark=True))
    return f"""<!-- {GEN}
     Starting point for a Claude artifact or any single-file page. Works in light and dark.
     Paste the <link> and <style> into the page, then use the tokens. Never type a hex in the page body. -->
<link href="{FONT_URL}" rel="stylesheet">
<style>
  :root {{
{light}
{cats}
    --color-cat-other: {D['other']['fill']};
{sev}
    --color-sev-none: {D['severity-none']};
    --font-family: {css_family(TY['family'])};
    --font-family-mono: {TY['family-mono']};
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
{dark}
    }}
  }}
  :root[data-theme="dark"] {{
{dark2}
  }}

  * {{ box-sizing: border-box; }}
  body {{ margin: 0; padding: 24px 16px; background: var(--color-background); color: var(--color-text);
         font-family: var(--font-family); font-size: 16px; line-height: 1.5; }}
  h1 {{ font-size: 2.125rem; line-height: 1.25; font-weight: 700; color: var(--color-link); margin: 0 0 8px; }}
  h2 {{ font-size: 1.625rem; line-height: 1.25; font-weight: 700; margin: 32px 0 8px; }}
  h3 {{ font-size: 1.25rem; line-height: 1.25; font-weight: 600; margin: 24px 0 8px; }}
  small, .muted {{ color: var(--color-text-muted); font-size: 0.875rem; }}
  a {{ color: var(--color-link); text-decoration: underline; }}
  a:hover {{ color: var(--color-link-hover); }}
  :focus-visible {{ outline: 2px solid var(--color-focus); outline-offset: 2px; }}
  mark {{ background: var(--color-highlight); color: #1A1A1A; }}
  code {{ font-family: var(--font-family-mono); font-size: 0.875em; }}

  .card {{ background: var(--color-surface); border: 1px solid var(--color-border); border-radius: 8px; padding: 24px; }}
  .button {{ display: inline-block; padding: 8px 16px; border: 0; border-radius: 8px; background: var(--color-primary);
            color: var(--color-white); font: inherit; font-weight: 600; text-decoration: none; cursor: pointer; }}
  .button:hover {{ background: var(--color-primary-hover); color: var(--color-white); }}
  .chip {{ display: inline-block; padding: 2px 8px; border-radius: 4px; background: var(--color-red-tint);
          color: var(--color-link); font-size: 0.875rem; font-weight: 600; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th {{ text-align: left; font-weight: 700; background: var(--color-fill); }}
  th, td {{ padding: 8px 12px; border-bottom: 1px solid var(--color-rule); }}
</style>
"""


def latex_sty():
    def cname(k):
        return "airi" + "".join(p.capitalize() for p in k.split("-"))

    L = [f"% {GEN}", "%", "% AIRI colours for LaTeX. \\usepackage{airi-colors}",
         "%   \\textcolor{airiPrimary}{...}   \\airilinks (red links, after hyperref)   \\airimark (title-block line)",
         "\\NeedsTeXFormat{LaTeX2e}", f"\\ProvidesPackage{{airi-colors}}[2026/11/13 v{VERSION} AIRI brand colours]",
         "\\RequirePackage{xcolor}", ""]
    for k, v in C.items():
        if k in ("link", "link-hover", "link-visited", "focus", "surface", "info-ink"):
            continue
        L.append(f"\\definecolor{{{cname(k)}}}{{HTML}}{{{bare(v)}}}")
    L.append("")
    for c in CATS:
        nm = "airiCat" + c["name"].capitalize()
        L.append(f"\\definecolor{{{nm}}}{{HTML}}{{{bare(c['fill'])}}}\\definecolor{{{nm}Ink}}{{HTML}}{{{bare(c['ink'])}}}\\definecolor{{{nm}Tint}}{{HTML}}{{{bare(c['tint'])}}}")
    L.append("")
    for i, h in enumerate(D["severity"], 1):
        L.append(f"\\definecolor{{airiSev{'ABCDE'[i - 1]}}}{{HTML}}{{{bare(h)}}}% severity {i}")
    L += ["",
          "% Red, underline-free links for print; call after loading hyperref.",
          "\\newcommand{\\airilinks}{\\hypersetup{colorlinks=true,linkcolor=airiText,citecolor=airiText,urlcolor=airiPrimary}}",
          "% A small identity line for a title block: a red rule and the initiative name.",
          "\\newcommand{\\airimark}{{\\color{airiPrimary}\\rule{2.4em}{1.6pt}}\\par\\vspace{2pt}%",
          "  {\\sffamily\\small\\color{airiTextMuted}MIT AI Risk Initiative\\enspace\\textbar\\enspace airisk.mit.edu}\\par}",
          "\\endinput", ""]
    return "\n".join(L)


def templates_readme():
    return f"""# Templates

Ready-made files that already hold the AIRI colours and fonts, one per tool.
Start from these instead of typing hex values. All are generated from
`../tokens.json`, so they always match the spec in `../BRAND.md`.

| For | File | How to use |
|---|---|---|
| PowerPoint, Word, Excel | `office-theme-colors.xml`, `office-theme-fonts.xml`, `office-theme.md` | Copy the two XML files into Office's theme folders; "AIRI" then appears under Colors and Fonts. Steps and Word styles are in the .md |
| Google Slides, Sheets | `google-slides-theme.md` | Hex per theme slot, by hand or as one API request |
| Google Docs | `google-docs-styles.md` | Named styles, page furniture, colours to paste |
| Websites and apps | `../brand.css` | Import it, or copy the variables |
| Tailwind | `tailwind-theme.css` | Paste after `@import "tailwindcss"` |
| Apps using short names | `short-aliases.css` | Maps `--ink`, `--muted`, `--rule` and friends onto the kit tokens |
| Claude artifacts, single-file pages | `claude-artifact.html` | Paste the `<link>` and `<style>`; light and dark |
| matplotlib | `airi.mplstyle`, `airi_mpl.py` | `import airi_mpl; plt.style.use(airi_mpl.STYLE)` |
| Plotly | `airi-plotly-template.json` | See below |
| R, ggplot2 | `airi_palette.R` | `source("airi_palette.R")`, then `airi$...`, `airi_ramp()`, `theme_airi()` |
| LaTeX | `airi-colors.sty` | `\\usepackage{{airi-colors}}` |

## Chart defaults

The default colour order in the chart templates is red, grey, blue, then the
other theme accents. That makes a one- or two-series chart read as "the
subject, and everything else" without any work. For named categories, switch
to the category colours (`airi_mpl.use_categorical()`, `airi$categorical`, or
the `cat` values in `tokens.json`). Categories never use red.

The default colour scale for heatmaps is blue, because blue means "more" and
nothing else. Use the red scale only when more means more risk.

## Plotly

```python
import json, plotly.io as pio, plotly.graph_objects as go
pio.templates["airi"] = go.layout.Template(json.load(open("airi-plotly-template.json")))
pio.templates.default = "airi"

AIRI_RED_SCALE = {json.dumps(D['red-continuous'])}       # more means more risk
AIRI_SEVERITY = {json.dumps(D['severity'])}              # ordered levels 1 to 5
AIRI_CATEGORIES = {json.dumps([c['fill'] for c in CATS] + [D['other']['fill']])}
fig.update_traces(colorscale=AIRI_RED_SCALE)       # on a heatmap
fig.update_layout(colorway=AIRI_CATEGORIES)        # named categories
```

## Regenerating

Edit `skill/tokens.json`, then run `python3 dev/build-kit/build.py` from the
repository root. `--check` verifies that nothing is out of date.
"""


OUTPUTS = {
    SKILL / "brand.css": brand_css,
    TPL / "README.md": templates_readme,
    TPL / "office-theme-colors.xml": office_colors,
    TPL / "office-theme-fonts.xml": office_fonts,
    TPL / "office-theme.md": office_md,
    TPL / "google-slides-theme.md": google_slides_md,
    TPL / "google-docs-styles.md": google_docs_md,
    TPL / "airi.mplstyle": mplstyle,
    TPL / "airi_mpl.py": mpl_py,
    TPL / "airi-plotly-template.json": plotly_template,
    TPL / "airi_palette.R": r_palette,
    TPL / "tailwind-theme.css": tailwind_css,
    TPL / "short-aliases.css": aliases_css,
    TPL / "claude-artifact.html": artifact_html,
    TPL / "airi-colors.sty": latex_sty,
    ROOT / "guide" / "index.html": guide.render,
}

# ---------------------------------------------------------------- checks

HEX = re.compile(r"#[0-9A-Fa-f]{6}\b")
HAND_WRITTEN = [SKILL / "BRAND.md", SKILL / "SKILL.md", ROOT / "guide" / "index.html",
                ROOT / "README.md", ROOT / "CONTRIBUTING.md", ROOT / ".claude" / "CLAUDE.md"]


def all_hexes(node, out=None):
    out = set() if out is None else out
    if isinstance(node, str):
        out.update(h.upper() for h in HEX.findall(node))
    elif isinstance(node, dict):
        for k, v in node.items():
            all_hexes(k, out)
            all_hexes(v, out)
    elif isinstance(node, list):
        for v in node:
            all_hexes(v, out)
    return out


def check():
    problems = []
    for path, fn in OUTPUTS.items():
        if not path.exists() or path.read_text() != fn():
            problems.append(f"{path.relative_to(ROOT)} is out of date: run dev/build-kit/build.py")
    allowed = all_hexes(T)
    names = dict(C)
    row = re.compile(r"^\|\s*`([a-z0-9-]+)`\s*\|\s*`(#[0-9A-Fa-f]{6})`", re.M)
    for path in HAND_WRITTEN:
        if not path.exists():
            continue
        text = path.read_text()
        for h in sorted({h.upper() for h in HEX.findall(text)} - allowed):
            problems.append(f"{path.relative_to(ROOT)} names {h}, which is not in tokens.json")
        # Rows under a "Dark mode" heading are checked against the dark values.
        for section in re.split(r"^(?=#{1,4} )", text, flags=re.M):
            want = {**names, **DARK} if section.split("\n", 1)[0].lower().find("dark mode") >= 0 else names
            for name, h in row.findall(section):
                if name in want and want[name].upper() != h.upper():
                    problems.append(f"{path.relative_to(ROOT)} gives {name} as {h}; tokens.json says {want[name]}")
    for p in problems:
        print("FAIL", p)
    print("ok: everything agrees with tokens.json" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


def main():
    if "--check" in sys.argv:
        sys.exit(check())
    TPL.mkdir(exist_ok=True)
    for path, fn in OUTPUTS.items():
        path.write_text(fn())
        print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
