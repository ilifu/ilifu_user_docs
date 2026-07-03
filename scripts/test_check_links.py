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


if __name__ == "__main__":
    unittest.main(verbosity=2)
