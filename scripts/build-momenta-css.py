from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
src = (ROOT / "projects/chessrun/shared.css").read_text(encoding="utf-8")
layout = src.split("/* ── Reset")[1]

momenta_root = """/* Momenta Document Suite — shared.css */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg: #faf6ef;
  --surface-low: #f3ece0;
  --surface: #fdfaf3;
  --surface-bright: #ebe3d4;
  --surface-highest: #e3dccf;
  --paper: #fdfaf3;
  --bg-alt: #f3ece0;
  --primary: #7a3a2c;
  --primary-light: #a76353;
  --secondary: #a76353;
  --error: #c0392b;
  --text-primary: #2a2522;
  --text-secondary: #4a4341;
  --text-muted: #807773;
  --on-surface-var: #6b625c;
  --code-bg: #f3ece0;
  --code-surface: #ebe3d4;
  --code-text: #2a2522;
  --code-blue: #5c4a3a;
  --code-green: #3d5c4a;
  --code-yellow: #8a6b2c;
  --code-purple: #6b4a5c;
  --code-red: #a63d2f;
  --code-comment: #807773;
  --severity-critical: #c0392b;
  --severity-significant: #c9a227;
  --severity-developing: #5c6b7a;
  --severity-positive: #3d5c4a;
  --sidebar-width: 260px;
  --topbar-height: 56px;
  --content-max: 820px;
  --content-gutter: 48px;
  --serif: "Cormorant Garamond", Georgia, serif;
  --sans: "Inter", -apple-system, sans-serif;
  --mono: "JetBrains Mono", monospace;
  --mermaid-primary: #fdfaf3;
  --mermaid-text: #2a2522;
  --mermaid-border: #a76353;
  --mermaid-line: #7a3a2c;
  --mermaid-secondary: #f3ece0;
  --mermaid-tertiary: #faf6ef;
  --mermaid-bg: #faf6ef;
  --mermaid-main: #fdfaf3;
  --mermaid-title: #7a3a2c;
  --mermaid-font: Inter, sans-serif;
  --mermaid-muted: #4a4341;
  --mermaid-border-strong: #d2c9b8;
  --mermaid-accent-soft: #a76353;
  --mermaid-paper: #fdfaf3;
}

body.theme-momenta {
  background: var(--bg);
  color: var(--text-secondary);
  font-family: var(--sans);
}

"""

replacements = [
    ("#0a0f14", "var(--bg)"),
    ("rgba(10, 15, 20, 0.96)", "rgba(250, 246, 239, 0.96)"),
    ("rgba(20, 26, 32, 0.5)", "rgba(243, 236, 224, 0.8)"),
    ("rgba(132, 255, 0, 0.06)", "rgba(122, 58, 44, 0.08)"),
    ("rgba(132, 255, 0, 0.08)", "rgba(122, 58, 44, 0.1)"),
    ("rgba(105, 246, 184, 0.08)", "rgba(167, 99, 83, 0.1)"),
    ("rgba(132, 255, 0, 0.12)", "rgba(122, 58, 44, 0.1)"),
    ("rgba(132, 255, 0, 0.14)", "rgba(122, 58, 44, 0.12)"),
    ("0 0 16px rgba(132, 255, 0, 0.3)", "0 0 16px rgba(122, 58, 44, 0.2)"),
    ("'Space Grotesk'", "var(--serif)"),
]

for a, b in replacements:
    layout = layout.replace(a, b)

extra = """
.topbar-brand { font-family: var(--serif); font-size: 20px; }
.doc-title { font-family: var(--serif); font-weight: 500; }

.momenta-doc h2 {
  font-family: var(--serif);
  font-size: 30px;
  font-weight: 500;
  color: var(--text-primary);
  margin: 48px 0 20px;
  line-height: 1.2;
}
.momenta-doc h2 .num {
  display: block;
  font-family: var(--sans);
  font-size: 11px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--primary);
  margin-bottom: 10px;
}
.momenta-doc h2.section-break {
  margin-top: 64px;
  padding-top: 24px;
  border-top: 1px solid var(--rule, #e3dccf);
}
.momenta-doc h3 {
  font-family: var(--serif);
  font-size: 20px;
  color: var(--text-primary);
  margin: 32px 0 12px;
}
.momenta-doc p.lead {
  font-family: var(--serif);
  font-size: 19px;
  font-style: italic;
  color: var(--text-secondary);
  line-height: 1.55;
}
.momenta-doc .callout {
  background: var(--bg-alt);
  border: 1px solid var(--rule, #e3dccf);
  border-radius: 4px;
  padding: 22px 28px;
  margin: 28px 0;
  font-family: var(--serif);
  font-style: italic;
  font-size: 18px;
  color: var(--text-primary);
}
.momenta-doc figure.diagram {
  margin: 28px 0;
  padding: 24px;
  background: var(--paper);
  border: 1px solid var(--rule, #e3dccf);
  border-radius: 4px;
}
.momenta-doc figure.diagram figcaption {
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 16px;
}
.momenta-doc pre.codeblock {
  font-family: var(--mono);
  font-size: 13px;
  background: var(--paper);
  border: 1px solid var(--rule, #e3dccf);
  border-left: 2px solid var(--secondary);
  padding: 18px 22px;
  overflow-x: auto;
}
.momenta-doc table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  font-size: 14px;
}
.momenta-doc th,
.momenta-doc td {
  border: 1px solid var(--rule, #e3dccf);
  padding: 10px 14px;
  text-align: left;
}
.momenta-doc th {
  background: var(--bg-alt);
  color: var(--text-muted);
  font-size: 11px;
  text-transform: uppercase;
}
.momenta-doc .mermaid { display: flex; justify-content: center; min-height: 60px; }
.momenta-doc code {
  font-family: var(--mono);
  font-size: 0.88em;
  background: var(--bg-alt);
  border: 1px solid var(--rule, #e3dccf);
  padding: 1px 6px;
  border-radius: 3px;
}
"""

out = momenta_root + "/* ── Reset" + layout + extra
(ROOT / "projects/momenta/shared.css").write_text(out, encoding="utf-8")
print("Wrote shared.css", len(out), "bytes")
