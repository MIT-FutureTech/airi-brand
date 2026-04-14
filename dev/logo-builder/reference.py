#!/usr/bin/env python3
"""Reference diagram: every square in the AIRI Initiative icon, labelled."""
from pathlib import Path
import re
import build

HERE = Path(__file__).resolve().parent
OUT = HERE / "output" / "variants"
OUT.mkdir(parents=True, exist_ok=True)

S_SIZE, M_SIZE, L_SIZE = 25.77, 52.08, 83.36

# Hand-verified from sources/icon.svg (top-left corners, source coords)
SMALL = [(24.86, 187.91), (191.60, 21.17), (108.23, 104.54),
         (24.86, 317.82), (191.60, 484.56), (108.23, 401.19)]
MEDIUM = [(243.35, 73.03), (160.09, 156.40), (76.72, 239.66),
          (243.35, 406.39), (160.09, 323.02)]
LARGE = [(311.12, 140.70),   # top
         (227.76, 224.07),   # mid-left
         (311.12, 224.07),   # mid-center
         (394.39, 224.07),   # mid-right
         (311.12, 307.43)]   # bottom

OUTLINE = {"S": "#2563eb", "M": "#16a34a", "L": "#ea580c"}
LABEL  = {"S": "#1e3a8a", "M": "#14532d", "L": "#7c2d12"}


def build_svg() -> str:
    defs, body, tight = build.load_icon_parts()
    min_x, min_y, w, h = tight
    pad = 40
    title_h = 60
    legend_h = 90
    vb_x = min_x - pad - 160  # extra left for plus-height label
    vb_y = min_y - pad - title_h
    vb_w = w + pad * 2 + 160
    vb_h = h + pad * 2 + title_h + legend_h

    muted = re.sub(r'fill="#[Aa]32035"', 'fill="#e5d5d8"', body)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="{vb_x:.2f} {vb_y:.2f} {vb_w:.2f} {vb_h:.2f}" '
        f'font-family="sans-serif">',
        f'<defs>{defs}</defs>' if defs.strip() else "",
        f'<text x="{min_x + w/2:.1f}" y="{min_y - pad - 20:.1f}" '
        f'text-anchor="middle" font-size="30" font-weight="700" fill="#111">'
        f'AIRI icon — square reference</text>',
        muted,
    ]

    def add(group, size, cls):
        c = OUTLINE[cls]
        lc = LABEL[cls]
        for i, (x, y) in enumerate(group, 1):
            parts.append(
                f'<rect x="{x:.2f}" y="{y:.2f}" width="{size}" height="{size}" '
                f'fill="none" stroke="{c}" stroke-width="3"/>'
            )
            cx, cy = x + size / 2, y + size / 2
            fs = max(11, size * 0.32)
            parts.append(
                f'<text x="{cx:.1f}" y="{cy:.1f}" text-anchor="middle" '
                f'dominant-baseline="central" font-size="{fs:.1f}" '
                f'font-weight="700" fill="{lc}">{cls}{i}</text>'
            )

    add(SMALL, S_SIZE, "S")
    add(MEDIUM, M_SIZE, "M")
    add(LARGE, L_SIZE, "L")

    # Plus vertical-extent bracket on the LEFT (top of top L to bottom of bot L)
    top_y, bot_y = 140.70, 390.80
    bx = min_x - 60
    parts += [
        f'<line x1="{bx}" y1="{top_y}" x2="{bx}" y2="{bot_y}" '
        f'stroke="#ea580c" stroke-width="3"/>',
        f'<line x1="{bx-10}" y1="{top_y}" x2="{bx+10}" y2="{top_y}" '
        f'stroke="#ea580c" stroke-width="3"/>',
        f'<line x1="{bx-10}" y1="{bot_y}" x2="{bx+10}" y2="{bot_y}" '
        f'stroke="#ea580c" stroke-width="3"/>',
        f'<text x="{bx-14}" y="{(top_y+bot_y)/2:.1f}" text-anchor="end" '
        f'dominant-baseline="central" font-size="20" font-weight="700" '
        f'fill="#7c2d12">3×L = {bot_y - top_y:.1f}</text>',
    ]

    # Legend
    ly = min_y + h + pad + 10
    items = [("S", f"Small = {S_SIZE}"),
             ("M", f"Medium = {M_SIZE}"),
             ("L", f"Large = {L_SIZE}")]
    col_w = w / 3
    for i, (cls, txt) in enumerate(items):
        lx = min_x + i * col_w
        parts += [
            f'<rect x="{lx}" y="{ly}" width="26" height="26" '
            f'fill="none" stroke="{OUTLINE[cls]}" stroke-width="3"/>',
            f'<text x="{lx+34}" y="{ly+20}" font-size="22" fill="#111">{txt}</text>',
        ]

    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    svg = build_svg()
    (OUT / "reference-grid.svg").write_text(svg)
    build.render_png(svg, OUT / "reference-grid.png", target_width=1600)
    print("wrote reference-grid.{svg,png}")


if __name__ == "__main__":
    main()
