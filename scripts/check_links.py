#!/usr/bin/env python3
"""Docsify-aware internal link checker for the ilifu user documentation.

Docsify resolves links relative to the current page and treats the ``docs/``
folder as the site root. Links frequently omit the ``.md`` extension and may
carry ``#anchor`` fragments, so a generic file-based link checker produces false
positives. This script mirrors Docsify's resolution rules and only flags links
whose target genuinely cannot be found.

Checks, for every ``*.md`` file under ``docs/``:
  * Markdown links ``[text](target)``
  * Image targets ``![alt](target)`` and ``<img src="target">``

External links (http, https, protocol-relative ``//``, ``mailto:``) and pure
anchors (``#...``) are skipped. Exit status is non-zero if any broken link is
found, so it can gate a CI job.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

DOCS_ROOT = Path(__file__).resolve().parent.parent / "docs"

# [text](target) but not images (negative lookbehind for the leading '!').
MD_LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)]+)\)")
# ![alt](target)
MD_IMAGE = re.compile(r"\!\[[^\]]*\]\(([^)]+)\)")
# <img ... src="target" ...>
HTML_IMG = re.compile(r"<img[^>]*\ssrc=[\"']([^\"']+)[\"']", re.IGNORECASE)

SKIP_PREFIXES = ("http://", "https://", "//", "mailto:", "tel:", "data:")


def is_external(target: str) -> bool:
    return target.startswith(SKIP_PREFIXES)


def _candidates(base: Path) -> list[Path]:
    """Files a link may point at: as-is, plus .md / folder-README for extensionless."""
    cands = [base]
    if base.suffix == "":
        cands.append(base.with_suffix(".md"))
        cands.append(base / "README.md")
    return cands


def resolve(target: str, source: Path) -> Path | None:
    """Return a resolved filesystem path for a link, or None if genuinely broken.

    Docsify strips ``#anchor`` and ``?id=anchor`` fragments. With the default
    ``relativePath: false`` links resolve from the site root (DOCS_ROOT); some
    content (e.g. tutorial images beside their page) reads more naturally as
    source-relative. To avoid false positives on that ambiguity, a link is
    considered valid if it resolves under *either* interpretation, and only
    flagged when it resolves under neither. Extensionless links try ``.md`` and a
    folder ``README.md`` fallback, matching Docsify's routing.

    A CommonMark link destination may be wrapped in ``<...>`` and/or followed by
    an optional title: ``[t](path "title")`` / ``[t](<path> 'title')``. Extract
    the bare destination before resolving.
    """
    target = target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1:target.index(">")]
    elif target.split():
        # Unbracketed destination is the first whitespace-delimited token; any
        # remainder is a title (CommonMark requires <...> for spaces in a path).
        target = target.split()[0]

    # Strip anchor (#...) and query (?id=...) fragments.
    clean = target.split("#", 1)[0].split("?", 1)[0].strip()
    if not clean:  # was a pure anchor / query — same-page reference
        return source

    if clean.startswith("/"):
        bases = [DOCS_ROOT / clean.lstrip("/")]
    else:
        # Try both root-relative (Docsify default) and source-relative.
        bases = [DOCS_ROOT / clean, source.parent / clean]

    root = DOCS_ROOT.resolve()
    for base in bases:
        for cand in _candidates(base):
            try:
                resolved = cand.resolve()
                # Only accept targets served by Docsify: real files under docs/.
                # A `../` path that escapes the site root would 404 on the live
                # site, so treat it as broken even if it exists on disk.
                if resolved.is_file() and resolved.is_relative_to(root):
                    return cand
            except OSError:
                continue
    return None


def check_file(md: Path) -> list[tuple[int, str]]:
    broken: list[tuple[int, str]] = []
    for lineno, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
        targets = (
            MD_LINK.findall(line)
            + MD_IMAGE.findall(line)
            + HTML_IMG.findall(line)
        )
        for target in targets:
            target = target.strip()
            if not target or target.startswith("#") or is_external(target):
                continue
            # Bare email address written as a link target (no scheme, no path).
            if "@" in target and "/" not in target:
                continue
            if resolve(target, md) is None:
                broken.append((lineno, target))
    return broken


def main() -> int:
    if not DOCS_ROOT.is_dir():
        print(f"docs directory not found at {DOCS_ROOT}", file=sys.stderr)
        return 2

    total_broken = 0
    for md in sorted(DOCS_ROOT.rglob("*.md")):
        broken = check_file(md)
        if broken:
            rel = md.relative_to(DOCS_ROOT.parent)
            for lineno, target in broken:
                print(f"{rel}:{lineno}: broken internal link -> {target}")
                total_broken += 1

    if total_broken:
        print(f"\n{total_broken} broken internal link(s) found.", file=sys.stderr)
        return 1
    print("All internal links resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
