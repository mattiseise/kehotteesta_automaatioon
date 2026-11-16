# Kehotteesta automaatioon

Staattinen sivusto yhden päivän tekoälykoulutuksesta "Kehotteesta automaatioon" (2.12.2026 klo 9–15, kouluttajat Matti ja Kari). Tämä on **tilaajaversio**: se sisältää myös kouluttajan materiaalit. Osallistujille jaetaan vain osallistujan sivusto.

Sivusto toimii GitHub Pagesin alipolusta (`https://mattiseise.github.io/kehotteesta_automaatioon/`). Kaikki linkit ja resurssit ovat suhteellisia. Sivustossa ei ole palvelinpuolta.

## Rakenne

```
index.html                 tilaajan aloitussivu, neljä korttia
.nojekyll                  Jekyll pois päältä
assets/                    aloitussivun logo

osallistuja/               osallistujan sivusto (itsenäinen)
  index.html               yksi sivu, osat vaihtuvat URL-hashilla (#osa-1 ...)
  tiedostot/               liitteet sellaisinaan (md, txt, csv, pdf)
  assets/pages-shim.js     latausrajapinnan korvike (ks. alla)

diat/esittajat/            esittäjien diat (26 kpl), itsenäinen
diat/luennoija/            luennoijan diat (36 kpl, puhujan muistiinpanot), itsenäinen
  index.html               katselin
  slides/NN.html           yksittäiset diat
  assets/                  katselimen ja diojen skriptit, tyylit ja logo

kouluttaja/                kouluttajan ohjeet, käsikirjoitukset, lisäharjoitukset, aineisto (itsenäinen)
  index.html               hakemisto
  assets/                  navigaation tyyli ja logo

lahde/                     raakakopiot lähteistä (ks. alla)
tools/build.py             lähteistä sivustoksi
tools/mallit/              rakennuksen mallipohjat ja skriptit
```

Jokainen osio (`osallistuja/`, `diat/esittajat/`, `diat/luennoija/`, `kouluttaja/`) on itsenäinen: se ei viittaa toisten osioiden tiedostoihin, ja sen tarvitsemat jaetut resurssit (logo, skriptit) ovat sen omassa `assets/`-kansiossa.

## Diaesityksen katselin

- Nuolinäppäimet, välilyönti, Page Up ja Page Down siirtävät diasta toiseen. Home ja End hyppäävät alkuun ja loppuun.
- `G` avaa ruudukkoyleiskatsauksen, `N` näyttää puhujan muistiinpanot, `F` vaihtaa koko ruudun.
- Kosketuslaitteella dioja pyyhkäistään, ja alapalkissa on napit.
- Diaindeksi on URL-hashissa, esimerkiksi `diat/luennoija/#9` avaa 9. dian.
- Dia (1920 × 1080) skaalautuu ikkunaan kuvasuhde säilyttäen.
- Animoiduissa dioissa (esittäjien diat 8, 9 ja 11) animaatio toistuu, kun dia avautuu. Dialla on painike "Toista animaatio". Jos selain pyytää vähemmän liikettä (`prefers-reduced-motion`), loppu­tila näytetään heti.

## Miten sivusto on rakennettu

Lähteenä on kaksi claude.ai-artifaktia:

1. Osallistujan sivusto: `https://claude.ai/artifact/6Cqu5ec9eBoXui2dBBvh27` (`index.html` ja `tiedostot/`).
2. Yhteinen Design-kanvas: `https://claude.ai/artifact/Xve1QnkQuwnUgwUiAZubfk`, versio `1794817508-5012` (diat, luennoijan diat, kouluttajan sivut ja `canvas.json`).

Osallistujan sivusto otettiin sellaisenaan. Kaksi muutosta: `<meta name="robots" content="noindex">` ja `assets/pages-shim.js`. Alkuperäinen sivu tallentaa liitteet claude.ai:n omalla `window.claude.use('downloads')` -rajapinnalla, jota GitHub Pagesissa ei ole. Korvike tarjoaa saman rajapinnan tavallisella selaimen latauksella, joten lataa-painikkeet näkyvät ja toimivat.

Kanvaksen `.dc.html`-tiedostot muunnettiin staattisiksi sivuiksi (`tools/build.py`):

- `<x-dc>`, `<helmet>` ja komponenttiskripti poistettiin. Helmetin fontti- ja tyylilohkot siirrettiin `<head>`-osaan.
- Logo (`/_blob/...`) korvattiin tiedostolla `assets/logo-valkoinen.png`.
- Animaatiot (`{{ a.tN }}`-sidonnat ja diojen 8 ja 11 omat tilat) toteutetaan skriptillä `slide.js`. Se lisää luokan `on` määrätyillä ajoilla.
- Dioihin lisättiin `noindex`-meta ja skaalaus ikkunaan.
- Diojen järjestys ja otsikot tulevat `canvas.json`ista. Puhujan muistiinpanot ovat siellä kanvaksen muistilappuina: esittäjien dioilla `muistiinpano-NN` ja luennoijan dioilla `luento-puhe-NN`.
- Kouluttajan sivuille lisättiin yläreunan navigaatio ja hakemistosivu. Sivuja `sivu-alku` ja `sivu-osa-*` ei tuoda, koska ne ovat osallistujan sivun kopioita.

Tekstejä ei ole muokattu muuten kuin muuntamisen vaatimilta osin.

### Lähteet ja päivitys

`lahde/` sisältää raakakopiot: `canvas.json`, `diat/*.dc.html`, `luento/*.dc.html`, `kouluttaja/sivu-*.dc.html`, `osallistuja/` ja `assets/logo-valkoinen.png`. Kanvaksen ajoympäristön tiedostoja (`dc-runtime.js` ym.) ei ole mukana.

Lähteen alkuperäinen rakennus on tehty PC:llä. Kun kanvaksella tai osallistujan sivulla muokataan jotain:

1. Lataa muuttuneet tiedostot kanvaksesta ja artifaktista `lahde/`-kansioon samoille nimille.
2. Aja `python3 tools/build.py` (Python 3, vain standardikirjasto). Skripti kirjoittaa `index.html`, `assets/`, `diat/`, `kouluttaja/` ja `osallistuja/` uudelleen.
3. Tarkista sivusto paikallisesti (alla) ja tee commit.

## Paikallinen esikatselu alipolusta

```
mkdir /tmp/pages && ln -s "$PWD" /tmp/pages/kehotteesta_automaatioon
cd /tmp/pages && python3 -m http.server 8000
# http://localhost:8000/kehotteesta_automaatioon/
```

## Osallistujaosion lohkominen omaksi repokseen

`osallistuja/` toimii sellaisenaan omana sivustonaan: kopioi sen sisältö uuden repon juureen (`index.html`, `tiedostot/`, `assets/`), lisää `.nojekyll` ja ota Pages käyttöön. Mitään polkuja ei tarvitse muuttaa. Jos osallistuja-repoon ei haluta tilaajaversion hakukonekieltoa, poista `<meta name="robots">` tiedoston alusta.

## Sisältörajaukset

Sivusto ei sisällä osallistujien nimiä tai yrityksiä. Virtaama Oy ja sen henkilöt ovat keksittyä harjoitusaineistoa. Kaikilla sivuilla on `noindex`.

## Julkaisu

Repoa ei ole työnnetty GitHubiin eikä Pagesia ole otettu käyttöön. Repo on julkinen, joten julkaisu on Matin päätös. Sivusto on `noindex`, mutta osoite on silti kenen tahansa luettavissa.
