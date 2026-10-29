# AIRI Brand Kit

The visual identity of the MIT AI Risk Initiative (AIRI): logo, icon, colours and font, plus a Claude skill that applies them to generated work. Use it for all AIRI work, including the AI Risk Repository and the AI Risk Index.

## Start here

- **See the brand:** open [guide/index.html](guide/index.html) in a browser. It shows the logo, icon, font, palette and the MIT FutureTech parent logo on one page, with download links for each file.
- **Get the logo files:** [skill/logos/initiative/](skill/logos/initiative/) has the AIRI icon and horizontal logo as SVG and PNG. [skill/logos/futuretech/](skill/logos/futuretech/) has the FutureTech logo for co-branded materials.
- **Read the full spec:** [skill/BRAND.md](skill/BRAND.md) covers colours, typography, logo usage and component patterns (buttons, cards, tables, charts).
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
| `skill/` | The brand kit itself: `BRAND.md` (spec), `SKILL.md` (Claude skill entry point), `brand.css` (CSS custom properties), `tokens.json` (design tokens), `logos/` |
| `guide/` | The one-page visual guide. `guide/logos` and `guide/brand.css` link back into `skill/`, so the guide always shows the current files |
| `airi-brand-skill.zip` | `skill/` packaged for upload to Claude.ai |
| `dev/logo-builder/` | The Python script that generates the AIRI logo files (see its README) |
| `legacy/logos/` | Retired Index and Repository logos. Don't use them for new work |
