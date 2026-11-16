/* Osallistujan sivun "Etusivu"-linkki tilaajaversiossa. Poista tämä tiedosto ja sen script-viittaus index.html:stä,
   kun osallistujaosio lohkotaan omaksi repokseen. */
(function () {
  'use strict';
  function lisaa() {
    if (document.getElementById('pages-etusivu')) return;
    var st = document.createElement('style');
    st.textContent = '#pages-etusivu{position:fixed;left:12px;bottom:12px;z-index:2147483000;font:600 14px Montserrat,Arial,sans-serif;color:#fff;background:#33195A;padding:10px 16px;text-decoration:none;transition:background-color .2s cubic-bezier(.2,0,0,1)}#pages-etusivu:hover{background:#9D7DFF;color:#1A0530}#pages-etusivu:focus-visible{outline:3px solid #9D7DFF;outline-offset:2px}@media print{#pages-etusivu{display:none}}';
    document.head.appendChild(st);
    var a = document.createElement('a');
    a.id = 'pages-etusivu';
    a.href = '../index.html';
    a.textContent = 'Etusivu';
    document.body.appendChild(a);
  }
  if (document.body) lisaa(); else document.addEventListener('DOMContentLoaded', lisaa);
})();
