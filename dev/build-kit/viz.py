"""Helpers for pages that show the brand: contrast, colour-blind simulation, swatches, example charts.

Used by guide.py. Everything reads skill/tokens.json, so pages cannot drift from the kit.
"""
import html
import json
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]
T = json.loads((KIT / "skill" / "tokens.json").read_text())
C = T["color"]
D = T["data"]
CATS = D["categorical"]
S = T["status"]
FONT = "Figtree, Arial, sans-serif"
INK, MUTED, GRAY, RULE, LINE, FILL, RED = C["text"], C["text-muted"], C["gray"], C["rule"], C["border"], C["fill"], C["primary"]

esc = html.escape


def rgb(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def to_hex(c):
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(x))) for x in c)


def _lin(v):
    v /= 255
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def _unlin(v):
    v = max(0.0, min(1.0, v))
    return 255 * (12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055)


def lum(h):
    r, g, b = [_lin(x) for x in rgb(h)]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def on(h):
    """Ink or white, whichever reads better on this fill."""
    return INK if contrast(INK, h) >= contrast("#FFFFFF", h) else "#FFFFFF"


_CVD = {  # Machado, Oliveira & Fernandes 2009, severity 1.0
    "deutan": [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
    "protan": [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
}


def cvd(h, kind):
    lin = [_lin(x) for x in rgb(h)]
    if kind == "grey":
        y = 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
        return to_hex([_unlin(y)] * 3)
    m = _CVD[kind]
    return to_hex([_unlin(sum(m[i][j] * lin[j] for j in range(3))) for i in range(3)])


# ------------------------------------------------------------ HTML pieces

def swatch(h, name="", note="", wide=False):
    fg = on(h)
    edge = f"border:1px solid {LINE};" if contrast(h, "#FFFFFF") < 1.25 else ""
    cls = "swatch wide" if wide else "swatch"
    return (f'<div class="{cls}" style="background:{h};color:{fg};{edge}">'
            f'<strong>{esc(name)}</strong><code>{h}</code>'
            + (f'<span>{esc(note)}</span>' if note else "") + "</div>")


def swatches(items, wide=False):
    return '<div class="swatches">' + "".join(swatch(h, n, note, wide) for h, n, note in items) + "</div>"


def strip(colors, labels=None, sims=True):
    """A palette strip, with colour-blind and greyscale rows under it."""
    def row(kind, name):
        cells = "".join(
            f'<div style="background:rgb({",".join(str(x) for x in rgb(cvd(h, kind)))})"></div>' for h in colors)
        return f'<div class="strip-row sim"><span>{name}</span><div class="strip-cells">{cells}</div></div>'

    top = "".join(
        f'<div style="background:{h};color:{on(h)}">'
        + (f'<b>{esc(labels[i])}</b>' if labels else "") + f'<code>{h}</code></div>'
        for i, h in enumerate(colors))
    out = f'<div class="strip"><div class="strip-cells main">{top}</div>'
    if sims:
        out += row("deutan", "Green-blind") + row("protan", "Red-blind") + row("grey", "Greyscale")
    return out + "</div>"


def chips():
    out = []
    for c in CATS:
        out.append(f'<span class="chip" style="background:{c["tint"]};color:{c["ink"]}">{esc(c["domain"])}</span>')
    return '<div class="chiprow">' + "".join(out) + "</div>"


# ------------------------------------------------------------ SVG charts

def _svg(w, h, body, label):
    return (f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}" '
            f'xmlns="http://www.w3.org/2000/svg" font-family="{FONT}">'
            f'<rect width="{w}" height="{h}" fill="#FFFFFF"/>{body}</svg>')


def _t(x, y, s, size=12, fill=INK, anchor="start", weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{esc(str(s))}</text>'


SOURCE = "Illustrative data"
DOM_SHORT = ["Discrimination", "Privacy", "Misinformation", "Misuse", "Human-AI", "Socioeconomic", "AI safety"]


def chart_highlight():
    vals = [41, 68, 37, 52, 29, 33, 47]
    b = _t(16, 26, "Privacy and security is the risk named most often", 15, INK, weight=700)
    b += _t(16, 44, "Share of documents that name each domain (%)", 12, MUTED)
    for i, (n, v) in enumerate(zip(DOM_SHORT, vals)):
        y = 62 + i * 28
        col = RED if i == 1 else GRAY
        b += _t(118, y + 15, n, 12, INK if i == 1 else MUTED, "end", 700 if i == 1 else 400)
        b += f'<rect x="126" y="{y}" width="{v * 4.6:.0f}" height="20" fill="{col}"/>'
        b += _t(126 + v * 4.6 + 6, y + 15, v, 12, INK if i == 1 else MUTED, weight=700 if i == 1 else 400)
    b += _t(16, 276, "Source: " + SOURCE, 11, MUTED)
    return _svg(520, 290, b, "Bar chart: one red bar against grey bars")


def chart_pair():
    groups = ["Minor or worse", "Substantial", "Severe", "Catastrophic"]
    a, p = [90, 72, 44, 18], [80, 55, 30, 9]
    b = _t(16, 26, "Mitigations lower every estimate, most at the severe end", 15, INK, weight=700)
    b += f'<rect x="16" y="38" width="12" height="12" fill="{RED}"/>' + _t(34, 48, "Business as usual", 12, MUTED)
    b += f'<rect x="150" y="38" width="12" height="12" fill="{C["red-300"]}"/>' + _t(168, 48, "With mitigations", 12, MUTED)
    base = 240
    b += f'<line x1="16" y1="{base}" x2="504" y2="{base}" stroke="{RULE}"/>'
    for i, g in enumerate(groups):
        x = 40 + i * 118
        for j, (v, col) in enumerate(((a[i], RED), (p[i], C["red-300"]))):
            hgt = v * 1.7
            b += f'<rect x="{x + j * 44}" y="{base - hgt:.0f}" width="40" height="{hgt:.0f}" fill="{col}"/>'
            b += _t(x + j * 44 + 20, base - hgt - 5, f"{v}%", 12, INK, "middle", 700 if j == 0 else 400)
        b += _t(x + 42, base + 17, g, 12, MUTED, "middle")
    b += _t(16, 280, "Source: " + SOURCE, 11, MUTED)
    return _svg(520, 290, b, "Paired bars in red and pale red")


def _heat(title, sub, scale, none, label):
    rows = ["Health", "Finance", "Education", "Public sector", "Transport"]
    grid = [[5, 4, 3, 4, 2, 3, 5], [4, 5, 2, 4, 1, 4, 3], [3, 3, 4, 2, 3, 2, 2], [4, 4, 5, 3, 2, 3, 4], [2, 1, 0, 2, 1, 2, 4]]
    b = _t(16, 26, title, 15, INK, weight=700) + _t(16, 44, sub, 12, MUTED)
    for j, n in enumerate(DOM_SHORT):
        b += _t(124 + j * 55 + 26, 68, n if len(n) < 10 else n[:8] + ".", 10.5, MUTED, "middle")
    for i, r in enumerate(rows):
        y = 76 + i * 32
        b += _t(116, y + 20, r, 12, INK, "end")
        for j, v in enumerate(grid[i]):
            col = none if v == 0 else scale[v - 1]
            b += f'<rect x="{124 + j * 55}" y="{y}" width="53" height="30" fill="{col}"/>'
            b += _t(124 + j * 55 + 26, y + 20, v if v else "–", 12, on(col) if v else MUTED, "middle", 700 if v >= 4 else 400)
    b += _t(16, 262, "Source: " + SOURCE, 11, MUTED)
    return _svg(520, 276, b, label)


def chart_severity():
    return _heat("Health and finance are the most exposed sectors", "Vulnerability by sector and risk domain, 1 (low) to 5 (high)",
                 D["severity"], D["severity-none"], "Heat map in five red steps")


def chart_blue():
    return _heat("Most documents come from health and the public sector", "Documents reviewed, by sector and risk domain (quintile)",
                 D["blue-5"], D["severity-none"], "Heat map in five blue steps")


def chart_div():
    items = [("Misuse", [3, 7, 14, 40, 36]), ("AI safety", [6, 12, 24, 36, 22]),
             ("Privacy", [14, 26, 30, 22, 8]), ("Discrimination", [22, 32, 26, 14, 6])]
    cols = D["diverging-5"]
    b = _t(16, 26, "Concern rose most for misuse and fell for discrimination", 15, INK, weight=700)
    b += _t(16, 44, "Change in expert concern since last year. Blue fell, grey unchanged, red rose (%)", 12, MUTED)
    mid = 300
    for i, (n, v) in enumerate(items):
        y = 62 + i * 44
        b += _t(16, y + 19, n, 12, INK)
        x = mid - (v[0] + v[1] + v[2] / 2) * 2.1
        for k, seg in enumerate(v):
            w = seg * 2.1
            b += f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="28" fill="{cols[k]}"/>'
            if seg >= 12:
                b += _t(x + w / 2, y + 19, seg, 11.5, on(cols[k]), "middle")
            x += w
    b += f'<line x1="{mid}" y1="56" x2="{mid}" y2="236" stroke="{INK}" stroke-dasharray="2 3"/>'
    b += _t(16, 262, "Source: " + SOURCE, 11, MUTED)
    return _svg(520, 276, b, "Two-sided stacked bars from blue through grey to red")


def chart_cat():
    vals = [12, 16, 9, 21, 8, 14, 20]
    b = _t(16, 26, "Misuse and AI safety make up two fifths of entries", 15, INK, weight=700)
    b += _t(16, 44, "Share of entries by risk domain (%)", 12, MUTED)
    x = 16.0
    for c, v, n in zip(CATS, vals, DOM_SHORT):
        w = v * 4.88
        b += f'<rect x="{x:.1f}" y="60" width="{w - 2:.1f}" height="44" fill="{c["fill"]}"/>'
        b += _t(x + w / 2, 87, v, 13, "#FFFFFF" if c["label"] == "white" else INK, "middle", 700)
        b += f'<g transform="translate({x + w / 2:.1f},116) rotate(35)">' + _t(0, 0, n, 11, c["ink"], weight=700) + "</g>"
        x += w
    b += _t(16, 206, "Source: " + SOURCE + ". Every segment is labelled, so no legend is needed.", 11, MUTED)
    return _svg(520, 220, b, "Stacked bar in the seven category colours")


def chart_lines():
    """Several groups across the same items: one line per group, in slot order, labelled at the end."""
    risks = ["Discrim.", "Privacy", "Misinfo.", "Misuse", "Human-AI", "Socioecon.", "AI safety"]
    actors = [("Developers", [62, 71, 48, 66, 30, 22, 74]), ("Deployers", [41, 58, 27, 35, 24, 18, 39]),
              ("Governments", [55, 63, 52, 47, 15, 41, 33]), ("Investors", [12, 20, 8, 15, 6, 29, 10])]
    b = _t(16, 26, "Developers disclose most, except on socioeconomic risk", 15, INK, weight=700)
    b += _t(16, 44, "Share of organisations that disclose each risk, by type of actor (%)", 12, MUTED)
    x0, dx, top, base = 40, 58, 64, 236
    for g in range(0, 81, 20):
        gy = base - g * (base - top) / 80
        b += f'<line x1="{x0}" y1="{gy:.0f}" x2="{x0 + dx * 6}" y2="{gy:.0f}" stroke="{LINE}"/>' + _t(x0 - 6, gy + 4, g, 11, MUTED, "end")
    for i, r in enumerate(risks):
        b += _t(x0 + i * dx, base + 16, r, 10.5, MUTED, "middle")
    for (name, vals), c in zip(actors, CATS):
        pts = " ".join(f"{x0 + i * dx},{base - v * (base - top) / 80:.1f}" for i, v in enumerate(vals))
        b += f'<polyline points="{pts}" fill="none" stroke="{c["fill"]}" stroke-width="2.5"/>'
        b += "".join(f'<circle cx="{x0 + i * dx}" cy="{base - v * (base - top) / 80:.1f}" r="3.5" fill="{c["fill"]}"/>' for i, v in enumerate(vals))
        b += _t(x0 + dx * 6 + 8, base - vals[-1] * (base - top) / 80 + 4, name, 11.5, c["ink"], weight=700)
    b += _t(16, 276, "Source: " + SOURCE + ". Lines take category slots 1 to 4 and are labelled at their ends.", 11, MUTED)
    return _svg(520, 290, b, "Line chart: four actor types across seven risk domains, one category colour each")


def chart_dots():
    rows = [("Any risk", 38, 68), ("Discrimination", 19, 41), ("Cyberattacks", 17, 39), ("Privacy", 14, 34),
            ("Misinformation", 9, 27), ("Governance failure", 7, 22), ("AI welfare", 2, 9)]
    b = _t(16, 26, "The largest companies name every risk more often", 15, INK, weight=700)
    b += f'<circle cx="22" cy="42" r="5" fill="{RED}"/>' + _t(32, 46, "Largest 100", 12, MUTED)
    b += f'<circle cx="116" cy="42" r="5" fill="{GRAY}"/>' + _t(126, 46, "Next 900, with range", 12, MUTED)
    for g in range(0, 81, 20):
        gx = 150 + g * 4.3
        b += f'<line x1="{gx}" y1="58" x2="{gx}" y2="250" stroke="{LINE}"/>' + _t(gx, 264, f"{g}%", 11, MUTED, "middle")
    for i, (n, lo, hi) in enumerate(rows):
        y = 74 + i * 26
        b += _t(142, y + 4, n, 12, INK, "end")
        b += f'<rect x="{150 + (lo - 5) * 4.3:.0f}" y="{y - 7}" width="{10 * 4.3:.0f}" height="14" fill="{LINE}"/>'
        b += f'<circle cx="{150 + lo * 4.3:.0f}" cy="{y}" r="5" fill="{GRAY}"/><circle cx="{150 + hi * 4.3:.0f}" cy="{y}" r="5.5" fill="{RED}"/>'
    b += _t(16, 284, "Source: " + SOURCE, 11, MUTED)
    return _svg(520, 294, b, "Dot plot: red dots for the subject, grey dots and bands for context")


def grade_table():
    g = S["grade"]
    def cell(k, word):
        s = g[k]
        return (f'<td><span class="grade" style="background:{s["fill"]};border-color:{s["border"]};color:{s["text"]};'
                f'font-weight:{400 if k == "yes" else 700}">{word}</span></td>')
    rows = [("Publish a safety framework", "yes", "yes", "partial"), ("Report serious incidents", "partial", "no", "yes"),
            ("Describe testing before release", "yes", "partial", "partial")]
    words = {"yes": "Yes", "partial": "Partial", "no": "No"}
    body = "".join("<tr><th>" + r[0] + "</th>" + "".join(cell(k, words[k]) for k in r[1:]) + "</tr>" for r in rows)
    return ('<table class="grades"><thead><tr><th>Requirement</th><th>Company A</th><th>Company B</th><th>Company C</th></tr></thead>'
            f"<tbody>{body}</tbody></table>")


def status_chips():
    out = []
    for k, icon, word in (("good", "✓", "Held"), ("partial", "!", "Partial"), ("poor", "✕", "Not met"), ("info", "i", "Note"), ("none", "–", "No data")):
        s = S[k]
        out.append(f'<span class="status" style="background:{s["tint"]};color:{s["ink"]}">'
                   f'<i style="background:{s["mark"]};color:{on(s["mark"])}">{icon}</i>{word}</span>')
    return '<div class="chiprow">' + "".join(out) + "</div>"
