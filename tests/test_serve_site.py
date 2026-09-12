"""The tagging system that lets every craft share one repo.

Craft and tags are the only reason multiple drones can live side by side without
the sections becoming a junk drawer, so the parsing and the generated collection
pages are worth pinning down.
"""
import os
import shutil
import sys
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from tools import serve_site


class FrontmatterTest(unittest.TestCase):

    def test_inline_list_and_scalars(self):
        meta, body = serve_site.parse_frontmatter(
            '---\ntitle: "Air65"\ncraft_name: "AIR65 F"\n'
            "tags: [setup, rates, osd]\n---\n\n## Body\n"
        )
        self.assertEqual(meta["title"], "Air65")
        self.assertEqual(meta["craft_name"], "AIR65 F")
        self.assertEqual(meta["tags"], ["setup", "rates", "osd"])
        self.assertIn("## Body", body)

    def test_block_list(self):
        meta, _ = serve_site.parse_frontmatter(
            "---\ntitle: Spec\ntags:\n  - hardware\n  - setup\n---\nbody\n"
        )
        self.assertEqual(meta["tags"], ["hardware", "setup"])

    def test_document_without_frontmatter_is_untouched(self):
        meta, body = serve_site.parse_frontmatter("# Just markdown\n")
        self.assertEqual(meta, {})
        self.assertEqual(body, "# Just markdown\n")

    def test_body_containing_horizontal_rules_survives(self):
        """`---` is used as a section break throughout the workshop pages."""
        meta, body = serve_site.parse_frontmatter(
            "---\ntitle: Doc\n---\n\n## One\n\n---\n\n## Two\n"
        )
        self.assertEqual(meta["title"], "Doc")
        self.assertIn("## Two", body)


class TaxonomyTest(unittest.TestCase):

    def test_craft_name_is_accepted_as_craft(self):
        """Flight logs and capture_log.py already write `craft_name`."""
        self.assertEqual(serve_site.page_craft({"craft_name": "Crafty"}), "Crafty")
        self.assertEqual(serve_site.page_craft({"craft": "AIR65 F"}), "AIR65 F")
        self.assertEqual(serve_site.page_craft({}), "")

    def test_craft_field_wins_over_craft_name(self):
        self.assertEqual(
            serve_site.page_craft({"craft": "AIR65 F", "craft_name": "Crafty"}),
            "AIR65 F",
        )

    def test_tags_accept_a_bare_string(self):
        self.assertEqual(serve_site.page_tags({"tags": "setup, rates"}), ["setup", "rates"])
        self.assertEqual(serve_site.page_tags({}), [])

    def test_slugs_are_url_safe_and_stable(self):
        self.assertEqual(serve_site.slugify("AIR65 F"), "air65-f")
        self.assertEqual(serve_site.slugify("WHOOP_SHOP_01"), "whoop-shop-01")
        self.assertEqual(serve_site.slugify("!!!"), "untagged")


class BuildSiteTest(unittest.TestCase):

    def setUp(self):
        self.base = tempfile.mkdtemp()
        self.out = os.path.join(self.base, "public_html")
        content = os.path.join(self.base, "content")
        os.makedirs(os.path.join(content, "spec"))
        os.makedirs(os.path.join(content, "log"))

        self._write(content, "spec/_index.md", '---\ntitle: "Build Specs"\n---\nIntro prose.\n')
        self._write(content, "spec/air65.md",
                    '---\ntitle: "Air65 Build"\ncraft_name: "AIR65 F"\n'
                    "tags: [hardware, setup]\n---\n\n# Air65 Build\n\nBody.\n")
        self._write(content, "log/_index.md", '---\ntitle: "Logs"\n---\nLog intro.\n')
        self._write(content, "log/first.md",
                    '---\ntitle: "First Flight"\ncraft_name: "AIR65 F"\n'
                    "tags: [setup]\n---\n\n# First Flight\n\nBody.\n")
        self._write(content, "log/other.md",
                    '---\ntitle: "Other Craft"\ncraft_name: "Crafty"\n'
                    "tags: [tuning]\n---\n\n# Other Craft\n\nBody.\n")

        serve_site.build_site(self.base, self.out)

    def tearDown(self):
        shutil.rmtree(self.base, ignore_errors=True)

    def _write(self, root, rel, text):
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

    def _read(self, rel):
        with open(os.path.join(self.out, rel), encoding="utf-8") as f:
            return f.read()

    def test_a_page_exists_for_each_tag(self):
        for tag in ("hardware", "setup", "tuning"):
            self.assertTrue(os.path.exists(os.path.join(self.out, "tags", f"{tag}.html")), tag)

    def test_tag_page_gathers_pages_across_sections(self):
        """`setup` is used in both spec/ and log/, which is the whole point."""
        html = self._read("tags/setup.html")
        self.assertIn("/spec/air65.html", html)
        self.assertIn("/log/first.html", html)
        self.assertNotIn("/log/other.html", html)

    def test_craft_page_gathers_one_drone(self):
        html = self._read("craft/air65-f.html")
        self.assertIn("/spec/air65.html", html)
        self.assertIn("/log/first.html", html)
        self.assertNotIn("/log/other.html", html)

    def test_craft_index_lists_every_drone(self):
        html = self._read("craft/index.html")
        self.assertIn("AIR65 F", html)
        self.assertIn("Crafty", html)

    def test_tag_index_shows_usage_counts(self):
        html = self._read("tags/index.html")
        self.assertIn("/tags/setup.html", html)
        self.assertIn('<span class="count">2</span>', html)

    def test_pages_render_their_own_chips(self):
        html = self._read("spec/air65.html")
        self.assertIn('class="meta-bar"', html)
        self.assertIn('href="/craft/air65-f.html"', html)
        self.assertIn('href="/tags/hardware.html"', html)

    def test_section_index_keeps_its_intro_prose(self):
        html = self._read("spec/index.html")
        self.assertIn("Intro prose.", html)
        self.assertIn("/spec/air65.html", html)

    def test_untagged_site_still_builds(self):
        base = tempfile.mkdtemp()
        try:
            self._write(os.path.join(base, "content"), "docs/plain.md", "# Plain\n\nNo frontmatter.\n")
            out = os.path.join(base, "public_html")
            serve_site.build_site(base, out)
            self.assertTrue(os.path.exists(os.path.join(out, "tags", "index.html")))
            self.assertIn("No tags in use yet.", open(os.path.join(out, "tags", "index.html")).read())
        finally:
            shutil.rmtree(base, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
