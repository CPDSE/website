/* CPDSE Reference Models: progressive enhancement only. Every page works without this file. */
(function () {
  "use strict";

  var root = document.documentElement.getAttribute("data-root") || "./";
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) { /* storage unavailable */ } }
  };
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }

  /* ---- theme toggle: auto → light → dark ------------------------------------- */
  function initTheme() {
    var btn = $("[data-theme-toggle]");
    if (!btn) return;
    var order = ["auto", "light", "dark"];
    function current() { return document.documentElement.getAttribute("data-theme") || "auto"; }
    function render() {
      var t = current();
      var label = btn.querySelector(".tt-label");
      label.textContent = "Theme: " + t;
      btn.setAttribute("aria-label", "Colour theme: " + t + ". Change theme");
    }
    btn.hidden = false;
    render();
    btn.addEventListener("click", function () {
      var next = order[(order.indexOf(current()) + 1) % order.length];
      if (next === "auto") document.documentElement.removeAttribute("data-theme");
      else document.documentElement.setAttribute("data-theme", next);
      store.set("cpdse-rm-theme", next === "auto" ? null : next);
      render();
    });
  }

  /* ---- search ------------------------------------------------------------------ */
  var indexPromise = null;
  function loadIndex() {
    if (!indexPromise) {
      indexPromise = fetch(root + "assets/search-index.json").then(function (r) {
        if (!r.ok) throw new Error("index " + r.status);
        return r.json();
      }).then(function (items) {
        items.forEach(function (e) {
          e._t = norm(e.t); e._s = norm(e.s || ""); e._x = norm(e.x || ""); e._b = norm(e.b || ""); e._p = norm(e.p || "");
        });
        return items;
      });
    }
    return indexPromise;
  }
  function norm(s) {
    return String(s).normalize("NFKD").replace(/[\u0300-\u036f]/g, "").toLowerCase()
      .replace(/&/g, " and ").replace(/[^a-z0-9.]+/g, " ").trim();
  }
  var GROUPS = [["where", "Where · Pharma Value Chain"], ["what", "What · PDS Competence Model"], ["how", "How · Pedagogic Practices"],
    ["ex", "Examples"], ["neutral", "Tools, glossary and pages"], ["start", "Start page"]];

  function search(items, q) {
    var tokens = norm(q).split(" ").filter(Boolean);
    if (!tokens.length) return [];
    var full = tokens.join(" ");
    var hits = [];
    items.forEach(function (e) {
      var score = 0;
      for (var i = 0; i < tokens.length; i++) {
        var t = tokens[i], s = 0;
        if (e._t === t || e._t === full) s = 100;
        else if (e._t.indexOf(t) === 0) s = 60;
        else if ((" " + e._t).indexOf(" " + t) >= 0) s = 40;
        else if ((" " + e._s).indexOf(" " + t) >= 0) s = 30;
        else if (e._t.indexOf(t) >= 0) s = 20;
        else if (e._x.indexOf(t) >= 0 || e._p.indexOf(t) >= 0) s = 10;
        else if (e._b.indexOf(t) >= 0) s = 5;
        if (!s) return;
        score += s;
      }
      if (e._t === full) { score += 100; e._best = true; } else { e._best = (" " + e._t + " ").indexOf(" " + full + " ") >= 0 && tokens.length === 1 && e._t.length <= full.length + 12; }
      if (e.k === "section") score -= 3;
      hits.push({ e: e, score: score });
    });
    hits.sort(function (a, b) { return b.score - a.score || a.e.t.length - b.e.t.length; });
    return hits.map(function (h) { return h.e; });
  }

  function renderResults(container, results, idPrefix, limitPerGroup, asOptions) {
    var html = "", n = 0;
    var best = results.filter(function (e) { return e._best; }).slice(0, 3);
    var rest = results.filter(function (e) { return best.indexOf(e) < 0; });
    var groups = (best.length ? [["_best", "Best match"]] : []).concat(GROUPS);
    groups.forEach(function (g) {
      var list = g[0] === "_best" ? best : rest.filter(function (e) { return e.m === g[0]; });
      if (!list.length) return;
      var shown = limitPerGroup ? list.slice(0, limitPerGroup) : list;
      var gid = idPrefix + "-g-" + g[0];
      html += '<div class="sd-group"' + (asOptions ? ' role="group" aria-labelledby="' + gid + '"' : "") + '><p class="sd-group-h" id="' + gid + '">' + esc(g[1]) +
        (shown.length < list.length ? " · top " + shown.length + " of " + list.length : "") + '</p><ul class="sd-list" role="presentation">';
      shown.forEach(function (e) {
        var inner = '<span class="sd-t">' + esc(e.t) + '</span>' +
          (e.p ? '<span class="sd-p">' + esc(e.p) + "</span>" : "") +
          (e.x ? '<span class="sd-x">' + esc(e.x) + "</span>" : "");
        if (asOptions) {
          html += '<li class="sd-item m-' + esc(e.m) + '" role="option" id="' + idPrefix + "-o-" + n + '" aria-selected="false" data-href="' + esc(root + e.u) + '"><div class="sd-opt">' + inner + "</div></li>";
        } else {
          html += '<li class="sd-item m-' + esc(e.m) + '"><a href="' + esc(root + e.u) + '">' + inner + "</a></li>";
        }
        n++;
      });
      html += "</ul></div>";
    });
    container.innerHTML = html;
    return n;
  }

  function initSearchDialog() {
    var triggers = $$("[data-search-trigger]");
    if (!triggers.length || typeof HTMLDialogElement !== "function" || $("[data-search-page]")) {
      if ($("[data-search-page]")) initShortcut(function () { var i = $("#sp-q"); if (i) { i.focus(); i.select(); } });
      return;
    }
    var isMac = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent);
    triggers.forEach(function (t) { var k = t.querySelector(".st-kbd"); if (k) { k.textContent = isMac ? "⌘K" : "Ctrl K"; k.hidden = false; } });

    var dlg = document.createElement("dialog");
    dlg.className = "sd";
    dlg.setAttribute("aria-label", "Search the reference models");
    dlg.innerHTML =
      '<div class="sd-inner"><div class="sd-head"><svg class="ico" aria-hidden="true" focusable="false"><use href="#i-search"></use></svg>' +
      '<label class="sr-only" for="sd-input">Search substeps, competencies, practices, tools and examples</label>' +
      '<input id="sd-input" class="sd-input" type="search" autocomplete="off" spellcheck="false" role="combobox" aria-expanded="false" aria-controls="sd-results" aria-autocomplete="list" placeholder="Search the models…">' +
      '<button type="button" class="sd-close">Close</button></div>' +
      '<p class="sr-only" id="sd-status" aria-live="polite"></p>' +
      '<div id="sd-results" class="sd-results" role="listbox" aria-label="Search results"></div>' +
      '<div class="sd-foot"><span>↑ ↓ to move · Enter to open · Esc to close</span><a href="' + esc(root + "search/") + '">Browse the full index</a></div></div>';
    document.body.appendChild(dlg);
    var input = $("#sd-input", dlg), results = $("#sd-results", dlg), status = $("#sd-status", dlg);
    var active = -1, count = 0, opener = null, timer = null;

    function setActive(i) {
      var opts = $$('[role="option"]', results);
      opts.forEach(function (o) { o.setAttribute("aria-selected", "false"); });
      active = i;
      if (i >= 0 && opts[i]) {
        opts[i].setAttribute("aria-selected", "true");
        input.setAttribute("aria-activedescendant", opts[i].id);
        opts[i].scrollIntoView({ block: "nearest" });
      } else {
        input.removeAttribute("aria-activedescendant");
      }
    }
    function run() {
      var q = input.value;
      if (!q.trim()) { results.innerHTML = ""; count = 0; status.textContent = ""; input.setAttribute("aria-expanded", "false"); setActive(-1); return; }
      loadIndex().then(function (items) {
        var r = search(items, q);
        count = renderResults(results, r, "sd", 6, true);
        if (!count) results.innerHTML = '<p class="sd-empty">No matches for “' + esc(q) + '”. Try a shorter word, or browse the full index.</p>';
        status.textContent = r.length ? (count < r.length ? "Showing " + count + " of " + r.length + " results" : r.length + " results") : "No results";
        input.setAttribute("aria-expanded", count ? "true" : "false");
        setActive(count ? 0 : -1);
      }).catch(function () {
        results.innerHTML = '<p class="sd-empty">Search could not load. Use the full index instead.</p>';
      });
    }
    function open(e) {
      if (e && (e.metaKey || e.ctrlKey || e.shiftKey || e.button === 1)) return;
      if (e) e.preventDefault();
      opener = document.activeElement;
      dlg.showModal();
      input.focus();
      input.select();
      loadIndex();
    }
    function close() { dlg.close(); }
    dlg.addEventListener("close", function () { if (opener && opener.focus) opener.focus(); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) close(); });
    $(".sd-close", dlg).addEventListener("click", close);
    input.addEventListener("input", function () { clearTimeout(timer); timer = setTimeout(run, 60); });
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") { e.preventDefault(); if (count) setActive((active + 1) % count); }
      else if (e.key === "ArrowUp") { e.preventDefault(); if (count) setActive((active - 1 + count) % count); }
      else if (e.key === "Enter") {
        var opt = $$('[role="option"]', results)[active];
        if (opt) { e.preventDefault(); window.location.href = opt.getAttribute("data-href"); }
      } else if (e.key === "Escape") { e.preventDefault(); close(); }
    });
    results.addEventListener("click", function (e) {
      var opt = e.target.closest('[role="option"]');
      if (opt) window.location.href = opt.getAttribute("data-href");
    });
    triggers.forEach(function (t) { t.addEventListener("click", open); });
    initShortcut(function () { if (!dlg.open) open(); });
  }

  function initShortcut(fn) {
    document.addEventListener("keydown", function (e) {
      if ((e.metaKey || e.ctrlKey) && !e.altKey && (e.key === "k" || e.key === "K")) { e.preventDefault(); fn(); }
    });
  }

  function initSearchPage() {
    var form = $("[data-search-page]");
    if (!form) return;
    form.hidden = false;
    var input = $("#sp-q", form), results = $("#sp-results", form), status = $(".search-status", form);
    function run(push) {
      var q = input.value;
      if (push) {
        var url = new URL(window.location.href);
        if (q.trim()) url.searchParams.set("q", q); else url.searchParams.delete("q");
        history.replaceState(null, "", url.toString());
      }
      if (!q.trim()) { results.innerHTML = ""; status.textContent = ""; return; }
      loadIndex().then(function (items) {
        var r = search(items, q);
        renderResults(results, r.slice(0, 80), "sp", 0, false);
        status.textContent = r.length ? r.length + (r.length === 1 ? " result" : " results") + (r.length > 80 ? ", showing the best 80" : "") : "No results. Try a shorter word, or use the index below.";
      });
    }
    var timer = null;
    input.addEventListener("input", function () { clearTimeout(timer); timer = setTimeout(function () { run(true); }, 120); });
    form.addEventListener("submit", function (e) { e.preventDefault(); run(true); });
    var q = new URLSearchParams(window.location.search).get("q");
    if (q) { input.value = q; run(false); }
  }

  /* ---- compare levels ------------------------------------------------------------ */
  function initCompare() {
    $$("[data-compare]").forEach(function (panel) {
      panel.hidden = false;
      var fallback = $("[data-compare-fallback]");
      var onLevelsPage = !!fallback;
      var ladder = $(".ladder");
      var levelNames = ["", "Awareness", "Familiarity", "Proficiency", "Mastery", "Expertise"];
      function value(name) { var c = panel.querySelector('input[name$="-' + name + '"]:checked'); return c ? parseInt(c.value, 10) : 0; }
      function set(name, v) { var r = panel.querySelector('input[name$="-' + name + '"][value="' + v + '"]'); if (r) r.checked = true; }
      function update(fromHash) {
        var f = value("from"), t = value("to");
        panel.setAttribute("data-from", f);
        panel.setAttribute("data-to", t);
        var lo = Math.min(f, t), hi = Math.max(f, t);
        $(".cmp-status", panel).textContent = f === t
          ? "Pick two different levels to see what changes."
          : "L" + f + " " + levelNames[f] + " → L" + t + " " + levelNames[t];
        $$(".cmp-gate", panel).forEach(function (g) {
          var l = parseInt(g.getAttribute("data-l"), 10);
          g.hidden = !(f !== t && l >= lo && l < hi);
        });
        if (ladder) {
          $$(".rung", ladder).forEach(function (r) {
            var l = parseInt(r.getAttribute("data-level"), 10);
            r.classList.toggle("is-dim", l !== f && l !== t);
          });
        }
        if (onLevelsPage && !fromHash) history.replaceState(null, "", "#from-" + f + "-to-" + t);
      }
      if (onLevelsPage) {
        fallback.hidden = true;
        var m = /^#from-([1-5])-to-([1-5])$/.exec(window.location.hash);
        if (m) { set("from", m[1]); set("to", m[2]); panel.scrollIntoView({ block: "start", behavior: reduceMotion ? "auto" : "smooth" }); }
      }
      panel.addEventListener("change", function () { update(false); });
      update(true);
      // Keep every level readable until someone actually picks a pair.
      if (ladder) $$(".rung", ladder).forEach(function (r) { r.classList.remove("is-dim"); });
    });
  }

  /* ---- level focus on sub-area pages --------------------------------------------- */
  function initLevelFocus() {
    var section = $("[data-level-focus]");
    if (!section) return;
    var control = $(".focus-control", section);
    control.hidden = false;
    var note = $("[data-focus-note]", section);
    if (note) note.hidden = true;
    function apply(l) {
      $$(".focus-level", section).forEach(function (el) { el.hidden = el.getAttribute("data-l") !== String(l); });
    }
    var fromUrl = new URLSearchParams(window.location.search).get("level");
    var initial = /^[1-5]$/.test(fromUrl || "") ? fromUrl : (/^[1-5]$/.test(store.get("cpdse-rm-level") || "") ? store.get("cpdse-rm-level") : "3");
    var radio = control.querySelector('input[value="' + initial + '"]');
    if (radio) radio.checked = true;
    apply(initial);
    control.addEventListener("change", function (e) {
      var l = e.target.value;
      apply(l);
      store.set("cpdse-rm-level", l);
      var url = new URL(window.location.href);
      url.searchParams.set("level", l);
      history.replaceState(null, "", url.toString());
    });
  }

  /* ---- step rail scroll-spy ------------------------------------------------------ */
  function initRail() {
    var rail = $("[data-step-rail]");
    if (!rail || !("IntersectionObserver" in window)) return;
    var links = $$("a", rail);
    var byId = {};
    links.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });
    var visible = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { visible[en.target.id] = en.isIntersecting ? en.boundingClientRect.top : null; });
      var best = null, bestTop = Infinity;
      Object.keys(visible).forEach(function (id) {
        var top = visible[id];
        if (top !== null && top < bestTop) { best = id; bestTop = top; }
      });
      if (!best) return;
      links.forEach(function (a) { a.removeAttribute("aria-current"); });
      if (byId[best]) byId[best].setAttribute("aria-current", "step");
    }, { rootMargin: "-20% 0px -55% 0px" });
    $$(".flow-section").forEach(function (s) { io.observe(s); });
  }

  /* ---- tools filter --------------------------------------------------------------- */
  function initToolFilter() {
    var form = $("[data-tool-filter]");
    if (!form) return;
    form.hidden = false;
    var q = $("#tf-q", form), type = $("#tf-type", form), count = $(".filter-count", form), empty = $("[data-tool-empty]");
    var rows = $$("table.tools tbody tr");
    function apply() {
      var term = norm(q.value), ty = type.value, shown = 0;
      rows.forEach(function (r) {
        var ok = (!term || norm(r.getAttribute("data-name")).indexOf(term) >= 0) && (!ty || r.getAttribute("data-type") === ty);
        r.hidden = !ok;
        if (ok) shown++;
      });
      count.textContent = shown === rows.length ? "Showing all " + rows.length : "Showing " + shown + " of " + rows.length;
      empty.hidden = shown !== 0;
    }
    form.addEventListener("input", apply);
    form.addEventListener("submit", function (e) { e.preventDefault(); });
    apply();
  }

  /* ---- position strips: keep the current cell in view on narrow screens ------------ */
  function initStrips() {
    $$("[data-strip]").forEach(function (strip) {
      var cur = strip.querySelector('[aria-current="page"], .is-on');
      if (!cur || strip.scrollWidth <= strip.clientWidth) return;
      strip.scrollLeft = Math.max(0, cur.offsetLeft - strip.clientWidth / 2 + cur.offsetWidth / 2);
    });
  }

  function start() {
    initStrips();
    initTheme();
    initSearchDialog();
    initSearchPage();
    initCompare();
    initLevelFocus();
    initRail();
    initToolFilter();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
