/* Diaesityksen katselin: yksi dia kerrallaan, nuolinäppäimet, ruudukko, muistiinpanot, koko ruutu. */
(function () {
  'use strict';
  var DATA = JSON.parse(document.getElementById('dia-data').textContent);
  var S = DATA.slides, N = S.length;
  var kehys = document.getElementById('dia');
  var laskuri = document.getElementById('laskuri');
  var otsikko = document.getElementById('otsikko');
  var edellinen = document.getElementById('edellinen');
  var seuraava = document.getElementById('seuraava');
  var ruudukkoNappi = document.getElementById('ruudukko-nappi');
  var muistNappi = document.getElementById('muist-nappi');
  var kokoNappi = document.getElementById('koko-nappi');
  var muist = document.getElementById('muist');
  var muistAika = document.getElementById('muist-aika');
  var muistTeksti = document.getElementById('muist-teksti');
  var ruudukko = document.getElementById('ruudukko');
  var idx = 0, ruudukkoRakennettu = false, taaksepain = false, vaiheTeksti = '';
  /* Animoitu dia käyttää askeleen ensin itse (slide.js: diaAskel). Vasta kun sen vaiheet ovat
     lopussa, siirrytään seuraavaan diaan. Taaksepäin tultaessa dia näytetään valmiina. */
  var odottaa = null;
  function siirry(suunta) { taaksepain = suunta < 0; nayta(idx + suunta); }
  function askel(suunta) {
    var w = kehys.contentWindow, suora = false;
    try {
      if (w && typeof w.diaAskel === 'function') { suora = true; if (w.diaAskel(suunta)) return; }
    } catch (e) { suora = false; }
    if (suora || !w) { siirry(suunta); return; }
    /* Varatie, jos dian ikkunaan ei päästä suoraan: kysytään dialta viestillä. */
    if (odottaa) return;
    odottaa = { suunta: suunta, ajastin: setTimeout(function () { var s = odottaa.suunta; odottaa = null; siirry(s); }, 400) };
    w.postMessage({ dia: 'askel', suunta: suunta }, '*');
  }
  kehys.addEventListener('load', function () {
    if (!taaksepain) return;
    taaksepain = false;
    var w = kehys.contentWindow;
    try { if (w && typeof w.diaKaikki === 'function') { w.diaKaikki(); return; } } catch (e) {}
    if (w) w.postMessage({ dia: 'kaikki' }, '*');
  });
  function paivitaLaskuri() { laskuri.textContent = (idx + 1) + ' / ' + N + vaiheTeksti; }
  var muistiinpanoja = S.some(function (s) { return s.note; });
  if (!muistiinpanoja) muistNappi.hidden = true;

  function lue() {
    var n = parseInt(location.hash.replace(/^#/, ''), 10);
    return isNaN(n) ? 0 : Math.max(0, Math.min(N - 1, n - 1));
  }
  function nayta(i, paivitaHash) {
    idx = Math.max(0, Math.min(N - 1, i));
    var s = S[idx];
    kehys.src = s.src;
    kehys.title = s.title;
    vaiheTeksti = '';
    paivitaLaskuri();
    otsikko.textContent = s.title;
    edellinen.disabled = idx === 0;
    seuraava.disabled = idx === N - 1;
    document.title = (idx + 1) + '. ' + s.title + ' · ' + DATA.title;
    if (paivitaHash !== false) {
      var h = '#' + (idx + 1);
      if (location.hash !== h) history.replaceState(null, '', h);
    }
    paivitaMuist();
    if (ruudukkoRakennettu) [].forEach.call(ruudukko.querySelectorAll('.ruutu'), function (b, j) { b.classList.toggle('nyt', j === idx); });
  }
  function paivitaMuist() {
    var t = S[idx].note || '';
    var rivit = t.split('\n');
    var ensin = rivit[0] || '';
    var aikaRivi = /^\d{1,2}\.\d{2}/.test(ensin);
    muistAika.textContent = aikaRivi ? ensin : '';
    muistAika.hidden = !aikaRivi;
    muistTeksti.textContent = t ? (aikaRivi ? rivit.slice(1).join('\n').replace(/^\n+/, '') : t) : 'Tälle dialle ei ole puhujan muistiinpanoa.';
  }
  function muistiinpanot(auki) {
    if (!muistiinpanoja) return;
    var on = auki === undefined ? !muist.classList.contains('nakyy') : auki;
    muist.classList.toggle('nakyy', on);
    muistNappi.setAttribute('aria-pressed', on ? 'true' : 'false');
  }
  function ruudukkoNakyviin(auki) {
    var on = auki === undefined ? !ruudukko.classList.contains('nakyy') : auki;
    if (on && !ruudukkoRakennettu) rakennaRuudukko();
    ruudukko.classList.toggle('nakyy', on);
    ruudukkoNappi.setAttribute('aria-pressed', on ? 'true' : 'false');
    if (on) { var nyt = ruudukko.querySelector('.nyt'); if (nyt) { nyt.focus(); nyt.scrollIntoView({ block: 'center' }); } }
    else kehys.focus();
  }
  function rakennaRuudukko() {
    var rivi = ruudukko.querySelector('.rivi');
    S.forEach(function (s, i) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'ruutu' + (i === idx ? ' nyt' : '');
      var kuva = document.createElement('div'); kuva.className = 'kuva';
      var f = document.createElement('iframe'); f.src = s.src; f.loading = 'lazy'; f.tabIndex = -1; f.setAttribute('aria-hidden', 'true'); f.title = '';
      kuva.appendChild(f);
      var t = document.createElement('span'); t.innerHTML = '<b></b> '; t.querySelector('b').textContent = (i + 1) + '.'; t.appendChild(document.createTextNode(s.title));
      b.appendChild(kuva); b.appendChild(t);
      b.addEventListener('click', function () { nayta(i); ruudukkoNakyviin(false); });
      rivi.appendChild(b);
    });
    ruudukkoRakennettu = true;
  }
  function kokoRuutu() {
    var d = document, el = d.documentElement;
    try {
      if (d.fullscreenElement) d.exitFullscreen();
      else if (el.requestFullscreen) el.requestFullscreen();
    } catch (e) {}
  }
  function nappain(avain) {
    switch (avain) {
      case 'ArrowRight': case 'ArrowDown': case 'PageDown': case ' ': if (!ruudukko.classList.contains('nakyy')) askel(1); break;
      case 'ArrowLeft': case 'ArrowUp': case 'PageUp': if (!ruudukko.classList.contains('nakyy')) askel(-1); break;
      case 'Home': nayta(0); break;
      case 'End': nayta(N - 1); break;
      case 'g': case 'G': ruudukkoNakyviin(); break;
      case 'n': case 'N': muistiinpanot(); break;
      case 'f': case 'F': kokoRuutu(); break;
      case 'Escape': ruudukkoNakyviin(false); break;
      default: return false;
    }
    return true;
  }
  var KAYTETYT = { ArrowRight: 1, ArrowLeft: 1, ArrowUp: 1, ArrowDown: 1, PageDown: 1, PageUp: 1, Home: 1, End: 1, ' ': 1, Escape: 1, g: 1, G: 1, n: 1, N: 1, f: 1, F: 1 };
  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey || !KAYTETYT[e.key]) return;
    if (e.key === ' ' && e.target && e.target.tagName === 'BUTTON') return;
    e.preventDefault();
    nappain(e.key);
  });
  window.addEventListener('message', function (e) {
    if (e.source !== kehys.contentWindow || !e.data) return;
    if (e.data.dia === 'key') nappain(e.data.key);
    else if (e.data.dia === 'swipe') askel(e.data.dir === 'next' ? 1 : -1);
    else if (e.data.dia === 'askel-tulos' && odottaa) {
      clearTimeout(odottaa.ajastin);
      var s = odottaa.suunta; odottaa = null;
      if (!e.data.kaytetty) siirry(s);
    }
    else if (e.data.dia === 'vaihe') {
      vaiheTeksti = e.data.yht ? ' · vaihe ' + e.data.nyt + '/' + e.data.yht : '';
      paivitaLaskuri();
    }
  });
  var x0 = null, y0 = null;
  document.addEventListener('touchstart', function (e) { var t = e.changedTouches[0]; x0 = t.clientX; y0 = t.clientY; }, { passive: true });
  document.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var t = e.changedTouches[0], dx = t.clientX - x0, dy = t.clientY - y0; x0 = null;
    if (Math.abs(dx) > 50 && Math.abs(dx) > 1.5 * Math.abs(dy)) askel(dx < 0 ? 1 : -1);
  }, { passive: true });
  edellinen.addEventListener('click', function () { askel(-1); });
  seuraava.addEventListener('click', function () { askel(1); });
  ruudukkoNappi.addEventListener('click', function () { ruudukkoNakyviin(); });
  muistNappi.addEventListener('click', function () { muistiinpanot(); });
  kokoNappi.addEventListener('click', kokoRuutu);
  document.getElementById('ruudukko-sulje').addEventListener('click', function () { ruudukkoNakyviin(false); });
  window.addEventListener('hashchange', function () { var i = lue(); if (i !== idx) nayta(i, false); ruudukkoNakyviin(false); });
  nayta(lue(), false);
})();
