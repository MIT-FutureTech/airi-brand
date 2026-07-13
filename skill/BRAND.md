# AIRI Brand Kit

## Overview

The MIT AI Risk Initiative (AIRI) is the umbrella project. It has two named sub-products — the AI Risk Repository and the AI Risk Index — each with its own horizontal lockup. All three lockups share a single icon and a single wordmark structure; only the second line of the wordmark differs ("Initiative", "Repository", or "Index"). Earlier versions of this kit shipped three fully independent logo designs; those have been retired to `legacy/logos/` at the repo root.

## Colors

| Token | Hex | Role |
|-------|-----|------|
| `primary` | `#A32035` | AIRI red. Buttons, links, headings, accents, logo. Distinct from MIT's institutional red (`#750014`) |
| `primary-light` | `#D07886` | Lighter accent. Hover tints, secondary highlights, tags |
| `primary-dark` | `#5E0E20` | Darkest red. Hover states for primary buttons |
| `dark` | `#1A1A1A` | Body text, headings on light backgrounds |
| `gray` | `#898A8D` | Muted text, captions, secondary borders |
| `background` | `#FAFAFA` | Page background |
| `white` | `#FFFFFF` | Cards, panels, reversed logo |

Derived values:
- Borders: `#e0e0e0` (light) or `gray` (strong)
- Primary button hover: `#8a1b2d`
- Links: `primary`, hover to `primary-dark`

Do not introduce additional brand colors. Use opacity variations of existing colors if you need lighter fills (e.g., `rgba(163, 32, 53, 0.1)` for light red backgrounds).

## Typography

**Font family:** Figtree (Google Fonts). Fallback: `sans-serif`.

**Weights:** 400 (regular), 600 (semibold), 700 (bold).

**General guidance:**
- Headings: semibold or bold
- Body: regular
- Use the size scale in `tokens.json` / `brand.css` as a guide, but exact sizing is flexible
- Prefer left-aligned text. Center only for hero sections or short labels.

## Logos

Three product folders live under `logos/`: `initiative/`, `index/`, and `repository/`. Each contains the same icon and a horizontal lockup that differs only in the second line of the wordmark. Each layout has four colour variants in both SVG and PNG.

File structure in `logos/`:

```
logos/
  initiative/                    Lockup: "MIT AI Risk / Initiative"
    icon.svg / .png              Default (red on transparent)
    icon-on-light.svg / .png     Red content, transparent background
    icon-on-dark.svg / .png      White content, transparent background
    icon-on-red.svg / .png       White content, #A32035 background
    horizontal.svg / .png        Default horizontal lockup
    horizontal-on-light.*        Red content, transparent background
    horizontal-on-dark.*         White content, transparent background
    horizontal-on-red.*          White content, #A32035 background
  index/                         Lockup: "MIT AI Risk / Index" — same 16 files
  repository/                    Lockup: "MIT AI Risk / Repository" — same 16 files
```

**The icon is shared.** `icon.svg` is byte-identical across the three folders; each product carries its own copy only so that consumers can grab one folder and have a complete set. Do not create modified icons per product.

**Variant guide:**
- `on-light` / default: Use on white or light backgrounds. Content is `primary` (#A32035).
- `on-dark`: Use on dark backgrounds. Content is white.
- `on-red`: Use where you need a self-contained logo with the brand red background baked in (presentations, documents, social media).

**Horizontal lockup:** Icon + "MIT AI Risk" (Figtree 400) / product name (Figtree 700), stacked as two lines with no vertical divider. Text is rendered as outlined SVG paths so the files have no font dependencies. The lockup proportions are locked: the gap between the icon and the text equals one "large square" from the icon, and the text is sized so the cap-top of "MIT AI Risk" sits on the top of the upper medium square and the baseline of the second line sits on the bottom of the lower medium square.

Usage:
- Pick the folder that matches the project: `initiative/` for general AIRI work, `index/` for AI Risk Index pages, `repository/` for AI Risk Repository pages. If a project doesn't fit one of the two named sub-products, default to `initiative/`.
- Navigation bars: horizontal variant, constrained to roughly 200-250px width
- Favicons / small contexts: icon-only variant (any folder — the icon is the same)
- Title pages / hero sections: any variant at appropriate size
- PNG icons are 1024x1024. PNG horizontals are 512px tall.

To regenerate logos, change proportions, or add a new product lockup, see `dev/logo-builder/` on the `dev` branch. The product list lives in `build.py` as `PRODUCTS`.

## Component patterns

These are defaults, not strict rules. The goal is visual consistency across AIRI outputs.

**Buttons:**
- Primary: `primary` background, white text, `radius-md` corners, `semibold` weight
- Primary hover: `primary-dark` background
- Secondary/outline: white background, `primary` border and text
- Secondary hover: light red background (`rgba(163, 32, 53, 0.08)`)

**Cards/panels:**
- White background, subtle border (`#e0e0e0`), `radius-md` corners
- Optional: light shadow for elevation

**Links:**
- Color: `primary`. Hover: `primary-dark`. Underline on hover only, or always, either is fine.

**Tables:**
- Header row: `primary` background, white text, or `dark` background, white text
- Alternating rows: white / `background` (#FAFAFA)
- Borders: `#e0e0e0`

**Charts and data visualization:**
- Primary data series: `primary` (#A32035)
- Secondary series: `primary-light` (#D07886)
- Additional series: `gray` (#898A8D), `dark` (#1A1A1A)
- If more colors are needed, derive from the palette (e.g., lighter/darker variants) rather than introducing unrelated hues
- Background: white or `background`

**Navigation:**
- White background, `dark` text for links
- Active/current page: `primary` colored text or underline
- Logo on the left, links on the right

## File reference

- `tokens.json`: machine-readable design tokens
- `brand.css`: CSS custom properties, ready to import or paste
- `logos/initiative/`, `logos/index/`, `logos/repository/`: production logo files (SVG + PNG). Same icon in all three; different horizontal lockup per product.
- `BRAND.md`: this file
- `SKILL.md`: Claude Code skill wrapper (loads this file as context before generating visual output)

Retired assets (no longer part of the skill): the pre-consolidation AI Risk Repository and AI Risk Index logos (which used fully independent icons) now live in `legacy/logos/` at the repo root. Logo build tooling lives in `dev/logo-builder/` on the `dev` branch.
