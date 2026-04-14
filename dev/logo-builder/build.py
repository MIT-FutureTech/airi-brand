#!/usr/bin/env python3
"""
AIRI logo builder.

Reads sources/icon.svg (the AIRI Initiative icon) and Figtree[wght].ttf,
composites standalone icons and horizontal lockups in four colour variants,
and writes SVG + PNG outputs to output/.

Pipeline:
    sources/icon.svg  ─►  icon-*.svg (padded square)   ─►  icon-*.png
                      │
                      └►  horizontal-*.svg (icon + text) ─►  horizontal-*.png

Design decisions:
    - No divider line (removed from old build)
    - Figtree everywhere (400 for "MIT AI Risk", 700 for "Initiative")
    - Horizontal lockup proportions (locked after variant comparison in
      dev/logo-builder/output/variants/):
        - Gap between icon and text = 1 × L-square (the largest square in
          the icon), computed from the icon's own geometry
        - Text is pinned to the M1→M4 vertical span: cap-top of "MIT AI Risk"
          sits on the top edge of M1, baseline of "Initiative" sits on the
          bottom edge of M4
        - Line-height ratio = 1.0 (tight)
        - Font size is solved so that cap-height + one line-spacing exactly
          fills the M-span — no hard-coded font size
    - Tight bounds are computed from the raw path data, so the current
      pre-padded icon.svg works without needing an un-padded source
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path

import cairosvg
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from svgpathtools import parse_path

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------

BRAND_RED = "#a32035"
WHITE = "#ffffff"

HERE = Path(__file__).resolve().parent
SOURCES = HERE / "sources"
FONTS = HERE / "fonts"
OUTPUT = HERE / "output"

ICON_PADDING_RATIO = 0.02   # 2% padding on all sides of the square icon
HORIZ_HEIGHT = 120          # logical units, not pixels
ICON_MARGIN = 4             # gutter around icon inside the lockup
LINE_SPACING_RATIO = 1.0    # tight line spacing (variant 9)

PNG_ICON_SIZE = 1024
PNG_HORIZ_HEIGHT = 512

LOCKUP_LINE1 = "MIT AI Risk"
LOCKUP_LINE2 = "Initiative"

# Icon geometry landmarks, in sources/icon.svg source units. Hand-catalogued
# from the path data — the icon is composed of small/medium/large squares.
ICON_LARGE_SQUARE_SOURCE = 83.36   # side of an L-square
ICON_M1_TOP_SOURCE = 73.03         # top edge of M1 (upper-right medium square)
ICON_M4_BOTTOM_SOURCE = 458.47     # bottom edge of M4 (lower-right medium square)


# -----------------------------------------------------------------------------
# Font loading — instantiate the variable font at two weights
# -----------------------------------------------------------------------------

def load_figtree_at_weight(weight: int) -> TTFont:
    src = FONTS / "Figtree[wght].ttf"
    var = TTFont(str(src))
    return instantiateVariableFont(var, {"wght": weight})


FIGTREE_400 = load_figtree_at_weight(400)
FIGTREE_700 = load_figtree_at_weight(700)
FONTS_BY_WEIGHT = {400: FIGTREE_400, 700: FIGTREE_700}

# True cap-height ratio from Figtree's OS/2 table — used to pin the cap-top
# of the first line to a geometric landmark in the icon.
CAP_HEIGHT_RATIO = FIGTREE_400["OS/2"].sCapHeight / FIGTREE_400["head"].unitsPerEm


# -----------------------------------------------------------------------------
# Text → SVG path
# -----------------------------------------------------------------------------

def text_to_path_d(text: str, weight: int, size: float, x: float, y: float) -> tuple[str, float]:
    """
    Return (path `d` string, advance_width) for `text` rendered at baseline (x, y)
    with `size` in SVG user units. Weight is 400 or 700.

    Glyphs are drawn in Y-up font coordinates; we wrap SVGPathPen in a
    TransformPen that applies the Y-flip, scale, and per-glyph translation
    on the fly, so fontTools handles all the SVG path command quirks
    (H/V shortcuts, compressed commands, etc.).
    """
    font = FONTS_BY_WEIGHT[weight]
    upem = font["head"].unitsPerEm
    scale = size / upem

    cmap = font.getBestCmap()
    glyph_set = font.getGlyphSet()

    svg_pen = SVGPathPen(glyph_set)
    cursor = x
    for ch in text:
        glyph_name = cmap.get(ord(ch))
        if glyph_name is None:
            continue
        glyph = glyph_set[glyph_name]
        # Affine (a, b, c, d, e, f) maps (px, py) → (a*px + c*py + e, b*px + d*py + f)
        # We want: x' = scale*px + cursor, y' = -scale*py + y
        transform = (scale, 0, 0, -scale, cursor, y)
        xform_pen = TransformPen(svg_pen, transform)
        glyph.draw(xform_pen)
        cursor += glyph.width * scale

    return svg_pen.getCommands(), cursor - x


def text_advance_width(text: str, weight: int, size: float) -> float:
    font = FONTS_BY_WEIGHT[weight]
    upem = font["head"].unitsPerEm
    scale = size / upem
    cmap = font.getBestCmap()
    glyph_set = font.getGlyphSet()
    total = 0.0
    for ch in text:
        glyph_name = cmap.get(ord(ch))
        if glyph_name is None:
            continue
        total += glyph_set[glyph_name].width * scale
    return total


# -----------------------------------------------------------------------------
# Icon loading — compute tight bounds from path data
# -----------------------------------------------------------------------------

def load_icon_parts() -> tuple[str, str, tuple[float, float, float, float]]:
    """
    Read sources/icon.svg.

    Returns:
        defs_content:  everything inside any <defs> blocks, concatenated
        body_content:  the SVG inner markup with <defs> removed
        tight_bounds:  (min_x, min_y, width, height) of the actual path content,
                       ignoring any padding or whitespace in the source viewBox
    """
    raw = (SOURCES / "icon.svg").read_text()

    inner = re.search(r"<svg[^>]*>(.*)</svg>", raw, re.DOTALL).group(1)

    defs_content = ""
    def _extract(m: re.Match) -> str:
        nonlocal defs_content
        defs_content += m.group(1)
        return ""
    body = re.sub(r"<defs>(.*?)</defs>", _extract, inner, flags=re.DOTALL)

    # Compute tight bounds from every <path d="..."> inside body
    min_x = min_y = float("inf")
    max_x = max_y = float("-inf")
    for d in re.findall(r'<path[^>]*\bd="([^"]+)"', body):
        try:
            path = parse_path(d)
            x0, x1, y0, y1 = path.bbox()
        except Exception:
            continue
        if x0 < min_x: min_x = x0
        if y0 < min_y: min_y = y0
        if x1 > max_x: max_x = x1
        if y1 > max_y: max_y = y1

    if min_x == float("inf"):
        raise RuntimeError("No <path d='...'> elements found in icon.svg")

    # Intersect with clipPath rects if they exist — the path may extend beyond
    # the visible clip, and we care about the visible content bounds
    for clip_d in re.findall(r'<clipPath[^>]*>.*?d="([^"]+)".*?</clipPath>', raw, flags=re.DOTALL):
        try:
            path = parse_path(clip_d)
            x0, x1, y0, y1 = path.bbox()
        except Exception:
            continue
        # Only tighten; never expand
        if x0 > min_x: min_x = x0
        if y0 > min_y: min_y = y0
        if x1 < max_x: max_x = x1
        if y1 < max_y: max_y = y1

    return defs_content, body, (min_x, min_y, max_x - min_x, max_y - min_y)


def recolor(svg_fragment: str, new_color: str) -> str:
    """Swap any fill=#a32035 to new_color. Also handles the uppercase form."""
    return re.sub(r'fill="#[Aa]32035"', f'fill="{new_color}"', svg_fragment)


# -----------------------------------------------------------------------------
# Standalone icon (square + padded)
# -----------------------------------------------------------------------------

def build_icon_svg(defs: str, body: str, tight: tuple, fill: str) -> str:
    min_x, min_y, w, h = tight
    size = max(w, h)
    # Centre the content in a square
    cx_shift = (size - w) / 2
    cy_shift = (size - h) / 2
    sq_min_x = min_x - cx_shift
    sq_min_y = min_y - cy_shift
    pad = size * ICON_PADDING_RATIO
    new_size = size + pad * 2
    vb_x = sq_min_x - pad
    vb_y = sq_min_y - pad

    coloured_body = recolor(body, fill)
    defs_block = f"<defs>{defs}</defs>" if defs.strip() else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="{vb_x:.3f} {vb_y:.3f} {new_size:.3f} {new_size:.3f}">'
        f"{defs_block}"
        f"{coloured_body}"
        f"</svg>"
    )


# -----------------------------------------------------------------------------
# Horizontal lockup (icon + two-line text, no divider)
# -----------------------------------------------------------------------------

def build_horizontal_svg(defs: str, body: str, tight: tuple, fill: str) -> str:
    min_x, min_y, vb_w, vb_h = tight

    icon_target_h = HORIZ_HEIGHT - ICON_MARGIN * 2
    icon_scale = icon_target_h / vb_h
    icon_render_w = vb_w * icon_scale
    icon_x = ICON_MARGIN
    icon_y = ICON_MARGIN

    # Gap between icon and text = one L-square, in rendered units. Symmetric
    # right-pad of the same amount gives the lockup an icon-sized breathing
    # room on either side of the text block.
    gap = ICON_LARGE_SQUARE_SOURCE * icon_scale
    text_x = icon_x + icon_render_w + gap

    # Map M1-top and M4-bottom from source coords into rendered coords.
    m_top = (ICON_M1_TOP_SOURCE - min_y) * icon_scale + icon_y
    m_bottom = (ICON_M4_BOTTOM_SOURCE - min_y) * icon_scale + icon_y
    m_span = m_bottom - m_top

    # Solve for the font size that makes cap-height + one line-spacing fill
    # the M-span exactly, at LINE_SPACING_RATIO = 1.0.
    #   cap_height + line_spacing = m_span
    #   font * CAP_HEIGHT_RATIO + font * LINE_SPACING_RATIO = m_span
    font_size = m_span / (CAP_HEIGHT_RATIO + LINE_SPACING_RATIO)

    cap_height = font_size * CAP_HEIGHT_RATIO
    line_spacing = font_size * LINE_SPACING_RATIO
    # Cap-top of "MIT AI Risk" sits on M1-top; baseline of "Initiative"
    # sits on M4-bottom. Line 1 baseline = M1-top + cap-height.
    line1_y = m_top + cap_height
    line2_y = line1_y + line_spacing

    d1, _ = text_to_path_d(LOCKUP_LINE1, 400, font_size, text_x, line1_y)
    d2, _ = text_to_path_d(LOCKUP_LINE2, 700, font_size, text_x, line2_y)

    w1 = text_advance_width(LOCKUP_LINE1, 400, font_size)
    w2 = text_advance_width(LOCKUP_LINE2, 700, font_size)
    # Symmetric right padding of one L-square.
    total_width = text_x + max(w1, w2) + gap

    coloured_icon_body = recolor(body, fill)
    defs_block = f"<defs>{defs}</defs>" if defs.strip() else ""

    # Icon transform chain (right-to-left in SVG):
    #   translate(-min_x, -min_y)  — normalise to origin
    #   scale(icon_scale)          — fit to target height
    #   translate(icon_x, icon_y)  — place in gutter
    icon_transform = (
        f"translate({icon_x}, {icon_y}) "
        f"scale({icon_scale:.6f}) "
        f"translate({-min_x:.3f}, {-min_y:.3f})"
    )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {total_width:.1f} {HORIZ_HEIGHT}">'
        f"{defs_block}"
        f'<g transform="{icon_transform}">{coloured_icon_body}</g>'
        f'<path fill="{fill}" d="{d1}"/>'
        f'<path fill="{fill}" d="{d2}"/>'
        f"</svg>"
    )


# -----------------------------------------------------------------------------
# On-red variant — inject a background rect at the back of any SVG
# -----------------------------------------------------------------------------

def add_red_background(svg: str) -> str:
    vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
    min_x, min_y, w, h = [float(x) for x in vb.split()]
    rect = (
        f'<rect x="{min_x}" y="{min_y}" width="{w}" height="{h}" fill="{BRAND_RED}"/>'
    )
    insert_at = svg.index(">") + 1
    return svg[:insert_at] + rect + svg[insert_at:]


# -----------------------------------------------------------------------------
# PNG rendering via cairosvg
# -----------------------------------------------------------------------------

def render_png(svg: str, out_path: Path, target_height: int = None, target_width: int = None) -> None:
    kwargs = {}
    if target_width is not None:
        kwargs["output_width"] = target_width
    if target_height is not None:
        kwargs["output_height"] = target_height
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(out_path), **kwargs)


def horizontal_png_width(svg: str) -> int:
    vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
    _, _, w, h = [float(x) for x in vb.split()]
    return round(PNG_HORIZ_HEIGHT * (w / h))


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> None:
    OUTPUT.mkdir(exist_ok=True)

    print("Loading icon...")
    defs, body, tight = load_icon_parts()
    min_x, min_y, w, h = tight
    print(f"  tight bounds: x={min_x:.2f} y={min_y:.2f} w={w:.2f} h={h:.2f}")

    # --- Standalone icons ---
    print("Building standalone icons...")
    icon_variants = {
        "icon.svg": BRAND_RED,
        "icon-on-light.svg": BRAND_RED,
        "icon-on-dark.svg": WHITE,
    }
    for name, fill in icon_variants.items():
        svg = build_icon_svg(defs, body, tight, fill)
        (OUTPUT / name).write_text(svg)
        render_png(svg, OUTPUT / name.replace(".svg", ".png"),
                   target_width=PNG_ICON_SIZE, target_height=PNG_ICON_SIZE)
        print(f"  {name}")

    # on-red derived from on-dark
    on_dark_svg = (OUTPUT / "icon-on-dark.svg").read_text()
    red_icon = add_red_background(on_dark_svg)
    (OUTPUT / "icon-on-red.svg").write_text(red_icon)
    render_png(red_icon, OUTPUT / "icon-on-red.png",
               target_width=PNG_ICON_SIZE, target_height=PNG_ICON_SIZE)
    print("  icon-on-red.svg")

    # --- Horizontal lockups ---
    print("Building horizontal lockups...")
    lockup_variants = {
        "horizontal.svg": BRAND_RED,
        "horizontal-on-light.svg": BRAND_RED,
        "horizontal-on-dark.svg": WHITE,
    }
    for name, fill in lockup_variants.items():
        svg = build_horizontal_svg(defs, body, tight, fill)
        (OUTPUT / name).write_text(svg)
        render_png(svg, OUTPUT / name.replace(".svg", ".png"),
                   target_height=PNG_HORIZ_HEIGHT,
                   target_width=horizontal_png_width(svg))
        print(f"  {name}")

    on_dark_lockup = (OUTPUT / "horizontal-on-dark.svg").read_text()
    red_lockup = add_red_background(on_dark_lockup)
    (OUTPUT / "horizontal-on-red.svg").write_text(red_lockup)
    render_png(red_lockup, OUTPUT / "horizontal-on-red.png",
               target_height=PNG_HORIZ_HEIGHT,
               target_width=horizontal_png_width(red_lockup))
    print("  horizontal-on-red.svg")

    print(f"\nDone. {len(list(OUTPUT.glob('*')))} files in {OUTPUT}")


if __name__ == "__main__":
    main()
