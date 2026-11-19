#!/usr/bin/env python3
"""Scan existing work against the AIRI brand kit and report what differs.

    python3 brand_scan.py PATH [PATH ...]            Markdown report
    python3 brand_scan.py PATH --json                the same findings, for a program
    python3 brand_scan.py PATH --include-categories  also judge category palettes
    python3 brand_scan.py PATH --exclude docs        leave a folder or pattern out

Read-only: it never changes a file. It reads the kit's tokens.json from the folder
above this script, finds colour values and font names in the paths given, and sorts
what it finds into four groups.

Must fix          a hard rule is broken: a red that is not the kit's (rule 2), a
                  typeface other than Figtree (rule 3), or text that fails contrast
                  where both colours sit in one style block (rule 4).
Probably drift    a value very close to a kit colour, a kit 1.x value, or a tool
                  default the kit lists to avoid. The report names the token to use.
Needs a decision  a colour with no close kit colour. A person decides: reuse the
                  closest kit colour, use a neutral, or raise the gap with the kit.
For information   category palettes and other things that look deliberate. The
                  agreed category colours are for new work only, so the scan proposes
                  no change to an existing palette unless --include-categories is set.

What it reads: .html .htm .css .scss .less .js .jsx .ts .tsx .vue .svelte .json .py
.ipynb .R .r .Rmd .qmd .tex .sty .svg .md, and the XML inside .pptx .docx .xlsx
(theme colours, colours set by hand, typefaces). It skips .git, node_modules,
virtual environments, build and vendor folders, minified files and very long lines.

What it cannot see: the logo (rule 1), colour used as the only signal (rule 5), what
red means in a chart (rule 6), video (rule 7; use templates/video/check_video.py),
images, colours computed at run time, and utility classes such as text-red-600.
Check those by eye.

Exit code 0 unless --fail-on-hard is given and a hard rule is broken.
Standard library only; Python 3.10 or later.
"""
import argparse
import colorsys
import fnmatch
import hashlib
import json
import math
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEXT_EXT = {".html", ".htm", ".css", ".scss", ".less", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".json",
            ".py", ".ipynb", ".r", ".rmd", ".qmd", ".tex", ".sty", ".svg", ".md"}
OFFICE_EXT = {".pptx", ".docx", ".xlsx"}
# In these, "#abc" is as likely a comment, heading or issue number as a colour, so short hex must be quoted.
STRICT_EXT = {".py", ".ipynb", ".r", ".rmd", ".qmd", ".tex", ".sty", ".json", ".md"}
CSS_EXT = {".css", ".scss", ".less"}
SKIP_DIRS = {".git", "node_modules", "venv", ".venv", "env", "dist", "build", "vendor", "vendors", "__pycache__",
             ".next", ".nuxt", ".astro", ".svelte-kit", ".cache", "coverage", "site-packages", "bower_components",
             ".ipynb_checkpoints", ".tox", ".mypy_cache", ".pytest_cache", "renv", "packrat", "_site", ".quarto",
             ".vercel", ".wrangler", ".output", "target"}
SKIP_NAMES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "composer.lock"}
MINIFIED = re.compile(r"(\.min\.|-min\.|\.bundle\.|\.chunk\.|\.map$)")
MAX_LINE = 2000          # longer lines are minified code or embedded data
MAX_BYTES = 1_500_000    # larger text files are data, not styling
MAX_PALETTE = 24         # more colours than this in one block is a design system, not a category palette
NEAR = 5.0               # CIEDE2000 below this is "the same colour, typed slightly wrong"


# ------------------------------------------------------------------ colour maths

def norm_hex(h):
    """'#abc', 'abc', '#AABBCCDD' -> ('AABBCC', alpha 0..1). None if not a hex colour."""
    h = h.lstrip("#")
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h)
    if len(h) not in (6, 8) or re.search(r"[^0-9A-Fa-f]", h):
        return None
    alpha = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
    return h[:6].upper(), alpha


def hex_to_rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _linear(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_to_lab(h):
    """sRGB hex -> CIE L*a*b* (D65)."""
    r, g, b = (_linear(c) for c in hex_to_rgb(h))
    x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047
    y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
    z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116

    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def ciede2000(lab1, lab2):
    """Colour difference, CIEDE2000 (Sharma, Wu and Dalal 2005). About 1 is just visible; 5 is clearly different."""
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    cbar = (math.hypot(a1, b1) + math.hypot(a2, b2)) / 2
    g = 0.5 * (1 - math.sqrt(cbar ** 7 / (cbar ** 7 + 25 ** 7)))
    a1p, a2p = (1 + g) * a1, (1 + g) * a2
    c1p, c2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if c1p else 0.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if c2p else 0.0
    dL, dC = L2 - L1, c2p - c1p
    if c1p * c2p == 0:
        dh = 0.0
    else:
        dh = h2p - h1p
        if dh > 180:
            dh -= 360
        elif dh < -180:
            dh += 360
    dH = 2 * math.sqrt(c1p * c2p) * math.sin(math.radians(dh) / 2)
    Lbar, Cbar = (L1 + L2) / 2, (c1p + c2p) / 2
    if c1p * c2p == 0:
        hbar = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbar = (h1p + h2p) / 2
    else:
        hbar = (h1p + h2p + 360) / 2 if h1p + h2p < 360 else (h1p + h2p - 360) / 2
    t = (1 - 0.17 * math.cos(math.radians(hbar - 30)) + 0.24 * math.cos(math.radians(2 * hbar))
         + 0.32 * math.cos(math.radians(3 * hbar + 6)) - 0.20 * math.cos(math.radians(4 * hbar - 63)))
    sl = 1 + 0.015 * (Lbar - 50) ** 2 / math.sqrt(20 + (Lbar - 50) ** 2)
    sc = 1 + 0.045 * Cbar
    sh = 1 + 0.015 * Cbar * t
    rt = (-math.sin(math.radians(60 * math.exp(-((hbar - 275) / 25) ** 2)))
          * 2 * math.sqrt(Cbar ** 7 / (Cbar ** 7 + 25 ** 7)))
    return math.sqrt((dL / sl) ** 2 + (dC / sc) ** 2 + (dH / sh) ** 2 + rt * (dC / sc) * (dH / sh))


def delta_e(h1, h2):
    return ciede2000(hex_to_lab(h1), hex_to_lab(h2))


def chroma_hue(h):
    _, a, b = hex_to_lab(h)
    return math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def is_red(h):
    """A saturated colour in the hue range of the kit's reds: what hard rule 2 means by 'a red'."""
    c, hue = chroma_hue(h)
    return c >= 35 and (hue <= 45 or hue >= 355)


def luminance(h):
    r, g, b = (_linear(c) for c in hex_to_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(h1, h2):
    a, b = sorted((luminance(h1), luminance(h2)), reverse=True)
    return (a + 0.05) / (b + 0.05)


# ------------------------------------------------------------------ the kit

class Kit:
    """The colours and fonts in tokens.json, indexed for lookup."""

    def __init__(self, tokens):
        self.version = tokens.get("version", "?")
        self._cache = {}
        self.names = {}          # 'A32035' -> token name (first name wins: core names before data names)
        self.rules = {r["id"]: n for n, r in enumerate(tokens["rules"]["hard"], 1)}
        color, data, status = tokens["color"], tokens["data"], tokens.get("status", {})

        def add(h, name):
            n = norm_hex(h) if isinstance(h, str) and h.startswith("#") else None
            if n:
                self.names.setdefault(n[0], name)

        for k, v in color.items():
            add(v, k)
        for c in data["categorical"]:
            add(c["fill"], f"cat-{c['slot']}")
            add(c["ink"], f"cat-{c['slot']}-ink")
            add(c["tint"], f"cat-{c['slot']}-tint")
            add(c.get("fill-dark", ""), f"cat-{c['slot']} (dark mode)")
        for k, v in data.get("other", {}).items():
            add(v, "cat-other" if k == "fill" else f"cat-other-{k}")
        short = {"severity": "sev", "blue-sequential": "seq-blue", "diverging-7": "div"}
        for scale, vals in data.items():
            if isinstance(vals, list) and vals and isinstance(vals[0], str):
                for n, h in enumerate(vals, 1):
                    add(h, f"{short.get(scale, scale)}-{n}")
        for k, v in data.get("chrome", {}).items():
            add(v, f"chart {k}")
        for k, v in status.items():
            if isinstance(v, dict):
                for kk, vv in v.items():
                    if isinstance(vv, dict):
                        for kkk, vvv in vv.items():
                            add(vvv, f"status {k} {kk} {kkk}")
                    else:
                        add(vv, f"status {k} {kk}")
        for k, v in tokens.get("color-dark", {}).items():
            add(v, f"{k} (dark mode)")
        self.slots = {k: norm_hex(v)[0] for k, v in tokens["theme"]["slots"].items()}
        for k, v in tokens["theme"]["slots"].items():
            add(v, f"theme {k}")
        for v in tokens["theme"].get("custom-swatches", []):
            add(v, "custom swatch")
        self.lab = {h: hex_to_lab(h) for h in self.names}
        # Near-misses are judged against the light values; a dark-mode value counts only when matched exactly.
        self.light = [h for h, n in self.names.items() if "(dark mode)" not in n]
        self.primary = norm_hex(color["primary"])[0]
        self.text = norm_hex(color["text"])[0]
        self.gray = norm_hex(color["gray"])[0]
        self.reds = [h for h, n in self.names.items() if is_red(h) and "(dark mode)" not in n]
        self.cat_fills = [norm_hex(c["fill"])[0] for c in data["categorical"]]
        # Old or foreign values: hex -> (kind, token to use or None, what it is)
        self.special = {}
        for old, new in tokens.get("replaced", {}).items():
            if old.startswith("#"):
                self.special[norm_hex(old)[0]] = ("replaced", new, "a kit 1.x value")
        for k, v in tokens.get("avoid", {}).items():
            if k != "note":
                h = norm_hex(v)[0]
                use = "link" if "link" in k else ("primary" if is_red(h) else None)
                self.special[h] = ("avoid", use, "a tool default the kit says to avoid (" + k.replace("-", " ") + ")")
        for k, v in tokens.get("not-airi", {}).items():
            if k != "note":
                self.special[norm_hex(v)[0]] = ("other-mark", "primary", "the red of another mark (" + k.replace("-", " ") + ")")
        self.hex_of = {name: h for h, name in self.names.items()}
        for k, v in color.items():
            self.hex_of[k] = norm_hex(v)[0]
        self.deprecated = {k: v for k, v in tokens.get("deprecated", {}).items() if k != "note"}
        fam = tokens["typography"]
        self.sans = [f.strip().strip("'\"").lower() for f in fam["family"].split(",")]
        self.mono = [f.strip().strip("'\"").lower() for f in fam["family-mono"].split(",")]
        self.family, self.family_mono = fam["family"], fam["family-mono"]

    def nearest(self, h, among=None):
        lab = hex_to_lab(h)
        return min(((ciede2000(lab, self.lab[k]), k) for k in (among or self.light)), default=(999.0, None))

    def classify(self, h, alpha=1.0, near=NEAR, in_logo=False):
        """Sort one colour. Returns a dict: kind, group, use (token name), use_hex, delta, rule, note."""
        key = (h, alpha < 1, near, in_logo)
        if key not in self._cache:
            self._cache[key] = self._classify(h, alpha, near, in_logo)
        return self._cache[key]

    def _classify(self, h, alpha, near, in_logo):
        out = {"kind": "token", "group": "ok", "use": None, "use_hex": None, "delta": 0.0, "rule": None, "note": ""}

        def to(kind, group, use=None, delta=None, rule=None, note=""):
            out.update(kind=kind, group=group, use=use, use_hex=self.hex_of.get(use) if use else None,
                       delta=delta, rule=rule, note=note)
            return out

        if alpha < 1 and h in ("000000", "FFFFFF"):
            return to("overlay", "ok", note="a see-through black or white, used for shadows and overlays")
        if h == self.primary and alpha < 1:
            return to("red-opacity", "drift", "red-tint", note="AIRI red made see-through; the kit has red-tint and red-wash for pale red")
        if h in self.special:
            kind, use, what = self.special[h]
            if kind == "other-mark":
                if in_logo:
                    return to(kind, "info", note=what + ", inside a logo file, where it belongs")
                return to(kind, "must", use, delta_e(h, self.primary), "red", what + "; it stays inside that logo")
            if kind == "avoid" and is_red(h):
                return to(kind, "must", use, delta_e(h, self.primary), "red", what)
            return to(kind, "drift", use, None, None, what)
        if h in self.names:
            out["use"] = self.names[h]
            return out
        if h == "000000":
            return to("black", "drift", "text", delta_e(h, self.text), note="pure black; the kit's ink is softer")
        d, k = self.nearest(h)
        if is_red(h):
            dr, kr = self.nearest(h, self.reds)
            if dr < near:
                return to("near-red", "must", self.names[kr], dr, "red", "a near-miss of a kit red")
            return to("foreign-red", "must", self.names[kr], dr, "red", "a red from outside the kit; the closest kit red is shown")
        if d < near:
            return to("near", "drift", self.names[k], d, note="a near-miss of a kit colour")
        return to("off-kit", "decision", self.names[k], d, note="no close kit colour")


def load_kit(path=None):
    path = Path(path) if path else SKILL_DIR / "tokens.json"
    return Kit(json.loads(path.read_text(encoding="utf-8")))


# ------------------------------------------------------------------ finding colours and fonts in text

HEX_RE = re.compile(r"(?<![\w&/#])#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})(?![\w-])")
RGB_RE = re.compile(r"rgba?\(\s*(\d{1,3})\s*[, ]\s*(\d{1,3})\s*[, ]\s*(\d{1,3})\s*(?:[,/]\s*([\d.]+%?)\s*)?\)", re.I)
HSL_RE = re.compile(r"hsla?\(\s*([\d.]+)(?:deg)?\s*[, ]\s*([\d.]+)%\s*[, ]\s*([\d.]+)%\s*(?:[,/]\s*([\d.]+%?)\s*)?\)", re.I)
NAMED = {"red": "FF0000", "darkred": "8B0000", "crimson": "DC143C", "firebrick": "B22222", "maroon": "800000",
         "tomato": "FF6347", "blue": "0000FF", "navy": "000080", "royalblue": "4169E1", "dodgerblue": "1E90FF",
         "steelblue": "4682B4", "green": "008000", "orange": "FFA500", "yellow": "FFFF00", "gold": "FFD700",
         "purple": "800080", "pink": "FFC0CB", "teal": "008080", "gray": "808080", "grey": "808080",
         "lightgray": "D3D3D3", "lightgrey": "D3D3D3", "darkgray": "A9A9A9", "darkgrey": "A9A9A9",
         "dimgray": "696969", "dimgrey": "696969", "silver": "C0C0C0", "gainsboro": "DCDCDC",
         "whitesmoke": "F5F5F5", "black": "000000", "white": "FFFFFF"}
NAMED_RE = re.compile(
    r"(?<![\w-])(?:color|colour|background|background-color|backgroundColor|border(?:-[a-z]+)*|borderColor|fill|stroke"
    r"|outline(?:-color)?|stop-color|facecolor|edgecolor)[\"']?\s*[:=,]\s*[\"']?\s*(?:[\w.]+\s+){0,3}?("
    + "|".join(sorted(NAMED, key=len, reverse=True)) + r")(?![\w(-])", re.I)
NAMED_HINT = ("color", "colour", "background", "border", "fill", "stroke", "outline")
NOT_A_COLOUR = re.compile(r"(?:href|url|querySelector(?:All)?|select(?:All)?|getElementById|closest|matches|\$|for"
                          r"|data-[\w-]+|aria-[\w-]+|to|id|action|src)\s*[=(:]\s*[\"'(]*\s*$", re.I)
DEFINES = re.compile(r"(?:(--[\w-]+|[$@][A-Za-z_][\w-]*)\s*:\s*|([A-Za-z_][\w.]*)\s*=\s*[\"']|[\"']?([A-Za-z_][\w-]*)[\"']?\s*:\s*[\"'])$")
STYLE_PROP = re.compile(r"(?:^|[.\-_])(?:colou?r|fill|stroke|background|bg|border|outline|shadow|style|value|hex|stop)\w*$"
                        r"|(?:Style|Color|Colour)$", re.I)
FONT_KEY = re.compile(r"(font-family|fontFamily|font_family|font\.family|font\.sans-serif|fontFace|base_family"
                      r"|(?<![\w.-])family(?=\s*=\s*[\"'])"
                      r"|\\set(?:main|sans|mono)font)([\"']?\]?\s*[:=,]\s*|\s*\(\s*|\s*\{)", re.I)
GFONT = re.compile(r"fonts\.googleapis\.com/css2?\?([^\"')\s>]+)")
GENERIC = {"sans-serif", "serif", "monospace", "system-ui", "ui-sans-serif", "ui-serif", "ui-monospace", "cursive",
           "fantasy", "-apple-system", "blinkmacsystemfont", "emoji", "math"}
EMOJI = {"apple color emoji", "segoe ui emoji", "segoe ui symbol", "noto color emoji"}
MONO_HINT = re.compile(r"mono|courier|consol|menlo|monaco|code|terminal|typewriter", re.I)
ICON_HINT = re.compile(r"icon|awesome|glyph|symbol|dings\b|dingbat|katex|mathjax|math|fontello|icomoon", re.I)
CAT_WORDS = re.compile(r"domain|categor|palette|series|scheme|colou?r_?(?:map|scale|way)|colou?rs\b|cluster|sector"
                       r"|scaleOrdinal|scale_(?:fill|colou?r)_manual|legend", re.I)
CUSTOM_PROP = re.compile(r"^\s*--[\w-]+\s*:")
CAT_CSS = re.compile(r"--(?:[\w-]*-)?(?:cat|category|categories|domain|series|chart|viz|group|sector)s?(?:-[\w-]*)?\s*:", re.I)


class Scan:
    """Everything found, before it is sorted into groups."""

    def __init__(self):
        self.colours = []     # dicts: file, loc, line, hex, alpha, raw, name, text_use, in_logo, palette
        self.fonts = []       # dicts: file, loc, stack (list of names as written)
        self.extra = []       # ready-made findings: contrast, theme slots, deprecated names, logos
        self.palettes = []    # dicts: file, loc, kind ('category' or 'scale'), colours
        self.files = 0
        self.skipped = defaultdict(int)
        self.long_lines = 0


def colours_in_line(line, strict):
    """Yield (start, hex, alpha, raw) for every colour value written on one line."""
    for m in HEX_RE.finditer(line):
        body = m.group(1)
        before, after = line[:m.start()], line[m.end():]
        if len(body) in (3, 4):
            quoted = before[-1:] in "\"'" and after[:1] in "\"'"
            if strict and not quoted:
                continue
            if after.lstrip()[:1] == "{" or NOT_A_COLOUR.search(before[-40:]):
                continue
            if after.rstrip().endswith("{") or (not before and after.rstrip().endswith(",")):
                continue                      # a CSS id selector
        elif NOT_A_COLOUR.search(before[-40:]):
            continue
        h, a = norm_hex(body)
        yield m.start(), h, a, m.group(0)
    for m in RGB_RE.finditer(line):
        r, g, b = (int(x) for x in m.group(1, 2, 3))
        if max(r, g, b) > 255:
            continue
        yield m.start(), f"{r:02X}{g:02X}{b:02X}", _alpha(m.group(4)), m.group(0)
    for m in HSL_RE.finditer(line):
        hh, s, l = float(m.group(1)), float(m.group(2)), float(m.group(3))
        if s > 100 or l > 100:
            continue
        r, g, b = colorsys.hls_to_rgb((hh % 360) / 360, l / 100, s / 100)
        yield m.start(), f"{round(r * 255):02X}{round(g * 255):02X}{round(b * 255):02X}", _alpha(m.group(4)), m.group(0)
    for m in NAMED_RE.finditer(line):
        yield m.start(1), NAMED[m.group(1).lower()], 1.0, m.group(1).lower()


def _alpha(s):
    if not s:
        return 1.0
    try:
        return min(1.0, float(s[:-1]) / 100 if s.endswith("%") else float(s))
    except ValueError:
        return 1.0


def font_stacks_in_line(line):
    """Yield a list of family names for each font declaration on the line."""
    for m in GFONT.finditer(line):
        for fam in re.findall(r"family=([^&:;]+)", m.group(1)):
            yield [fam.replace("+", " ")]
    for m in FONT_KEY.finditer(line):
        key, rest = m.group(1), line[m.end():].strip()
        css_key = key.lower() == "font-family" and ":" in m.group(2) and "'" not in m.group(2) and '"' not in m.group(2)
        if rest.startswith(("var(", "$", "@", "inherit", "initial", "unset", "revert", "{")):
            continue
        if not css_key and not rest.startswith(("'", '"', "[", "c(", "(", "{")) and not key.startswith("\\"):
            continue                          # a variable, not a font name
        rest = re.split(r";|\}|!important|\bvar\(|</|/>|\s/\*", rest)[0]
        if css_key:                           # style="font-family: Inter" class="..."
            rest = re.split(r"\"\s*/?>|\"\s+[\w:-]+=|\"\s*$", rest)[0]
        if not css_key:
            # keep only what is inside quotes: fontFamily: "Inter, sans-serif", size: 12
            quoted = re.match(r"""[\[(c{\s]*((?:(?:"[^"]*"|'[^']*')\s*,?\s*)+)""", rest)
            if quoted:
                rest = quoted.group(1)
            elif key.startswith("\\"):
                rest = rest.split("}")[0]
            else:
                continue
        names = [n.strip().strip("\"'`[](){}\\ ").strip() for n in rest.split(",")]
        names = [n for n in names if n and re.fullmatch(r"[A-Za-z0-9 _+.\-]{2,40}", n) and not n.isdigit()]
        if names:
            yield names


def scan_lines(scan, rel, lines, ext, loc_of=lambda n: n):
    """Find colours and fonts in a list of text lines. Returns this file's colour occurrences."""
    strict = ext in STRICT_EXT
    in_logo = "logo" in rel.lower()
    found = []
    for n, line in enumerate(lines, 1):
        if len(line) > MAX_LINE:
            scan.long_lines += 1
            continue
        low = line.lower()
        if "#" in line or "rgb" in low or "hsl" in low or any(w in low for w in NAMED_HINT):
            for start, h, alpha, raw in colours_in_line(line, strict):
                before = line[:start]
                d = DEFINES.search(before)
                prop = re.search(r"(?<![\w-])([\w-]+)\s*:\s*$", before)
                found.append({"file": rel, "loc": loc_of(n), "line": n, "hex": h, "alpha": alpha, "raw": raw,
                              "name": next((g for g in d.groups() if g and len(g) > 2 and not STYLE_PROP.search(g)), None) if d else None,
                              "prop": next((g for g in d.groups() if g), None) if d else None,
                              "text_use": bool(prop and prop.group(1).lower() == "color"),
                              "in_logo": in_logo, "palette": None, "context": line.strip()[:160]})
        if "font" in low or "family" in low:
            for stack in font_stacks_in_line(line):
                scan.fonts.append({"file": rel, "loc": loc_of(n), "stack": stack})
        if "var(--" in line or "--" in line:
            for m in re.finditer(r"var\(\s*--([\w-]+)", line):
                scan.extra.append({"kind": "var", "name": m.group(1), "file": rel, "loc": loc_of(n)})
    find_palettes(scan, rel, lines, found, ext)
    scan.colours.extend(found)
    return found


def hue_bins(hexes):
    """How many clearly different hues a set of colours has (30 degree bins, greys ignored)."""
    bins = set()
    for h in hexes:
        c, hue = chroma_hue(h)
        if c >= 18:
            bins.add(int(((hue + 15) % 360) // 30))
    return len(bins)


def find_palettes(scan, rel, lines, found, ext):
    """Mark runs of colours that look like a category palette or a colour scale.

    A category palette is four or more colours of four or more different hues, written
    together, with a sign that they are meant as a set: all on one line, or words such
    as 'domain', 'category', 'palette' or 'series' on or just above the run.
    """
    if not found:
        return
    per_line = defaultdict(set)
    for o in found:
        per_line[o["line"]].add(o["hex"])
    lists = {n for n, v in per_line.items() if len(v) >= 4}      # a whole palette written on one line
    runs, run = [[o for o in found if o["line"] == n] for n in sorted(lists)], []
    for occ in found:
        if occ["line"] in lists:
            continue
        if run and occ["line"] - run[-1]["line"] > 2:
            runs.append(run)
            run = []
        run.append(occ)
    if run:
        runs.append(run)
    for run in runs:
        distinct = list(dict.fromkeys(o["hex"] for o in run))
        if len(distinct) < 4:
            continue
        first, last = run[0]["line"], run[-1]["line"]
        nearby = "\n".join(l for l in lines[max(0, first - 3):last] if len(l) <= MAX_LINE)
        by_line = defaultdict(list)
        for o in run:
            by_line[o["line"]].append(o["hex"])
        together = any(len(set(v)) >= 4 for v in by_line.values())
        together_hues = any(len(set(v)) >= 4 and hue_bins(v) >= 4 for v in by_line.values())
        signal = bool(CAT_CSS.search(nearby)) or (ext not in CSS_EXT and bool(CAT_WORDS.search(nearby)))
        # The same variable given a different hue in rule after rule is one colour per category.
        by_prop = defaultdict(list)
        for o in run:
            if o.get("prop"):
                by_prop[o["prop"]].append(o["hex"])
        signal = signal or any(len(set(v)) >= 4 and hue_bins(v) >= 4 for v in by_prop.values())
        if len(distinct) > MAX_PALETTE and not together:
            continue                          # a whole design system, not a palette
        kind, members = None, run
        ls = [hex_to_lab(h)[0] for h in distinct]
        steps = [b - a for a, b in zip(ls, ls[1:])]
        monotone = all(x > 1 for x in steps) or all(x < -1 for x in steps)
        coloured = sum(chroma_hue(h)[0] >= 18 for h in distinct)
        if monotone and coloured >= 3 and (together or signal) and (hue_bins(distinct) <= 2 or len(distinct) >= 5):
            kind = "scale"                    # steps of one ramp, light to dark or dark to light
        elif hue_bins(distinct) >= 4 and (together_hues or signal):
            kind = "category"
            # A block of CSS variables holds a whole theme; only the lines named as data colours are the palette.
            def is_member(o):
                line = lines[o["line"] - 1]
                return not CUSTOM_PROP.search(line) or bool(CAT_CSS.search(line))
            members = [o for o in run if is_member(o)]
            if len({o["hex"] for o in members}) < 4:
                kind = None
        if kind:
            pal = {"file": rel, "loc": members[0]["loc"], "kind": kind,
                   "colours": list(dict.fromkeys(o["hex"] for o in members))}
            scan.palettes.append(pal)
            for o in members:
                o["palette"] = pal


STYLE_BLOCK = re.compile(r"\{([^{}]{0,1500})\}|style\s*=\s*\"([^\"]{0,600})\"")
COLOUR_VALUE = r"(#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\))"
FG = re.compile(r"(?<![\w-])color\s*:\s*" + COLOUR_VALUE, re.I)
BG = re.compile(r"(?<![\w-])background(?:-color)?\s*:\s*" + COLOUR_VALUE, re.I)


def find_contrast(scan, rel, text):
    """Rule 4, where it can be checked: a text colour and a background set in the same style block."""
    for m in STYLE_BLOCK.finditer(text):
        block = m.group(1) or m.group(2) or ""
        fg, bg = FG.search(block), BG.search(block)
        if not (fg and bg):
            continue
        a = next(colours_in_line("c: " + fg.group(1), False), None)
        b = next(colours_in_line("c: " + bg.group(1), False), None)
        if not a or not b or a[2] < 1 or b[2] < 1:
            continue
        ratio = contrast(a[1], b[1])
        if ratio < 4.5:
            scan.extra.append({"kind": "contrast", "fg": a[1], "bg": b[1], "ratio": round(ratio, 2), "file": rel,
                               "loc": text.count("\n", 0, m.start(1 if m.group(1) else 2) + fg.start()) + 1})


def scan_text_file(scan, path, rel):
    ext = path.suffix.lower()
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        scan.skipped["unreadable"] += 1
        return
    scan.files += 1
    if ext == ".ipynb":
        try:
            cells = json.loads(text).get("cells", [])
        except (ValueError, AttributeError):
            scan.skipped["unreadable"] += 1
            return
        for i, cell in enumerate(cells, 1):
            src = cell.get("source", [])
            lines = src if isinstance(src, list) else str(src).split("\n")
            scan_lines(scan, rel, [str(l).rstrip("\n") for l in lines], ext, lambda n, i=i: f"cell {i}, line {n}")
        return
    scan_lines(scan, rel, text.split("\n"), ext)
    if ext in CSS_EXT | {".html", ".htm", ".vue", ".svelte"}:
        find_contrast(scan, rel, text)


# ------------------------------------------------------------------ Office files

OFFICE_COLOUR = re.compile(r"<a:srgbClr val=\"([0-9A-Fa-f]{6})\"|<w:color [^>]*?w:val=\"([0-9A-Fa-f]{6})\""
                           r"|\bw:(?:fill|color)=\"([0-9A-Fa-f]{6})\"|\brgb=\"[0-9A-Fa-f]{2}([0-9A-Fa-f]{6})\"")
OFFICE_FONT = re.compile(r"<a:latin typeface=\"([^\"]+)\"|w:rFonts[^>]*?w:ascii=\"([^\"]+)\"|<(?:name|rFont) val=\"([^\"]+)\"")
SLOT_TAGS = {"dk1": "dark1", "lt1": "light1", "dk2": "dark2", "lt2": "light2", "hlink": "hyperlink",
             "folHlink": "followed-hyperlink", **{f"accent{i}": f"accent{i}" for i in range(1, 7)}}
PART_WANTED = re.compile(r"^(ppt/(slides|slideLayouts|slideMasters|theme|charts|notesSlides)/[^/]+\.xml"
                         r"|word/(document|styles|header\d*|footer\d*|footnotes|theme/[^/]+|charts/[^/]+)\.xml"
                         r"|xl/(styles|theme/[^/]+|charts/[^/]+|drawings/[^/]+)\.xml)$")


def part_label(name):
    m = re.search(r"/(slide|slideLayout|slideMaster|notesSlide|theme|chart|drawing|header|footer)(\d*)\.xml$", name)
    words = {"slide": "slide", "slideLayout": "layout", "slideMaster": "master", "notesSlide": "notes", "theme": "theme",
             "chart": "chart", "drawing": "drawing", "header": "header", "footer": "footer"}
    if m:
        return (words[m.group(1)] + " " + m.group(2)).strip()
    return {"word/document.xml": "body text", "word/styles.xml": "styles", "word/footnotes.xml": "footnotes",
            "xl/styles.xml": "cell styles"}.get(name, name)


def scan_office_file(scan, kit, path, rel):
    try:
        z = zipfile.ZipFile(path)
    except (zipfile.BadZipFile, OSError):
        scan.skipped["unreadable"] += 1
        return
    scan.files += 1
    in_logo = False
    with z:
        names = [i for i in z.infolist() if PART_WANTED.match(i.filename) and i.file_size < 30_000_000]

        def order(i):
            m = re.search(r"(\d+)\.xml$", i.filename)
            return (re.sub(r"\d+\.xml$", "", i.filename), int(m.group(1)) if m else 0)

        for info in sorted(names, key=order):
            try:
                xml = z.read(info).decode("utf-8", errors="replace")
            except (OSError, RuntimeError, zipfile.BadZipFile):
                continue
            label = part_label(info.filename)
            xml = re.sub(r"<(indexedColors|mruColors)>.*?</\1>", "", xml, flags=re.S)   # Excel's own swatch lists
            if "/theme/" in info.filename:
                scheme = re.search(r"<a:clrScheme.*?</a:clrScheme>", xml, re.S)
                wrong = []
                for tag, slot in SLOT_TAGS.items():
                    m = scheme and re.search(rf"<a:{tag}>\s*<a:(?:srgbClr val|sysClr [^>]*?lastClr)=\"([0-9A-Fa-f]{{6}})\"", scheme.group(0))
                    if m and m.group(1).upper() != kit.slots[slot]:
                        wrong.append({"slot": slot, "found": m.group(1).upper(), "kit": kit.slots[slot]})
                if wrong and "theme1" in info.filename:
                    scan.extra.append({"kind": "theme", "file": rel, "loc": label, "wrong": wrong})
                fonts = re.search(r"<a:fontScheme.*?</a:fontScheme>", xml, re.S)
                for role in ("majorFont", "minorFont"):
                    m = fonts and re.search(rf"<a:{role}>\s*<a:latin typeface=\"([^\"]*)\"", fonts.group(0))
                    if m and m.group(1) and "theme1" in info.filename:
                        scan.fonts.append({"file": rel, "loc": f"theme {'heading' if role == 'majorFont' else 'body'} font",
                                           "stack": [m.group(1)]})
                continue
            found = []
            for m in OFFICE_COLOUR.finditer(xml):
                h = next(g for g in m.groups() if g).upper()
                found.append({"file": rel, "loc": label, "line": 1, "hex": h, "alpha": 1.0, "raw": "#" + h, "name": None,
                              "text_use": False, "in_logo": in_logo, "palette": None, "context": ""})
            for m in OFFICE_FONT.finditer(xml):
                face = next(g for g in m.groups() if g)
                if not face.startswith("+") and face.strip():
                    scan.fonts.append({"file": rel, "loc": label, "stack": [face]})
            if "/charts/" in info.filename:
                distinct = list(dict.fromkeys(o["hex"] for o in found))
                if len(distinct) >= 4 and hue_bins(distinct) >= 4:
                    pal = {"file": rel, "loc": label, "kind": "category", "colours": distinct}
                    scan.palettes.append(pal)
                    for o in found:
                        o["palette"] = pal
            scan.colours.extend(found)


# ------------------------------------------------------------------ walking the paths

def walk(paths, skipped, exclude=()):
    """Yield (path, display name) for every file worth a look, counting what is skipped."""
    for root in paths:
        root = Path(root)
        if root.is_file():
            yield root, root.name
            continue
        stack = [root]
        while stack:
            folder = stack.pop()
            try:
                entries = sorted(folder.iterdir(), reverse=True)
            except OSError:
                continue
            files = []
            for p in entries:
                if p.is_symlink():
                    continue
                rel = p.relative_to(root).as_posix()
                if any(fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(p.name, pat) for pat in exclude):
                    skipped["excluded with --exclude"] += 1
                    continue
                if p.is_dir():
                    if p.name in SKIP_DIRS or p.name.startswith("."):
                        skipped["vendor, build or hidden folders"] += 1
                    else:
                        stack.append(p)
                    continue
                ext = p.suffix.lower()
                if ext not in TEXT_EXT and ext not in OFFICE_EXT and ext != ".png":
                    continue
                if p.name in SKIP_NAMES or MINIFIED.search(p.name.lower()) or p.name.startswith("~$"):
                    skipped["minified or generated files"] += 1
                    continue
                files.append(p)
            for p in reversed(files):
                rel = p.relative_to(root).as_posix()
                yield p, (f"{root.name}/{rel}" if len(paths) > 1 else rel)


def logo_hashes():
    out = set()
    logos = SKILL_DIR / "logos"
    if logos.is_dir():
        out = {hashlib.sha256(p.read_bytes()).hexdigest() for p in logos.rglob("*") if p.is_file()}
    return out


def run_scan(paths, kit, exclude=()):
    scan = Scan()
    known_logos = logo_hashes()
    for path, rel in walk(paths, scan.skipped, exclude):
        ext = path.suffix.lower()
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if ext in (".svg", ".png") and "logo" in path.name.lower() and size < 5_000_000 and known_logos:
            try:
                if hashlib.sha256(path.read_bytes()).hexdigest() not in known_logos:
                    scan.extra.append({"kind": "logo", "file": rel, "loc": ""})
            except OSError:
                pass
        if ext == ".png":
            continue
        if ext in OFFICE_EXT:
            scan_office_file(scan, kit, path, rel)
        elif size > MAX_BYTES:
            scan.skipped["large files (data, not styling)"] += 1
        else:
            scan_text_file(scan, path, rel)
    return scan


# ------------------------------------------------------------------ sorting into findings

def font_verdict(kit, stack):
    """(group, kind, key) for one font stack."""
    low = [s.lower() for s in stack]
    real = [s for s in low if s not in GENERIC and s not in EMOJI]
    first = real[0] if real else (low[0] if low else "")
    if ICON_HINT.search(first):
        return "info", "icon-font", stack[0]
    if first.startswith("figtree "):          # Office lists each weight as its own font: "Figtree Medium"
        return "drift", "weight", stack[0]
    if low[-1:] == ["monospace"] or (real and MONO_HINT.search(first)):
        return ("ok", "mono", "") if low == kit.mono else ("drift", "mono", ", ".join(stack))
    if first == "figtree":
        rest = [s for s in low if s != "figtree"]
        return ("ok", "sans", "") if rest in ([], kit.sans[1:], kit.sans[2:]) else ("drift", "fallbacks", ", ".join(stack))
    if not real:
        return "must", "no-figtree", ", ".join(stack)
    return "must", "other-font", next(s for s in stack if s.lower() == first)


def places(occs, per=3):
    """'a.css:3, :9, :40 (+2 more); b.html:7' -- examples of where, capped."""
    by_file = defaultdict(list)
    for o in occs:
        by_file[o["file"]].append(o["loc"])
    bits = []
    for f, locs in list(by_file.items())[:per]:
        locs = [x for x in dict.fromkeys(locs) if x != ""]
        shown = locs[:per]
        if not shown:
            s = f
        elif all(isinstance(x, int) for x in shown):
            s = f + ":" + ", :".join(str(x) for x in shown)
        else:
            s = f + " (" + ", ".join(str(x) for x in shown) + ")"
        if len(locs) > per:
            s += f" (+{len(locs) - per} more)"
        bits.append(s)
    if len(by_file) > per:
        bits.append(f"and {len(by_file) - per} more file{'s' if len(by_file) - per > 1 else ''}")
    return "; ".join(bits)


FONT_NOTES = {"other-font": "not Figtree", "no-figtree": "a generic family with no Figtree in front",
              "fallbacks": "Figtree first, with fallbacks other than the kit's",
              "weight": "Figtree in a weight the kit does not use; the kit uses regular and bold (semibold on the web only)",
              "mono": "a monospace stack other than the kit's; fine for code, but the kit has one",
              "icon-font": "an icon or maths font; not text, so rule 3 does not cover it"}


def finding(group, kind, value, occs, note, use=None, use_hex=None, delta=None, rule=None, **more):
    """One line of the report: a value, where it is, and what the kit offers instead."""
    by_file = defaultdict(int)
    for o in occs:
        by_file[o["file"]] += 1
    return {"group": group, "kind": kind, "rule": rule, "value": value, "use": use,
            "use_hex": "#" + use_hex if use_hex else None, "delta_e": round(delta, 1) if delta is not None else None,
            "note": note, "count": len(occs), "files": len(by_file), "places": places(occs), "by_file": dict(by_file),
            "examples": [{"file": o["file"], "loc": o["loc"], "context": o.get("context", "")} for o in occs[:8]], **more}


def build_findings(scan, kit, near=NEAR, include_categories=False):
    """Turn raw occurrences into a list of findings, each with a group, a count and examples."""
    findings, on_kit, overlays, cat_hidden = [], 0, 0, 0
    groups = defaultdict(list)
    in_category = {o["hex"] for o in scan.colours if o["palette"] and o["palette"]["kind"] == "category"}
    for o in scan.colours:
        pal = o["palette"]
        v = kit.classify(o["hex"], o["alpha"], near, o["in_logo"])
        if pal and pal["kind"] == "category" and not include_categories:
            # A near-copy of AIRI red inside a palette is still the brand red, typed wrong; everything else is left alone.
            if not (v["group"] == "must" and v["kind"] != "foreign-red" and v["use"] == "primary"):
                cat_hidden += v["kind"] != "token"
                on_kit += v["kind"] == "token"
                continue
        if pal and pal["kind"] == "scale" and v["kind"] in ("off-kit", "near", "foreign-red"):
            continue                          # judged as a whole scale below, not step by step
        if v["kind"] == "token":
            on_kit += 1
            if o["hex"] == kit.gray and o["text_use"]:
                groups[("gray-text", o["hex"])].append(o)
        elif v["kind"] == "overlay":
            overlays += 1
        else:
            groups[(v["kind"], o["hex"])].append(o)
    for (kind, h), occs in groups.items():
        names = list(dict.fromkeys(o["name"] for o in occs if o["name"]))[:3]
        more = {"defined_as": names, "in_scale": any(o["palette"] for o in occs),
                "also_in_palette": h in in_category and not include_categories}
        if kind == "gray-text":
            findings.append(finding("drift", kind, "#" + h, occs, "kit grey used as a text colour; it is for graphics, and fails contrast as small text",
                                    "text-muted", kit.hex_of["text-muted"], **more))
            continue
        v = kit.classify(h, occs[0]["alpha"], near, occs[0]["in_logo"])
        findings.append(finding(v["group"], kind, "#" + h, occs, v["note"], v["use"], v["use_hex"], v["delta"], v["rule"], **more))
    # fonts
    fgroups, fonts_ok = defaultdict(list), 0
    for f in scan.fonts:
        group, kind, key = font_verdict(kit, f["stack"])
        if group == "ok":
            fonts_ok += 1
        else:
            fgroups[(group, kind, key.lower())].append({**f, "key": key})
    for (group, kind, _), occs in fgroups.items():
        findings.append(finding(group, "font-" + kind, occs[0]["key"], occs, FONT_NOTES[kind],
                                kit.family_mono if kind == "mono" else kit.family, rule="font" if group == "must" else None))
    # contrast, old names, logo files, Office themes
    extra = defaultdict(list)
    for e in scan.extra:
        if e["kind"] == "contrast":
            extra[("contrast", e["fg"], e["bg"])].append(e)
        elif e["kind"] == "var" and e["name"] in kit.deprecated:
            extra[("deprecated", e["name"])].append(e)
        elif e["kind"] == "var" and e["name"] in ("font-size-lg", "font-size-xl", "font-size-2xl"):
            extra[("resized", e["name"])].append(e)
        elif e["kind"] == "logo":
            extra[("logo",)].append(e)
        elif e["kind"] == "theme":
            extra[("theme", tuple((w["slot"], w["found"]) for w in e["wrong"]))].append(e)
    for key, occs in extra.items():
        if key[0] == "contrast":
            ratio = occs[0]["ratio"]
            note = (f"contrast {ratio}:1; fails even for large text" if ratio < 3
                    else f"contrast {ratio}:1; passes only for large text (24 px, or 19 px bold)")
            findings.append(finding("must", "contrast", f"#{key[1]} on #{key[2]}", occs, note, rule="contrast", ratio=ratio))
        elif key[0] == "deprecated":
            new = kit.deprecated[key[1]]
            findings.append(finding("drift", "old-name", f"--{key[1]}", occs, "a kit 1.x variable name; it still works through an alias",
                                    new if new[0].isdigit() else f"--{new}"))
        elif key[0] == "resized":
            findings.append(finding("info", "resized-name", f"--{key[1]}", occs,
                                    "this name gives a larger size in kit 2.0; check the headings that use it"))
        elif key[0] == "logo":
            findings.append(finding("info", "logo-file", "logo files", occs,
                                    "files named 'logo' that are not byte-for-byte a kit logo; check rule 1 by eye (partner logos are fine)"))
        elif key[0] == "theme":
            wrong = occs[0]["wrong"]
            findings.append(finding("drift", "theme", f"theme colours ({len(wrong)} of 12 slots differ from the kit)", occs,
                                    "apply the kit theme (templates/office-theme.md) instead of fixing colours one by one",
                                    "the kit theme", slots=wrong))
    # palettes and scales: one finding per distinct set, however many files repeat it
    sets = defaultdict(list)
    for pal in scan.palettes:
        sets[(pal["kind"], tuple(pal["colours"]))].append(pal)
    for (kind, colours), pals in sets.items():
        if all(h in kit.names for h in colours):
            continue
        shown = " ".join("#" + h for h in colours[:10]) + (f" and {len(colours) - 10} more" if len(colours) > 10 else "")
        off = sum(h not in kit.names for h in colours)
        reds = [h for h in colours if is_red(h) and h not in kit.names]
        if kind == "category" and not include_categories:
            note = f"a category palette of {len(colours)} colours, {off} not in the kit. Left as it is: the kit's category colours are for new work only"
            if reds:
                note += ". It includes a red from outside the kit (" + ", ".join("#" + h for h in reds[:3]) + "); mention it, do not change it"
            findings.append(finding("info", "category-palette", shown, pals, note, colours=["#" + h for h in colours]))
        elif kind == "category":
            findings.append(finding("decision", "category-palette", shown, pals,
                                    f"a category palette of {len(colours)} colours, {off} not in the kit. The kit's slots, in order, are "
                                    + " ".join("#" + h for h in kit.cat_fills) + "; risk domains take the slot BRAND.md gives each",
                                    "cat-1 to cat-7", colours=["#" + h for h in colours]))
        elif kind == "scale":
            red = len(reds) >= 2
            findings.append(finding("must" if red else "decision", "scale", shown, pals,
                                    ("a red scale that is not the kit's" if red else "a colour scale that is not one of the kit's")
                                    + "; judge the whole scale, not each step",
                                    "sev-1 to sev-5" if red else "sev-1 to sev-5 (risk) or seq-blue-1 to seq-blue-7 (amounts)",
                                    rule="red" if red else None, colours=["#" + h for h in colours]))
    order = {"must": 0, "drift": 1, "decision": 2, "info": 3}
    findings.sort(key=lambda f: (order[f["group"]], -f["count"], f["value"]))
    folders = defaultdict(lambda: defaultdict(int))
    for f in findings:
        for name, n in f["by_file"].items():
            folders[name.split("/")[0] + "/" if "/" in name else "(top level)"][f["group"]] += n
    stats = {"files": scan.files, "skipped": dict(scan.skipped), "long_lines_skipped": scan.long_lines,
             "colour_values": len(scan.colours), "distinct_colours": len({o["hex"] for o in scan.colours}),
             "on_kit": on_kit, "overlays": overlays, "in_category_palettes": cat_hidden,
             "font_declarations": len(scan.fonts), "fonts_on_kit": fonts_ok,
             **{g: sum(1 for f in findings if f["group"] == g) for g in order},
             "by_folder": {k: dict(v) for k, v in folders.items()}}
    return findings, stats


# ------------------------------------------------------------------ the report

def line_for(f, kit):
    v = f"`{f['value']}`"
    k = f["kind"]
    where = f"{f['count']} place{'s' if f['count'] != 1 else ''} in {f['files']} file{'s' if f['files'] != 1 else ''}"
    named = f" Defined as `{f['defined_as'][0]}`." if f.get("defined_as") else ""
    de = f", difference {f['delta_e']}" if f["delta_e"] is not None else ""
    use = f"`{f['use']}` `{f['use_hex']}`" if f["use_hex"] else (f"`{f['use']}`" if f["use"] else "")
    if k in ("near-red", "near", "black", "replaced", "avoid", "other-mark", "red-opacity", "gray-text"):
        if not use:
            head = f"{v}: {f['note']}. No kit colour replaces it one for one; pick from the kit"
        else:
            head = f"{v} → {use} ({f['note']}{de})"
    elif k == "foreign-red":
        head = f"{v}: a red from outside the kit. Closest kit red: {use}{de}"
    elif k == "off-kit":
        head = f"{v}: closest kit colour is {use}{de}"
        if f.get("also_in_palette"):
            head += "; also used in a category palette"
    elif k.startswith("font-"):
        head = f"{v}: {f['note']}"
        if k in ("font-other-font", "font-no-figtree", "font-fallbacks", "font-mono"):
            head += f". Kit stack: `{f['use']}`"
    elif k == "contrast":
        head = f"{v}: {f['note']}"
    elif k == "old-name":
        head = f"{v} → `{f['use']}` ({f['note']})"
    elif k == "theme":
        slots = ", ".join(f"{s['slot']} is #{s['found']}, kit #{s['kit']}" for s in f["slots"][:3])
        return f"- {f['value'].capitalize()}: {f['note']}. For example {slots}.\n  - {f['places']}"
    elif k in ("category-palette", "scale"):
        times = f" Appears {f['count']} times in {f['files']} file{'s' if f['files'] != 1 else ''}." if f["count"] > 1 else ""
        kit_scale = f" Kit {'scale' if k == 'scale' else 'colours'}: `{f['use']}`." if f["use"] else ""
        return f"- {v}\n  - {f['note'][0].upper() + f['note'][1:]}.{kit_scale}{times}\n  - {f['places']}"
    else:
        head = f"{v}: {f['note']}"
    return f"- {head}. {where}.{named}\n  - {f['places']}"


def render_markdown(findings, stats, kit, top=20, include_categories=False):
    out = [f"# Brand scan against AIRI kit {kit.version}", ""]
    skipped = ", ".join(f"{n} {k}" for k, n in stats["skipped"].items())
    out.append(f"Read {stats['files']} file{'s' if stats['files'] != 1 else ''}"
               + (f" (skipped {skipped})" if skipped else "") + ". "
               f"Found {stats['colour_values']} colour values, {stats['distinct_colours']} distinct, "
               f"and {stats['font_declarations']} font declarations. "
               f"Already matching the kit: {stats['on_kit']} colour values, {stats['fonts_on_kit']} font declarations.")
    if stats["long_lines_skipped"]:
        out.append(f"Skipped {stats['long_lines_skipped']} very long lines (minified code or embedded data).")
    out.append("")
    out.append("| Group | Findings |\n|---|---|\n" + "\n".join(
        f"| {t} | {stats[g]} |" for g, t in (("must", "Must fix (hard rules)"), ("drift", "Probably drift"),
                                             ("decision", "Needs a decision"), ("info", "For information"))))
    out.append("")
    out.append("A finding is one value, however many places use it. \"Difference\" is a colour distance (CIEDE2000): "
               f"under 1 cannot be seen, under {NEAR:g} is a near-miss.")
    folders = sorted(stats["by_folder"].items(), key=lambda kv: -sum(v for g, v in kv[1].items() if g != "info"))
    if len(folders) > 1:
        out.append("")
        out.append("Where the differences are (places, by top-level folder): " + "; ".join(
            f"`{k}` {sum(v for g, v in d.items() if g != 'info')}" for k, d in folders[:8]
            if sum(v for g, v in d.items() if g != "info")) + ". Use --exclude to leave out folders that are not AIRI's own work, such as saved pages, archives and data.")
    out.append("")
    out.append("This scan only reads. Nothing has been changed. Ask which differences are deliberate before changing any.")
    sections = [
        ("must", "Must fix (hard rules)", "These break a hard rule of the kit. Fix them unless the work is partner-led."),
        ("drift", "Probably drift", "Each is very close to a kit colour, or is an old or default value. The kit value is shown. "
                                    "Propose the change; leave any that a person says are deliberate."),
        ("decision", "Needs a decision", "No kit colour is close. A person decides for each: reuse the closest kit colour, "
                                         "use a neutral (ink or a grey), or keep it and raise the gap with the kit. Do not invent a new colour."),
        ("info", "For information", "Nothing to change here unless a person asks."),
    ]
    rule_names = {"red": "AIRI red", "font": "Figtree", "contrast": "contrast"}
    for group, title, lead in sections:
        items = [f for f in findings if f["group"] == group]
        out += ["", f"## {title}", ""]
        if not items:
            out.append("Nothing found.")
            continue
        out += [lead, ""]
        if group == "must":
            for rule in ("red", "font", "contrast"):
                sub = [f for f in items if f["rule"] == rule]
                if sub:
                    out += [f"**Rule {kit.rules.get(rule, '?')}, {rule_names[rule]}**", ""]
                    out += [line_for(f, kit) for f in sub[:top]]
                    if len(sub) > top:
                        out.append(f"- and {len(sub) - top} more, each used {sub[top]['count']} time{'s' if sub[top]['count'] != 1 else ''} or fewer (see --json or raise --top)")
                    out.append("")
        else:
            out += [line_for(f, kit) for f in items[:top]]
            if len(items) > top:
                rest = items[top:]
                out.append(f"- and {len(rest)} more, each in {rest[0]['count']} place{'s' if rest[0]['count'] != 1 else ''} or fewer "
                           f"({sum(f['count'] for f in rest)} places in all; see --json or raise --top)")
        if group == "info":
            if stats["in_category_palettes"] and not include_categories:
                out += ["", f"{stats['in_category_palettes']} colour values sit in the category palettes above and were not judged. "
                            "The kit's category colours are a default for new work only. Run again with --include-categories only if a person asks to change them."]
    if stats["overlays"]:
        out += ["", f"Ignored: {stats['overlays']} see-through blacks and whites (shadows and overlays)."]
    out += ["", "## What this scan cannot see", "",
            "Check these by eye: the logo files and how they are used (rule 1), colour used as the only signal (rule 5), "
            "what red means in each chart (rule 6), video (rule 7), images and screenshots, colours worked out at run time, "
            "and utility classes such as `text-red-600`. Contrast is checked only where a text colour and a background are set in the same style block."]
    return "\n".join(out) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="brand_scan.py", formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__.split("\n\n", 1)[1],
        usage="brand_scan.py PATH [PATH ...] [--json] [--include-categories] [--exclude GLOB] [--top N] [--near N] [--fail-on-hard]")
    ap.add_argument("paths", nargs="+", metavar="PATH", help="files or folders to scan")
    ap.add_argument("--json", action="store_true", help="print the findings as JSON instead of a Markdown report")
    ap.add_argument("--include-categories", action="store_true",
                    help="judge colours in category palettes like any other colour (only when a person asks to change them)")
    ap.add_argument("--top", type=int, default=20, metavar="N", help="findings to list per group in the report (default 20; JSON lists all)")
    ap.add_argument("--near", type=float, default=NEAR, metavar="N",
                    help=f"colour distance (CIEDE2000) below which a value counts as a near-miss of a kit colour (default {NEAR:g})")
    ap.add_argument("--exclude", action="append", default=[], metavar="GLOB",
                    help="leave out files or folders matching this pattern, such as 'docs' or 'data/*' (may be repeated)")
    ap.add_argument("--fail-on-hard", action="store_true", help="exit with code 1 if a hard rule is broken")
    ap.add_argument("--tokens", metavar="FILE", help="use this tokens.json instead of the one beside the skill")
    args = ap.parse_args(argv)
    missing = [p for p in args.paths if not Path(p).exists()]
    if missing:
        ap.error("no such file or folder: " + ", ".join(missing))
    try:
        kit = load_kit(args.tokens)
    except (OSError, ValueError, KeyError) as e:
        ap.error(f"cannot read the kit's tokens.json ({e}); keep this script inside the skill folder or pass --tokens")
    scan = run_scan(args.paths, kit, args.exclude)
    findings, stats = build_findings(scan, kit, args.near, args.include_categories)
    if args.json:
        json.dump({"kit_version": kit.version, "near_threshold": args.near, "include_categories": args.include_categories,
                   "stats": stats, "findings": findings}, sys.stdout, indent=1, ensure_ascii=False)
        print()
    else:
        sys.stdout.write(render_markdown(findings, stats, kit, args.top, args.include_categories))
    return 1 if args.fail_on_hard and stats["must"] else 0


if __name__ == "__main__":
    sys.exit(main())
