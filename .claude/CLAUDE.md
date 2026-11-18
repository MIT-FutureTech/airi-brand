# AIRI Brand Kit

The visual brand of the MIT AI Risk Initiative (AIRI), and a Claude skill that applies it. Public repo in the MIT-FutureTech org. README.md is the overview for people; CONTRIBUTING.md explains how the pieces depend on each other.

## Layout

```
skill/                 the brand kit; also a Claude skill (path-sensitive: don't rename)
  BRAND.md             full spec: colour system, type scales, logo rules, a section per medium
  SKILL.md             skill entry point: hard rules, defaults, the rule for gaps, swatches
  tokens.json          every value; the source the generated files are built from
  brand.css            CSS custom properties, light and opt-in dark (generated)
  templates/           a starting file per tool: Office theme XML, Google set-up, Tailwind,
                       Claude artifact, matplotlib, Plotly, R, LaTeX (generated)
  templates/video/     video styles, sample composition and captions (generated); check_video.py and
                       fonts/ are the only hand-kept files in templates/
  logos/initiative/    the AIRI icon + horizontal logo, 4 variants, SVG + PNG
  logos/futuretech/    MIT FutureTech parent logo, 4 variants, SVG (traced from FutureTech's PNG)
guide/index.html       one-page visual guide (generated); guide/logos and guide/brand.css are symlinks into skill/
airi-brand-skill.zip   skill/ zipped for Claude.ai upload
dev/build-kit/         build.py generates brand.css, templates/ and the guide from tokens.json; --check verifies
                       (guide.py is the guide, viz.py its charts, video.py the motion and video files)
dev/logo-builder/      build.py generates skill/logos/initiative/ (output/ is gitignored)
legacy/logos/          retired Index and Repository lockups
install/               git hooks that keep ~/.claude/skills/airi-brand in sync with skill/ on main
```

## Facts that aren't obvious from the files

- **One AIRI logo.** The Index and Repository lockups were retired in October 2026; both products use the Initiative logo.
- **Three reds.** AIRI primary `#A32035`. MIT institutional red `#750014`. FutureTech logo red `#9A2030`, used only inside that logo.
- **Three files must agree, and one is the source.** Edit `skill/tokens.json`, run `python3 dev/build-kit/build.py` (rewrites brand.css, templates/ and the guide), update BRAND.md and SKILL.md by hand, then run `python3 dev/build-kit/build.py --check`. Never hand-edit a generated file.
- **The palette (kit 2.0, November 2026).** One red `#A32035` with a fixed ramp and two tints. Two text colours, ink `#1A1A1A` and muted `#666666`; gray `#898A8D` is for graphics only. Four of the greys (muted, rule, border, fill) are Google presets; ink, chart gray and background are not. Red text uses the `link` token and red fills use `primary`, because only `link` changes in dark mode. Blue `#2171B5` is the one second colour. Data colour has fixed meanings: red is the subject or more risk, grey is context, blue is an amount; seven category colours that never include red; status colours; a provisional dark mode.
- **Red headings stop at the top level.** Slide titles, the document Title and Heading 1, and the page h1 are red. Everything below is ink.
- **Rules come in three tiers (team review, November 2026).** Seven hard rules that always hold, listed in `tokens.json` under `rules.hard` and word for word in BRAND.md section 2 and SKILL.md. Everything else is a default: Claude follows it unless a person asks for something different, and then does what they ask without arguing. Where the kit says nothing, Claude reuses the closest pattern or picks the most neutral option, never a new treatment, and reports the gap. Keep the hard list short; a new rule is a default unless the team says otherwise.
- **Checkers follow the tiers.** `check_video.py` fails on a hard-rule breach or a broken file and warns on a changed default. Keep that split when adding a check.
- **Decided and open items live in `tokens.json` under `decisions`.** The guide's open questions are generated from it, and BRAND.md section 15 lists the same items by hand. Still open: which seven colours the risk domains get (the policy is settled: a default for new work only, no retrofitting, a person can set it aside for a figure), and the speed and style of the logo build.
- **Motion has two registers.** Interface motion is IBM Carbon's productive set (70 to 700 ms), exposed in `brand.css`. Video motion is Carbon's expressive curves at 400, 700 and 1000 ms, in `templates/video/airi-video.css`. Transitions are conventional. Square-step transitions (the red-square wipe, the stepped title reveal) were dropped; do not rebuild them. The logo build from the icon's squares stays as the one logo animation, with interim timing in `motion.logo-build`.
- **The video templates sit on the `generate-video` skill's template.** `stage.js` and `stage.css` are copied from that skill when a video is started; they are not in this repo. `airi-video.css` holds no time or curve of its own outside its tokens block, and `--check` enforces that.
- **The zip goes stale silently.** Rebuild it after any change to `skill/`: `rm airi-brand-skill.zip && zip -rq airi-brand-skill.zip skill/`
- **The installed skill is a copy kept in sync by git hooks.** `install/install-hooks.sh` adds post-commit and post-merge hooks that mirror the committed `skill/` into `~/.claude/skills/airi-brand` whenever `main` changes it (other branches are skipped). The copy must stay a plain folder, not a symlink, because a Syncthing share carries it to other machines. Re-run the installer after a fresh clone; run `install/sync-installed-skill.sh --force` to sync by hand.
- **Logo proportions are fixed.** In the horizontal lockup, the icon-to-text gap and the right padding each equal one large square of the icon. The text spans the two medium squares: cap-top of "MIT AI Risk" on the top of the upper one, baseline of "Initiative" on the bottom of the lower one, line spacing 1.0. build.py computes all of this from the icon geometry.
- **The builder needs its venv.** `cd dev/logo-builder && python3 -m venv venv && venv/bin/pip install -r requirements.txt && venv/bin/python build.py`, then copy `output/initiative/` over `skill/logos/initiative/`.

## The guide

`guide/index.html` is generated by `dev/build-kit/guide.py`; edit that file, not the HTML. The hard rules sit at the top, generated from `tokens.json`. Section order after that, most important first: 1 Logo, 2 Icon, 3 Font & colour, 4 Parent organisation logo (FutureTech), 5 Open questions (collapsed `<details>`, generated from `decisions.open`). Every logo cell has SVG/PNG download links. Load assets through the `logos/` symlink, never as base64. Component patterns and file references belong in BRAND.md, not the guide. The repo is public: the guide shows only illustrative data, never screenshots of real work.

## Working here

- Questions and proposals come in as GitHub issues. Changes have gone in through short-lived branches and PRs; there is no long-lived `dev` branch.
- `.claude/settings.local.json` and `.claude/launch.json` are per-machine and gitignored.
