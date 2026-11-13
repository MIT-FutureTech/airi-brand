# AIRI Brand Kit

The visual identity of the MIT AI Risk Initiative (AIRI): logo, icon, colours and font, with ready-made files for each tool and a Claude skill that applies them. Use it for all AIRI work, including the AI Risk Repository and the AI Risk Index.

## The brand in five rules

1. One red: `#A32035`. Take it from a theme, template or token; never retype it.
2. Two text colours: ink `#1A1A1A` and muted `#666666`. White on red or dark.
3. In data, red is the subject, the finding or more risk. Grey `#898A8D` is context. Blue `#2171B5` is a neutral amount.
4. A figure uses a red scale or a red highlight, never both.
5. Figtree for all text.

## Start here

- **See the brand:** open [guide/index.html](guide/index.html) in a browser. It shows the logo, icon, font, palette, chart colours and the MIT FutureTech parent logo on one page, with download links.
- **Get a starting file for your tool:** [skill/templates/](skill/templates/README.md) has theme colours and fonts for PowerPoint and Word, set-up steps for Google Slides, Sheets and Docs, and palette files for CSS, Tailwind, matplotlib, Plotly, R and LaTeX.
- **Get the logo files:** [skill/logos/initiative/](skill/logos/initiative/) has the AIRI icon and horizontal logo as SVG and PNG. [skill/logos/futuretech/](skill/logos/futuretech/) has the FutureTech logo for co-branded materials.
- **Read the full spec:** [skill/BRAND.md](skill/BRAND.md) covers colour (including charts, status and dark mode), type sizes, logo rules, and a section for each medium: slides, documents, website, interactive tools, papers and Claude artifacts.
- **Ask a question or propose a change:** open a [GitHub issue](https://github.com/MIT-FutureTech/airi-brand/issues). See [CONTRIBUTING.md](CONTRIBUTING.md).

## Logo variants

Every logo comes in four colour variants:

| File | Use on |
|------|--------|
| default / `-on-light` | White or light backgrounds (red logo, transparent background) |
| `-on-dark` | Dark backgrounds (white logo, transparent background) |
| `-on-red` | Anywhere you need a self-contained logo (white logo on brand red) |

## Using the brand with Claude

In Claude.ai, upload [airi-brand-skill.zip](airi-brand-skill.zip) as a skill or project file. Claude will apply AIRI branding to HTML, charts, slides and other visual output.

In Claude Code, the `skill/` folder works as a skill on its own. Link it into your skills folder:

```bash
# For all your projects
ln -s /path/to/airi-brand/skill ~/.claude/skills/airi-brand

# For one project
ln -s /path/to/airi-brand/skill .claude/skills/airi-brand
```

Claude Code picks it up when you mention AIRI, the Repository or the Index. You can also run `/airi-brand`.

## What's in the repo

| Path | What it is |
|------|------------|
| `skill/` | The brand kit itself: `BRAND.md` (spec), `SKILL.md` (Claude skill entry point), `tokens.json` (every value), `brand.css` (CSS custom properties), `templates/` (a starting file per tool), `logos/` |
| `guide/` | The one-page visual guide. `guide/logos` and `guide/brand.css` link back into `skill/` |
| `airi-brand-skill.zip` | `skill/` packaged for upload to Claude.ai |
| `dev/build-kit/` | `build.py` generates `brand.css`, the templates and the guide from `tokens.json`, and checks that everything agrees |
| `dev/logo-builder/` | The Python script that generates the AIRI logo files (see its README) |
| `legacy/logos/` | Retired Index and Repository logos. Don't use them for new work |
