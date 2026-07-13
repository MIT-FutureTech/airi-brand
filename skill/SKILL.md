---
name: airi-brand
description: |
  Apply AIRI (MIT AI Risk Initiative) visual branding to generated output.
  Use when creating HTML, React, SVG, CSS, charts, presentations, or any
  visual artifact for AIRI projects. Triggers on mentions of AIRI, AI Risk
  Repository, AI Risk Index, AI Risk Initiative, airisk.mit.edu, or requests
  to style or brand outputs for these projects.
allowed-tools: Read, Glob
---

# AIRI Brand Skill

Before generating any visual output for an AIRI project, read and apply the brand specification.

## Setup

1. Read [BRAND.md](BRAND.md) for the full specification including colors, typography, logos, and component patterns.
2. Read [tokens.json](tokens.json) for exact color, typography, spacing, and radius values.
3. Use [brand.css](brand.css) directly if the output supports CSS imports, or replicate the custom properties.

## Quick reference

**Colors:**
- Primary (AIRI red): `#A32035`
- Primary light: `#D07886`
- Primary dark: `#5E0E20`
- Text: `#1A1A1A`
- Muted: `#898A8D`
- Background: `#FAFAFA`
- White: `#FFFFFF`

**Font:** Figtree (Google Fonts), weights 400/600/700. Fallback: `sans-serif`.

**Logos:** One shared icon, three horizontal lockups that only differ in the second line of the wordmark. Organized by product under `logos/`:

- `logos/initiative/` — for general AIRI projects. Lockup reads "MIT AI Risk / **Initiative**".
- `logos/index/` — for AI Risk Index pages. Lockup reads "MIT AI Risk / **Index**".
- `logos/repository/` — for AI Risk Repository pages. Lockup reads "MIT AI Risk / **Repository**".

Each folder contains:

- `icon.*` — square mark (the "plus of squares" composition). **Identical across all three folders** — a single icon serves every product.
- `horizontal.*` — icon + two-line wordmark lockup for that product.

Each comes in four colour variants:
- Default / `-on-light` — red content, transparent background (for light backgrounds)
- `-on-dark` — white content, transparent background (for dark backgrounds)
- `-on-red` — white content, `#A32035` background (self-contained, for documents/slides)

Available as both SVG and PNG. PNGs are 1024px (icons) or 512px tall (horizontal). If a project doesn't have its own horizontal, use `logos/initiative/`.

## Rules

1. Always use the AIRI color palette. Do not introduce other brand colors.
2. Always load Figtree from Google Fonts (or reference it if already available).
3. Use the appropriate product folder's horizontal lockup: `initiative/` for general AIRI work, `index/` for AI Risk Index, `repository/` for AI Risk Repository. The icon is the same in every folder — do not invent new icons or modified variants.
4. For interactive sites: import or inline the CSS custom properties from `brand.css`.
5. For charts: use the data visualization color sequence from BRAND.md.
6. For slide decks: use `primary` as the accent color, Figtree as the font.
7. Keep it simple. The brand is minimal: red, dark, gray, white, one font. Consistency matters more than elaboration.
