#!/usr/bin/env python3
"""Unit tests for the Docsify-aware link checker's resolve() logic.

Run: python3 scripts/test_check_links.py   (or: python3 -m unittest)

Uses a self-contained temporary docs tree so the tests do not depend on the
actual documentation content.
"""

import importlib.util
import tempfile
import unittest
from pathlib import Path


def _load_module(docs_root: Path):
    spec = importlib.util.spec_from_file_location(
        "check_links", Path(__file__).with_name("check_links.py")
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load check_links.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.DOCS_ROOT = docs_root  # point the checker at our fixture tree
    return mod


class ResolveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        base = Path(cls._tmp.name)
        root = base / "docs"
        (root / "guide").mkdir(parents=True)
        (root / "README.md").write_text("# root", encoding="utf-8")
        (root / "guide" / "intro.md").write_text("# intro", encoding="utf-8")
        (root / "guide" / "img.png").write_text("x", encoding="utf-8")
        # A file that is a sibling of docs/ — reachable via ../ but NOT served.
        (base / "outside.md").write_text("# outside", encoding="utf-8")
        cls.cl = _load_module(root)
        cls.src = root / "guide" / "intro.md"

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def ok(self, target: str) -> bool:
        return self.cl.resolve(target, self.src) is not None

    # --- valid targets ---------------------------------------------------
    def test_root_relative(self):
        self.assertTrue(self.ok("guide/intro.md"))

    def test_extensionless_adds_md(self):
        self.assertTrue(self.ok("guide/intro"))

    def test_absolute_from_docs_root(self):
        self.assertTrue(self.ok("/README.md"))

    def test_source_relative_image(self):
        self.assertTrue(self.ok("img.png"))  # sits beside the source file

    def test_title_is_stripped(self):
        self.assertTrue(self.ok('guide/intro.md "Some title"'))
        self.assertTrue(self.ok("guide/intro.md 'Some title'"))

    def test_angle_bracket_wrapped(self):
        self.assertTrue(self.ok("<guide/intro.md>"))

    def test_anchor_and_query_fragments(self):
        self.assertTrue(self.ok("guide/intro.md#a-heading"))
        self.assertTrue(self.ok("guide/intro?id=a-heading"))

    def test_pure_fragment_is_same_page(self):
        self.assertIsNotNone(self.cl.resolve("?id=only-anchor", self.src))

    # --- broken targets --------------------------------------------------
    def test_missing_file(self):
        self.assertFalse(self.ok("guide/missing.md"))

    def test_missing_file_with_title(self):
        self.assertFalse(self.ok('guide/missing.md "title"'))

    def test_escapes_docs_root(self):
        # exists on disk (sibling of docs/) but is not served by Docsify
        self.assertFalse(self.ok("../outside.md"))

    def test_escapes_to_filesystem(self):
        self.assertFalse(self.ok("../../../../../../etc/hostname"))

    # --- extraction helpers ---------------------------------------------
    def test_external_and_email_skipped(self):
        self.assertTrue(self.cl.is_external("https://example.com"))
        self.assertTrue(self.cl.is_external("//unpkg.com/x"))
        self.assertFalse(self.cl.is_external("guide/intro.md"))


class CheckFileTests(unittest.TestCase):
    """End-to-end extraction tests: which targets check_file() flags."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        root = Path(cls._tmp.name) / "docs"
        (root / "guide").mkdir(parents=True)
        (root / "guide" / "intro.md").write_text("# intro", encoding="utf-8")
        (root / "guide" / "policy.pdf").write_text("x", encoding="utf-8")
        cls.cl = _load_module(root)
        cls.root = root

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def broken(self, text: str) -> list:
        page = self.root / "page.md"
        page.write_text(text, encoding="utf-8")
        return self.cl.check_file(page)

    # --- <a href> internal links ------------------------------------------
    def test_html_anchor_with_missing_target_is_flagged(self):
        result = self.broken('<a href="/guide/missing.pdf">Policy</a>\n')
        self.assertEqual(result, [(1, "/guide/missing.pdf")])

    def test_html_anchor_with_valid_target_passes(self):
        self.assertEqual(self.broken('<a href="/guide/policy.pdf">Policy</a>\n'), [])

    def test_html_anchor_external_is_skipped(self):
        self.assertEqual(self.broken('<a href="https://example.com/x">x</a>\n'), [])

    def test_html_anchor_pure_fragment_is_skipped(self):
        self.assertEqual(self.broken('<a href="#section">jump</a>\n'), [])

    # --- fenced code blocks are not scanned --------------------------------
    def test_link_inside_fenced_code_block_is_skipped(self):
        text = "```markdown\n[example](does/not/exist.md)\n```\n"
        self.assertEqual(self.broken(text), [])

    def test_link_after_fence_closes_is_still_checked(self):
        text = "```text\noutput\n```\n[bad](does/not/exist.md)\n"
        self.assertEqual(self.broken(text), [(4, "does/not/exist.md")])


if __name__ == "__main__":
    unittest.main(verbosity=2)
