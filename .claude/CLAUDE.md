# AIRI Brand Kit

The visual brand of the MIT AI Risk Initiative (AIRI), and a Claude skill that applies it. Public repo in the MIT-FutureTech org. README.md is the overview for people; CONTRIBUTING.md explains how the pieces depend on each other.

## Layout

```
skill/                 the brand kit; also a Claude skill (path-sensitive: don't rename)
  BRAND.md             full spec: colours, type, logo usage, component patterns
  SKILL.md             skill entry point and quick reference
  brand.css            CSS custom properties
  tokens.json          design tokens
  logos/initiative/    the AIRI icon + horizontal logo, 4 variants, SVG + PNG
  logos/futuretech/    MIT FutureTech parent logo, 4 variants, SVG (traced from FutureTech's PNG)
guide/index.html       one-page visual guide; guide/logos and guide/brand.css are symlinks into skill/
airi-brand-skill.zip   skill/ zipped for Claude.ai upload
dev/logo-builder/      build.py generates skill/logos/initiative/ (output/ is gitignored)
legacy/logos/          retired Index and Repository lockups
```

## Facts that aren't obvious from the files

- **One AIRI logo.** The Index and Repository lockups were retired in October 2026; both products use the Initiative logo.
- **Three reds.** AIRI primary `#A32035`. MIT institutional red `#750014`. FutureTech logo red `#9A2030`, used only inside that logo.
- **Three files must agree.** BRAND.md, brand.css and tokens.json all define the tokens. A token change touches all three.
- **The zip goes stale silently.** Rebuild it after any change to `skill/`: `rm airi-brand-skill.zip && zip -rq airi-brand-skill.zip skill/`
- **The installed skill is a separate copy.** `~/.claude/skills/airi-brand` on Alexander's machine is not linked to this repo; changes here don't reach it automatically.
- **Logo proportions are fixed.** In the horizontal lockup, the icon-to-text gap and the right padding each equal one large square of the icon. The text spans the two medium squares: cap-top of "MIT AI Risk" on the top of the upper one, baseline of "Initiative" on the bottom of the lower one, line spacing 1.0. build.py computes all of this from the icon geometry.
- **The builder needs its venv.** `cd dev/logo-builder && python3 -m venv venv && venv/bin/pip install -r requirements.txt && venv/bin/python build.py`, then copy `output/initiative/` over `skill/logos/initiative/`.

## The guide

Section order, most important first: 1 Logo, 2 Icon, 3 Font & colour, 4 Parent organisation logo (FutureTech), 5 Open questions (collapsed `<details>`). Every logo cell has SVG/PNG download links. Load assets through the `logos/` symlink, never as base64. Component patterns and file references belong in BRAND.md, not the guide.

## Working here

- Questions and proposals come in as GitHub issues. Changes have gone in through short-lived branches and PRs; there is no long-lived `dev` branch.
- `.claude/settings.local.json` and `.claude/launch.json` are per-machine and gitignored.
