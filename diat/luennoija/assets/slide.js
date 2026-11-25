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

  /* Animaatio etenee esittäjän tahdissa. Elementit, joilla on luokka at-<ms>, saavat luokan "on",
     kun animaation aika on kulunut. Aika etenee vaiheittain: jokainen nuoli oikealle, välilyönti tai
     Seuraava-painallus toistaa seuraavan vaiheen. Vaiheen rajat ovat koukun listassa pysahdykset
     (oletus: jokainen aika on oma vaiheensa). Kun vaiheet ovat lopussa, katselin siirtyy seuraavaan diaan.
     Diakohtainen koukku (window.DIA_ANIM = {times, pysahdykset, render(aika)}) hoitaa muut tilat. */
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
  var vaiheet = (cfg.pysahdykset || aikalista).slice().sort(function (a, b) { return a - b; });
  var vaihe = 0, ajastimet = [];
  var nappi = document.querySelector('[data-anim-btn]');
  var vahenna = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function aseta(aika) {
    kohteet.forEach(function (o) { o.el.classList.toggle('on', aika >= o.t); });
    if (cfg.render) cfg.render(aika);
  }
  function tyhjenna() { ajastimet.forEach(clearTimeout); ajastimet = []; }
  function raja(i) { return i <= 0 ? -1 : vaiheet[i - 1]; }
  function ilmoita() {
    if (nappi) nappi.textContent = vaihe >= vaiheet.length ? 'Aloita alusta' : 'Näytä kaikki';
    if (upotettu) window.parent.postMessage({ dia: 'vaihe', nyt: vaihe, yht: vaiheet.length }, '*');
  }
  function mene(i, toista) {
    tyhjenna();
    var vanha = raja(vaihe);
    vaihe = Math.max(0, Math.min(vaiheet.length, i));
    var uusi = raja(vaihe);
    if (!toista || vahenna || uusi <= vanha) { aseta(uusi); ilmoita(); return; }
    var valilla = aikalista.filter(function (t) { return t > vanha && t <= uusi; });
    var ensin = valilla.length ? valilla[0] : uusi;
    valilla.forEach(function (t) {
      ajastimet.push(setTimeout(function () { aseta(t); }, t - ensin + 150));
    });
    ilmoita();
  }
  /* Katselin kutsuu: palauttaa true, jos dia käytti askeleen itse. */
  window.diaAskel = function (suunta) {
    if (!vaiheet.length) return false;
    if (suunta > 0 && vaihe < vaiheet.length) { mene(vaihe + 1, true); return true; }
    if (suunta < 0 && vaihe > 0) { mene(vaihe - 1, false); return true; }
    return false;
  };
  window.diaKaikki = function () { if (vaiheet.length) mene(vaiheet.length, false); };
  if (upotettu) {
    window.addEventListener('message', function (e) {
      if (e.source !== window.parent || !e.data) return;
      if (e.data.dia === 'askel') window.parent.postMessage({ dia: 'askel-tulos', kaytetty: window.diaAskel(e.data.suunta) }, '*');
      else if (e.data.dia === 'kaikki') window.diaKaikki();
    });
  }

  if (vaiheet.length) {
    if (nappi) nappi.addEventListener('click', function () { mene(vaihe >= vaiheet.length ? 0 : vaiheet.length, false); });
    var pienoiskuva = false;
    try { pienoiskuva = !!(window.frameElement && window.frameElement.getAttribute('aria-hidden') === 'true'); } catch (e) {}
    if (pienoiskuva) mene(vaiheet.length, false); else mene(0, false);
    if (!upotettu) {
      document.addEventListener('keydown', function (e) {
        if (e.ctrlKey || e.metaKey || e.altKey) return;
        if (e.key === ' ' && e.target && e.target.tagName === 'BUTTON') return;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === 'PageDown' || e.key === ' ') { if (window.diaAskel(1)) e.preventDefault(); }
        else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp' || e.key === 'PageUp') { if (window.diaAskel(-1)) e.preventDefault(); }
      });
    }
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
