#!/usr/bin/env python3
"""Keep the published ChessRun docs honest about their markdown sources.

    python scripts/check-chessrun-docs.py

Checks every page in ``projects/chessrun/``:

1. **Well-formed** — tag balance via ``html.parser`` (unclosed or stray tags).
2. **Anchors resolve** — every in-page ``#link`` has a matching ``id``.
3. **Markdown coverage** — each page is compared with its source document in the
   product repository, and any section heading present in the markdown but
   absent from the page is reported. The pages are hand-authored (they carry
   diagrams and layout the markdown does not), so this is a *drift report*, not
   a build: review the missing headings and either publish them or accept them
   deliberately. A page that is not listed in ``PAIRS`` yet is flagged too.

Exit code is non-zero when something is wrong, so it can be wired into CI later.

The product repository is expected next to this one (``../../chess-AI``). Pass
``--product-docs <path>`` to point somewhere else.
"""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "projects" / "chessrun"
DEFAULT_PRODUCT_DOCS = ROOT.parent / "chess-AI" / "docs"

VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}

#: published page -> markdown source, relative to the product docs directory
PAIRS = {
    "ai_model_strategy.html": "architecture/AI_MODEL_STRATEGY.md",
    "frd_product.html": "product/FRD_PRODUCT.md",
    "frd_technical.html": "requirements/FRD_TECHNICAL.md",
    "memory_retrieval_context_architecture.html": "architecture/MEMORY_RETRIEVAL_CONTEXT_ARCHITECTURE.md",
    "player_intelligence_architecture.html": "architecture/PLAYER_INTELLIGENCE_ARCHITECTURE.md",
    "pricing_monetization_strategy.html": "strategy/PRICING_MONETIZATION_STRATEGY.md",
}


class _Balance(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, int]] = []
        self.problems: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID_TAGS:
            return
        self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        if not self.stack:
            self.problems.append(f"line {self.getpos()[0]}: </{tag}> with nothing open")
            return
        open_tag, line = self.stack.pop()
        if open_tag != tag:
            self.problems.append(
                f"line {self.getpos()[0]}: </{tag}> closes <{open_tag}> opened at line {line}"
            )


def _norm(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    for entity, char in (
        ("&amp;", "&"), ("&nbsp;", " "), ("&#39;", "'"), ("&quot;", '"'),
        ("&lt;", "<"), ("&gt;", ">"), ("&mdash;", "-"), ("&ndash;", "-"),
    ):
        text = text.replace(entity, char)
    text = re.sub(r"[^a-z0-9 ]+", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def check_page(page: Path) -> tuple[list[str], list[str], list[str]]:
    html = page.read_text(encoding="utf-8", errors="replace")
    parser = _Balance()
    parser.feed(html)
    problems = list(parser.problems)
    for tag, line in parser.stack:
        problems.append(f"line {line}: <{tag}> never closed")

    ids = set(re.findall(r'\bid="([^"]+)"', html))
    anchors = set(re.findall(r'href="#([^"]+)"', html))
    dangling = sorted(a for a in anchors if a not in ids)

    return problems, dangling, []


def check_coverage(page: Path, md_path: Path) -> list[str]:
    md = md_path.read_text(encoding="utf-8", errors="replace")
    html = _norm(page.read_text(encoding="utf-8", errors="replace"))
    headings = [h.strip() for h in re.findall(r"^#{2,4}\s+(.+)$", md, flags=re.MULTILINE)]
    return [h for h in headings if _norm(h) and _norm(h) not in html]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--product-docs", default=str(DEFAULT_PRODUCT_DOCS))
    ap.add_argument("--quiet-coverage", action="store_true", help="skip the markdown drift report")
    args = ap.parse_args()
    product_docs = Path(args.product_docs)

    failures = 0
    for page in sorted(PAGES.glob("*.html")):
        problems, dangling, _ = check_page(page)
        print(f"\n=== {page.name} ===")
        if problems:
            failures += 1
            print("  STRUCTURE FAILURES:")
            for item in problems[:10]:
                print(f"    - {item}")
        else:
            print("  structure: ok")

        if dangling:
            failures += 1
            print("  ANCHORS THAT GO NOWHERE:")
            for item in dangling[:10]:
                print(f"    - #{item}")
        else:
            print("  anchors: ok")

        source = PAIRS.get(page.name)
        if not source:
            print("  coverage: NOT MAPPED to a markdown source (add it to PAIRS)")
            continue
        md_path = product_docs / source
        if not md_path.exists():
            print(f"  coverage: source missing at {md_path}")
            continue
        if args.quiet_coverage:
            continue
        missing = check_coverage(page, md_path)
        if missing:
            print(f"  coverage: {len(missing)} markdown heading(s) not published from {source}")
            for item in missing[:12]:
                print(f"    - {item}")
            if len(missing) > 12:
                print(f"    ... and {len(missing) - 12} more")
        else:
            print(f"  coverage: every heading in {source} is represented")

    print("\nOK" if failures == 0 else f"\n{failures} page(s) with structural problems")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
