# AIRI logo builder

Regenerates the AIRI logo set from a single source icon and the Figtree
variable font. Produces standalone icons and horizontal lockups (icon +
two-line wordmark) in four colour variants: default (red on transparent),
`-on-light`, `-on-dark`, `-on-red`.

## What it produces

Running `build.py` writes 16 files into `output/`:

- `icon.svg` / `icon.png` — red on transparent (default)
- `icon-on-light.svg` / `.png` — red on transparent (light bg)
- `icon-on-dark.svg` / `.png` — white on transparent (dark bg)
- `icon-on-red.svg` / `.png` — white on #A32035 background
- `horizontal.svg` / `.png` — red + "MIT AI Risk / Initiative"
- `horizontal-on-light.svg` / `.png`
- `horizontal-on-dark.svg` / `.png`
- `horizontal-on-red.svg` / `.png`

## Sources

- `sources/icon.svg` — the AIRI Initiative icon. This is now the single
  canonical icon for the whole brand; the old index and repository icons
  have been retired to `skill/logos/legacy/`.
- `fonts/Figtree[wght].ttf` — the Figtree variable font (SIL OFL, see
  `fonts/OFL.txt`). The builder instantiates weight 400 for "MIT AI Risk"
  and weight 700 for "Initiative".

## Design

- No divider line between icon and text (removed from the old build).
- The text's left edge sits where the old divider used to be, so the
  "M" of "MIT" aligns with that column — no gap where the divider was.
- Text is rendered as outlined paths, so output SVGs are self-contained
  and don't need Figtree installed on the consumer's machine.
- Icon bounds are computed from the raw path data, so the current
  pre-padded `icon.svg` works without needing a fresh un-padded source.

## Setup

```bash
cd dev/logo-builder
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
source venv/bin/activate
python build.py
```

Outputs land in `output/`. To refresh `skill/logos/initiative/`, copy
from there after checking the result visually.

## Dependencies

- [fonttools](https://github.com/fonttools/fonttools) — variable font
  instancing and glyph → SVG path conversion
- [cairosvg](https://cairosvg.org/) — pure-Python SVG → PNG rendering
- [svgpathtools](https://github.com/mathandy/svgpathtools) — path bbox
  computation for tight icon bounds
