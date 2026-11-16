/* Yksittäisen dian apuskripti: skaalaus ikkunaan, animaatio ja näppäinten välitys katselimelle. */
(function () {
  'use strict';
  var W = 1920, H = 1080;
  var dia = document.querySelector('.dia');
  var upotettu = window.parent !== window;

  /* Skaalaus: dia (1920x1080) sovitetaan ikkunaan kuvasuhde säilyttäen */
  function skaalaa() {
    if (!dia) return;
    var s = Math.min(window.innerWidth / W, window.innerHeight / H);
    dia.style.position = 'absolute';
    dia.style.transformOrigin = '0 0';
    dia.style.left = ((window.innerWidth - W * s) / 2) + 'px';
    dia.style.top = ((window.innerHeight - H * s) / 2) + 'px';
    dia.style.transform = 'scale(' + s + ')';
  }
  window.addEventListener('resize', skaalaa);
  skaalaa();

  /* Animaatio: elementit, joilla on luokka at-<ms>, saavat luokan "on", kun aika on kulunut.
     Diakohtainen koukku (window.DIA_ANIM = {times, render(aika)}) hoitaa muut tilat. */
  var cfg = window.DIA_ANIM || {};
  var kohteet = [], ajat = {};
  [].forEach.call(document.querySelectorAll('[class]'), function (el) {
    [].forEach.call(el.classList, function (c) {
      var m = /^at-(\d+)$/.exec(c);
      if (m) { kohteet.push({ el: el, t: +m[1] }); ajat[+m[1]] = 1; }
    });
  });
  (cfg.times || []).forEach(function (t) { ajat[t] = 1; });
  var aikalista = Object.keys(ajat).map(Number).sort(function (a, b) { return a - b; });

  if (aikalista.length) {
    var nappi = document.querySelector('[data-anim-btn]');
    var ajastimet = [], soi = false;
    var vahenna = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    var aseta = function (aika) {
      kohteet.forEach(function (o) { o.el.classList.toggle('on', aika >= o.t); });
      if (cfg.render) cfg.render(aika);
    };
    var teksti = function () { if (nappi) nappi.textContent = soi ? 'Näytä kaikki heti' : 'Toista animaatio'; };
    var tyhjenna = function () { ajastimet.forEach(clearTimeout); ajastimet = []; };
    var valmis = function () { tyhjenna(); soi = false; aseta(1e9); teksti(); };
    var toista = function () {
      tyhjenna();
      if (vahenna) { valmis(); return; }
      soi = true; teksti(); aseta(-1);
      aikalista.forEach(function (t) { ajastimet.push(setTimeout(function () { aseta(t); }, t)); });
      ajastimet.push(setTimeout(function () { soi = false; teksti(); }, aikalista[aikalista.length - 1] + 1200));
    };
    if (nappi) nappi.addEventListener('click', function () { if (soi) valmis(); else toista(); });
    toista();
  }

  /* Katselimessa: näppäimet ja pyyhkäisyt välitetään ylös, jotta ne toimivat myös kun fokus on diassa */
  if (upotettu) {
    var VALITETTAVAT = { ArrowRight: 1, ArrowLeft: 1, ArrowUp: 1, ArrowDown: 1, PageDown: 1, PageUp: 1, Home: 1, End: 1, ' ': 1, Escape: 1, g: 1, G: 1, n: 1, N: 1, f: 1, F: 1 };
    document.addEventListener('keydown', function (e) {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      if (!VALITETTAVAT[e.key]) return;
      if (e.key === ' ' && e.target && e.target.tagName === 'BUTTON') return;
      e.preventDefault();
      window.parent.postMessage({ dia: 'key', key: e.key }, '*');
    });
    var x0 = null, y0 = null;
    document.addEventListener('touchstart', function (e) { var t = e.changedTouches[0]; x0 = t.clientX; y0 = t.clientY; }, { passive: true });
    document.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var t = e.changedTouches[0], dx = t.clientX - x0, dy = t.clientY - y0;
      x0 = null;
      if (Math.abs(dx) > 50 && Math.abs(dx) > 1.5 * Math.abs(dy)) window.parent.postMessage({ dia: 'swipe', dir: dx < 0 ? 'next' : 'prev' }, '*');
    }, { passive: true });
  }
})();
