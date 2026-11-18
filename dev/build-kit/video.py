"""Motion and video: the files in skill/templates/video/, generated from tokens.json.

build.py imports this module. Nothing here is run on its own.

  airi-video.css   tokens as CSS variables, then the scene components
  comp.html        a sample composition that uses every component
  script.txt       narration for the sample
  captions.srt     captions for the sample
  README.md        how to start a video

The components section of the CSS holds no times or easing curves of its own: every
one is a variable from the tokens section. motion_problems() enforces that.
"""
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skill"
T = json.loads((SKILL / "tokens.json").read_text())
C = T["color"]
CATS = T["data"]["categorical"]
M = T["motion"]
V = T["video"]
GRID = V["grid"]
BUILD = M["logo-build"]
CAP = V["captions"]
LT = V["lower-third"]
FMT = V["formats"]
GEN = f"AIRI brand kit {T['version']}. Generated from tokens.json by dev/build-kit/build.py. Do not edit by hand."

MODULE = GRID["module-px"]
LARGE = MODULE * GRID["squares-in-modules"]["large"]
MEDIUM = MODULE * GRID["squares-in-modules"]["medium"]


def bezier(p):
    return "cubic-bezier(" + ", ".join(f"{x:g}" for x in p) + ")"


def safe(px, pct):
    """A safe-area inset, rounded up to the square grid so furniture sits on it."""
    need = px * pct / 100
    return int(-(-need // MODULE) * MODULE)



# ---------------------------------------------------------------- the icon's squares

def icon_squares():
    """The 15 squares of the icon, read from the logo file: (x, y, side) in the icon's own units.

    The path holds six small and five medium squares as four-point boxes, the right arm of the
    plus as a box two squares wide, and the other three arms as one eight-point outline.
    """
    d = re.search(r'<path fill="#a32035" d="([^"]+)"', (SKILL / "logos/initiative/icon.svg").read_text()).group(1)
    out = []
    for sub in d.split("M")[1:]:
        pts = [(float(a), float(b)) for a, b in re.findall(r"(-?[\d.]+) (-?[\d.]+)", sub.split("Z")[0])]
        xs, ys = sorted({round(p[0], 1) for p in pts}), sorted({round(p[1], 1) for p in pts})
        if len(pts) < 4:
            continue
        if len(xs) == 2 and len(ys) == 2:
            w, h = xs[1] - xs[0], ys[1] - ys[0]
            if w > 1.5 * h:                       # centre + right arm: keep the right arm
                out.append((xs[1] - h, ys[0], h))
            else:
                out.append((xs[0], ys[0], w))
        else:                                     # top, left and bottom arms
            side = xs[1] - xs[0]
            out += [(xs[1], ys[0], side), (xs[0], ys[1], side), (xs[1], ys[2], side)]
    return sorted(out)


def logo_mask():
    """Mask boxes for the horizontal logo, in its viewBox, grouped into beats from left to right.

    The logo file itself is shown through the mask, so the logo is never redrawn.
    """
    svg = (SKILL / "logos/initiative/horizontal-on-light.svg").read_text()
    vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    m = re.search(r"translate\(([\d.]+), ([\d.]+)\) scale\(([\d.]+)\) translate\((-?[\d.]+), (-?[\d.]+)\)", svg)
    tx, ty, s, ox, oy = (float(x) for x in m.groups())
    beats, rects, right = [], [], 0
    for x, y, side in icon_squares():
        key = round(x / 10)
        if key not in beats:
            beats.append(key)
        pad = 0.15
        X, Y, S = tx + s * (x + ox), ty + s * (y + oy), s * side
        right = max(right, X + S)
        rects.append((beats.index(key), X - pad, Y - pad, S + 2 * pad))
    return vb, rects, len(beats), right


# ---------------------------------------------------------------- airi-video.css

def token_css():
    col = [f"  --color-{k}: {v};" for k, v in C.items()]
    col += [f"  --color-cat-{c['slot']}: {c['fill']};" for c in CATS]
    col += [f"  --color-cat-other: {T['data']['other']['fill']};"]
    v, land = M["video"], FMT["landscape"]
    ty = V["type-px"]

    def frame(f, indent="  "):
        w, h = f["width"], f["height"]
        return [f"{indent}--w: {w}px; --h: {h}px;",
                f"{indent}--airi-safe-x: {safe(w, V['safe-area-pct']['title'])}px; --airi-safe-y: {safe(h, V['safe-area-pct']['title'])}px;"]

    L = [f"/* {GEN}",
         "   Video styles for compositions made with the generate-video template (stage.js, stage.css).",
         "   Put class \"airi\" on <html>.",
         "   Self-contained: no web fonts and no imports, because a render uses local files only. */", "",
         '@font-face { font-family: "Figtree"; font-weight: 300 900; src: url("fonts/Figtree-wght.ttf") format("truetype"), local("Figtree"); }', "",
         "/* ---- tokens ---- */", ":root {"]
    L += col
    L += [f"  --airi-font: 'Figtree', Arial, sans-serif;", "",
          "  /* Frame: landscape by default. Safe insets are the title-safe area, rounded up to the square grid */"]
    L += frame(land)
    L += ["", "  /* Motion for video: three durations, three curves, one stagger */"]
    L += [f"  --airi-dur-{k}: {ms}ms;" for k, ms in v["duration-ms"].items()]
    L += [f"  --airi-ease: {bezier(v['easing']['standard'])};",
          f"  --airi-ease-in: {bezier(v['easing']['entrance'])};",
          f"  --airi-ease-out: {bezier(v['easing']['exit'])};",
          f"  --airi-stagger: {v['stagger-ms']['default']}ms;", "",
          "  /* Layout grid: the icon's small, medium and large squares */",
          f"  --airi-sq: {MODULE}px;", f"  --airi-sq-m: {MEDIUM}px;", f"  --airi-sq-l: {LARGE}px;", "",
          "  /* Logo build (being finalised; these are the interim values): one tick, and ticks per beat */",
          f"  --airi-tick: calc(1s / {BUILD['ticks-per-second']});",
          "  --airi-nudge: calc(var(--airi-tick) / 4);  /* steps land between frames, never on one */",
          f"  --airi-logo-beat: calc({BUILD['beat-ticks']} * var(--airi-tick));", "",
          "  /* Furniture */"]
    L += [f"  --airi-type-{k}: {px}px;" for k, px in ty.items()]
    L += [f"  --airi-caption-size: {CAP['size-px']}px;",
          f"  --airi-caption-text: {CAP['text']};", f"  --airi-caption-plate: {CAP['plate']};",
          f"  --airi-lt-in: {LT['in-ms']}ms;", f"  --airi-lt-out: {LT['out-ms']}ms;",
          f"  --airi-end-hold: {V['end-card']['hold-s']}s;",
          f"  --radius-sm: {T['radius']['sm']};", "}"]
    for name in ("vertical", "square"):
        L += [f"html.format-{name} {{"] + frame(FMT[name]) + ["}"]
    return "\n".join(L)


COMPONENTS = r"""
/* ---- components ----
   Every time and curve below is a variable from the tokens above. */

.airi body { background: var(--color-background); color: var(--color-text); font-family: var(--airi-font);
             font-weight: 400; font-size: var(--airi-type-body); line-height: 1.25; }
.airi h1, .airi h2, .airi p { margin: 0; }
.airi em { font-style: normal; color: var(--color-link); }

/* Scenes cut. Add class "fade" for a short crossfade. */
.airi .scene { --scene-fade: 0s; display: flex; flex-direction: column; justify-content: center; gap: var(--airi-sq);
               padding: var(--airi-safe-y) var(--airi-safe-x); background: var(--color-background); }
.airi .scene.fade { --scene-fade: var(--airi-dur-short); transition-timing-function: var(--airi-ease); }

/* Anything with data-at arrives calmly: the entrance curve, the long duration. */
.airi [data-at] { transition-duration: var(--airi-dur-long); transition-timing-function: var(--airi-ease-in); }

/* Statement: one large sentence at a time. */
.airi-statement p { font-size: var(--airi-type-statement); font-weight: 700; line-height: 1.15; max-width: 22ch; }

/* Chart scene: finding as the title, direct labels, bars grow last. */
.airi .airi-chart { justify-content: flex-start; }
.airi-chart h2 { font-size: var(--airi-type-chart-title); font-weight: 700; color: var(--color-link); }
.airi-bars { display: grid; grid-template-columns: max-content 1fr; column-gap: var(--airi-sq);
             row-gap: calc(var(--airi-sq) * 0.8); align-items: center; font-size: var(--airi-type-label); }
.airi-bars .track { display: flex; align-items: center; gap: calc(var(--airi-sq) / 2); height: var(--airi-sq); }
.airi-bars .track i { display: block; height: 100%; width: calc(var(--v) * 85%); background: var(--c); }
.airi .airi-bars .track i[data-at] { opacity: 1; transform: scaleX(0); transform-origin: left;
                                     transition: transform var(--airi-dur-long) var(--airi-ease); }
.airi .airi-bars .track i[data-at].in { transform: scaleX(1); }
.airi .airi-bars .track b[data-at] { font-weight: 700; transform: none; transition-duration: var(--airi-dur-short); }
.airi-source { font-size: var(--airi-type-smallest); color: var(--color-text-muted); }

/* Caption plate: white on ink, bottom centre, inside the title-safe area. Captions cut in and out.
   #captions is the element stage.js fills from the narration. */
.airi .airi-caption[data-at], .airi #captions {
  position: absolute; left: 50%; bottom: var(--airi-safe-y); z-index: 30; transform: translateX(-50%);
  max-width: calc(var(--w) - 2 * var(--airi-safe-x)); padding: calc(var(--airi-sq) * 0.3) calc(var(--airi-sq) * 0.6);
  border-radius: var(--radius-sm); font-size: var(--airi-caption-size); font-weight: 400; line-height: 1.25;
  text-align: center; white-space: nowrap; color: var(--airi-caption-text); background: var(--airi-caption-plate);
  opacity: 0; transition: none; }
.airi #captions { white-space: normal; text-wrap: balance; max-width: 22em; }
.airi .airi-caption[data-at].in, .airi #captions.in { opacity: 1; }

/* Lower third: bottom left, inside title-safe. In, hold, out; set data-out to data-at plus the in time plus the hold. */
.airi .airi-lower-third[data-at] {
  position: absolute; left: var(--airi-safe-x); bottom: var(--airi-safe-y); z-index: 10;
  display: grid; grid-template-columns: var(--airi-sq-l) auto; column-gap: calc(var(--airi-sq) * 0.75);
  align-content: center; min-height: var(--airi-sq-l); padding-right: var(--airi-sq);
  background: var(--color-surface); color: var(--color-text); line-height: 1.2;
  opacity: 1; transform: none; clip-path: inset(0 100% 0 0); visibility: hidden;
  transition: clip-path var(--airi-lt-out) var(--airi-ease-out), visibility 0s linear var(--airi-lt-out); }
.airi .airi-lower-third[data-at].in { clip-path: inset(0 0 0 0); visibility: visible;
  transition: clip-path var(--airi-lt-in) var(--airi-ease-in), visibility 0s; }
.airi-lower-third::before { content: ""; grid-row: 1 / span 2; background: var(--color-primary); min-height: var(--airi-sq-l); }
.airi-lower-third strong { align-self: end; font-size: var(--airi-type-body); font-weight: 700; }
.airi-lower-third span { align-self: start; font-size: var(--airi-type-label); color: var(--color-text-muted); }

/* End card and logo card. The logo is never faded, slid or scaled. A plain logo image cuts in.
   The masked logo that comp.html uses builds: its squares appear in the icon's own order, small
   to large, then the wordmark. The logo file is shown through the mask and never redrawn. */
.airi .airi-endcard, .airi .airi-logocard { gap: calc(2 * var(--airi-sq)); }
.airi .airi-logo[data-at] { display: block; width: calc(9 * var(--airi-sq-l)); max-width: 100%; height: auto;
                            opacity: 1; transform: none; transition: none; visibility: hidden; }
.airi .airi-logo[data-at].in { visibility: visible; }
.airi .airi-logo .sq { opacity: 0; }
.airi .airi-logo.in .sq {
  animation: airi-appear var(--airi-tick) steps(1, end) calc(var(--b) * var(--airi-logo-beat) - var(--airi-nudge)) forwards; }
@keyframes airi-appear { to { opacity: 1; } }
.airi-url { font-size: var(--airi-type-statement); font-weight: 700; }

/* Red card: the title card and the section card. One element placed above the scenes.
   It slides on, holds for --hold while its text shows, then slides off. Change the scene
   underneath while it holds. Class "airi-title" starts already on. */
.airi .airi-card[data-at] {
  --airi-on: var(--airi-dur-scene); --airi-off: var(--airi-dur-scene); --hold: var(--airi-end-hold); --lead: 0s;
  position: absolute; inset: 0; z-index: 20; overflow: hidden;
  display: flex; flex-direction: column; justify-content: center; gap: calc(var(--airi-sq) / 2);
  padding: var(--airi-safe-y) var(--airi-safe-x); color: var(--color-white);
  opacity: 1; transform: none; transition: none; visibility: hidden; }
.airi .airi-card.airi-title[data-at] { --airi-on: 0s; --lead: var(--airi-dur-short); }
.airi .airi-card[data-at].in { visibility: visible; }
.airi-card h1 { font-size: var(--airi-type-title); font-weight: 700; line-height: var(--airi-sq-l); }
.airi-card h2 { font-size: var(--airi-type-section); font-weight: 700; line-height: var(--airi-sq-l); }
.airi-card .airi-card-logo { position: absolute; left: var(--airi-safe-x); top: var(--airi-safe-y); height: var(--airi-sq-m); }

.airi-card::before { content: ""; position: absolute; z-index: -1; inset: 0;
                     background: var(--color-primary); transform: translateX(-100%); }
.airi .airi-card.in::before {
  animation: airi-wipe-on var(--airi-on) var(--airi-ease) forwards,
             airi-wipe-off var(--airi-off) var(--airi-ease) calc(var(--airi-on) + var(--hold)) forwards; }
@keyframes airi-wipe-on { from { transform: translateX(-100%); } to { transform: translateX(0); } }
@keyframes airi-wipe-off { from { transform: translateX(0); } to { transform: translateX(100%); } }

/* The card's text shows only while the card holds. */
.airi-card > * { visibility: hidden; --d: 0s; }
.airi-card > :nth-child(2) { --i: 1; }
.airi-card > :nth-child(3) { --i: 2; }
.airi-card > :nth-child(4) { --i: 3; }
.airi-card > :not(.airi-card-logo) { --d: calc(var(--lead) + var(--i, 0) * var(--airi-dur-short)); }
.airi .airi-card.in > * { animation: airi-hold calc(var(--hold) - var(--d)) linear calc(var(--airi-on) + var(--d)); }
.airi .airi-card.in > :not(.airi-card-logo) {
  animation: airi-hold calc(var(--hold) - var(--d)) linear calc(var(--airi-on) + var(--d)),
             airi-rise var(--airi-dur-long) var(--airi-ease-in) calc(var(--airi-on) + var(--d)) backwards,
             airi-fade-out var(--airi-dur-short) var(--airi-ease-out) calc(var(--airi-on) + var(--hold) - var(--airi-dur-short)) forwards; }
@keyframes airi-hold { from, to { visibility: visible; } }
@keyframes airi-rise { from { opacity: 0; transform: translateY(var(--airi-sq)); } }
@keyframes airi-fade-out { to { opacity: 0; } }

"""


def video_css():
    return token_css() + "\n" + COMPONENTS


# ---------------------------------------------------------------- the sample

TITLE = ("Seven domains", "of AI risk")
CUES = [
    (21.8, 24.7, ["The repository groups risks from AI", "into seven domains."]),
    (25.0, 28.3, ["Each domain keeps the same colour", "in every chart."]),
]
SCRIPT = [
    "People describe the risks from A I in many ways.",
    "A shared map makes them comparable.",
    "[pause 1.5]",
    "The repository groups risks from A I into seven domains.",
    "Each domain keeps the same colour in every chart.",
]
SHARES = [0.62, 0.48, 0.34, 0.55, 0.41, 0.72, 1.0]   # illustrative bar lengths, not data
DURATION = 34


def logo_svg(at, indent="  "):
    vb, rects, beats, right = logo_mask()
    w, h = vb[2], vb[3]
    L = [f'{indent}<svg class="airi-logo" data-at="{at}" viewBox="0 0 {w:g} {h:g}" role="img" aria-label="MIT AI Risk Initiative">',
         f'{indent}  <mask id="airi-logo-mask" maskUnits="userSpaceOnUse" x="0" y="0" width="{w:g}" height="{h:g}" fill="#fff">']
    for b, x, y, s in rects:
        L.append(f'{indent}    <rect class="sq" style="--b:{b}" x="{x:.2f}" y="{y:.2f}" width="{s:.2f}" height="{s:.2f}"/>')
    L += [f'{indent}    <rect class="sq" style="--b:{beats + 1}" x="{right + 1:.2f}" y="0" width="{w - right - 1:.2f}" height="{h:g}"/>',
          f"{indent}  </mask>",
          f'{indent}  <image href="logos/initiative/horizontal-on-light.svg" width="{w:g}" height="{h:g}" mask="url(#airi-logo-mask)"/>',
          f"{indent}</svg>"]
    return "\n".join(L), beats


def comp_html():
    land = FMT["landscape"]
    t0 = 19.8
    stag = M["video"]["stagger-ms"]["default"] / 1000
    rows = []
    for i, (c, v) in enumerate(zip(CATS, SHARES)):
        at = round(t0 + 0.9 + i * stag, 2)
        rows.append(f'    <span>{escape(c["domain"])}</span>'
                    f'<span class="track"><i data-at="{at:g}" style="--v:{v:g}; --c:var(--color-cat-{c["slot"]})"></i>'
                    f'<b data-at="{round(at + 0.7, 2):g}" data-enter="fade">{round(v * 25)}</b></span>')
    caps = "\n".join(f'<div class="airi-caption" data-at="{a:g}" data-out="{b:g}">{"<br>".join(escape(x) for x in lines)}</div>' for a, b, lines in CUES)
    logo, beats = logo_svg("28.9", "  ")
    done = 28.9 + (beats + 2) * BUILD["beat-ticks"] / BUILD["ticks-per-second"]
    nl = "\n"
    return f"""<!doctype html>
<!-- {GEN}
     A sample AIRI video: every component, on the generate-video template. Silent, so the times are
     plain seconds; in a narrated video tie them to the narration (data-at="n03") as that template shows.
     The words and bar lengths are illustrative. See README.md in this folder. -->
<html lang="en" class="airi" data-width="{land['width']}" data-height="{land['height']}" data-fps="{V['fps']['default']}" data-duration="{DURATION:g}">
<head>
<meta charset="utf-8">
<title>Seven domains of AI risk (sample)</title>
<link rel="stylesheet" href="stage.css">
<link rel="stylesheet" href="airi-video.css">
</head>
<body>

<!-- 1. Title card (brand moment 1). Already on at the start; holds, then slides off. -->
<div class="airi-card airi-title" data-at="0" style="--hold: 5.6s">
  <img class="airi-card-logo" src="logos/initiative/horizontal-on-dark.svg" alt="MIT AI Risk Initiative">
  <h1>{TITLE[0]}<br>{TITLE[1]}</h1>
  <p>A sample explainer from the AIRI brand kit</p>
</div>

<!-- 2. Statement, with a lower third: 1 s in, 4 s hold, 1 s out. -->
<section class="scene airi-statement" data-from="5" data-to="15">
  <p data-at="6.9">People describe the risks from AI in <em>many ways</em>.</p>
  <p data-at="9.6">A shared map makes them comparable.</p>
  <div class="airi-lower-third" data-at="7.4" data-out="12.4"><strong>Presenter name</strong><span>Role, organisation</span></div>
</section>

<!-- 3. Section card (brand moment 2). The scene underneath changes at 15 s, while the card holds. -->
<div class="airi-card" data-at="13.8" style="--hold: 2.8s">
  <p>Part 1</p>
  <h2>The seven domains</h2>
</div>

<!-- 4. Chart. Order: title, then labels, then the bars, {round(stag * 1000)} ms apart. Category colours, in their fixed order. -->
<section class="scene airi-chart" data-from="15" data-to="28.7">
  <h2 data-at="{t0 - 0.7:g}">AI risks fall into seven domains</h2>
  <div class="airi-bars" data-at="{t0:g}" data-enter="fade">
{nl.join(rows)}
  </div>
  <p class="airi-source" data-at="{t0 + 2.6:g}" data-enter="fade">Bar lengths are illustrative, to show the layout. They are not data.</p>
</section>

<!-- Captions: two lines at most, {CAP['max-chars-per-line']} characters a line. The same cues are in captions.srt. -->
{caps}

<!-- 5. End card (brand moment 3). The logo builds from its squares, then holds {V['end-card']['hold-s']} s. -->
<section class="scene airi-endcard" data-from="28.7" data-to="end">
{logo}
  <p class="airi-url" data-at="{done:.1f}" data-enter="fade">{V['end-card']['url']}</p>
</section>

<!-- For narration: uncomment the next line (narrate.js writes the file) and add <div id="captions"></div>. -->
<!-- <script src="audio/narration.js"></script> -->
<script src="stage.js"></script>
</body>
</html>
"""


def stamp(t):
    ms = round(t * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def captions_srt():
    return "\n".join(f"{i}\n{stamp(a)} --> {stamp(b)}\n" + "\n".join(lines) + "\n" for i, (a, b, lines) in enumerate(CUES, 1))


def script_txt():
    return "\n".join(SCRIPT) + "\n"


def readme():
    v, ui = M["video"], M["ui"]
    fm = " | ".join(f"{f['width']} x {f['height']}" for f in FMT.values())
    return f"""# Video templates

A starting point for AIRI explainer videos and explanatory animations. It sits on
top of the composed-video template from the `generate-video` skill: that template
supplies the timing (`stage.js`, `stage.css`) and the renderer; these files supply
the AIRI look, motion and furniture. Everything here except `check_video.py` and
the font is generated from `../../tokens.json`.

| File | What it is |
|---|---|
| `airi-video.css` | Tokens as CSS variables and the scene components |
| `comp.html` | A sample that uses every component. Copy it and replace the content |
| `script.txt` | Narration for the sample, one line per line |
| `captions.srt` | Captions for the sample |
| `check_video.py` | Checks a composition and its captions against the rules |
| `fonts/` | Figtree, so a render never falls back to another font |

## Start a video

```bash
cp -r ~/.claude/skills/generate-video/assets/template my-video
cp -r airi-video.css comp.html script.txt captions.srt fonts my-video/
cp -r ../../logos my-video/logos
cd my-video
python3 /path/to/skill/templates/video/check_video.py comp.html captions.srt
node ~/.claude/skills/generate-video/scripts/render.js comp.html --check
node ~/.claude/skills/generate-video/scripts/render.js comp.html --sheet every=1 --out out/sheet.jpg
node ~/.claude/skills/generate-video/scripts/render.js comp.html --out out/video.mp4
```

Write the storyboard and the script first, as the `generate-video` skill says.
Renders use local files only: no web fonts, no remote images.

## Motion

Put class `airi` on `<html>`. Transitions are conventional: the red card slides on and off
smoothly, titles rise in, scenes cut or crossfade. These are defaults. A person can ask for
something different.

The logo builds from its squares, small to large, then the wordmark. Its speed and style are
being finalised; the current timing is the default until then. The logo is never faded, slid
or scaled. That one is a hard rule.

The title card, section cards and the end card are the brand moments. Aim for
{v['brand-moments-max']} in a video.

Square-step transitions (the red-square wipe and the stepped title reveal) were dropped after
team review. `style-square` and `airi-reveal` no longer do anything.

## Components

| Class | Use |
|---|---|
| `airi-card airi-title` | Title card: red, white logo top left, `h1`, one line under it. `--hold` is how long it stays |
| `airi-card` | Section card: slides on, holds for `--hold`, slides off. Change the scene underneath during the hold |
| `scene airi-statement` | One large sentence at a time. `<em>` is the red emphasis |
| `scene airi-chart` | `h2` states the finding; `airi-bars` rows grow last; `airi-source` under it |
| `airi-lower-third` | Name and role, bottom left. `data-out` is `data-at` plus {LT['in-ms'] // 1000} s plus a {LT['hold-s-min']} to {LT['hold-s-max']} s hold; the scene must last {LT['out-ms'] // 1000} s longer |
| `airi-caption` | A burned-in caption cue, `<br>` between its two lines. `#captions` gets the same look |
| `scene airi-endcard` | The logo and `{V['end-card']['url']}`, held {V['end-card']['hold-s']} s after the logo is complete. Copy the masked logo from `comp.html` for the build |
| `scene airi-logocard` | The logo alone, {V['logo-card']['length-s-min']} to {V['logo-card']['length-s-max']} s, to open a video shorter than {V['logo-card']['videos-under-s']} s |

Formats: {fm}. For the second and third add `format-vertical` or `format-square`
to `<html>` and set `data-width` and `data-height` to match.

## Values

| | Value |
|---|---|
| Durations | {", ".join(f"{k} {ms} ms ({v['duration-use'][k]})" for k, ms in v['duration-ms'].items())} |
| Easing | standard `{bezier(v['easing']['standard'])}`, entrance `{bezier(v['easing']['entrance'])}`, exit `{bezier(v['easing']['exit'])}` |
| Stagger | {v['stagger-ms']['min']} to {v['stagger-ms']['max']} ms between items that arrive together |
| Order | {", then ".join(v['order'])} |
| Layout grid | module {MODULE} px; squares of {MODULE}, {MEDIUM} and {LARGE} px |
| Logo build | {BUILD['ticks-per-second']} steps a second, {BUILD['beat-ticks']} steps a beat. Being finalised |
| Frame rate | {V['fps']['default']} fps; {V['fps']['data-heavy']} for data-heavy animation |
| Safe areas | title-safe {V['safe-area-pct']['title']}% inset, action-safe {V['safe-area-pct']['action']}% |
| Captions | {CAP['size-px']} px or larger, {CAP['max-chars-per-line']} characters a line ({CAP['max-chars-per-line-narrow']} in vertical and square), {CAP['max-lines']} lines, {CAP['max-chars-per-second']} characters a second, at least {CAP['min-frames']} frames |

Never: {", ".join(M['prohibited'])}.

## Captions and the alternative

Every video ships with an SRT file, a transcript and one static key frame
(`render.js comp.html --frame 12 --out key-frame.png`). Keep each narration line
to {CAP['max-chars-per-line'] * CAP['max-lines']} characters or fewer so it fits one two-line caption. Run `check_video.py`
on the SRT before rendering.

## Sound

Keep videos under a minute and narrate briskly: `narrate.js script.txt --style "clear, warm, brisk"`,
about 140 words for 55 s. Music is off by default (people speed explainers up). If a video
wants it, use the style in BRAND.md and place it with `data-role="music"`; the renderer sets the
level. Say when music or a voice was generated.

## On a web page

These files are for rendered video. Motion in a web page or tool uses the
interface values in `../../brand.css` ({ui['duration-ms']['fast-01']} to {ui['duration-ms']['slow-02']} ms) and must honour
`prefers-reduced-motion`.
"""


OUTPUTS = {
    "airi-video.css": video_css,
    "comp.html": comp_html,
    "script.txt": script_txt,
    "captions.srt": captions_srt,
    "README.md": readme,
}


# ---------------------------------------------------------------- checks

TIME = re.compile(r"(?<![\w.#-])(\d*\.?\d+)(ms|s)\b")
BANNED = re.compile(r"rotate|skew|bounce|elastic|glitch|cubic-bezier|ease-in|ease-out|\bease\b(?!-)", re.I)


def motion_problems():
    """The motion and video tokens are sane, and the generated CSS takes every time from them."""
    out = []
    ui, v = M["ui"], M["video"]
    d = list(ui["duration-ms"].values())
    if d != sorted(d) or len(set(d)) != len(d):
        out.append("motion.ui.duration-ms is not a rising ladder")
    for reg, block in (("ui", ui), ("video", v)):
        for name in ("standard", "entrance", "exit"):
            p = block["easing"].get(name)
            if not p or len(p) != 4:
                out.append(f"motion.{reg}.easing.{name} needs four control points")
            elif not all(0 <= x <= 1 for x in p):
                out.append(f"motion.{reg}.easing.{name} leaves 0 to 1: that is overshoot, which the brand prohibits")
    if set(v["duration-ms"]) != {"short", "long", "scene"}:
        out.append("motion.video.duration-ms must be exactly short, long and scene")
    s = v["stagger-ms"]
    if not s["min"] <= s["default"] <= s["max"]:
        out.append("motion.video.stagger-ms default is outside min to max")
    if ui["stagger-ms"] * 2 > ui["stagger-total-max-ms"]:
        out.append("motion.ui stagger and its total limit disagree")
    for name, f in FMT.items():
        if f["width"] % LARGE or f["height"] % LARGE:
            out.append(f"video.formats.{name} is not a whole number of large squares ({LARGE} px)")
        if f["width"] % 2 or f["height"] % 2:
            out.append(f"video.formats.{name} has an odd side")
    if MODULE * 27 != min(FMT["landscape"]["width"], FMT["landscape"]["height"]):
        out.append("video.grid.module-px is not 1/27 of the frame's short side")
    for fps in V["fps"].values():
        if fps % BUILD["ticks-per-second"]:
            out.append(f"{fps} fps is not a whole number of frames per logo-build tick")
    if "style-square" in COMPONENTS or "airi-reveal" in COMPONENTS:
        out.append("airi-video.css components still carry a dropped square-step transition")
    for key in ("size-px", "max-chars-per-line", "max-chars-per-line-narrow", "max-lines", "max-chars-per-second", "min-frames", "text", "plate"):
        if not CAP.get(key):
            out.append(f"video.captions.{key} is missing")
    if CAP["size-px"] * 20 < 1080:
        out.append("video.captions.size-px is under 1/20 of a 1080 px frame")
    if V["type-px"]["smallest"] < 28:
        out.append("video.type-px.smallest is under 28 px")
    if len(icon_squares()) != 15:
        out.append("the icon no longer reads as 15 squares; check video.icon_squares()")
    # check_video.py carries a copy of the limits for when it is used away from tokens.json.
    src = (SKILL / "templates/video/check_video.py").read_text()
    m = re.search(r"^DEFAULTS = (\{.*\})$", src, re.M)
    want = {k: CAP[k] for k in ("max-chars-per-line", "max-chars-per-line-narrow", "max-lines", "max-chars-per-second", "min-frames")}
    want.update({"fps": sorted(V["fps"].values()), "formats": [[f["width"], f["height"]] for f in FMT.values()],
                 "brand-moments-max": M["video"]["brand-moments-max"]})
    if not m or json.loads(m.group(1)) != want:
        out.append("skill/templates/video/check_video.py: DEFAULTS differ from tokens.json")
    # No stray times or curves in the components.
    for m in TIME.finditer(COMPONENTS):
        if float(m.group(1)) != 0:
            out.append(f"airi-video.css components hold a time that is not a token: {m.group(0)}")
    for m in BANNED.finditer(re.sub(r"/\*.*?\*/", "", COMPONENTS, flags=re.S).replace("--airi-ease-in", "").replace("--airi-ease-out", "").replace("--airi-ease", "")):
        out.append(f"airi-video.css components use {m.group(0)!r}: curves come from the tokens, and that motion may be prohibited")
    # The sample's captions must pass their own limits.
    fps = V["fps"]["default"]
    for a, b, lines in CUES:
        chars = sum(len(x) for x in lines)
        if len(lines) > CAP["max-lines"] or any(len(x) > CAP["max-chars-per-line"] for x in lines):
            out.append(f"sample caption at {a} s breaks the line limits")
        if chars / (b - a) > CAP["max-chars-per-second"] or (b - a) * fps < CAP["min-frames"]:
            out.append(f"sample caption at {a} s breaks the timing limits")
    return out


def prose_problems(brand, skill):
    """BRAND.md must give every motion value; SKILL.md must carry the short rules."""
    out = []
    ui, v = M["ui"], M["video"]
    for name, ms in ui["duration-ms"].items():
        if not re.search(rf"`{name}`\s*\|\s*{ms} ms", brand):
            out.append(f"skill/BRAND.md does not give the interface duration {name} as {ms} ms")
    for name, ms in v["duration-ms"].items():
        if not re.search(rf"`{name}`\s*\|\s*{ms} ms", brand):
            out.append(f"skill/BRAND.md does not give the video duration {name} as {ms} ms")
    for reg in (ui, v):
        for name, p in reg["easing"].items():
            if bezier(p) not in brand:
                out.append(f"skill/BRAND.md does not give the {name} curve {bezier(p)}")
    need = {
        "caption size": f"{CAP['size-px']} px", "caption line length": f"{CAP['max-chars-per-line']} characters",
        "caption reading speed": f"{CAP['max-chars-per-second']} characters a second", "caption minimum": f"{CAP['min-frames']} frames",
        "end-card hold": f"{V['end-card']['hold-s']} s", "end-card address": V["end-card"]["url"],
        "title-safe": f"{V['safe-area-pct']['title']}%", "action-safe": f"{V['safe-area-pct']['action']}%",
        "grid module": f"{MODULE} px", "logo-build tick rate": f"{BUILD['ticks-per-second']} steps a second",
        "interface stagger": f"{ui['stagger-ms']} ms", "frame rate": f"{V['fps']['default']} fps",
    }
    for what, text in need.items():
        if text not in brand:
            out.append(f"skill/BRAND.md does not state the {what} as: {text}")
    for word in M["prohibited"][:5]:
        if word not in brand.lower():
            out.append(f"skill/BRAND.md does not list the prohibited motion: {word}")
        if word not in skill.lower():
            out.append(f"skill/SKILL.md does not list the prohibited motion: {word}")
    for text in ("templates/video", "check_video.py"):
        if text not in skill:
            out.append(f"skill/SKILL.md does not mention {text}")
    return out
