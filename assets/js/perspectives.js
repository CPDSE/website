// Perspectives listing — client-side tag filter (_layouts/perspectives.html).
// Tag links work without JS (they just reload with ?tag=); with JS the list
// filters in place and the URL stays shareable.
(() => {
  const filter = document.querySelector('[data-perspectives-filter]');
  const list = document.querySelector('[data-perspectives-list]');
  if (!list) return;

  const cards = Array.from(list.querySelectorAll('.perspective-card'));
  const empty = document.querySelector('[data-perspectives-empty]');
  const chips = filter ? Array.from(filter.querySelectorAll('[data-tag]')) : [];

  const apply = (tag) => {
    let shown = 0;
    cards.forEach((card) => {
      const tags = card.dataset.tags.trim().split(/\s+/);
      const match = !tag || tags.includes(tag);
      card.hidden = !match;
      if (match) shown++;
    });
    chips.forEach((chip) => {
      const on = chip.dataset.tag === tag;
      chip.classList.toggle('is-active', on);
      if (on) chip.setAttribute('aria-current', 'true');
      else chip.removeAttribute('aria-current');
    });
    if (empty) empty.hidden = shown > 0;
  };

  const current = () => new URLSearchParams(window.location.search).get('tag') || '';

  // Any tag link inside the listing (toolbar chips or card chips) filters in place
  document.querySelector('.perspectives-main').addEventListener('click', (e) => {
    const link = e.target.closest('a[data-tag]');
    if (!link) return;
    e.preventDefault();
    const tag = link.dataset.tag;
    history.pushState({ tag }, '', tag ? `?tag=${encodeURIComponent(tag)}` : window.location.pathname);
    apply(tag);
  });

  window.addEventListener('popstate', () => apply(current()));
  apply(current());
})();
