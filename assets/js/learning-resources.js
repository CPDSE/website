/* CPDSE — Learning Resources page interactions
   1) Starter path: Python/R toggle + per-step carousels
   2) External Courses library: search / topic / language / free / certificate + load-more
   Operates on server-rendered DOM (no data duplicated in JS). */
(() => {
  'use strict';

  /* ── 1 · Starter-path carousels ─────────────────────────────── */
  const stepcars = Array.from(document.querySelectorAll('.stepcar'));

  const visibleTrack = (car) => car.querySelector('.stepcar__track:not([hidden])');

  const moveTrack = (track, dir) => {
    if (!track) return;
    const n = track.children.length;
    if (!n) return;
    let i = (parseInt(track.dataset.idx || '0', 10) + dir + n) % n;
    track.dataset.idx = i;
    track.style.transform = `translateX(-${i * 100}%)`;
  };

  stepcars.forEach((car) => {
    const prev = car.querySelector('.carbtn--prev');
    const next = car.querySelector('.carbtn--next');
    if (prev) prev.addEventListener('click', () => moveTrack(visibleTrack(car), -1));
    if (next) next.addEventListener('click', () => moveTrack(visibleTrack(car), 1));
  });

  const langToggle = document.querySelectorAll('.toggle button[data-lang]');
  langToggle.forEach((btn) => {
    btn.addEventListener('click', () => {
      const lang = btn.dataset.lang;
      langToggle.forEach((b) => b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'));
      stepcars.forEach((car) => {
        car.querySelectorAll('.stepcar__track').forEach((t) => {
          const on = t.dataset.lang === lang;
          t.hidden = !on;
          if (on) { t.dataset.idx = '0'; t.style.transform = 'translateX(0)'; }
        });
      });
    });
  });

  /* ── 2 · Library filter dashboard ───────────────────────────── */
  const grid = document.getElementById('lr-grid');
  if (!grid) return;

  const cards   = Array.from(grid.querySelectorAll('.rcard'));
  const countEl = document.getElementById('lr-count');
  const emptyEl = document.getElementById('lr-empty');
  const moreBtn = document.getElementById('lr-more');
  const total   = cards.length;
  const BATCH   = 12;

  const state = { q: '', topic: '', lang: '', free: false, cert: false };
  let shown = BATCH;

  const matches = (card) => {
    const d = card.dataset;
    if (state.q && !(d.search || '').includes(state.q)) return false;
    if (state.topic && d.topic !== state.topic) return false;
    if (state.lang && d.lang !== state.lang && d.lang !== 'Both') return false;
    if (state.free && d.free !== 'true') return false;
    if (state.cert && d.cert !== 'true') return false;
    return true;
  };

  const anyFilter = () => state.q || state.topic || state.lang || state.free || state.cert;

  const render = () => {
    let matched = 0, visible = 0;
    cards.forEach((card) => {
      if (!matches(card)) { card.hidden = true; return; }
      matched++;
      if (matched <= shown) { card.hidden = false; visible++; } else { card.hidden = true; }
    });

    if (emptyEl) emptyEl.hidden = matched !== 0;

    const remaining = matched - visible;
    if (moreBtn) {
      moreBtn.hidden = remaining <= 0;
      if (remaining > 0) moreBtn.textContent = `Load more (${remaining})`;
    }
    if (countEl) {
      countEl.textContent = anyFilter()
        ? `${matched} match${matched !== 1 ? 'es' : ''} · showing ${visible}`
        : `Showing ${visible} of ${total} resources`;
    }
  };

  const reset = () => { shown = BATCH; render(); };

  const q = document.getElementById('lr-q');
  if (q) q.addEventListener('input', (e) => { state.q = e.target.value.trim().toLowerCase(); reset(); });

  const topic = document.getElementById('lr-topic');
  if (topic) topic.addEventListener('change', (e) => { state.topic = e.target.value; reset(); });

  document.querySelectorAll('#lr-langChips .chip').forEach((c) => {
    c.addEventListener('click', () => {
      state.lang = c.dataset.lang;
      document.querySelectorAll('#lr-langChips .chip').forEach((x) => x.setAttribute('aria-pressed', x === c ? 'true' : 'false'));
      reset();
    });
  });

  const toggleChip = (el, key) => {
    if (!el) return;
    el.addEventListener('click', () => { state[key] = !state[key]; el.setAttribute('aria-pressed', String(state[key])); reset(); });
  };
  toggleChip(document.getElementById('lr-freeOnly'), 'free');
  toggleChip(document.getElementById('lr-certOnly'), 'cert');

  if (moreBtn) moreBtn.addEventListener('click', () => { shown += BATCH; render(); });

  render();
})();
