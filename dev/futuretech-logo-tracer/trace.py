#!/usr/bin/env python3
"""
Trace the MIT FutureTech PNG logo into SVG paths, producing four color variants.

Approach:
1. Separate the logo into two color regions: black text ("MIT" + tagline)
   and red text ("FutureTech")
2. Convert each to a binary mask
3. Use OpenCV findContours to get polygon outlines
4. Smooth polygons with approxPolyDP and optional Bezier fitting
5. Emit SVG paths for each region
6. Assemble four variant SVGs with different fill colors
"""

import cv2
import numpy as np
from PIL import Image
from pathlib import Path
import sys


SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "inbox/futuretech_logo/MIT FutureTech-full.png"
OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

# The actual red in the logo (measured from opaque pixels)
LOGO_RED_RGB = (154, 32, 48)

# Target colors for variants
COLORS = {
    "default":  {"black": "#000000", "red": "#9A2030"},
    "on-light": {"black": "#000000", "red": "#9A2030"},
    "on-dark":  {"black": "#ffffff", "red": "#ffffff"},
    "on-red":   {"black": "#ffffff", "red": "#ffffff"},
}
BG_COLORS = {
    "default":  None,
    "on-light": None,
    "on-dark":  None,
    "on-red":   "#9A2030",
}


def load_and_crop(path):
    """Load RGBA image, crop to content with small margin."""
    img = Image.open(path).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]
    rows = np.where(np.any(alpha > 10, axis=1))[0]
    cols = np.where(np.any(alpha > 10, axis=0))[0]
    margin = 20
    r0 = max(0, rows[0] - margin)
    r1 = min(arr.shape[0], rows[-1] + margin)
    c0 = max(0, cols[0] - margin)
    c1 = min(arr.shape[1], cols[-1] + margin)
    return arr[r0:r1, c0:c1]


def make_masks(arr):
    """Separate into black-text mask and red-text mask."""
    rgb = arr[:, :, :3]
    alpha = arr[:, :, 3]

    # Threshold: pixel must be somewhat visible
    visible = alpha > 64

    # Red channel dominant = red text; otherwise = black text
    r, g, b = rgb[:, :, 0].astype(int), rgb[:, :, 1].astype(int), rgb[:, :, 2].astype(int)
    is_reddish = (r > 80) & (r > g + 40) & (r > b + 30)

    red_mask = (visible & is_reddish).astype(np.uint8) * 255
    black_mask = (visible & ~is_reddish).astype(np.uint8) * 255

    # Clean up with morphological ops
    kernel = np.ones((3, 3), np.uint8)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    return black_mask, red_mask


def contours_to_svg_path(contours, hierarchy, epsilon_factor=0.0008):
    """Convert OpenCV contours to an SVG path string with proper holes."""
    h, w = 0, 0  # not needed for path data
    parts = []

    if hierarchy is None:
        return ""

    hier = hierarchy[0]

    for i, contour in enumerate(contours):
        if len(contour) < 3:
            continue

        # Simplify
        peri = cv2.arcLength(contour, True)
        epsilon = epsilon_factor * peri
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) < 3:
            continue

        pts = approx.reshape(-1, 2)

        # Build path: M x,y L x,y ... Z
        d = f"M {pts[0][0]},{pts[0][1]}"
        for pt in pts[1:]:
            d += f" L {pt[0]},{pt[1]}"
        d += " Z"
        parts.append(d)

    return " ".join(parts)


def trace_mask(mask, epsilon_factor=0.0008):
    """Trace a binary mask into SVG path data."""
    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS
    )
    return contours_to_svg_path(contours, hierarchy, epsilon_factor)


def build_svg(black_path, red_path, width, height, colors, bg_color=None):
    """Assemble a complete SVG."""
    # Scale down to a reasonable viewBox (original is ~6000x1400 px)
    # We'll keep the native pixel coords in the viewBox
    padding = 40
    vb_w = width + padding * 2
    vb_h = height + padding * 2

    bg_rect = ""
    if bg_color:
        bg_rect = f'  <rect width="{vb_w}" height="{vb_h}" fill="{bg_color}" rx="40"/>\n'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w} {vb_h}" width="{vb_w}" height="{vb_h}">
{bg_rect}  <g transform="translate({padding},{padding})">
    <path d="{black_path}" fill="{colors['black']}" fill-rule="evenodd"/>
    <path d="{red_path}" fill="{colors['red']}" fill-rule="evenodd"/>
  </g>
</svg>
'''
    return svg


def main():
    print(f"Loading {SRC} ...")
    arr = load_and_crop(SRC)
    h, w = arr.shape[:2]
    print(f"Cropped to {w}x{h}")

    print("Separating color regions ...")
    black_mask, red_mask = make_masks(arr)

    # Save debug masks
    cv2.imwrite(str(OUT / "debug-black-mask.png"), black_mask)
    cv2.imwrite(str(OUT / "debug-red-mask.png"), red_mask)
    print(f"Debug masks saved to {OUT}/")

    print("Tracing contours ...")
    black_path = trace_mask(black_mask)
    red_path = trace_mask(red_mask)

    print(f"Black path: {len(black_path)} chars")
    print(f"Red path: {len(red_path)} chars")

    print("Generating SVG variants ...")
    for variant in COLORS:
        svg = build_svg(black_path, red_path, w, h, COLORS[variant], BG_COLORS[variant])
        out_file = OUT / f"futuretech-{variant}.svg" if variant != "default" else OUT / "futuretech.svg"
        out_file.write_text(svg)
        print(f"  -> {out_file.name} ({len(svg)} bytes)")

    print("\nDone! Check output/ for results.")


if __name__ == "__main__":
    main()
