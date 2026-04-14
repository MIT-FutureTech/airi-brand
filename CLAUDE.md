# AIRI Brand Kit — AI assistant briefing

Briefing for Claude Code, Codex, Cursor, or any AI coding assistant working in this repository. Start here, then read `skill/BRAND.md` for the full specification and `CONTRIBUTING.md` for recipes.

## Purpose

This repo is the **distribution** of the MIT AI Risk Initiative visual brand — logos, typography, colours, component patterns, and a Claude Code skill that applies them to generated output. It is **not** collaborative: there are no issues, PRs, or contributor branches. All proposals go to Jess Graham (jgra98@mit.edu).

## Structure

```
airi-brand/
├── skill/                  authoritative brand kit (do not move/rename)
│   ├── BRAND.md            full spec — colours, typography, logos, components
│   ├── SKILL.md            Claude Code skill entry point
│   ├── brand.css           CSS custom properties
│   ├── tokens.json         machine-readable design tokens
│   └── logos/              one shared icon, three horizontal lockups
│       ├── initiative/         MIT AI Risk / Initiative
│       ├── index/              MIT AI Risk / Index
│       └── repository/         MIT AI Risk / Repository
├── guide/                  visual brand guide (labs target + clone entry)
│   ├── index.html              the one-page guide — see section below
│   ├── logos → ../skill/logos  symlink, do not replace with copy
│   ├── brand.css → ../skill/brand.css
│   └── project.yaml            labs-publish metadata
├── dev/                    exploratory work (tracked, not a branch)
│   ├── logo-builder/           Python builder for the logos
│   └── brand-identity-exploration.html
├── legacy/logos/           retired pre-consolidation sub-brand logos
├── airi-brand-skill.zip    packaged skill/ for Claude.ai web uploads
├── CLAUDE.md               this file
├── CONTRIBUTING.md         guided tour and recipes for AI-assisted work
└── README.md               quick start for consumers
```

## Branch model

**`main` is the only branch.** Do not create `dev`, feature branches, or long-lived branches. Exploratory work goes in the `dev/` folder on main. An earlier two-branch scheme caused cherry-pick overhead and labs-serving bugs — don't bring it back.

## The three sources of truth

When you change anything about the brand tokens (colours, spacing, typography, radii), update **all three** in the same commit:

1. `skill/BRAND.md` — human-readable spec
2. `skill/brand.css` — runtime CSS custom properties
3. `skill/tokens.json` — programmatic tokens

If they drift apart, the kit is broken. This is the first thing Jess checks on any proposal.

## Three things that must stay consistent

Any change to the brand surface needs all three to move together:

1. **The skill** (`skill/BRAND.md`, `skill/brand.css`, `skill/tokens.json`, `skill/logos/`)
2. **The visual brand guide** (`guide/index.html`)
3. **The Claude.ai upload bundle** (`airi-brand-skill.zip`) — regenerate with `rm airi-brand-skill.zip && zip -rq airi-brand-skill.zip skill/` any time `skill/` changes

## The visual brand guide — `guide/index.html`

The guide is a single self-contained HTML page that renders both locally (double-click) and on labs (`https://labs.aksaeri.com/airi/brand/`). It is **deliberately prioritised** — the order of sections matters, because this is often the first thing a new collaborator sees.

**Required section order:**

1. **Logo** — the Initiative horizontal lockup in all four colour variants (on-light / default / on-dark / on-red). This is the primary mark; everything else supports it.
2. **Icon** — the shared icon in all four variants. Call out that the icon is the same across Initiative / Index / Repository.
3. **Font & colour** — Figtree weights 400 / 600 / 700 (with samples), then the seven-colour palette with tokens and usage.
4. **Sub-project lockups** — compact presentations of the Index and Repository horizontal lockups. Lower visual priority than sections 1–3: denser layout, single row per product. Explain that they share the icon and the first wordmark line with the Initiative.
5. **Open questions** — proposed extensions in `<details>` elements so they don't dominate. Tag each (`proposed`, `under review`, `out of scope`).

**Do not add sections** for component patterns, file references, or tooling in the guide — those belong in `skill/BRAND.md` and `README.md`. The guide is a visual introduction, not a comprehensive reference. Link out from the footer.

**Assets** in the guide must be loaded via the `logos/` and `brand.css` symlinks (`logos/initiative/horizontal-on-light.svg`, etc.) — **never** embed base64 or duplicate files. The symlinks keep the guide in sync with the source automatically.

**Footer** should link back to `skill/BRAND.md` for the full spec and `CONTRIBUTING.md` for the working recipes, plus the contributing note pointing to Jess.

## Labs publishing

The guide is served at `https://labs.aksaeri.com/airi/brand/` via a symlink:

```
/home/alex/projects-server/labs/projects/airi/brand → /home/alex/projects/GitHub/airi/airi-brand/guide
```

The symlink points at `guide/`, not the repo root. That keeps `.git/`, `dev/`, `node_modules/`, and the rest out of the served surface. Do not repoint it at the repo root. Do not add `project.yaml` files anywhere outside `guide/` — the labs walker follows symlinks with `followlinks=True` and will list any `project.yaml` it finds under the published subtree.

## Logos

One shared icon lives in `skill/logos/initiative/icon*.svg`. The `index/` and `repository/` folders contain byte-identical copies so that consumers can grab one folder and have a complete set. **Do not modify the icon per product** — it is a single design.

Horizontal lockups differ only in the second wordmark line:

- `initiative/horizontal*.svg` — "MIT AI Risk / Initiative"
- `index/horizontal*.svg` — "MIT AI Risk / Index"
- `repository/horizontal*.svg` — "MIT AI Risk / Repository"

All three are regenerated by `dev/logo-builder/build.py`. To add or rename a product, edit the `PRODUCTS` list at the top of `build.py` and re-run. Text is rendered as outlined SVG paths, so the files have no font dependency.

Lockup proportions are locked after the `dev/logo-builder/output/variants/` comparison — do not change them without talking to Jess. The rules:

- Gap between icon and text = one "large square" (L-square) from the icon
- Text is pinned so the cap-top of "MIT AI Risk" sits on the top edge of the upper medium square (M1) and the baseline of the second line sits on the bottom edge of the lower medium square (M4)
- Line-spacing ratio = 1.0 (tight)
- Right padding = one L-square (symmetric with the left gap)

## Rules for visual output you generate

1. Use the AIRI colour palette only. No new brand colours. Opacity variants of `primary` (`rgba(163, 32, 53, 0.1)` etc.) are the right move for lighter fills.
2. Load Figtree from Google Fonts, with `sans-serif` fallback. No other brand fonts.
3. Pick the matching logo folder: `initiative/` for general AIRI work, `index/` for AI Risk Index, `repository/` for AI Risk Repository. Default to `initiative/` when in doubt.
4. For interactive sites: import or inline `skill/brand.css`.
5. For charts: use `primary`, `primary-light`, `gray`, `dark` as the data-visualisation sequence (in that order). Derive extras from opacity variants, not new hues.
6. Keep it simple. The brand is minimal: red, dark, gray, white, one font. Consistency matters more than elaboration.

## Common mistakes to avoid

- **Editing only one of the three sources of truth.** The brand breaks if BRAND.md, brand.css, and tokens.json drift apart.
- **Hand-editing SVGs in `skill/logos/`.** Use `dev/logo-builder/build.py` and copy the output.
- **Embedding assets in `guide/index.html` as base64.** Use the `logos/` symlink. The earlier guide was 700 KB of base64 and impossible to edit — don't regress.
- **Forgetting to regenerate `airi-brand-skill.zip`** after touching `skill/`. The Claude.ai web upload will serve stale content until you do.
- **Adding a `project.yaml` outside `guide/`.** Labs auto-discovery will pick it up and list it under `/airi/brand/...` in the category index.
- **Creating a `dev` or feature branch.** Work on `main`, always.

## Getting help

Do not open GitHub issues or PRs — the repo is distribution-only. For brand questions, change proposals, or bug reports, contact **Jess Graham** (jgra98@mit.edu, or Slack in the AIRI workspace). Include which files you were looking at and, if possible, a screenshot.
