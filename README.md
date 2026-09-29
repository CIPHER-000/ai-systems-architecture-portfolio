# ai-systems-architecture-portfolio

Static portfolio site (Netlify, `publish = "."`, no build step). Each project
lives under `projects/<name>/` with its own stylesheet.

## ChessRun docs

The ChessRun pages are the published form of the architecture and requirements
documents kept in the product repository (`chess-AI/docs/`). The pages are
hand-authored — they carry layout, diagrams and cross-links the markdown does
not — but every one of them has a single markdown source:

| Published page | Markdown source (in `chess-AI/docs/`) |
|---|---|
| `projects/chessrun/index.html` | hub page, no source |
| `projects/chessrun/frd_product.html` | `product/FRD_PRODUCT.md` |
| `projects/chessrun/frd_technical.html` | `requirements/FRD_TECHNICAL.md` |
| `projects/chessrun/ai_model_strategy.html` | `architecture/AI_MODEL_STRATEGY.md` |
| `projects/chessrun/memory_retrieval_context_architecture.html` | `architecture/MEMORY_RETRIEVAL_CONTEXT_ARCHITECTURE.md` |
| `projects/chessrun/player_intelligence_architecture.html` | `architecture/PLAYER_INTELLIGENCE_ARCHITECTURE.md` |
| `projects/chessrun/pricing_monetization_strategy.html` | `strategy/PRICING_MONETIZATION_STRATEGY.md` |

When a source document changes, the matching page has to change with it. The
pages are otherwise free to drift for months without anyone noticing, so:

```bash
python scripts/check-chessrun-docs.py
```

It checks every ChessRun page for well-formed markup and for in-page anchors
that resolve, and reports the section headings the markdown has but the page
does not. The product repository is expected as a sibling directory
(`../chess-AI`); point elsewhere with `--product-docs <path>`. Coverage output
is a drift report, not a build: some headings are deliberately merged into one
section on the page, and the report is there so that decision stays deliberate.

Run it before opening a pull request that touches `projects/chessrun/`.

## Other projects

- `projects/momenta/` — generated from standalone HTML sources by
  `scripts/build-momenta-docs.py` (styling by `scripts/build-momenta-css.py`).
