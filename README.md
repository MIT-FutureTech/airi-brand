# AIRI Brand Kit

Visual identity assets for the MIT AI Risk Initiative (AIRI), AI Risk Index, and AI Risk Repository.

## Quick start

- Open **[brand-guide.html](brand-guide.html)** in a browser for a visual overview (self-contained, shareable)
- Browse **[skill/logos/](skill/logos/)** for SVG and PNG logo files

## Using as a Claude Code skill

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
| `skill/logos/` | SVG + PNG logos for Index, Initiative, and Repository |

## Logo variants

Each product (index, initiative, repository) has icon and horizontal layouts in four color variants:

| Variant | Use case |
|---------|----------|
| default / `-on-light` | Light backgrounds (red content, transparent bg) |
| `-on-dark` | Dark backgrounds (white content, transparent bg) |
| `-on-red` | Self-contained with #A32035 background (documents, slides) |

## Logo development

The build tooling for regenerating logos (font changes, layout tweaks, etc.) lives in a separate repository. See [airi-logo-development](https://github.com/MIT-FutureTech/airi-logo-development) if it exists, or ask the maintainer.
