#!/usr/bin/env python3
"""
Exploration variants of the horizontal lockup for design review.

Generates three PNG + SVG pairs into output/variants/, varying gap and
text sizing while keeping the icon, font, and no-divider decisions fixed.

Icon analysis:
    The AIRI Initiative icon is composed of squares at three sizes
    (25.77, 52.08, 83.36 source units). The "large square" is 83.36 and
    vertically spans y ∈ [224.07, 307.43] — the central band of the
    cross shape. All three variants use the large-square dimension as
    the unit for gap sizing.
"""

from pathlib import Path

import build

HERE = Path(__file__).resolve().parent
OUT = HERE / "output" / "variants"
OUT.mkdir(parents=True, exist_ok=True)

LARGE_SQUARE_SOURCE = 83.36
LARGE_SQUARE_TOP_SRC = 224.07
LARGE_SQUARE_BOTTOM_SRC = 307.43

# The five large squares form a plus/cross spanning 3×L vertically.
# Top of topmost L to bottom of bottommost L:
PLUS_TOP_SRC = 140.70
PLUS_BOTTOM_SRC = 390.80

# M1 top-edge to M4 bottom-edge (the upper and lower medium squares
# nearest the central plus, on the right flank)
M_TOP_SRC = 73.03
M_BOTTOM_SRC = 458.47

# S2 top-edge to S5 bottom-edge (the extreme top and bottom small squares,
# which sit essentially at the clip boundary — i.e. full icon height)
S_TOP_SRC = 21.17
S_BOTTOM_SRC = 510.33

HORIZ_HEIGHT = build.HORIZ_HEIGHT
ICON_MARGIN = build.ICON_MARGIN
LINE_SPACING_RATIO = build.LINE_SPACING_RATIO
BRAND_RED = build.BRAND_RED

# True cap height from the font's OS/2 table
_upem = build.FIGTREE_400["head"].unitsPerEm
CAP_HEIGHT_RATIO = build.FIGTREE_400["OS/2"].sCapHeight / _upem


def build_variant(defs, body, tight, fill, *, gap, font_size, mode,
                  line_spacing_ratio=LINE_SPACING_RATIO):
    """
    mode:
      "centered"    — baseline vertically centred like build.py default
      "square-span" — cap-top of M and baseline of "Initiative" aligned to
                      the top/bottom of the large square
      "icon-span"   — cap-top of M and baseline of "Initiative" aligned to
                      the top/bottom of the icon's rendered box
    """
    min_x, min_y, vb_w, vb_h = tight

    icon_target_h = HORIZ_HEIGHT - ICON_MARGIN * 2
    icon_scale = icon_target_h / vb_h
    icon_render_w = vb_w * icon_scale
    icon_x = ICON_MARGIN
    icon_y = ICON_MARGIN

    text_x = icon_x + icon_render_w + gap

    line_spacing = font_size * line_spacing_ratio
    cap_height = font_size * CAP_HEIGHT_RATIO

    if mode == "centered":
        mid_y = HORIZ_HEIGHT / 2
        line1_y = mid_y - line_spacing * build.BASELINE_NUDGE_RATIO
        line2_y = line1_y + line_spacing
    elif mode == "square-span":
        top = (LARGE_SQUARE_TOP_SRC - min_y) * icon_scale + icon_y
        bottom = (LARGE_SQUARE_BOTTOM_SRC - min_y) * icon_scale + icon_y
        line1_y = top + cap_height
        line2_y = bottom
    elif mode == "plus-span":
        top = (PLUS_TOP_SRC - min_y) * icon_scale + icon_y
        bottom = (PLUS_BOTTOM_SRC - min_y) * icon_scale + icon_y
        line1_y = top + cap_height
        line2_y = bottom
    elif mode == "m-span":
        top = (M_TOP_SRC - min_y) * icon_scale + icon_y
        bottom = (M_BOTTOM_SRC - min_y) * icon_scale + icon_y
        line1_y = top + cap_height
        line2_y = bottom
    elif mode == "s-span":
        top = (S_TOP_SRC - min_y) * icon_scale + icon_y
        bottom = (S_BOTTOM_SRC - min_y) * icon_scale + icon_y
        line1_y = top + cap_height
        line2_y = bottom
    elif mode == "icon-span":
        top = icon_y
        bottom = icon_y + icon_target_h
        line1_y = top + cap_height
        line2_y = bottom
    else:
        raise ValueError(mode)

    d1, _ = build.text_to_path_d(build.LOCKUP_LINE1, 400, font_size, text_x, line1_y)
    d2, _ = build.text_to_path_d(build.LOCKUP_LINE2, 700, font_size, text_x, line2_y)

    w1 = build.text_advance_width(build.LOCKUP_LINE1, 400, font_size)
    w2 = build.text_advance_width(build.LOCKUP_LINE2, 700, font_size)
    total_width = text_x + max(w1, w2) + gap  # symmetric right pad = gap

    coloured_icon_body = build.recolor(body, fill)
    defs_block = f"<defs>{defs}</defs>" if defs.strip() else ""

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


def font_size_for_span(span: float, line_spacing_ratio: float = LINE_SPACING_RATIO) -> float:
    """Solve cap_height + line_spacing = span for font_size.
    text block height = font_size * (CAP_HEIGHT_RATIO + line_spacing_ratio)"""
    return span / (CAP_HEIGHT_RATIO + line_spacing_ratio)


def main() -> None:
    defs, body, tight = build.load_icon_parts()
    min_x, min_y, vb_w, vb_h = tight

    icon_scale = (HORIZ_HEIGHT - ICON_MARGIN * 2) / vb_h
    gap = LARGE_SQUARE_SOURCE * icon_scale
    plus_span = (PLUS_BOTTOM_SRC - PLUS_TOP_SRC) * icon_scale
    m_span = (M_BOTTOM_SRC - M_TOP_SRC) * icon_scale
    s_span = (S_BOTTOM_SRC - S_TOP_SRC) * icon_scale

    # Span variants: font sized to fill the span at default line-height 1.2
    font_s_span = font_size_for_span(s_span)
    font_m_span = font_size_for_span(m_span)
    font_l_span = font_size_for_span(plus_span)

    # Line-height variants: pin the text block vertically to L1→L5 (the
    # central plus) and solve for font size at each line-height so the block
    # exactly fills that span no matter the line-height. This means all four
    # line-height variants have text whose cap-top sits on L1 and whose
    # baseline sits on L5; only the internal baseline spacing (and the font
    # size needed to maintain that span) changes.
    def font_for_lh(lh: float) -> float:
        return plus_span / (CAP_HEIGHT_RATIO + lh)

    def font_for_m_lh(lh: float) -> float:
        return m_span / (CAP_HEIGHT_RATIO + lh)

    print(f"Figtree cap height ratio: {CAP_HEIGHT_RATIO:.3f}")
    print(f"Gap (1 × L):                   {gap:.2f}")
    print(f"S-span (full icon):            {s_span:.2f}  → font {font_s_span:.2f}")
    print(f"M-span (M1→M4):                {m_span:.2f}  → font {font_m_span:.2f}")
    print(f"L-span (plus, L1→L5):          {plus_span:.2f}  → font {font_l_span:.2f}")
    print("Line-height variants pinned to L1→L5 span:")
    for lh in (0.9, 1.0, 1.1, 1.2):
        print(f"  lh={lh} → font {font_for_lh(lh):.2f}")
    print("Line-height variants pinned to M1→M4 span:")
    for lh in (0.9, 1.0, 1.1, 1.2):
        print(f"  lh={lh} → font {font_for_m_lh(lh):.2f}")

    variants = [
        ("1-span-S2-S5",
         dict(gap=gap, font_size=font_s_span, mode="s-span")),
        ("2-span-M1-M4",
         dict(gap=gap, font_size=font_m_span, mode="m-span")),
        ("3-span-L1-L5",
         dict(gap=gap, font_size=font_l_span, mode="plus-span")),
        ("4-lh-0.9",
         dict(gap=gap, font_size=font_for_lh(0.9), mode="plus-span")),
        ("5-lh-1.0",
         dict(gap=gap, font_size=font_for_lh(1.0), mode="plus-span")),
        ("6-lh-1.1",
         dict(gap=gap, font_size=font_for_lh(1.1), mode="plus-span")),
        ("7-lh-1.2",
         dict(gap=gap, font_size=font_for_lh(1.2), mode="plus-span")),
        ("8-m-lh-0.9",
         dict(gap=gap, font_size=font_for_m_lh(0.9), mode="m-span")),
        ("9-m-lh-1.0",
         dict(gap=gap, font_size=font_for_m_lh(1.0), mode="m-span")),
        ("10-m-lh-1.1",
         dict(gap=gap, font_size=font_for_m_lh(1.1), mode="m-span")),
        ("11-m-lh-1.2",
         dict(gap=gap, font_size=font_for_m_lh(1.2), mode="m-span")),
    ]

    for name, kwargs in variants:
        svg = build_variant(defs, body, tight, BRAND_RED, **kwargs)
        svg_path = OUT / f"horizontal-{name}-on-light.svg"
        svg_path.write_text(svg)
        png_path = OUT / f"horizontal-{name}-on-light.png"
        build.render_png(
            svg, png_path,
            target_height=build.PNG_HORIZ_HEIGHT,
            target_width=build.horizontal_png_width(svg),
        )
        print(f"  wrote {png_path.name}")


if __name__ == "__main__":
    main()
