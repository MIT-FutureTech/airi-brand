#!/usr/bin/env python3
"""Tests for skill/tools/brand_scan.py: the colour maths, the sorting into groups, and that it only reads.

    python3 dev/brand-scan/test_brand_scan.py
"""
import contextlib
import hashlib
import io
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skill" / "tools"))
import brand_scan as bs  # noqa: E402

KIT = bs.load_kit()


def scan_text(files, **kw):
    """Write {name: text} into a temp folder, scan it, return (findings, stats)."""
    with tempfile.TemporaryDirectory() as tmp:
        for name, text in files.items():
            path = Path(tmp) / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        return bs.build_findings(bs.run_scan([tmp], KIT), KIT, **kw)


def by_value(findings):
    return {f["value"]: f for f in findings}


class ColourMaths(unittest.TestCase):
    def test_ciede2000_reference_pairs(self):
        # From the test data published with Sharma, Wu and Dalal (2005).
        pairs = [((50.0, 2.6772, -79.7751), (50.0, 0.0, -82.7485), 2.0425),
                 ((50.0, 3.1571, -77.2803), (50.0, 0.0, -82.7485), 2.8615),
                 ((50.0, 2.8361, -74.0200), (50.0, 0.0, -82.7485), 3.4412),
                 ((50.0, -1.3802, -84.2814), (50.0, 0.0, -82.7485), 1.0000),
                 ((50.0, 2.5, 0.0), (50.0, 0.0, -2.5), 4.3065),
                 ((60.2574, -34.0099, 36.2677), (60.4626, -34.1751, 39.4387), 1.2644),
                 ((2.0776, 0.0795, -1.1350), (0.9033, -0.0636, -0.5514), 0.9082)]
        for a, b, want in pairs:
            self.assertAlmostEqual(bs.ciede2000(a, b), want, places=4)
            self.assertAlmostEqual(bs.ciede2000(b, a), want, places=4)

    def test_lab_of_white_black_and_identity(self):
        L, a, b = bs.hex_to_lab("FFFFFF")
        self.assertAlmostEqual(L, 100, places=2)
        self.assertAlmostEqual(a, 0, places=2)
        self.assertAlmostEqual(b, 0, places=2)
        self.assertAlmostEqual(bs.hex_to_lab("000000")[0], 0, places=4)
        self.assertEqual(bs.delta_e("A32035", "A32035"), 0)

    def test_norm_hex(self):
        self.assertEqual(bs.norm_hex("#abc"), ("AABBCC", 1.0))
        self.assertEqual(bs.norm_hex("#A32035"), ("A32035", 1.0))
        self.assertEqual(bs.norm_hex("#a3203580")[0], "A32035")
        self.assertAlmostEqual(bs.norm_hex("#a3203580")[1], 0.502, places=3)
        self.assertIsNone(bs.norm_hex("#zzz"))

    def test_contrast(self):
        self.assertAlmostEqual(bs.contrast("000000", "FFFFFF"), 21, places=1)
        self.assertLess(bs.contrast("898A8D", "FFFFFF"), 4.5)      # why kit grey is not a text colour
        self.assertGreater(bs.contrast("666666", "FFFFFF"), 4.5)

    def test_is_red(self):
        for h in ("A32035", "FF0000", "980000", "DC2626", "750014"):
            self.assertTrue(bs.is_red(h), h)
        for h in ("CC6699", "D4762C", "F8E1E5", "2171B5", "898A8D"):
            self.assertFalse(bs.is_red(h), h)


class Classify(unittest.TestCase):
    def kind(self, h, **kw):
        v = KIT.classify(h, **kw)
        return v["kind"], v["group"], v["use"]

    def test_exact_tokens_are_fine(self):
        for h in ("A32035", "1A1A1A", "2171B5", "2A9484", "FFFFFF", "F2F2F2"):
            self.assertEqual(KIT.classify(h)["group"], "ok", h)

    def test_near_red_is_a_hard_rule(self):
        self.assertEqual(self.kind("A52238"), ("near-red", "must", "primary"))
        self.assertEqual(KIT.classify("A52238")["rule"], "red")

    def test_red_from_outside_the_kit(self):
        kind, group, use = self.kind("DC2626")
        self.assertEqual((kind, group), ("foreign-red", "must"))
        self.assertIn(use, ("primary", "red-500"))

    def test_replaced_and_avoided_values(self):
        self.assertEqual(self.kind("E0E0E0"), ("replaced", "drift", "border"))
        self.assertEqual(self.kind("C4606F"), ("replaced", "drift", "red-500"))
        self.assertEqual(self.kind("1155CC"), ("avoid", "drift", "link"))
        self.assertEqual(self.kind("FF0000"), ("avoid", "must", "primary"))

    def test_other_marks_red(self):
        self.assertEqual(self.kind("750014")[:2], ("other-mark", "must"))
        self.assertEqual(self.kind("750014", in_logo=True)[:2], ("other-mark", "info"))

    def test_near_miss_and_off_kit(self):
        self.assertEqual(self.kind("F5F5F5"), ("near", "drift", "fill"))
        self.assertEqual(self.kind("2E8B57"), ("near", "drift", "good"))
        self.assertEqual(self.kind("14B8A6")[:2], ("off-kit", "decision"))
        # a tighter threshold turns a near-miss into a decision
        self.assertEqual(KIT.classify("2E8B57", near=1.0)["group"], "decision")

    def test_near_misses_are_not_matched_to_dark_mode_values(self):
        self.assertNotIn("dark mode", KIT.classify("999999")["use"])

    def test_black_overlays_and_see_through_red(self):
        self.assertEqual(self.kind("000000"), ("black", "drift", "text"))
        self.assertEqual(self.kind("000000", alpha=0.1)[0], "overlay")
        self.assertEqual(self.kind("A32035", alpha=0.1), ("red-opacity", "drift", "red-tint"))


class Finding(unittest.TestCase):
    def colours(self, line, strict=False):
        return [(h, round(a, 2)) for _, h, a, _ in bs.colours_in_line(line, strict)]

    def test_colour_syntaxes(self):
        self.assertEqual(self.colours("a { color: #a32035; background: #FFF }"), [("A32035", 1.0), ("FFFFFF", 1.0)])
        self.assertEqual(self.colours("fill: rgb(163, 32, 53); x: rgba(0,0,0,.5)"), [("A32035", 1.0), ("000000", 0.5)])
        self.assertEqual(self.colours("color: hsl(0, 100%, 50%)"), [("FF0000", 1.0)])
        self.assertEqual(self.colours("border: 1px solid red;"), [("FF0000", 1.0)])
        self.assertEqual(self.colours('.attr("fill", "steelblue")'), [("4682B4", 1.0)])

    def test_things_that_are_not_colours(self):
        self.assertEqual(self.colours("#feed { margin: 0 }"), [])
        self.assertEqual(self.colours('<a href="#abc">x</a>'), [])
        self.assertEqual(self.colours('document.querySelector("#add")'), [])
        self.assertEqual(self.colours("&#123; and page.html#fff"), [])
        self.assertEqual(self.colours("fixes #123 and #4567", strict=True), [])
        self.assertEqual(self.colours("color = '#abc'", strict=True), [("AABBCC", 1.0)])
        self.assertEqual(self.colours("const redScale = 1; color: redScale"), [])

    def test_font_stacks(self):
        stacks = lambda line: list(bs.font_stacks_in_line(line))
        self.assertEqual(stacks("body { font-family: 'Inter', system-ui, sans-serif; }"), [["Inter", "system-ui", "sans-serif"]])
        self.assertEqual(stacks('fontFamily: "Roboto, sans-serif", fontSize: 12'), [["Roboto", "sans-serif"]])
        self.assertEqual(stacks('<text font-family="Georgia" x="1">'), [["Georgia"]])
        self.assertEqual(stacks("fontFamily: FONT,"), [])
        self.assertEqual(stacks("font-family: var(--font-family);"), [])
        self.assertEqual(stacks('<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400&family=Figtree">'),
                         [["Open Sans"], ["Figtree"]])

    def test_font_verdicts(self):
        v = lambda *s: bs.font_verdict(KIT, list(s))[:2]
        self.assertEqual(v("Figtree", "Arial", "sans-serif"), ("ok", "sans"))
        self.assertEqual(v("Figtree"), ("ok", "sans"))
        self.assertEqual(v("Inter", "sans-serif"), ("must", "other-font"))
        self.assertEqual(v("sans-serif"), ("must", "no-figtree"))
        self.assertEqual(v("Figtree", "system-ui", "sans-serif"), ("drift", "fallbacks"))
        self.assertEqual(v("ui-monospace", "SFMono-Regular", "Menlo", "monospace"), ("ok", "mono"))
        self.assertEqual(v("Courier New", "monospace"), ("drift", "mono"))
        self.assertEqual(v("Figtree SemiBold"), ("drift", "weight"))
        self.assertEqual(v("Font Awesome 6 Free"), ("info", "icon-font"))


class Reports(unittest.TestCase):
    def test_groups(self):
        findings, stats = scan_text({"site.css": """
            :root { --brand: #A52238; --line: #e0e0e0; --accent: #14b8a6; --ok: #A32035; }
            body { font-family: Inter, sans-serif; color: var(--color-dark); }
            .muted { color: #898A8D }
            .faint { color: #999; background: #fff; }
        """})
        f = by_value(findings)
        self.assertEqual((f["#A52238"]["group"], f["#A52238"]["use"], f["#A52238"]["defined_as"]), ("must", "primary", ["--brand"]))
        self.assertEqual((f["#E0E0E0"]["group"], f["#E0E0E0"]["use"]), ("drift", "border"))
        self.assertEqual(f["#14B8A6"]["group"], "decision")
        self.assertEqual((f["Inter"]["group"], f["Inter"]["rule"]), ("must", "font"))
        self.assertEqual((f["#898A8D"]["kind"], f["#898A8D"]["use"]), ("gray-text", "text-muted"))
        self.assertEqual(f["--color-dark"]["use"], "--color-text")
        self.assertEqual((f["#999999 on #FFFFFF"]["group"], f["#999999 on #FFFFFF"]["rule"]), ("must", "contrast"))
        self.assertNotIn("#A32035", f)
        self.assertEqual(stats["must"], sum(x["group"] == "must" for x in findings))

    def test_category_palette_is_reported_but_not_judged(self):
        files = {"chart.js": 'const domainColors = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f"];\n'}
        findings, stats = scan_text(files)
        self.assertEqual([(f["group"], f["kind"]) for f in findings], [("info", "category-palette")])
        self.assertEqual(stats["in_category_palettes"], 5)
        self.assertIn("for new work only", findings[0]["note"])
        findings, _ = scan_text(files, include_categories=True)
        groups = {f["group"] for f in findings}
        self.assertNotIn("info", groups)
        self.assertIn("#4E79A7", by_value(findings))

    def test_near_copy_of_airi_red_in_a_palette_is_still_flagged(self):
        findings, _ = scan_text({"c.js": 'const palette = ["#A3203A", "#1C5AA0", "#A54A0C", "#6E2E8C", "#1C6B4A"];\n'})
        self.assertEqual(by_value(findings)["#A3203A"]["group"], "must")

    def test_theme_variables_are_not_a_palette(self):
        findings, stats = scan_text({"t.css": ":root {\n  --red: #b91c1c;\n  --blue: #1d4ed8;\n  --green: #15803d;\n  --amber: #b45309;\n  --violet: #6d28d9;\n}\n"})
        self.assertEqual(stats["in_category_palettes"], 0)
        self.assertEqual(by_value(findings)["#B91C1C"]["group"], "must")

    def test_named_data_variables_are_a_palette(self):
        _, stats = scan_text({"t.css": ":root {\n  --domain-1: #b91c1c;\n  --domain-2: #1d4ed8;\n  --domain-3: #15803d;\n  --domain-4: #b45309;\n}\n"})
        self.assertEqual(stats["in_category_palettes"], 4)

    def test_scale_is_one_finding(self):
        findings, _ = scan_text({"s.js": 'const ramp = ["#fee5d9", "#fcae91", "#fb6a4a", "#de2d26", "#a50f15"];\n'})
        scales = [f for f in findings if f["kind"] == "scale"]
        self.assertEqual(len(scales), 1)
        self.assertEqual((scales[0]["group"], scales[0]["rule"]), ("must", "red"))
        self.assertNotIn("#DE2D26", by_value(findings))

    def test_kit_palettes_raise_nothing(self):
        cats = ", ".join(f'"{c}"' for c in ["#2C6395", "#7DC1E3", "#443471", "#B973AB", "#ECBA7B", "#8F8D44", "#2A9484", "#ACC6B1"])
        findings, _ = scan_text({"k.js": f"const categories = [{cats}];\nconst sev = ['#E29CA8', '#D07886', '#B8455A', '#A32035', '#5E0E20'];\n"})
        self.assertEqual(findings, [])

    def test_the_kits_own_stylesheet_is_clean(self):
        findings, _ = bs.build_findings(bs.run_scan([str(ROOT / "skill" / "brand.css")], KIT), KIT)
        self.assertEqual([f for f in findings if f["group"] in ("must", "decision")], [])

    def test_skips_vendor_folders_and_minified_files(self):
        _, stats = scan_text({"a.css": "a{color:#123456}", "node_modules/x/b.css": "a{color:#654321}",
                              "lib.min.js": "var c='#abcdef'", ".git/c.css": "a{color:#111111}", "notes.txt": "#222222"})
        self.assertEqual((stats["files"], stats["distinct_colours"]), (1, 1))

    def test_exclude(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("site/a.css", "data/b.css"):
                (Path(tmp) / name).parent.mkdir(parents=True)
                (Path(tmp) / name).write_text("a{color:#123456}")
            self.assertEqual(bs.run_scan([tmp], KIT, exclude=["data"]).files, 1)

    def test_notebook_reads_source_only(self):
        nb = {"cells": [{"cell_type": "code", "source": ["plt.plot(x, color='#A52238')\n"],
                         "outputs": [{"data": {"text/html": ["<div style='color:#00ff00'>"]}}]}]}
        findings, stats = scan_text({"n.ipynb": json.dumps(nb)})
        self.assertEqual(stats["distinct_colours"], 1)
        self.assertEqual(findings[0]["examples"][0]["loc"], "cell 1, line 1")

    def test_office_file(self):
        theme = ('<a:theme xmlns:a="x"><a:themeElements><a:clrScheme name="Office"><a:dk1><a:sysClr val="windowText" lastClr="000000"/></a:dk1>'
                 '<a:accent1><a:srgbClr val="4472C4"/></a:accent1><a:accent2><a:srgbClr val="898A8D"/></a:accent2></a:clrScheme>'
                 '<a:fontScheme name="Office"><a:majorFont><a:latin typeface="Calibri Light"/></a:majorFont>'
                 '<a:minorFont><a:latin typeface="Figtree"/></a:minorFont></a:fontScheme></a:themeElements></a:theme>')
        slide = ('<p:sld xmlns:a="x" xmlns:p="y"><a:solidFill><a:srgbClr val="A31E38"/></a:solidFill>'
                 '<a:latin typeface="+mn-lt"/><a:latin typeface="Roboto"/></p:sld>')
        with tempfile.TemporaryDirectory() as tmp:
            deck = Path(tmp) / "deck.pptx"
            with zipfile.ZipFile(deck, "w") as z:
                z.writestr("ppt/theme/theme1.xml", theme)
                z.writestr("ppt/slides/slide3.xml", slide)
            before = hashlib.sha256(deck.read_bytes()).hexdigest()
            findings, _ = bs.build_findings(bs.run_scan([str(deck)], KIT), KIT)
            self.assertEqual(before, hashlib.sha256(deck.read_bytes()).hexdigest())
        f = by_value(findings)
        self.assertEqual((f["#A31E38"]["group"], f["#A31E38"]["use"]), ("must", "primary"))
        self.assertIn("slide 3", f["#A31E38"]["places"])
        self.assertEqual(f["Roboto"]["group"], "must")
        self.assertEqual(f["Calibri Light"]["group"], "must")
        theme_f = next(x for x in findings if x["kind"] == "theme")
        self.assertEqual({s["slot"] for s in theme_f["slots"]}, {"dark1", "accent1"})

    def test_command_line_reads_only_and_sets_exit_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "page.html"
            page.write_text("<style>h1 { color: #A52238; font-family: Georgia }</style>")
            before = (page.read_bytes(), page.stat().st_mtime_ns, sorted(p.name for p in Path(tmp).iterdir()))
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(bs.main([tmp]), 0)
                self.assertEqual(bs.main([tmp, "--fail-on-hard"]), 1)
            self.assertIn("## Must fix (hard rules)", out.getvalue())
            self.assertIn("page.html:1", out.getvalue())
            self.assertNotIn(tmp, out.getvalue())           # reports give paths relative to what was scanned
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                bs.main([tmp, "--json"])
            data = json.loads(out.getvalue())
            self.assertEqual(data["stats"]["must"], 2)
            self.assertEqual(before, (page.read_bytes(), page.stat().st_mtime_ns, sorted(p.name for p in Path(tmp).iterdir())))


if __name__ == "__main__":
    unittest.main(verbosity=1)
