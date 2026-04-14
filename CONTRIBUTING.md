# Working with the AIRI Brand Kit

A guided tour and cookbook for exploring and adapting the AIRI (MIT AI Risk Initiative) brand. Written for people using AI coding assistants — **Claude Code**, **Codex**, **Cursor**, or similar — to interact with this repository.

> **TL;DR** — Clone the repo, open it in your AI assistant, point it at `skill/BRAND.md`, and then pick a recipe below that matches your situation.

> ### ⚠️ Do not contribute changes via GitHub
>
> This repository does **not** accept branches, feature additions, issues, or pull requests from contributors. GitHub is used for distribution, not collaboration.
>
> If you have a proposed change, bug report, or question about the brand, **contact Jess Graham directly**:
>
> - **Email:** [jgra98@mit.edu](mailto:jgra98@mit.edu)
> - **Slack:** message Jess in the MIT AIRI workspace
>
> Please include rationale, use case, and (if possible) a screenshot or example. Jess will route it to the right place. Do **not** open a GitHub issue or PR — they will not be reviewed.

---

## Who this is for

- **You inherited a project** that uses old AIRI styling and you want to know what's current.
- **You made changes weeks or months ago** and need to reconcile them with what has since landed.
- **You're building something new** and want to apply AIRI branding without reinventing anything.
- **You have a suggestion for the brand itself** and want to raise it with the maintainers (see the callout above — contact Jess Graham; do not open a PR).

You do not need to be a designer. You do need to be comfortable reading diffs and steering an AI assistant through a small number of files.

---

## Orientation

### What lives where

```
airi-brand/
├── skill/                  # ← the authoritative brand kit
│   ├── SKILL.md            # Entry point for Claude Code skills
│   ├── BRAND.md            # Full brand specification (read this first)
│   ├── brand.css           # Drop-in CSS with custom properties
│   ├── tokens.json         # Machine-readable design tokens
│   └── logos/              # SVG + PNG in three product families
│       ├── initiative/     # General AIRI
│       ├── index/          # AI Risk Index
│       └── repository/     # AI Risk Repository
├── brand-guide.html        # Visual brand guide (open in browser)
├── airi-brand-skill.zip    # Upload this to Claude.ai projects
├── README.md               # Quick start for consumers
└── CONTRIBUTING.md         # This file
```

There are **three sources of truth**, and a change to one should usually update all three:

| File | Purpose | Format |
|---|---|---|
| `skill/BRAND.md` | Human-readable spec | Markdown |
| `skill/brand.css` | Runtime CSS | CSS custom properties |
| `skill/tokens.json` | Programmatic tokens | JSON |

If these drift apart, the brand is broken. Internal consistency is the first thing Jess will check when you flag a change.

### The `dev` branch

There is a separate `dev` branch for exploratory work — early iterations, proposed extensions, image style experiments. It contains a `dev/` folder that is gitignored on `main`. Check it out when you want to see what is being prototyped, but do not treat it as the brand:

```bash
git fetch origin
git checkout dev
# explore dev/brand-identity-exploration.html
git checkout main   # go back to the real brand
```

### Before any work

```bash
git fetch origin
git checkout main
git pull
```

Seriously. Most of the "this doesn't match what I have" confusion comes from working off stale clones.

---

## Recipes

Each recipe has (1) the scenario, (2) an AI-assistant prompt you can copy-paste, and (3) what you should expect back. Prompts are written to be tool-agnostic — paste them into Claude Code, Codex, or Cursor unchanged.

### Recipe 1 — Get a guided tour of the current brand

**Scenario:** You're new to AIRI or returning after a break. You want a compact mental model before touching anything.

**Prompt:**
```
Give me a guided tour of the current AIRI brand. Read skill/BRAND.md,
skill/brand.css, and skill/tokens.json. Summarize:

1. The color palette — which colors are brand primary vs. which are
   derived/supplementary, and the intended use of each
2. Typography — font family, weights, size scale
3. Logo system — the three product families and the four color variants
4. Component patterns that are specified (buttons, cards, etc.)
5. Any explicit "do not" rules

Do not make any changes. Output a one-page reference I can skim.
```

**Expect back:** A condensed brand reference, with file:line citations. Use this as your anchor for everything else.

---

### Recipe 2 — Audit an existing file against the current brand

**Scenario:** You have an old HTML page, React component, slide deck, or chart that was styled with some version of the AIRI brand. You want to know how far it has drifted.

**Prompt:**
```
I want you to audit [path/to/my/file] against the current AIRI brand.

Steps:
1. Read skill/BRAND.md and skill/brand.css so you know what "current" means
2. Read my file
3. Produce a categorized report:
   (a) MATCHES — elements that are already on-brand
   (b) DRIFT — specific things that conflict with current brand, with
       the current value and the correct value side by side
   (c) AMBIGUOUS — things I'll need to decide about (e.g., my file uses
       a color that is not in the brand but might be intentional)
   (d) MISSING — brand elements the file doesn't use but probably should
       (e.g., Figtree font, correct logo variant)

Do not edit anything yet. I want the audit first so I can decide what to change.
```

**Expect back:** A report that is actionable without being overwhelming. No changes on disk.

---

### Recipe 3 — Apply the current brand to an outdated file

**Scenario:** You've done Recipe 2, read the audit, and decided you want the drift fixed.

**Prompt:**
```
Based on the audit you just produced, update [path/to/my/file] to match
the current brand.

Rules:
- Preserve all content and structure. Only change presentation.
- Only fix items in the DRIFT and MISSING categories
- Leave AMBIGUOUS items alone unless I explicitly ask
- Show me a diff before writing anything to disk
- If you are going to make more than a handful of changes, group them
  into small logical chunks so I can review each one
```

**Expect back:** A diff, then (after you approve) the file updated in place. Do not let it rewrite the content or "improve" the prose.

---

### Recipe 4 — Apply the brand to a brand-new artifact

**Scenario:** You're creating something from scratch — a report, a landing page, a figure for a paper, a slide deck.

**Option A — Claude Code or Cursor with the skill installed:**

If you've installed the `skill/` folder as a Claude Code skill (see `README.md`), just mention AIRI in your prompt and it will auto-trigger. You can also invoke it explicitly with `/airi-brand`.

**Option B — any AI assistant:**

```
I'm building [thing]. Before you generate anything, read skill/BRAND.md
and skill/brand.css. Then create [thing] using ONLY the brand's colors,
typography, and component patterns. Reference brand.css as a stylesheet
if the output supports it.

Do not invent new colors or fonts. If you need a color that isn't in
the brand, tell me and stop — we'll decide together.
```

**Option C — Claude.ai web UI:**

Upload `airi-brand-skill.zip` as a project knowledge file. Claude will apply AIRI branding automatically to visual output in that project.

---

### Recipe 5 — Experiment locally without affecting anyone else

**Scenario:** You want to try a variant of the brand to see if it works for your use case. You're not sure yet whether it should influence the brand at all.

**Approach:**
1. Work in your local clone. Do **not** push a branch to GitHub — this repo does not accept contributor branches.
2. Put working files in `dev/` — that folder is gitignored on `main`, so nothing will leak back.
3. Track your rationale in a short note (`dev/NOTES.md`) so you can explain the experiment later.
4. Pull from `main` occasionally to stay current: `git pull origin main`

If the experiment turns into something you think the brand should adopt, jump to Recipe 7 — you'll send it to Jess, not push a branch.

---

### Recipe 6 — Reconcile a divergent local copy

**Scenario:** You (or a colleague) made changes to the brand weeks or months ago in a local copy or fork. Since then the brand has moved on. You need to figure out what's in, what's out, and what's worth flagging to Jess.

**Prompt:**
```
Compare my local copy against origin/main for the skill/ folder only.
For every divergence, categorize it:

(a) UPSTREAM WINS — main has evolved past mine; I should discard my
    version and take main's
(b) MINE IS A LEGITIMATE EXTENSION — something I added that does not
    conflict with main; worth raising with Jess as a possible brand change
(c) CONFLICT — both sides changed the same thing in incompatible ways;
    needs human judgment
(d) UNRELATED — changes in files that have nothing to do with each other

For each item, show me: the file, a short description, and which bucket
it's in. Do not attempt to resolve anything yet.

When you're done, also tell me whether skill/BRAND.md, skill/brand.css,
and skill/tokens.json are still internally consistent on my copy. If
they've drifted apart on my side, flag it.
```

**Expect back:** A reconciliation worksheet. Walk through it with the assistant one item at a time. Anything that ends up in bucket (b) goes to Jess (Recipe 7), not a GitHub PR.

---

### Recipe 7 — Propose a change to the brand

**Scenario:** You've used the brand in anger and you're convinced something should change — a missing color, a component pattern, a rule that's causing pain. You'd like the brand itself to evolve.

> **Reminder:** this repo does **not** accept GitHub branches, issues, or pull requests. All proposals go to Jess Graham — [jgra98@mit.edu](mailto:jgra98@mit.edu) or Slack.

**What Jess needs in order to act on a proposal:**

1. **Rationale.** What specific problem does this solve? Name the use case.
2. **Scope.** One concept per proposal. If you want to add an extended palette *and* new components, that's two separate messages.
3. **Compatibility.** Does this break existing consumers? If so, what's the migration story?
4. **Evidence.** Screenshots, before/after, or a link to the artifact that pushed you to propose this.
5. **Consistency (if you've drafted the change).** If you've already edited files locally, make sure `BRAND.md`, `brand.css`, and `tokens.json` are aligned — inconsistency is the first thing that will get the proposal bounced back.

**Workflow:**

1. **Draft the proposal locally (optional but helpful).** Edit the files on your machine so you can show Jess exactly what you have in mind. Use the prompt below.
2. **Package it for Jess.** A short email or Slack message with the summary, rationale, and (if drafted) a diff or a zip of the edited files. You can also link to a local branch visible to Jess if you share a workstation.
3. **Do not push a branch, open an issue, or open a PR on GitHub.** They will not be reviewed.

**Prompt for drafting the change locally:**
```
I want to propose [change] to the AIRI brand. The rationale is: [why].

Before writing anything, read skill/BRAND.md, skill/brand.css, and
skill/tokens.json so you understand the current state.

Then make the minimum edits required to implement the change across
ALL THREE files consistently. Keep the tone and structure of BRAND.md
matching what's already there. Update any "do not" rules if the proposal
changes them.

After the edits, produce a short write-up I can send to Jess with:
- Summary (2-3 sentences)
- Rationale (why this, why now, what it unlocks)
- What changed (per file)
- Compatibility notes
- Anything Jess should sanity-check

Give me the write-up as plain text I can paste into an email or Slack,
plus a unified diff of the file changes. Do NOT attempt to commit or push.
```

---

## Common gotchas

- **The three sources of truth must stay in sync.** `BRAND.md`, `brand.css`, and `tokens.json` are all authoritative. If you edit one, edit the others. AI assistants will sometimes only update one — check before committing.
- **Logos are generated, not hand-drawn.** If a logo needs changing, the tooling lives in a separate repo ([airi-logo-development](https://github.com/MIT-FutureTech/airi-logo-development) if it exists). Do not hand-edit SVGs in `skill/logos/`.
- **The `skill/` folder is a Claude Code skill.** Do not rename it or move its contents around. Skills are located by path.
- **The `dev/` folder is gitignored on `main`** and tracked on `dev`. If you put experimental work in `dev/` on `main`, it will stay local — that is the feature, not a bug.
- **Do not introduce new brand colors casually.** `BRAND.md` has an explicit rule against this. If you need a color that isn't there, raise it with Jess (Recipe 7), don't sneak it in.
- **Use opacity for lighter fills**, not new colors. `rgba(163, 32, 53, 0.1)` is the pattern for "light red background."
- **When in doubt about a file's purpose**, ask your AI assistant to read `README.md` + `skill/SKILL.md` before anything else.

---

## Getting help

**All paths go through Jess Graham — [jgra98@mit.edu](mailto:jgra98@mit.edu) or Slack.** Do not open GitHub issues or PRs.

- **Questions about the current brand** → email or Slack Jess. Include which file you were looking at.
- **Proposing a change** → see Recipe 7. Draft locally if you can, then send the write-up and diff to Jess.
- **Bug in the brand kit itself** (broken CSS, wrong token, stale asset) → email or Slack Jess with the file and a short description of the problem.
- **Wondering if someone has already proposed the same thing** → ask Jess. Proposals are tracked outside GitHub.

---

## A note on AI-assisted contributions

This cookbook assumes you're working with an AI assistant. A few principles that will save you time:

- **Always have the assistant read the spec before it writes code.** The brand is small enough to fit in context; there is no excuse for a blind edit.
- **Ask for a diff before any write.** "Show me the diff first" is the most valuable sentence in this workflow.
- **Do not delegate judgment calls.** "Based on your audit, fix everything" is how drift gets introduced, not removed. Walk through the audit, make the calls yourself, and *then* ask for edits.
- **Review the three-file consistency explicitly.** Assistants are not reliable at remembering to keep `BRAND.md`, `brand.css`, and `tokens.json` aligned unless you tell them to.
- **Keep proposals small.** One concept per message to Jess. Bundling an extended palette *and* new components together will just slow things down — split them.
