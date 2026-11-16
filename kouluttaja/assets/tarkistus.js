/* Kouluttajan tarkistuslistojen valintaruudut: tila säilyy selaimessa (localStorage), jos se on käytettävissä. */
(function () {
  'use strict';
  var avain = 'tarkistus:' + location.pathname;
  var tila = {};
  try { tila = JSON.parse(localStorage.getItem(avain) || '{}') || {}; } catch (e) { tila = {}; }
  var ruudut = document.querySelectorAll('input.tarkistus-ruutu');
  Array.prototype.forEach.call(ruudut, function (r, i) {
    if (tila[i]) r.checked = true;
    r.addEventListener('change', function () {
      tila[i] = r.checked ? 1 : 0;
      try { localStorage.setItem(avain, JSON.stringify(tila)); } catch (e) { /* ei tallennusta */ }
    });
  });
})();
