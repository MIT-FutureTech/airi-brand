# AIRI Brand Kit

Visual identity assets for the MIT AI Risk Initiative (AIRI), AI Risk Index, and AI Risk Repository.

## Quick start

- **Visual brand guide:** open **[guide/index.html](guide/index.html)** in a browser, or view it online at **[labs.aksaeri.com/airi/brand/](https://labs.aksaeri.com/airi/brand/)** — one logo, one icon, the palette, font, and sub-product lockups on a single page
- Browse **[skill/logos/](skill/logos/)** for SVG and PNG logo files (`initiative/`, `index/`, `repository/`)
- Read **[skill/BRAND.md](skill/BRAND.md)** for the full specification (colours, typography, component patterns)
- Read **[CONTRIBUTING.md](CONTRIBUTING.md)** for a guided tour and cookbook — especially if you're auditing old work, reconciling a divergent fork, or proposing changes with an AI assistant (Claude Code, Codex, Cursor)

## Using with Claude

### Upload to Claude.ai

Download **[airi-brand-skill.zip](airi-brand-skill.zip)** and upload it to a Claude conversation as a project knowledge file. Claude will automatically apply AIRI branding when generating HTML, CSS, charts, or other visual output.

### Claude Code skill

The `skill/` folder is a self-contained Claude Code skill. To install:

```bash
# Personal (all projects)
ln -s /path/to/this/repo/skill ~/.claude/skills/airi-brand

# Or project-specific
ln -s /path/to/this/repo/skill .claude/skills/airi-brand
```

Claude will auto-trigger the skill when working on AIRI projects. You can also invoke it manually with `/airi-brand`.

## What's in the skill

| File | Purpose |
|------|---------|
| `skill/SKILL.md` | Skill entry point — triggers, instructions, quick reference |
| `skill/BRAND.md` | Full brand specification — colors, typography, logos, component patterns |
| `skill/brand.css` | CSS custom properties, ready to import |
| `skill/tokens.json` | Machine-readable design tokens |
| `skill/logos/` | SVG + PNG logos — one shared icon, three horizontal lockups (`initiative/`, `index/`, `repository/`) |

## Logo variants

Each product folder (`initiative/`, `index/`, `repository/`) has an icon and a horizontal lockup in four colour variants. The icon is byte-identical across the three folders — only the horizontal lockup differs in its second wordmark line:

| Variant | Use case |
|---------|----------|
| default / `-on-light` | Light backgrounds (red content, transparent bg) |
| `-on-dark` | Dark backgrounds (white content, transparent bg) |
| `-on-red` | Self-contained with #A32035 background (documents, slides) |

## Logo development

The build tooling for regenerating logos lives in **[dev/logo-builder/](dev/logo-builder/)**. Run `python build.py` from a venv with the requirements installed, and the full set of icon + horizontal variants is emitted to `output/{initiative,index,repository}/`. To add a new product lockup, edit the `PRODUCTS` list at the top of `build.py`.
