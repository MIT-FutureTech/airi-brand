#!/usr/bin/env python3
"""Generate brand.css, skill/templates/ and guide/index.html from skill/tokens.json.

    python3 dev/build-kit/build.py           write the generated files
    python3 dev/build-kit/build.py --check   change nothing; fail if anything is out of sync

--check also:
  - recomputes the contrast of every "label on fill" and "text on ground" rule in
    tokens.json, light and dark, and fails below 4.5:1;
  - checks the motion and video tokens, that the video CSS takes every time and
    curve from them, and that BRAND.md and SKILL.md state the same values;
  - checks the rules block (5 to 7 hard rules, each with a reason; the defaults and
    gap rules present), that BRAND.md and SKILL.md give the hard rules word for word,
    and that BRAND.md lists every decided and open item;
  - checks that the changeover procedure and its scanner exist and SKILL.md points at them;
  - reads the hand-written files and fails if they name a colour that is not a
    token, give a token the wrong hex, list a palette in the wrong order, or get a
    category, status, grade or theme-slot row wrong.
It cannot check prose claims that carry no hex. Standard library only.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import guide  # noqa: E402  (the one-page visual guide)
import video  # noqa: E402  (motion tokens and the video templates)

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
SP = T["spacing"]
VERSION = T["version"]
MOTION = T["motion"]["ui"]
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


LABEL = {"text": C["text"], "white": C["white"]}  # label colours on fills; fixed, they do not flip in dark mode


def css_data_lines(indent="  ", dark=False):
    out = []
    if dark:
        for c in CATS:
            bits = []
            if "fill-dark" in c:
                bits.append(f"--color-cat-{c['slot']}: {c['fill-dark']};")
            if "label-dark" in c:
                bits.append(f"--color-cat-{c['slot']}-label: {LABEL[c['label-dark']]};")
            if bits:
                out.append(indent + " ".join(bits))
        return out
    for c in CATS:
        n = c["slot"]
        out.append(f"{indent}--color-cat-{n}: {c['fill']}; --color-cat-{n}-ink: {c['ink']}; --color-cat-{n}-tint: {c['tint']}; --color-cat-{n}-label: {LABEL[c['label']]};  /* {c['name']} */")
    o = D["other"]
    out.append(f"{indent}--color-cat-other: {o['fill']}; --color-cat-other-ink: {o['ink']}; --color-cat-other-tint: {o['tint']};")
    out.append("")
    out.append(indent + " ".join(f"--color-sev-{i}: {h};" for i, h in enumerate(D["severity"], 1)))
    out.append(f"{indent}--color-sev-none: {D['severity-none']};")
    out.append(indent + " ".join(f"--color-seq-blue-{i}: {h};" for i, h in enumerate(D["blue-sequential"], 1)))
    out.append(indent + " ".join(f"--color-div-{i}: {h};" for i, h in enumerate(D["diverging-7"], 1)))
    return out


def css_motion_lines(indent="  "):
    """Interface motion. Video motion is separate: templates/video/airi-video.css."""
    out = [f"{indent}/* Motion for interfaces: animate transform and opacity only */"]
    out += [f"{indent}--motion-{k}: {ms}ms;" for k, ms in MOTION["duration-ms"].items()]
    out += [f"{indent}--ease-{k}: {video.bezier(p)};" for k, p in MOTION["easing"].items()]
    out += [f"{indent}--motion-stagger: {MOTION['stagger-ms']}ms;"]
    return out


REDUCED_MOTION = """/* People who ask for less motion get none. Use a short opacity change if a state change needs a cue. */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 1ms !important; animation-iteration-count: 1 !important;
    transition-duration: 1ms !important; scroll-behavior: auto !important;
  }
}"""


def brand_css():
    L = [f"/* {GEN}", "   Import this file, or copy the variables into any project.", "   Dark mode is opt-in: set data-theme=\"dark\" on <html> or any container.",
         "   Red text is --color-link (it lightens in dark mode). Red fills are --color-primary.",
         "   --color-cat-N-label is the label colour to put on a --color-cat-N fill. */", "",
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
    L += ["  --focus-ring: 2px solid var(--color-focus);", ""] + css_motion_lines()
    L += ["", "  /* Deprecated names from kit 1.x. Kept so old code still works. */"]
    dep = {old: new for old, new in T["deprecated"].items() if old != "note"}

    def dep_line(old, new):
        return f"  --{old}: var(--{new});" if new.startswith(("color-", "font-", "line-", "radius-")) else f"  --{old}: {new};"

    L += [dep_line(old, new) for old, new in dep.items()]
    L += ["}", "", '[data-theme="dark"] {']
    L += css_color_lines(DARK)
    L += alias[1:] + css_data_lines(dark=True)
    # Aliases built from other variables are worked out where they are declared, so a dark
    # container that is not <html> needs them declared again.
    L += ["  --focus-ring: 2px solid var(--color-focus);"]
    L += [dep_line(old, new) for old, new in dep.items() if new.startswith("color-") and new[len("color-"):] in DARK]
    L += ["}", ""] + REDUCED_MOTION.splitlines() + [""]
    return "\n".join(L)


# ---------------------------------------------------------------- Office

def office_charts_block(tools, how):
    """Shared by the Office and Google how-tos: what theme-coloured charts get right, and what to set by hand."""
    order = ", ".join(f"`{SLOTS[f'accent{i}']}`" for i in range(1, 7))
    rows = "\n".join(f"| {c['slot']} | {c['name'].capitalize()} | `{c['fill']}` | {c['label'] if c['label'] == 'white' else 'ink'} | {c['domain']} |" for c in CATS)
    return f"""## Charts in {tools}

A chart made here takes its series colours from Accent 1 to 6 in order:
{order}: red (the subject), grey (context), ink (a comparison), then category colours
1 to 3. That suits a chart of one to three series. For named groups and scales, set the
colours by hand. {how}

- **Bars that compare groups** are one colour: grey, with the subject in red. Colour a
  grouping only when the colour says something.
- **Named groups** that each need their own mark (stacked bars, one line per group,
  a diagram's parts): set each series to its category colour, in slot order. The first
  group is blue, never red. More than eight groups: grey with direct labels.

| Slot | Colour | Hex | Label on it | AI Risk Repository domain |
|---|---|---|---|---|
{rows}
| | Other | `{D['other']['fill']}` | ink | Other, folded groups |

- **Ordered levels where higher is worse:** {' '.join(f'`{h}`' for h in D['severity'])}.
- **Counts:** {' '.join(f'`{h}`' for h in D['blue-5'])}.

The code templates (matplotlib, Plotly, R) default to the same order: red, grey, ink,
then the category colours.
"""


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
appears in the Colors and Fonts menus. A default chart then starts with AIRI red;
see "Charts" below for what to set by hand.

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
- Margins {SP['slides-margins-pt-960']['top']} pt top, {SP['slides-margins-pt-960']['sides']} pt sides, {SP['slides-margins-pt-960']['bottom']} pt bottom. Gaps of {', '.join(str(x) for x in SP['slides-pt-960'][:-1])} or {SP['slides-pt-960'][-1]} pt. Borders 1 pt.

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

{office_charts_block("PowerPoint, Word and Excel", "Click a series, then Format Data Series > Fill > More Colors, and type the hex.")}"""


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

Spacing on the 960 x 540 pt page: margins {SP['slides-margins-pt-960']['top']} pt top, {SP['slides-margins-pt-960']['sides']} pt sides, {SP['slides-margins-pt-960']['bottom']} pt bottom.
Gaps of {', '.join(str(x) for x in SP['slides-pt-960'][:-1])} or {SP['slides-pt-960'][-1]} pt. Borders 1 pt. Corner radius 4 pt for cards and images, 2 pt otherwise.

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

{office_charts_block("Slides and Sheets", "A chart in Slides is made in Sheets: double-click the chart, then Customize > Series > Fill colour > Custom, and type the hex.")}
## Do not click

- The dark red in the toolbar grid ("dark red berry 1", `{T['avoid']['google-toolbar-dark-red']}`) or any other toolbar red. AIRI red is the Accent 1 theme colour.
- The default link colours: teal `{T['avoid']['google-slides-teal-link']}` in Slides, blue `{T['avoid']['google-link-blue']}` in Docs. Links are `{C['link']}` and underlined.
- Four greys are safe to click, because they are Google presets: {', '.join(f'`{h}` ({n})' for h, n in T['theme']['google-presets'].items())}.
  Ink `{C['text']}`, chart grey `{C['gray']}` and background `{C['background']}` are not presets; take them from the theme or the custom colours.
  Google's preset named "gray" is `{C['rule']}`, the kit's `rule`. It is not the kit's chart grey.
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

Four greys are Google presets, so they can be clicked:
{', '.join(f'`{h}` ({n})' for h, n in T['theme']['google-presets'].items())}.
Ink `{C['text']}` is not a preset; it comes from the named styles. Google's preset named
"gray" is `{C['rule']}`, the kit's `rule`, not the kit's chart grey `{C['gray']}`.

## Do not click

- "Dark red berry 1" (`{T['avoid']['google-toolbar-dark-red']}`) or any other red in the toolbar grid.
- The default link blue (`{T['avoid']['google-link-blue']}`).
- Pure red (`{T['avoid']['pure-red']}`) for emphasis. Emphasis is bold, or bold in `{C['primary']}`.
"""


# ---------------------------------------------------------------- charts

def default_cycle():
    """Subject, context, comparison, then the category colours in slot order."""
    return [C["primary"], C["gray"], C["text"]] + [c["fill"] for c in CATS]


def mplstyle():
    ch = D["chrome"]
    fam = [p.strip() for p in TY["family"].split(",") if p.strip() != "sans-serif"] + ["DejaVu Sans"]
    cyc = ", ".join(f"'{bare(h)}'" for h in default_cycle())
    f = TY["figure-pt"]
    return f"""# {GEN}
# Use: plt.style.use("airi.mplstyle"). For colour maps and the category cycle, import airi_mpl.
# Default cycle: red (the subject), grey (context), ink (a comparison), then the category colours.
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
    """Colour cycle for named categories: the eight slots in order, then grey for Other."""
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
         "   Load after brand.css. Keep the short names in existing code; write new code with the --color-* names.",
         "",
         "   Careful: --red-tint here is the faint wash these apps already use (kit --color-red-wash, " + C["red-wash"] + ").",
         "   It is NOT the kit's --color-red-tint (" + C["red-tint"] + "). In new code use the --color-* names, which are unambiguous.",
         "   Likewise --line is the kit's --color-border, and --faint is --color-gray (graphics only, never text). */", "", ":root {"]
    L += [f"  --{a}: var(--color-{k});" for a, k in ALIASES]
    L += ["}", ""]
    return "\n".join(L)


def artifact_html():
    light = "\n".join(css_color_lines(C, "    "))
    cats = "\n".join(f"    --color-cat-{c['slot']}: {c['fill']}; --color-cat-{c['slot']}-ink: {c['ink']}; --color-cat-{c['slot']}-tint: {c['tint']};" for c in CATS)
    labels = "    " + " ".join(f"--color-cat-{c['slot']}-label: {LABEL[c['label']]};" for c in CATS)
    sev = "    " + " ".join(f"--color-sev-{i}: {h};" for i, h in enumerate(D["severity"], 1))
    dark = "\n".join(css_color_lines(DARK, "      ") + css_data_lines("      ", dark=True))
    dark2 = "\n".join(css_color_lines(DARK, "    ") + css_data_lines("    ", dark=True))
    motion = "\n".join(css_motion_lines("    "))
    reduced = "\n".join("  " + x for x in REDUCED_MOTION.splitlines()[1:])
    return f"""<!-- {GEN}
     Starting point for a Claude artifact or any single-file page. Works in light and dark.
     Paste the <link> and <style> into the page, then use the tokens. Never type a hex in the page body.
     Red text is --color-link, which lightens in dark mode. Red fills are --color-primary, with white text. -->
<link href="{FONT_URL}" rel="stylesheet">
<style>
  :root {{
{light}
{cats}
    --color-cat-other: {D['other']['fill']};
{labels}
{sev}
    --color-sev-none: {D['severity-none']};
    --font-family: {css_family(TY['family'])};
    --font-family-mono: {TY['family-mono']};
{motion}
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
  .button-secondary {{ display: inline-block; padding: 7px 15px; border: 1px solid var(--color-link); border-radius: 8px; background: var(--color-surface);
                      color: var(--color-link); font: inherit; font-weight: 600; text-decoration: none; cursor: pointer; }}
  .button-secondary:hover {{ background: var(--color-red-wash); }}
  .chip {{ display: inline-block; padding: 2px 8px; border-radius: 4px; background: var(--color-red-tint);
          color: var(--color-link); font-size: 0.875rem; font-weight: 600; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th {{ text-align: left; font-weight: 700; background: var(--color-fill); }}
  th, td {{ padding: 8px 12px; border-bottom: 1px solid var(--color-rule); }}

  /* Motion: the --motion and --ease variables, on transform and opacity only. */
{reduced}
</style>
"""


def latex_sty():
    def cname(k):
        return "airi" + "".join(p.capitalize() for p in k.split("-"))

    L = [f"% {GEN}", "%", "% AIRI colours for LaTeX. \\usepackage{airi-colors}",
         "%   \\textcolor{airiPrimary}{...}   \\airilinks (link colours, after hyperref)   \\airimark (title-block line)",
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
          "% Link colours for PDFs; call after loading hyperref. Web addresses are AIRI red. Cross-references and",
          "% citations stay ink. PDF links are coloured, not underlined (the print exception in BRAND.md, section 3).",
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
| Explainer videos, animation | `video/` | Sits on the `generate-video` template; see `video/README.md` |

## Chart defaults

The default colour order in the chart templates is red, grey, ink, then the
category colours. That makes a one- or two-series chart read as "the
subject, and everything else" without any work. Bars that compare groups
stay one colour. For named categories, switch
to the category colours (`airi_mpl.use_categorical()`, `airi$categorical`, or
the `cat` values in `tokens.json`). Categories never use red.

Office, Google Slides and Google Sheets are different: their charts take the
theme accents in order (red, grey, ink, blue, sky, violet). That suits a chart
of one to three series. `office-theme.md` and `google-slides-theme.md`
list what to set by hand.

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
OUTPUTS.update({TPL / "video" / name: fn for name, fn in video.OUTPUTS.items()})

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


label_phrase = guide.build_label  # 'ink on steps 1 to 5, white on steps 6 and 7'


def contrast_problems():
    """Every 'this text on that fill' rule in tokens.json must reach 4.5:1, in light and in dark."""
    out = []

    def need(what, fg, bg, floor=4.5):
        r = guide.v.contrast(fg, bg)
        if r < floor:
            out.append(f"contrast: {what}: {fg} on {bg} is {r:.2f}, below {floor}")

    for scale, labs in D["labels"].items():
        if scale == "note":
            continue
        if len(labs) != len(D[scale]):
            out.append(f"data.labels.{scale} has {len(labs)} entries; the scale has {len(D[scale])}")
            continue
        for n, (lab, fill) in enumerate(zip(labs, D[scale]), 1):
            need(f"{scale} step {n} label", LABEL[lab], fill)
    for c in CATS:
        need(f"category {c['name']} label", LABEL[c["label"]], c["fill"])
        need(f"category {c['name']} label (dark)", LABEL[c.get("label-dark", c["label"])], c.get("fill-dark", c["fill"]))
        need(f"category {c['name']} text on tint", c["ink"], c["tint"])
    need("category other text on tint", D["other"]["ink"], D["other"]["tint"])
    for k in ("good", "partial", "poor", "info", "none"):
        need(f"status {k} text on tint", S[k]["ink"], S[k]["tint"])
    for k, g in S["grade"].items():
        if k != "note":
            need(f"grade {k}", g["text"], g["fill"])
    for mode, col in (("light", C), ("dark", {**C, **DARK})):
        for fg in ("text", "text-muted", "link"):
            for bg in ("background", "surface", "fill", "red-tint", "red-wash"):
                need(f"{fg} on {bg} ({mode})", col[fg], col[bg])
        for k in ("good", "partial", "info"):
            need(f"{k}-ink on its tint ({mode})", col[f"{k}-ink"], col[f"{k}-tint" if k != "info" else "blue-tint"])
        need(f"link on red-tint, the poor status ({mode})", col["link"], col["red-tint"])
        need(f"focus ring on surface ({mode})", col["focus"], col["surface"], 3)
        need(f"white on primary ({mode})", C["white"], col["primary"])
    return out


def known_runs():
    """Every ordered list of colours the hand-written files may quote side by side."""
    runs = [D[k] for k in ("highlight", "pair", "severity", "red-continuous", "blue-sequential", "blue-5", "diverging-7", "diverging-5")]
    runs.append(D["severity"] + [D["severity-none"]])
    fills = [c["fill"] for c in CATS]
    runs += [fills, fills + [D["other"]["fill"]]]
    runs += [[c["fill"], c["ink"], c["tint"]] for c in CATS + [D["other"]]]
    runs += [[S[k]["mark"], S[k]["ink"], S[k]["tint"]] for k in ("good", "partial", "poor", "info", "none")]
    runs.append([S[k]["mark"] for k in ("good", "partial", "poor")])
    runs.append([SLOTS[f"accent{i}"] for i in range(1, 7)])
    return {tuple(h.upper() for h in r) for r in runs}


RUN = re.compile(r"`#[0-9A-Fa-f]{6}`(?:[ |]+`#[0-9A-Fa-f]{6}`){2,}")
WORD_HEX = re.compile(r"(?<![\w-])([A-Za-z][\w-]*)\s+`(#[0-9A-Fa-f]{6})`")
WORD_ALIAS = {"ink": "text", "muted": "text-muted", "grey": "gray"}
SLOT_NAMES = {"dark 1": "dark1", "light 1": "light1", "dark 2": "dark2", "light 2": "light2", "hyperlink": "hyperlink",
              "followed hyperlink": "followed-hyperlink", **{f"accent {i}": f"accent{i}" for i in range(1, 7)}}


def prose_problems(path, text):
    """Checks on hand-written Markdown beyond 'is this hex a token'."""
    out, rel = [], path.relative_to(ROOT)
    runs = known_runs()

    def bad(msg):
        out.append(f"{rel}: {msg}")

    # 1. Colours listed side by side must be one of the kit's palettes, in order.
    for m in RUN.finditer(text):
        got = tuple(h.upper() for h in HEX.findall(m.group(0)))
        if got not in runs:
            bad(f"the list {' '.join(got)} is not a palette in tokens.json (wrong order or wrong value)")
    # 2. A token or status name written straight before a hex must be that token's value.
    marks = {k: S[k]["mark"] for k in ("good", "partial", "poor")}
    for section in re.split(r"^(?=#{1,4} )", text, flags=re.M):
        head = section.split("\n", 1)[0].lower()
        if "changes from" in head:  # that section quotes old values on purpose
            continue
        dark = "dark mode" in head
        want = {**C, **marks, **(DARK if dark else {})}
        for word, h in WORD_HEX.findall(section):
            key = WORD_ALIAS.get(word.lower(), word.lower())
            if key in want and want[key].upper() != h.upper():
                bad(f"'{word} {h}': tokens.json says {key} is {want[key]}")
    # 3. Category rows: slot, name, fill (and text, tint, label where the table has them), domain.
    full = re.compile(r"^\| (\d) \| (\w+) \| `(#\w{6})` \| `(#\w{6})` \| `(#\w{6})` \| ([^|]+?) \| ([^|]+?) \|$", re.M)
    short = re.compile(r"^\| (\d) \| (\w+) \| `(#\w{6})` \| ([^|`]+?) \|$", re.M)
    for n, name, fill, ink, tint, label, domain in full.findall(text):
        c = CATS[int(n) - 1]
        if (name.lower(), fill, ink, tint, domain) != (c["name"], c["fill"], c["ink"], c["tint"], c["domain"]) \
                or label != ("white" if c["label"] == "white" else "ink"):
            bad(f"category row {n} ({name}) does not match tokens.json")
    for n, name, fill, domain in short.findall(text):
        c = CATS[int(n) - 1]
        if (name.lower(), fill, domain) != (c["name"], c["fill"], c["domain"]):
            bad(f"category row {n} ({name}) does not match tokens.json")
    # 4. Status and grade rows.
    for word, a, b, c3 in re.findall(r"^\| (Good|Partial|Poor|Info|None)\b[^|]*\| `(#\w{6})` \| `(#\w{6})` \| `(#\w{6})` \|$", text, re.M):
        st = S[word.lower()]
        if (a, b, c3) != (st["mark"], st["ink"], st["tint"]):
            bad(f"status row '{word}' does not match tokens.json")
    for word, a, b in re.findall(r"^\| (Yes|Partial|No) \| `(#\w{6})` \| `(#\w{6})` \|", text, re.M):
        g = S["grade"][word.lower()]
        if (a, b) != (g["fill"], g["border"]):
            bad(f"grade row '{word}' does not match tokens.json")
    # 5. Theme slots.
    for name, h in re.findall(r"\| (Dark [12]|Light [12]|Accent [1-6]|Hyperlink|Followed hyperlink)\b[^|`]*\| `(#\w{6})`", text):
        if SLOTS[SLOT_NAMES[name.lower()]] != h:
            bad(f"theme slot {name} is {h}; tokens.json says {SLOTS[SLOT_NAMES[name.lower()]]}")
    return out


def rules_problems(brand, skill):
    """The rules block is well formed, and BRAND.md and SKILL.md give the hard rules word for word."""
    out = []
    R = T.get("rules", {})
    hard = R.get("hard", [])
    if not 5 <= len(hard) <= 7:
        out.append(f"rules.hard has {len(hard)} rules; keep it to between 5 and 7")
    ids = [h.get("id") for h in hard]
    if len(set(ids)) != len(ids) or not all(ids):
        out.append("rules.hard: every rule needs its own id")
    for h in hard:
        if not h.get("rule") or not h.get("why"):
            out.append(f"rules.hard {h.get('id')}: needs a rule and a why")
    for key, parts in (("defaults", ("rule", "when-a-person-asks")), ("gap", ("rule", "where-to-look", "neutral", "report"))):
        for part in parts:
            if not R.get(key, {}).get(part):
                out.append(f"rules.{key}.{part} is missing")
    plain = lambda text: re.sub(r"\s+", " ", re.sub(r"[`*]", "", text)).lower()
    for name, text in (("skill/BRAND.md", plain(brand)), ("skill/SKILL.md", plain(skill))):
        for n, h in enumerate(hard, 1):
            if plain(h.get("rule", "")) not in text:
                out.append(f"{name} does not give hard rule {n} ({h.get('id')}) word for word")
            if plain(h.get("why", "")) not in text:
                out.append(f"{name} does not give the reason for hard rule {n} ({h.get('id')})")
    # Decisions: BRAND.md names every decided and open topic.
    dec = T.get("decisions", {})
    for item in dec.get("decided", []) + dec.get("open", []):
        if item["topic"].lower() not in brand.lower():
            out.append(f"skill/BRAND.md does not list the decision or open question: {item['topic']}")
    return out


def check():
    problems = []
    for path, fn in OUTPUTS.items():
        if not path.exists() or path.read_text() != fn():
            problems.append(f"{path.relative_to(ROOT)} is out of date: run dev/build-kit/build.py")
    problems += contrast_problems()
    problems += video.motion_problems()
    problems += video.prose_problems((SKILL / "BRAND.md").read_text(), (SKILL / "SKILL.md").read_text())
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
        if path.suffix == ".md":
            problems += prose_problems(path, text)
    # BRAND.md must state each scale's label rule in the words generated from tokens.json.
    brand = (SKILL / "BRAND.md").read_text()
    for scale in ("severity", "blue-sequential", "diverging-7", "diverging-5"):
        if label_phrase(scale) not in brand:
            problems.append(f"skill/BRAND.md does not state the {scale} label rule as: {label_phrase(scale)}")
    problems += rules_problems(brand, (SKILL / "SKILL.md").read_text())
    # The changeover procedure and its scanner ship with the skill, and SKILL.md must point at both.
    for rel in ("CHANGEOVER.md", "tools/brand_scan.py"):
        if not (SKILL / rel).exists():
            problems.append(f"skill/{rel} is missing")
        elif rel not in (SKILL / "SKILL.md").read_text():
            problems.append(f"skill/SKILL.md does not point at {rel}")
    for p in problems:
        print("FAIL", p)
    print("ok: everything agrees with tokens.json" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


def main():
    if "--check" in sys.argv:
        sys.exit(check())
    TPL.mkdir(exist_ok=True)
    for path, fn in OUTPUTS.items():
        path.parent.mkdir(exist_ok=True)
        path.write_text(fn())
        print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
