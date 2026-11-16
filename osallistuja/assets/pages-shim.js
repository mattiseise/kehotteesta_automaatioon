/* GitHub Pages -yhteensopivuus: alkuperäinen sivu tallentaa liitteet window.claude.use('downloads') -rajapinnan kautta.
   Tämä korvike tarjoaa saman rajapinnan tavallisella selaimen latauksella. */
(function () {
  'use strict';
  if (window.claude && typeof window.claude.use === 'function') return;
  var lataukset = {
    save: function (o) {
      return new Promise(function (ok, ei) {
        try {
          var blob = o.data instanceof Blob ? o.data : new Blob([o.data]);
          var url = URL.createObjectURL(blob);
          var a = document.createElement('a');
          a.href = url; a.download = o.filename;
          document.body.appendChild(a); a.click(); document.body.removeChild(a);
          setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
          ok();
        } catch (e) { ei({ code: 'unavailable' }); }
      });
    }
  };
  window.claude = {
    use: function (nimi) { return nimi === 'downloads' ? Promise.resolve(lataukset) : Promise.reject({ code: 'unavailable' }); }
  };
})();
