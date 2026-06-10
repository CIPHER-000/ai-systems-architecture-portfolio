/* ============================================================
   Architecture Portfolio — doc-suite.js
   Shared behavior for project documentation pages
   ============================================================ */

function initTOCObserver() {
  const anchors  = document.querySelectorAll('.section-anchor');
  const tocLinks = document.querySelectorAll('.toc-link');
  if (!anchors.length || !tocLinks.length) return;

  const linkMap = new Map();
  tocLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href && href.startsWith('#')) linkMap.set(href.slice(1), link);
  });

  let lastActive = null;
  const topOffset = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--topbar-height'), 10) || 56;

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      const link = linkMap.get(entry.target.id);
      if (!link) return;
      if (entry.isIntersecting) {
        if (lastActive) lastActive.classList.remove('active');
        link.classList.add('active');
        lastActive = link;
      }
    });
  }, {
    rootMargin: `-${topOffset + 20}px 0px -68% 0px`,
    threshold: 0
  });

  anchors.forEach(el => observer.observe(el));
}

function copyCode(btn) {
  const block  = btn.closest('.code-block');
  const codeEl = block ? block.querySelector('code') : null;
  if (!codeEl) return;

  const text = codeEl.textContent || codeEl.innerText;

  const finish = () => {
    btn.textContent = 'Copied ✓';
    btn.classList.add('copied');
    setTimeout(() => {
      btn.textContent = 'Copy';
      btn.classList.remove('copied');
    }, 2000);
  };

  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(finish).catch(() => fallbackCopy(text, finish));
  } else {
    fallbackCopy(text, finish);
  }
}

function fallbackCopy(text, callback) {
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.cssText = 'position:fixed;opacity:0;top:-9999px;left:-9999px';
  document.body.appendChild(ta);
  ta.select();
  try { document.execCommand('copy'); } catch (_) {}
  document.body.removeChild(ta);
  callback();
}

function initSidebarToggle() {
  const hamburger = document.getElementById('hamburger');
  const sidebar   = document.querySelector('.sidebar');
  const overlay   = document.querySelector('.sidebar-overlay');
  if (!hamburger || !sidebar) return;

  const open  = () => { sidebar.classList.add('open');    overlay && overlay.classList.add('visible'); };
  const close = () => { sidebar.classList.remove('open'); overlay && overlay.classList.remove('visible'); };

  hamburger.addEventListener('click', () =>
    sidebar.classList.contains('open') ? close() : open()
  );

  overlay && overlay.addEventListener('click', close);

  sidebar.querySelectorAll('.toc-link').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 768) close();
    });
  });
}

function initBackToTop() {
  const btn = document.getElementById('back-to-top');
  if (!btn) return;

  window.addEventListener('scroll', () => {
    btn.classList.toggle('visible', window.scrollY > 320);
  }, { passive: true });

  btn.addEventListener('click', () =>
    window.scrollTo({ top: 0, behavior: 'smooth' })
  );
}

function getMermaidThemeFromCSS() {
  const root = getComputedStyle(document.documentElement);
  const pick = (name, fallback) => (root.getPropertyValue(name).trim() || fallback);

  return {
    primaryColor:          pick('--mermaid-primary', '#141a20'),
    primaryTextColor:      pick('--mermaid-text', '#e7ebf3'),
    primaryBorderColor:    pick('--mermaid-border', '#252d35'),
    lineColor:             pick('--mermaid-line', '#4a5568'),
    secondaryColor:        pick('--mermaid-secondary', '#0e1419'),
    tertiaryColor:         pick('--mermaid-tertiary', '#252d35'),
    background:            pick('--mermaid-bg', '#0a0f14'),
    mainBkg:               pick('--mermaid-main', '#141a20'),
    nodeBorder:            pick('--mermaid-border', '#252d35'),
    clusterBkg:            pick('--mermaid-secondary', '#0e1419'),
    clusterBorder:         pick('--mermaid-border', '#252d35'),
    titleColor:            pick('--mermaid-title', '#84FF00'),
    edgeLabelBackground:   pick('--mermaid-main', '#141a20'),
    fontFamily:            pick('--mermaid-font', 'Inter, sans-serif'),
    nodeTextColor:         pick('--mermaid-text', '#e7ebf3'),
    labelTextColor:        pick('--mermaid-text', '#e7ebf3'),
    actorBkg:              pick('--mermaid-main', '#141a20'),
    actorBorder:           pick('--mermaid-border', '#252d35'),
    actorTextColor:        pick('--mermaid-text', '#e7ebf3'),
    actorLineColor:        pick('--mermaid-line', '#4a5568'),
    signalColor:           pick('--mermaid-muted', '#8a97a8'),
    signalTextColor:       pick('--mermaid-text', '#e7ebf3'),
    loopTextColor:         pick('--mermaid-text', '#e7ebf3'),
    noteBkgColor:          pick('--mermaid-tertiary', '#252d35'),
    noteTextColor:         pick('--mermaid-text', '#e7ebf3'),
    noteBorderColor:       pick('--mermaid-border-strong', '#2e3840'),
    labelBoxBkgColor:      pick('--mermaid-secondary', '#0e1419'),
    labelBoxBorderColor:   pick('--mermaid-accent-soft', '#a76353'),
    sequenceNumberColor:   pick('--mermaid-paper', '#fdfaf3'),
  };
}

function initMermaid() {
  if (typeof mermaid === 'undefined') return;

  mermaid.initialize({
    startOnLoad: true,
    theme: 'base',
    securityLevel: 'loose',
    themeVariables: getMermaidThemeFromCSS(),
    flowchart: { htmlLabels: true, curve: 'basis', diagramPadding: 16 },
    sequence:  { diagramMarginX: 20, diagramMarginY: 20 },
  });
}

function initHljs() {
  if (typeof hljs === 'undefined') return;
  hljs.configure({ ignoreUnescapedHTML: true });
  hljs.highlightAll();
}

function bootstrapDocSuite() {
  initMermaid();
  initHljs();
  initTOCObserver();
  initSidebarToggle();
  initBackToTop();
}

document.addEventListener('DOMContentLoaded', bootstrapDocSuite);

window.copyCode = copyCode;
window.DocSuite = {
  bootstrapDocSuite,
  initMermaid,
  initHljs,
  initTOCObserver,
  initSidebarToggle,
  initBackToTop,
};
