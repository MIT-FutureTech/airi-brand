"""The one-page visual guide (guide/index.html), rendered from tokens.json.

build.py calls render(). The hard rules come first, from tokens.json. Section order
after that is fixed: logo, icon, font and colour, parent organisation logo, open questions.
"""
import viz as v
from viz import C, D, CATS, S, T, KIT

OUT = KIT / "guide" / "index.html"
TY = T["typography"]
GH = "https://github.com/MIT-FutureTech/airi-brand"


def logo_cell(kind, folder, name, cls, png=True, h=None):
    style = f' style="height:{h}px"' if h else ""
    links = f'<a href="logos/{folder}/{name}.svg" target="_blank" rel="noopener">SVG</a>'
    if png:
        links += f'<a href="logos/{folder}/{name}.png" target="_blank" rel="noopener">PNG</a>'
    return (f'<div class="logo-cell {kind}"><img class="{cls}" src="logos/{folder}/{name}.svg" alt="{name}"{style}>'
            f'<span class="label">{name}</span><div class="asset-links">{links}</div></div>')


def logo_grid(folder, stem, cls, png=True, h=None):
    cells = [("light", f"{stem}-on-light"), ("light", stem), ("dark", f"{stem}-on-dark"), ("red", f"{stem}-on-red")]
    return '<div class="logo-grid">' + "".join(logo_cell(k, folder, n, cls, png, h) for k, n in cells) + "</div>"


core = [(C["primary"], "AIRI red", "primary"), (C["primary-hover"], "Red hover", "primary-hover"),
        (C["primary-dark"], "Red dark", "primary-dark"), (C["primary-light"], "Red light", "primary-light"),
        (C["red-tint"], "Red tint", "red-tint"), (C["red-wash"], "Red wash", "red-wash"),
        (C["text"], "Ink", "text"), (C["text-muted"], "Muted", "text-muted"), (C["gray"], "Gray", "gray"),
        (C["rule"], "Rule", "rule"), (C["border"], "Border", "border"), (C["fill"], "Fill", "fill"),
        (C["background"], "Background", "background"), (C["blue"], "Blue", "blue")]

pairs = [("Ink on white", C["text"], "#FFFFFF"), ("Muted on white", C["text-muted"], "#FFFFFF"),
         ("Red on white", C["primary"], "#FFFFFF"), ("White on red", "#FFFFFF", C["primary"]),
         ("Ink on red tint", C["text"], C["red-tint"]), ("Muted on red tint", C["text-muted"], C["red-tint"]),
         ("Red light on dark", C["primary-light"], C["text"]), ("Gray on white (graphics only)", C["gray"], "#FFFFFF")]
pair_html = "".join(
    f'<div class="pair" style="background:{bg};color:{fg};{"border:1px solid " + C["border"] if bg == "#FFFFFF" else ""}">'
    f'<strong>{name}</strong><span>{v.contrast(fg, bg):.1f} : 1</span></div>' for name, fg, bg in pairs)

sizes = TY["size"]
web_px = [int(float(x.replace("rem", "")) * 16) for x in sizes.values()]
sl, sp, dc, fg = TY["slides-px-1920"], TY["slides-pt-960"], TY["docs-pt"], TY["figure-pt"]

cat_rows = "".join(
    f'<tr><td>{c["slot"]}</td><td><span class="dot" style="background:{c["fill"]}"></span>{c["name"].capitalize()}</td>'
    f'<td><code>{c["fill"]}</code></td><td><span class="chip" style="background:{c["fill"]};color:{C["white"] if c["label"] == "white" else C["text"]}">{"white" if c["label"] == "white" else "ink"} {v.contrast(C["white"] if c["label"] == "white" else C["text"], c["fill"]):.1f}</span></td>'
    f'<td><span class="chip" style="background:{c["tint"]};color:{c["ink"]}">{c["ink"]} on {c["tint"]}</span></td>'
    f'<td>{v.esc(c["domain"])}</td></tr>' for c in CATS)


def build_label(scale):
    """'ink on steps 1 to 5, white on steps 6 and 7', from tokens.json (same words as BRAND.md)."""
    labs = D["labels"][scale]
    runs, start = [], 0
    for k in range(1, len(labs) + 1):
        if k == len(labs) or labs[k] != labs[start]:
            a, b = start + 1, k
            span = f"step {a}" if a == b else f"steps {a} and {b}" if b == a + 1 else f"steps {a} to {b}"
            runs.append(f"{'ink' if labs[start] == 'text' else 'white'} on {span}")
            start = k
    return ", ".join(runs)


def hard_rules():
    return "\n".join(f'  <li>{h["rule"]} <span class="why">{h["why"][0].upper() + h["why"][1:]}.</span></li>' for h in T["rules"]["hard"])


def open_questions():
    """The open items in tokens.json, as collapsed blocks."""
    out = []
    for q in T["decisions"]["open"]:
        tag = '<span class="tag">new</span>' if q["tag"] == "new" else '<span class="tag grey">open</span>'
        out.append(f'<details class="qna">\n  <summary>{tag}{q["topic"]}</summary>\n  <p>{q["text"]}</p>\n</details>')
    return "\n".join(out)


def render():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AIRI Brand Guide</title>
<link rel="stylesheet" href="brand.css">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: var(--font-family); color: var(--color-text); background: var(--color-background);
    padding: 40px 24px 80px; max-width: 1080px; margin: 0 auto; line-height: var(--line-height-normal);
  }}
  h1 {{ font-size: var(--font-size-2xl); font-weight: 700; color: var(--color-link); line-height: var(--line-height-tight); margin-bottom: 8px; }}
  h1 span {{ color: var(--color-text); font-weight: 400; }}
  .subtitle {{ color: var(--color-text-muted); margin-bottom: 32px; max-width: 720px; }}
  h2 {{ font-size: var(--font-size-xl); font-weight: 700; line-height: var(--line-height-tight); margin-top: 56px; margin-bottom: 16px; padding-top: 16px; border-top: 2px solid var(--color-primary); }}
  h3 {{ font-size: var(--font-size-lg); font-weight: 600; margin: 32px 0 8px; }}
  h4 {{ font-size: var(--font-size-base); font-weight: 700; margin: 24px 0 8px; }}
  p, li {{ font-size: var(--font-size-base); max-width: 760px; }}
  p {{ margin: 8px 0; }}
  ul, ol {{ padding-left: 24px; margin: 8px 0 16px; }}
  code {{ font-family: var(--font-family-mono); font-size: 0.85em; }}
  p code, li code, td code {{ background: var(--color-fill); padding: 2px 6px; border-radius: 4px; }}
  a {{ color: var(--color-link); text-decoration: underline; }}
  a:hover {{ color: var(--color-link-hover); }}
  :focus-visible {{ outline: var(--focus-ring); outline-offset: 2px; }}
  .note {{ background: var(--color-fill); padding: 16px; margin: 16px 0; border-radius: 8px; font-size: var(--font-size-sm); max-width: 760px; }}
  .rules {{ background: var(--color-surface); border: 1px solid var(--color-border); border-radius: 8px; padding: 16px 16px 16px 40px; margin: 16px 0; max-width: 760px; }}
  .rules li {{ margin: 8px 0; }}

  .logo-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 16px 0; }}
  .logo-cell {{ padding: 24px; border-radius: 8px; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 140px; }}
  .logo-cell.light {{ background: var(--color-surface); border: 1px solid var(--color-border); }}
  .logo-cell.dark {{ background: var(--color-text); }}
  .logo-cell.red {{ background: var(--color-primary); }}
  .logo-cell .label {{ display: block; font-size: var(--font-size-xs); color: var(--color-text-muted); margin-top: 16px; font-family: var(--font-family-mono); }}
  .logo-cell.dark .label, .logo-cell.red .label {{ color: var(--color-white); }}
  img.horiz {{ height: 72px; width: auto; max-width: 100%; }}
  img.icon {{ width: 96px; height: 96px; }}
  .asset-links {{ display: flex; gap: 8px; margin-top: 8px; }}
  .asset-links a {{ padding: 4px 12px; border: 1px solid var(--color-rule); border-radius: 4px; background: var(--color-surface); color: var(--color-text); text-decoration: none; font-family: var(--font-family-mono); font-size: var(--font-size-xs); font-weight: 600; }}
  .asset-links a:hover {{ background: var(--color-primary); border-color: var(--color-primary); color: var(--color-white); }}
  .logo-cell.dark .asset-links a, .logo-cell.red .asset-links a {{ background: transparent; border-color: var(--color-white); color: var(--color-white); }}
  .logo-cell.dark .asset-links a:hover, .logo-cell.red .asset-links a:hover {{ background: var(--color-white); color: var(--color-text); }}

  .swatches {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 8px; margin: 16px 0; }}
  .swatch {{ padding: 16px; border-radius: 8px; font-size: var(--font-size-sm); min-height: 96px; }}
  .swatch strong, .swatch code, .swatch span {{ display: block; }}
  .swatch span {{ font-family: var(--font-family-mono); font-size: var(--font-size-xs); }}
  .pairs {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 8px; margin: 16px 0; }}
  .pair {{ padding: 16px; border-radius: 8px; display: flex; justify-content: space-between; gap: 8px; font-size: var(--font-size-sm); }}

  .strip {{ margin: 8px 0 24px; }}
  .strip-cells {{ display: flex; }}
  .strip-cells > div {{ flex: 1; min-width: 0; }}
  .strip-cells.main > div {{ padding: 16px 4px; text-align: center; font-size: var(--font-size-xs); }}
  .strip-cells.main b, .strip-cells.main code {{ display: block; overflow-wrap: anywhere; }}
  .strip-row {{ display: flex; align-items: center; gap: 8px; margin-top: 4px; }}
  .strip-row span {{ width: 88px; flex: none; font-size: var(--font-size-xs); color: var(--color-text-muted); }}
  .strip-row .strip-cells {{ flex: 1; }}
  .strip-row .strip-cells > div {{ height: 16px; }}

  .charts {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; margin: 16px 0; }}
  figure {{ background: var(--color-surface); border: 1px solid var(--color-border); border-radius: 8px; padding: 16px; }}
  figure svg {{ width: 100%; height: auto; display: block; }}
  figcaption {{ font-size: var(--font-size-sm); color: var(--color-text-muted); margin-top: 8px; }}
  figcaption b {{ color: var(--color-text); }}

  .tablewrap {{ overflow-x: auto; margin: 16px 0; }}
  table {{ border-collapse: collapse; width: 100%; font-size: var(--font-size-sm); background: var(--color-surface); }}
  th {{ text-align: left; background: var(--color-fill); font-weight: 700; }}
  th, td {{ padding: 8px 12px; border-bottom: 1px solid var(--color-rule); vertical-align: top; }}
  .dot {{ display: inline-block; width: 12px; height: 12px; border-radius: 4px; margin-right: 8px; }}
  .chip, .status {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: var(--font-size-sm); font-weight: 600; white-space: nowrap; }}
  .chiprow {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0; }}
  .chiprow .chip {{ white-space: normal; }}
  .status i {{ display: inline-block; width: 16px; height: 16px; line-height: 16px; border-radius: 4px; text-align: center; font-style: normal; font-size: 11px; margin-right: 8px; }}
  .grades td, .grades th {{ border-bottom: 1px solid var(--color-rule); }}
  .grade {{ display: inline-block; padding: 2px 12px; border: 2px solid; border-radius: 4px; }}

  .type-sample {{ margin: 16px 0; }}
  .type-sample .label {{ font-size: var(--font-size-xs); color: var(--color-text-muted); }}

  .hardrules {{ margin: 24px 0; max-width: 760px; }}
  .hardrules .why {{ color: var(--color-text-muted); }}

  details.qna {{ background: var(--color-surface); border: 1px solid var(--color-border); border-radius: 8px; padding: 16px 24px; margin: 8px 0; }}
  details.qna summary {{ cursor: pointer; font-weight: 600; }}
  details.qna[open] summary {{ margin-bottom: 8px; }}
  .tag {{ font-size: var(--font-size-xs); font-weight: 700; padding: 2px 8px; border-radius: 4px; margin-right: 8px; background: var(--color-red-tint); color: var(--color-link); }}
  .tag.grey {{ background: var(--color-fill); color: var(--color-text-muted); }}

  footer {{ margin-top: 64px; padding-top: 24px; border-top: 1px solid var(--color-rule); color: var(--color-text-muted); font-size: var(--font-size-sm); }}

  @media (max-width: 640px) {{
    body {{ padding: 24px 16px 64px; }}
    h1 {{ font-size: var(--font-size-xl); }}
    h2 {{ font-size: var(--font-size-lg); margin-top: 48px; }}
    .logo-grid {{ grid-template-columns: 1fr; }}
    .logo-cell {{ padding: 24px 16px; }}
    .asset-links a {{ padding: 8px 16px; font-size: var(--font-size-sm); }}
    .strip-cells.main code {{ font-size: 9px; }}
    .strip-row span {{ width: 64px; }}
  }}
</style>
</head>
<body>

<h1>MIT AI Risk <span>Brand Guide</span></h1>
<p class="subtitle">The look of the MIT AI Risk Initiative, including the AI Risk Repository and the AI Risk Index. One logo, one icon, one typeface, one red, and fixed meanings for colour in data. Version {T["version"]}.</p>

<div class="hardrules">
<h3>{len(T["rules"]["hard"])} hard rules. Everything else is a default.</h3>
<ol class="rules">
{hard_rules()}
</ol>
<p>The rest of this guide shows defaults: a starting point, and the answer when nobody has said otherwise. People can stray from a default on purpose, and a little drift is fine. Claude follows the defaults unless a person asks for something different. Where the kit says nothing, Claude reuses the closest pattern here, or picks the plainest option, and says so.</p>
</div>

<!-- 1. Logo -->
<h2>1 · Logo</h2>
<p>The AIRI logo is the icon beside the two-line wordmark "MIT AI Risk / Initiative". Use it for all AIRI work, including the Repository and the Index, wherever the brand needs its full name: navigation bars, document headers, covers.</p>
{logo_grid("initiative", "horizontal", "horiz")}
<ul>
  <li>Use the red logo on white and light grounds, the white logo on dark grounds, and the on-red version where the logo needs its own red block.</li>
  <li>Keep one large square of the icon clear on every side.</li>
  <li>Do not recolour, stretch or rebuild the logo, and do not add a product name to it.</li>
  <li>Slides carry the logo on the cover only. Documents carry it top right in the header. Report covers carry it in white, top left, on red.</li>
</ul>
<div class="note">Text in the logo files is outlined, so they need no font. PNG horizontals are 512 px tall. The proportions are fixed and generated by a script.</div>

<!-- 2. Icon -->
<h2>2 · Icon</h2>
<p>The icon is the "plus of squares" mark. Use it alone for favicons, app icons, phone-width navigation and anywhere the wordmark would be too small to read (under about 120 px wide).</p>
{logo_grid("initiative", "icon", "icon")}
<div class="note">PNG icons are 1024 × 1024.</div>

<!-- 3. Font and colour -->
<h2>3 · Font &amp; colour</h2>

<h3>Colour in one breath</h3>
<ol class="rules">
  <li><strong>One red: <code>{C["primary"]}</code>.</strong> Take it from the theme, the template or the token.</li>
  <li><strong>Two text colours:</strong> ink <code>{C["text"]}</code> and muted <code>{C["text-muted"]}</code>. White on red or dark.</li>
  <li><strong>In data, red is the subject, the finding or more risk.</strong> Grey <code>{C["gray"]}</code> is context. Ink <code>{C["text"]}</code> is a comparison. Blue shades a neutral amount.</li>
  <li><strong>A figure uses a red scale or a red highlight, not both.</strong></li>
</ol>

<h3>Figtree, the only typeface</h3>
<p>Figtree is used for everything, including the wordmark. It is free from <a href="https://fonts.google.com/specimen/Figtree">Google Fonts</a>. Set text left-aligned and in sentence case. Slides, documents and figures use regular and bold; the web may also use semibold.</p>
<div class="type-sample"><div class="label">Bold 700 · titles and headings</div><div style="font-weight:700;font-size:var(--font-size-xl);color:var(--color-link)">A title states the point of the page</div></div>
<div class="type-sample"><div class="label">Semibold 600 · web only</div><div style="font-weight:600;font-size:var(--font-size-lg)">Sub-headings below the title are ink</div></div>
<div class="type-sample"><div class="label">Regular 400 · body</div><div>Body text is near-black on a light ground. <span style="color:var(--color-text-muted)">Captions, sources and footers are muted.</span> <a href="#">Links are red and underlined.</a></div></div>
<div class="tablewrap"><table>
  <thead><tr><th>Medium</th><th>Sizes</th></tr></thead>
  <tbody>
    <tr><td>Web and apps (px)</td><td>{", ".join(str(x) for x in web_px[:-1])}; hero {web_px[-1]}</td></tr>
    <tr><td>Slides, 1920 × 1080 canvas (px)</td><td>Cover {sl["cover"]}, title {sl["title"]}, outcome {sl["outcome"]}, body {sl["body"]}, small {sl["small"]}</td></tr>
    <tr><td>Slides, 960 × 540 pt page (pt)</td><td>Cover {sp["cover"]}, title {sp["title"]}, outcome {sp["outcome"]}, body {sp["body"]}, small {sp["small"]}</td></tr>
    <tr><td>Documents (pt)</td><td>Title {dc["title"]}, Heading 1 {dc["h1"]}, Heading 2 {dc["h2"]}, Heading 3 {dc["h3"]}, body {dc["body"]}, captions {dc["caption"]}</td></tr>
    <tr><td>Print figures (pt)</td><td>Panel title {fg["panel-title"]}, labels {fg["label"]}, smallest {fg["smallest"]}</td></tr>
  </tbody>
</table></div>

<h3>The palette</h3>
<p>Fourteen swatches cover almost all work. The red is for structure: titles, covers, bars, buttons and links. Text is ink or muted. The greys do the rest.</p>
{v.swatches(core)}
<p>Text must use a pair that passes contrast. Gray <code>{C["gray"]}</code> is for graphics, never text. Red text uses the <code>link</code> token, which becomes <code>{C["primary-light"]}</code> on dark grounds; red fills use <code>primary</code>.</p>
<p>Four of the neutrals are Google presets and can be clicked in Docs and Slides: muted (dark gray 3), rule (gray), border (light gray 1) and fill (light gray 3). Ink, the chart gray and the background are custom colours. Google's preset named "gray" is the kit's rule <code>{C["rule"]}</code>, not the kit's gray.</p>
<div class="pairs">{pair_html}</div>

<h3>Colour in data</h3>
<p>Pick the palette by what the data shows. Under each strip are the same colours as seen with the two common kinds of colour blindness, and in greyscale print.</p>

<h4>One thing that matters: red on grey</h4>
<p>The default chart. One series in red, everything else in grey. When two conditions are both the subject, pair red with pale red and label the bars.</p>
<div class="charts">
  <figure>{v.chart_highlight()}</figure>
  <figure>{v.chart_dots()}</figure>
  <figure>{v.chart_pair()}</figure>
</div>

<h4>Ordered levels where higher is worse: the severity scale</h4>
{v.strip(D["severity"], ["1", "2", "3", "4", "5"])}
<div class="charts"><figure>{v.chart_severity()}<figcaption>Use red only when more means more risk. Labels are ink on the two pale steps and white on the rest.</figcaption></figure>
<figure>{v.chart_blue()}<figcaption>Counts and coverage use blue, because more is only more. On the seven-step blue scale, labels are {build_label("blue-sequential")}.</figcaption></figure></div>

<h4>Amounts: the blue scale</h4>
{v.strip(D["blue-sequential"])}

<h4>Two directions from a midpoint</h4>
{v.strip(D["diverging-7"])}
<div class="charts"><figure>{v.chart_div()}<figcaption>Red is the riskier side. The midpoint is grey, never yellow.</figcaption></figure></div>

<h4>Named groups: eight category colours</h4>
<p>One palette for any grouping: risk domains, actors, sectors, mitigations. Groups take the colours in order from the first. The seven risk domains use colours 1 to 7 by default, in new work only. Red is never a category, so it stays free to pick one out.</p>
{v.strip([c["fill"] for c in CATS] + [D["other"]["fill"]], [c["name"].capitalize() for c in CATS] + ["Other"])}
<div class="tablewrap"><table>
  <thead><tr><th>Slot</th><th>Colour</th><th>Fill</th><th>Label on fill</th><th>Text on tint</th><th>Repository domain</th></tr></thead>
  <tbody>{cat_rows}</tbody>
</table></div>
<ul>
  <li><strong>Colour a grouping only when the colour says something.</strong> Bars that compare groups are one colour; the names and the lengths do the work. Pick one out in red, or give related groups one colour.</li>
  <li>Use the colours where each group needs its own mark: a diagram or schematic with a few named parts, a stacked bar, one line per group.</li>
  <li>More than eight groups: grey with names on the chart, and colour only the one or two the chart is about.</li>
  <li>Subgroups take lighter and darker steps of their parent's colour. Two groupings at once: colour one, put the other on the axis.</li>
  <li>Keep a group's colour the same within one paper or product.</li>
</ul>
<div class="charts"><figure>{v.chart_cat()}</figure><figure>{v.chart_lines()}</figure></div>
<p>Charts made in Google Sheets, Slides, PowerPoint or Excel take the theme accents in order: red, grey, ink, then category colours 1 to 3. That suits a chart of one to three series. For named groups, set each series to its slot colour by hand.</p>

<h4>Status</h4>
<p>Status always carries a word or an icon. A dense Yes / Partial / No table under a red header may use the grade style, which avoids red and green altogether.</p>
{v.status_chips()}
<div class="tablewrap">{v.grade_table()}</div>

<div class="note">Every value, with text pairs, dark mode and rules for each medium, is in <a href="{GH}/blob/main/skill/BRAND.md">BRAND.md</a>. Ready-made theme and palette files for Office, Google Workspace, CSS, Tailwind, matplotlib, Plotly, R and LaTeX are in <a href="{GH}/tree/main/skill/templates">templates</a>.</div>

<!-- 4. Parent organisation logo -->
<h2>4 · Parent organisation logo</h2>
<p>AIRI sits within <strong>MIT FutureTech</strong>. The FutureTech logo may appear beside the AIRI logo on co-branded work. It comes from FutureTech's own guidelines and is not an AIRI brand element; traced SVG versions are included for convenience.</p>
{logo_grid("futuretech", "futuretech", "horiz", png=False, h=48)}
<ul>
  <li>Set the two logos apart at a balanced size. Do not merge them into one mark.</li>
  <li>Report covers carry two logos, AIRI and FutureTech, in white on red.</li>
  <li>There are three different reds. AIRI red is <code>{C["primary"]}</code>. The FutureTech logo uses <code>{T["not-airi"]["futuretech-red"]}</code>. MIT's institutional red is <code>{T["not-airi"]["mit-red"]}</code>. The last two stay inside their own logos.</li>
  <li>With partners: in AIRI-led work, AIRI colours and type win and the partner's logo sits apart at equal height. In partner-led work, the partner's template wins and the AIRI logo appears in white or red, never recoloured.</li>
</ul>

<!-- 5. Open questions -->
<h2>5 · Open questions</h2>
<p>Not yet settled. Each has a default to use until it is. Open a <a href="{GH}/issues">GitHub issue</a> to weigh in.</p>

{open_questions()}

<footer>
  <p><strong>More detail:</strong> <a href="{GH}/blob/main/skill/BRAND.md">skill/BRAND.md</a> is the full specification. <a href="{GH}/blob/main/CONTRIBUTING.md">CONTRIBUTING.md</a> explains how the files fit together.</p>
  <p><strong>Questions or proposed changes:</strong> open an issue on <a href="{GH}/issues">GitHub</a>. Retired logos are in <a href="{GH}/tree/main/legacy/logos">legacy/logos/</a>.</p>
</footer>

</body>
</html>
"""

