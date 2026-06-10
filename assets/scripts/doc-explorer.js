/* Expandable documentation explorer for project dashboards */

function initDocExplorer() {
  document.querySelectorAll('[data-doc-explorer]').forEach(root => {
    root.querySelectorAll('.explorer-group').forEach(group => {
      const toggle = group.querySelector('.explorer-group-toggle');
      const panel  = group.querySelector('.explorer-panel');
      if (!toggle || !panel) return;

      const setOpen = (open) => {
        group.classList.toggle('is-open', open);
        toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      };

      const initiallyOpen = group.dataset.open !== 'false';
      setOpen(initiallyOpen);

      toggle.addEventListener('click', () => {
        setOpen(!group.classList.contains('is-open'));
      });
    });
  });
}

document.addEventListener('DOMContentLoaded', initDocExplorer);
