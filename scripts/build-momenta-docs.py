#!/usr/bin/env python3
"""Transform Momenta standalone HTML into portfolio doc-suite pages."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOMENTA = ROOT / "projects" / "momenta"

DOCS = [
    {
        "file": "momenta-product-ai-systems-proposal.html",
        "out": "product-ai-systems-proposal.html",
        "topbar": "Strategic Proposal",
        "title": "Product &amp; AI Systems Proposal",
        "eyebrow": "Strategic Proposal",
        "meta": "AI concierge direction, supply intelligence, and technical evolution",
        "nav_current": "product-ai-systems-proposal.html",
    },
    {
        "file": "momenta-execution-companion.html",
        "out": "execution-companion.html",
        "topbar": "Execution Companion",
        "title": "Product Execution Companion",
        "eyebrow": "Execution Companion",
        "meta": "Execution direction, product flows, and MVP structure",
        "nav_current": "execution-companion.html",
    },
    {
        "file": "momenta-engineering-architecture-addendum.html",
        "out": "engineering-architecture-addendum.html",
        "topbar": "Engineering Addendum",
        "title": "Engineering Architecture Addendum",
        "eyebrow": "Engineering Addendum",
        "meta": "System architecture and engineering design",
        "nav_current": "engineering-architecture-addendum.html",
    },
]

NAV_LINKS = [
    ("product-ai-systems-proposal.html", "Strategic Proposal"),
    ("execution-companion.html", "Execution Companion"),
    ("engineering-architecture-addendum.html", "Engineering Addendum"),
]


def parse_toc(html: str) -> list[tuple[str, str]]:
    toc_block = re.search(r'<nav class="toc"[^>]*>.*?</nav>', html, re.DOTALL)
    if not toc_block:
        return []
    items = []
    for m in re.finditer(r'<a href="(#[^"]+)">([^<]+)</a>', toc_block.group(0)):
        items.append((m.group(1), m.group(2).strip()))
    return items


def build_sidebar(toc: list[tuple[str, str]]) -> str:
    lines = ['<span class="toc-label">Contents</span>', '<ul class="toc-list">']
    for i, (href, label) in enumerate(toc, 1):
        sid = href.lstrip("#")
        lines.append(
            f'    <li class="toc-item"><a href="{href}" class="toc-link">'
            f'<span class="toc-num">{i}</span>{label}</a></li>'
        )
    lines.append("  </ul>")
    return "\n".join(lines)


def extract_main(html: str) -> str:
    m = re.search(r"<main class=\"page\">(.*?)</main>", html, re.DOTALL)
    if not m:
        raise ValueError('No <main class="page"> found')
    content = m.group(1)
    content = re.sub(r'<div class="colophon">.*?</div>\s*', "", content, flags=re.DOTALL)
    content = re.sub(
        r'<section id="([^"]+)"([^>]*)>',
        r'<section class="section-block">\n    <div id="\1" class="section-anchor"></div>',
        content,
    )
    return content.strip()


def build_doc_nav(current: str) -> str:
    parts = ['<span class="doc-nav-label">Suite:</span>', '<a href="index.html" class="doc-hub-link">Hub</a>']
    for href, label in NAV_LINKS:
        if href == current:
            parts.append(f'<span class="doc-current">{label}</span>')
        else:
            parts.append(f'<a href="{href}">{label}</a>')
    return "\n    ".join(parts)


MERMAID_MODULE = """<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs";
  window.mermaid = mermaid;
  if (window.DocSuite) window.DocSuite.initMermaid();
</script>"""

NO_MERMAID = ""


def render_page(cfg: dict, html: str) -> str:
    toc = parse_toc(html)
    sidebar = build_sidebar(toc)
    main = extract_main(html)
    doc_nav = build_doc_nav(cfg["nav_current"])
    mermaid_script = MERMAID_MODULE if "mermaid" in html else NO_MERMAID
    pills = (
        '<span class="meta-pill"><span class="pill-label">Project</span>Momenta</span>'
        '<span class="meta-pill"><span class="pill-label">Type</span>' + cfg["eyebrow"] + "</span>"
        '<span class="meta-pill"><span class="pill-label">Date</span>May 2026</span>'
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{cfg['title'].replace('&amp;', '&')} — Momenta Docs</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="shared.css" />
</head>
<body class="theme-momenta">

<header class="topbar">
  <div class="topbar-left">
    <a href="../../index.html" class="topbar-portfolio">← Portfolio</a>
    <a href="index.html" class="topbar-brand">Momenta</a>
  </div>
  <div class="topbar-right">
    <span class="topbar-title">{cfg['topbar']}</span>
    <button class="hamburger" id="hamburger" aria-label="Toggle navigation">&#9776;</button>
  </div>
</header>

<div class="sidebar-overlay"></div>

<nav class="sidebar" aria-label="Table of contents">
  {sidebar}
</nav>

<div class="doc-header">
  <h1 class="doc-title">{cfg['title']}</h1>
  <div class="meta-pills">
    {pills}
  </div>
  <p class="confidentiality-note">Prepared for Momenta · Internal architecture documentation</p>
  <nav class="doc-nav">
    {doc_nav}
  </nav>
</div>

<main class="main-content">
<div class="content-inner momenta-doc">
{main}
</div>
</main>

<button id="back-to-top" aria-label="Back to top" title="Back to top">↑</button>

<script src="../../assets/scripts/doc-suite.js"></script>
{mermaid_script}
</body>
</html>
""".replace("{mermaid_script}", mermaid_script)


def main():
    for cfg in DOCS:
        src = MOMENTA / cfg["file"]
        html = src.read_text(encoding="utf-8")
        out = render_page(cfg, html)
        (MOMENTA / cfg["out"]).write_text(out, encoding="utf-8")
        print("Wrote", cfg["out"])


if __name__ == "__main__":
    main()
