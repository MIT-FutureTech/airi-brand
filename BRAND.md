# AIRI Brand Kit

## Overview

The MIT AI Risk Initiative (AIRI) is the umbrella project. It has two named sub-projects with their own logos: the AI Risk Repository and the AI Risk Index. Other projects under the Initiative use the Initiative logo.

## Colors

| Token | Hex | Role |
|-------|-----|------|
| `primary` | `#A32035` | MIT red. Buttons, links, headings, accents, logo |
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

Three logo sets exist (Index, Initiative, Repository), each with horizontal and icon-only layouts. Each layout has four color variants in both SVG and PNG.

File structure in `logos/`:

```
logos/
  index/
    icon.svg / .png              Default (red on transparent)
    icon-on-light.svg / .png     Red content, transparent background
    icon-on-dark.svg / .png      White content, transparent background
    icon-on-red.svg / .png       White content, #A32035 background
    horizontal.svg / .png        Default horizontal lockup
    horizontal-on-light.*        Red content, transparent background
    horizontal-on-dark.*         White content, transparent background
    horizontal-on-red.*          White content, #A32035 background
  initiative/                    (same 16 files)
  repository/                    (same 16 files)
```

**Variant guide:**
- `on-light` / default: Use on white or light backgrounds. Content is `primary` (#A32035).
- `on-dark`: Use on dark backgrounds. Content is white.
- `on-red`: Use where you need a self-contained logo with the brand red background baked in (presentations, documents, social media).

**Horizontal lockup:** Icon | vertical divider | "MIT AI Risk" (Roboto 400) / "**Product Name**" (Roboto 700). Text is rendered as outlined paths (no font dependencies).

Usage:
- Navigation bars: horizontal variant, constrained to roughly 200-250px width
- Favicons / small contexts: icon-only variant
- Title pages / hero sections: any variant at appropriate size
- If a project does not have its own logo, use the Initiative logo.
- PNG icons are 1024x1024. PNG horizontals are 512px tall.

To regenerate logos or create variants (different font, no divider), see `logo_development/README.md`.

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
- `logos/`: production logo files (SVG + PNG), organized by product
- `logo_development/`: build script, fonts, and development variants
- `BRAND.md`: this file
- `SKILL.md`: Claude Code skill wrapper (loads this file as context before generating visual output)
