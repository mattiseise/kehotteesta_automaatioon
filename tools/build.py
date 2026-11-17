#!/usr/bin/env python3
"""Rakentaa sivuston lahde/-kansion raakakopioista (vain standardikirjasto).

Ajo repon juuresta:  python3 tools/build.py

Lähteet (kansio lahde/):
  canvas.json                      Design-kanvaksen järjestys, otsikot ja puhujan muistiinpanot
  diat/*.dc.html                   esittäjien diat (Main = dia 1, dia-02 ... dia-26)
  luento/*.dc.html                 luennoijan diat (luento-01 ... luento-36)
  kouluttaja/sivu-*.dc.html        kouluttajan sivut
  osallistuja/index.html + tiedostot/   osallistujan sivusto sellaisenaan
  video/<nimi>.html                sarjakuvaesitysmoottorin valmis video (standalone.html puheraitoineen)
  assets/logo-valkoinen.png        logo

Tulokset (kirjoitetaan yli): index.html, assets/, diat/, kouluttaja/, osallistuja/, video/
Ei koske kansioihin lahde/ ja tools/.
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAHDE = ROOT / 'lahde'
MALLIT = ROOT / 'tools' / 'mallit'
LOGO_BLOB = '/_blob/efed3696e0d96f7d44b8c687579618c8'
ROBOTS = '<meta name="robots" content="noindex">'


def lue(p):
    return Path(p).read_text(encoding='utf-8')


def kirjoita(p, teksti):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    # LF myös Windowsilla, jotta rakennus ei muuta jokaista tiedostoa gitissä.
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(teksti)


def tuo(lahde, kohde):
    kohde = Path(kohde)
    kohde.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(lahde, kohde)


def tyhjenna(p):
    p = Path(p)
    if p.exists():
        shutil.rmtree(p)


# ---------------------------------------------------------------- .dc.html -> staattinen

def pura_dc(src, nimi):
    """Palauttaa (otsikko, head-lisät, body). Kaataa rakennuksen, jos rakenne poikkeaa odotetusta."""
    t = re.search(r'<title>(.*?)</title>', src, re.S)
    h = re.search(r'<helmet>(.*?)</helmet>', src, re.S)
    b = re.search(r'</helmet>(.*?)</x-dc>', src, re.S)
    if not (t and h and b):
        sys.exit('Rakenne ei täsmää: ' + nimi)
    return t.group(1).strip(), h.group(1).strip(), b.group(1).strip()


def tarkista_jaannokset(teksti, nimi):
    for huono in ('{{', 'x-dc', 'support.js', '/_blob', '<helmet', 'DCLogic'):
        if huono in teksti:
            sys.exit('Jäännös "%s" tiedostossa %s' % (huono, nimi))


# Diakohtaiset animaatiokoukut (alkuperäisen komponentin renderVals-logiikka)
KOUKKU_AGENTTIDEMO = """window.DIA_ANIM = {
  render: function (aika) {
    var AA = [500, 1800, 3100, 4400, 5800, 8400], i = -1;
    AA.forEach(function (t, j) { if (aika >= t) i = j; });
    var mk = document.querySelector('.mk2');
    if (!mk) return;
    mk.style.left = i < 0 ? '114px' : (i * 282 + 114) + 'px';
    mk.style.opacity = i < 0 ? '0' : '1';
  }
};"""

KOUKKU_H3 = """window.DIA_ANIM = {
  times: [300, 4200],
  render: function (aika) {
    var M = [269, 284, 343, 243, 317, 213], KU = [237, 243, 256, 356, 250, 221];
    var pl = document.querySelectorAll('.pl'), kk = document.querySelectorAll('.kk'), lp = document.querySelectorAll('.lappu');
    var kasva = aika >= 300, kor = aika >= 4200;
    for (var i = 0; i < 6; i++) {
      var p = (i === 3 || i === 5) && kor;
      pl[2 * i].style.height = (kasva ? M[i] : 0) + 'px';
      pl[2 * i + 1].style.height = (kasva ? KU[i] : 0) + 'px';
      pl[2 * i + 1].style.background = p ? '#BBA53D' : '#FFFFFF';
      kk[i].style.color = p ? '#BBA53D' : '#CFC9DC';
    }
    for (var j = 0; j < lp.length; j++) lp[j].style.opacity = kor ? '1' : '0';
  }
};"""


def muunna_animaatio(body, nimi):
    """{{ a.tN }} -> at-N on (loppu­tila näkyy oletuksena, slide.js toistaa animaation)."""
    body = re.sub(r'\{\{\s*a\.t(\d+)\s*\}\}', r'at-\1 on', body)
    body = re.sub(
        r'<button type="button" class="toista" onClick="\{\{ animToiminto \}\}">\{\{ animNappi \}\}</button>',
        '<button type="button" class="toista" data-anim-btn>Toista animaatio</button>', body)
    koukku = ''
    if nimi.startswith('dia-08'):
        body = body.replace('left: {{ mk.left }}; opacity: {{ mk.op }}', 'left: 1524px; opacity: 1')
        koukku = KOUKKU_AGENTTIDEMO
    elif nimi.startswith('dia-11'):
        M = [269, 284, 343, 243, 317, 213]
        KU = [237, 243, 256, 356, 250, 221]
        for i in range(6):
            p = i in (3, 5)
            body = body.replace('{{ hp.m%d }}' % i, '%dpx' % M[i])
            body = body.replace('{{ hp.k%d }}' % i, '%dpx' % KU[i])
            body = body.replace('{{ vari.k%d }}' % i, '#BBA53D' if p else '#FFFFFF')
            body = body.replace('{{ vari.l%d }}' % i, '#BBA53D' if p else '#CFC9DC')
        body = body.replace('{{ lappu }}', '1')
        koukku = KOUKKU_H3
    return body, koukku


def dia_sivu(src, nimi, logo_polku):
    otsikko, helmet, body = pura_dc(src, nimi)
    body = body.replace(LOGO_BLOB, logo_polku)
    body, koukku = muunna_animaatio(body, nimi)
    sivu = (
        '<!doctype html>\n<html lang="fi">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n' + ROBOTS + '\n'
        '<title>' + otsikko + '</title>\n' + helmet + '\n'
        '<style>html,body{height:100%;margin:0;overflow:hidden;background:#1A0530}</style>\n'
        '</head>\n<body>\n' + body + '\n'
        + ('<script>\n' + koukku + '\n</script>\n' if koukku else '')
        + '<script src="../assets/slide.js"></script>\n</body>\n</html>\n')
    tarkista_jaannokset(sivu, nimi)
    return sivu, otsikko


# ---------------------------------------------------------------- diaesitykset

def jarjestys(canvas, sivu_id, tunnistin):
    return [k for k in canvas['order'] if canvas['boards'][k]['page'] == sivu_id and tunnistin(k)]


def muistiinpano(canvas, avain, taulu):
    n = canvas['notes'].get(avain)
    if not n:
        return ''
    # varmistus: muistiinpano on taulun alla samassa sarakkeessa
    if n['x'] != taulu['x'] or not (0 < n['y'] - taulu['y'] <= 1300):
        print('VAROITUS: muistiinpano %s ei osu tauluun' % avain)
    t = n['text']
    return re.sub(r'^Puhujan muistiinpano:\s*', '', t)


def rakenna_diat(canvas, sivu_id, lahdekansio, tunnistin, nimiavain, kohde, otsikko, tekija_kuvaus):
    tyhjenna(kohde)
    avaimet = jarjestys(canvas, sivu_id, tunnistin)
    dias = []
    for n, k in enumerate(avaimet, 1):
        src = lue(LAHDE / lahdekansio / k)
        sivu, _ = dia_sivu(src, k, '../assets/logo-valkoinen.png')
        kirjoita(kohde / 'slides' / ('%02d.html' % n), sivu)
        taulu = canvas['boards'][k]
        nimi = re.sub(r'^\d+\.\s*', '', taulu['title'])
        dias.append({'src': 'slides/%02d.html' % n, 'title': nimi, 'note': muistiinpano(canvas, nimiavain % n, taulu)})
    # katselin
    for f in ('slide.js', 'viewer.js', 'viewer.css'):
        tuo(MALLIT / f, kohde / 'assets' / f)
    tuo(LAHDE / 'assets' / 'logo-valkoinen.png', kohde / 'assets' / 'logo-valkoinen.png')
    data = json.dumps({'title': otsikko, 'slides': dias}, ensure_ascii=False).replace('</', '<\\/')
    kirjoita(kohde / 'index.html', katselin(otsikko, tekija_kuvaus, data))
    return len(dias), sum(1 for d in dias if d['note'])


def katselin(otsikko, kuvaus, data):
    return """<!doctype html>
<html lang="fi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
{robots}
<title>{otsikko}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&amp;display=swap">
<link rel="stylesheet" href="assets/viewer.css">
</head>
<body>
<main class="esitys" aria-label="{otsikko}">
<div class="lava"><iframe id="dia" title="Dia" tabindex="0" allow="fullscreen"></iframe></div>
<div class="palkki" role="toolbar" aria-label="Diaesityksen ohjaus">
<a class="etusivu" href="../../index.html">Etusivu</a>
<button type="button" id="edellinen" aria-label="Edellinen dia">Edellinen</button>
<span class="laskuri" id="laskuri" aria-live="polite"></span>
<button type="button" id="seuraava" aria-label="Seuraava dia">Seuraava</button>
<span class="otsikko" id="otsikko"></span>
<span class="ohje">Nuolet, välilyönti, Home, End</span>
<button type="button" id="ruudukko-nappi" aria-pressed="false" title="Ruudukko (G)">Ruudukko</button>
<button type="button" id="muist-nappi" aria-pressed="false" title="Puhujan muistiinpanot (N)">Muistiinpanot</button>
<button type="button" id="koko-nappi" title="Koko ruutu (F)">Koko ruutu</button>
</div>
<section class="muist" id="muist" aria-label="Puhujan muistiinpano">
<h2>Puhujan muistiinpano</h2>
<p class="aika" id="muist-aika"></p>
<p id="muist-teksti"></p>
</section>
</main>
<div class="ruudukko" id="ruudukko" role="dialog" aria-label="Diojen ruudukko">
<h2>{kuvaus} <button type="button" id="ruudukko-sulje">Sulje</button></h2>
<div class="rivi"></div>
</div>
<script type="application/json" id="dia-data">{data}</script>
<script src="assets/viewer.js"></script>
</body>
</html>
""".format(robots=ROBOTS, otsikko=html.escape(otsikko), kuvaus=html.escape(kuvaus), data=data)


# ---------------------------------------------------------------- kouluttaja

KOULUTTAJA_SIVUT = [
    # lähdetiedosto, tulostiedosto, nimi, kuvaus
    ('sivu-kouluttaja.dc.html', 'ohjeet.html', 'Kouluttajan ohjeet',
     'Tarkistuslista, päivän aikataulu ja osakohtaiset ohjeet kouluttajille.'),
    ('sivu-kasikirjoitus-1.dc.html', 'kasikirjoitus-1.html', 'Diojen käsikirjoitukset (1/3)',
     'Dioilla näytettävä ja sanottava sisältö, ensimmäinen osa.'),
    ('sivu-kasikirjoitus-2.dc.html', 'kasikirjoitus-2.html', 'Diojen käsikirjoitukset (2/3)',
     'Diojen käsikirjoitukset, toinen osa.'),
    ('sivu-kasikirjoitus-3.dc.html', 'kasikirjoitus-3.html', 'Diojen käsikirjoitukset (3/3)',
     'Diojen käsikirjoitukset, kolmas osa.'),
    ('sivu-lisaharjoitukset.dc.html', 'lisaharjoitukset.html', 'Lisäharjoitukset',
     'Harjoitukset, joita osallistuja voi tehdä päivän jälkeen.'),
    ('sivu-aineisto.dc.html', 'aineisto.html', 'Pohjat ja aineisto',
     'Päivän pohjat ja Virtaama Oy:n harjoitusaineisto.'),
]


def kouluttaja_nav(aktiivinen):
    rivit = ['<nav class="ko-nav" aria-label="Kouluttajan materiaali"><span class="ko-tunniste">Kouluttajan materiaali</span>',
             '<a href="index.html"%s>Hakemisto</a>' % (' aria-current="page"' if aktiivinen == 'index.html' else '')]
    for _, ulos, nimi, _k in KOULUTTAJA_SIVUT:
        rivit.append('<a href="%s"%s>%s</a>' % (ulos, ' aria-current="page"' if ulos == aktiivinen else '', html.escape(nimi)))
    rivit.append('</nav>')
    return ''.join(rivit)


def rakenna_kouluttaja():
    kohde = ROOT / 'kouluttaja'
    tyhjenna(kohde)
    for lahde_nimi, ulos, nimi, _k in KOULUTTAJA_SIVUT:
        src = lue(LAHDE / 'kouluttaja' / lahde_nimi)
        otsikko, helmet, body = pura_dc(src, lahde_nimi)
        body = body.replace(LOGO_BLOB, 'assets/logo-valkoinen.png')
        body, ruutuja = re.subn(r'<li>\[( |x)\] (.*?)</li>',
                                lambda m: '<li class="tarkistus"><label><input type="checkbox" class="tarkistus-ruutu"%s><span>%s</span></label></li>'
                                % (' checked' if m.group(1) == 'x' else '', m.group(2)), body, flags=re.S)
        body, rivi_ruutuja = re.subn(r'(?m)^- \[( |x)\] (.*)$',
                                     lambda m: '<label class="tarkistus-rivi"><input type="checkbox" class="tarkistus-ruutu"%s><span>%s</span></label>'
                                     % (' checked' if m.group(1) == 'x' else '', m.group(2)), body)
        ruutuja += rivi_ruutuja
        if ulos == 'lisaharjoitukset.html':
            def vaiheet(m):
                return re.sub(r'<li>(.*?)</li>',
                              lambda l: '<li class="tarkistus-vaihe"><label><input type="checkbox" class="tarkistus-ruutu"><span>%s</span></label></li>' % l.group(1),
                              m.group(0), flags=re.S)
            body, vaihe_n = re.subn(r'<ol>.*?</ol>', vaiheet, body, flags=re.S)
            ruutuja += body.count('tarkistus-vaihe')
        if ruutuja:
            body += '\n<script src="assets/tarkistus.js"></script>'
        sivu = ('<!doctype html>\n<html lang="fi">\n<head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width,initial-scale=1">\n' + ROBOTS + '\n'
                '<title>' + otsikko + '</title>\n' + helmet + '\n'
                '<link rel="stylesheet" href="assets/nav.css">\n</head>\n<body>\n'
                + kouluttaja_nav(ulos) + '\n' + body + '\n</body>\n</html>\n')
        tarkista_jaannokset(sivu, lahde_nimi)
        kirjoita(kohde / ulos, sivu)
    kortit = ''.join(
        '<a class="kortti" href="%s"><h2>%s</h2><p>%s</p></a>' % (ulos, html.escape(nimi), html.escape(k))
        for _, ulos, nimi, k in KOULUTTAJA_SIVUT)
    kirjoita(kohde / 'index.html', """<!doctype html>
<html lang="fi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
{robots}
<title>Kouluttajan materiaali</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&amp;display=swap">
<link rel="stylesheet" href="assets/nav.css">
<style>
body{{margin:0;background:#1A0530;color:#FFFFFF;font-family:'Montserrat',Arial,sans-serif;font-size:17px;line-height:1.6}}
main{{max-width:900px;margin:0 auto;padding:32px 20px 64px;display:flex;flex-direction:column;gap:28px}}
img{{width:171px;height:52px;display:block}}
h1{{margin:0;font-size:clamp(34px,6vw,56px);line-height:1.1}}
p{{margin:0}}
.pieni{{font-size:14px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#9D7DFF}}
.kortit{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,380px),1fr));gap:14px}}
.kortti{{display:flex;flex-direction:column;gap:8px;padding:22px;background:#33195A;color:#FFFFFF;text-decoration:none;transition:background-color .2s cubic-bezier(.2,0,0,1),color .2s cubic-bezier(.2,0,0,1)}}
.kortti:nth-child(2n){{background:#24103F}}
.kortti h2{{margin:0;font-size:22px;line-height:1.25}}
.kortti p{{font-size:15.5px;color:#CFC9DC}}
.kortti:hover,.kortti:focus-visible{{background:#9D7DFF;color:#1A0530}}
.kortti:hover p,.kortti:focus-visible p{{color:#1A0530}}
.kortti:focus-visible{{outline:3px solid #FFFFFF;outline-offset:3px}}
</style>
</head>
<body>
{nav}
<main>
<img src="assets/logo-valkoinen.png" alt="Business College Pro" width="171" height="52">
<div><p class="pieni">Kouluttajille</p><h1>Kouluttajan materiaali</h1></div>
<p>Kouluttajan omat sivut: ohjeet, käsikirjoitukset, lisäharjoitukset sekä pohjat ja aineisto. Osallistujalle jaetaan vain osallistujan sivusto.</p>
<div class="kortit">{kortit}</div>
</main>
</body>
</html>
""".format(robots=ROBOTS, nav=kouluttaja_nav('index.html'), kortit=kortit))
    tuo(MALLIT / 'nav.css', kohde / 'assets' / 'nav.css')
    tuo(MALLIT / 'tarkistus.js', kohde / 'assets' / 'tarkistus.js')
    tuo(LAHDE / 'assets' / 'logo-valkoinen.png', kohde / 'assets' / 'logo-valkoinen.png')
    return len(KOULUTTAJA_SIVUT) + 1


# ---------------------------------------------------------------- osallistuja

def rakenna_osallistuja():
    kohde = ROOT / 'osallistuja'
    tyhjenna(kohde)
    src = lue(LAHDE / 'osallistuja' / 'index.html')
    # Ainoat muutokset: robots-meta ja Pages-korvike lataus-rajapinnalle (ks. assets/pages-shim.js).
    lisays = ROBOTS + '<script src="assets/pages-shim.js"></script><script src="assets/etusivu-linkki.js" defer></script>'
    if '<head>' not in src:
        sys.exit('osallistuja/index.html: <head> puuttuu')
    src = src.replace('<head>', '<head>' + lisays, 1)
    # Brändin tumma ilme: ylikirjoitus viimeisen tyylilohkon perään ja valkoinen logo tummaa pohjaa vasten.
    brandi = '<style id="brandi">\n' + lue(MALLIT / 'osallistuja-brandi.css') + '</style>'
    paa = src.rfind('</style>')
    if paa < 0:
        sys.exit('osallistuja/index.html: </style> puuttuu')
    src = src[:paa + len('</style>')] + brandi + src[paa + len('</style>'):]
    src, n = re.subn(r'<img class="logo" src="data:image/png;base64,[^"]*"', '<img class="logo" src="assets/logo-valkoinen.png"', src)
    if n != 1:
        sys.exit('osallistuja/index.html: logoa ei löytynyt')
    for huono in ('/_blob', 'support.js', 'x-dc'):
        if huono in src:
            sys.exit('osallistuja/index.html: jäännös ' + huono)
    kirjoita(kohde / 'index.html', src)
    shutil.copytree(LAHDE / 'osallistuja' / 'tiedostot', kohde / 'tiedostot')
    tuo(MALLIT / 'pages-shim.js', kohde / 'assets' / 'pages-shim.js')
    tuo(MALLIT / 'etusivu-linkki.js', kohde / 'assets' / 'etusivu-linkki.js')
    tuo(LAHDE / 'assets' / 'logo-valkoinen.png', kohde / 'assets' / 'logo-valkoinen.png')
    return len(list((kohde / 'tiedostot').iterdir()))


# ---------------------------------------------------------------- video

def rakenna_video():
    """lahde/video/<nimi>.html -> video/<nimi>/index.html. Muutokset: robots-meta ja BC Pron ilme (tools/mallit/video-brandi.css)."""
    kohde = ROOT / 'video'
    tyhjenna(kohde)
    n = 0
    for src in sorted((LAHDE / 'video').glob('*.html')):
        t = lue(src)
        if '<head>' not in t:
            sys.exit('%s: <head> puuttuu' % src.name)
        if '</head>' not in t:
            sys.exit('%s: </head> puuttuu' % src.name)
        brandi = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&amp;display=swap">'
                  '<style id="brandi">\n' + lue(MALLIT / 'video-brandi.css') + '</style>')
        t = t.replace('</head>', brandi + '</head>', 1)
        # Paluulinkki sivuston etusivulle videon yläpuolelle (React-juuren ulkopuolelle).
        if t.count('<div id="agp-root">') != 1:
            sys.exit('%s: agp-root puuttuu' % src.name)
        t = t.replace('<div id="agp-root">', '<nav class="bc-paluu" aria-label="Sivusto"><a href="../../index.html">Etusivu</a></nav><div id="agp-root">', 1)
        # BC Pron ohje: ei emojeja painikkeissa.
        for emoji in ('\U0001F507 \u00c4\u00e4ni pois', '\U0001F50A \u00c4\u00e4ni p\u00e4\u00e4ll\u00e4'):
            t = t.replace(emoji, emoji[2:])
        kirjoita(kohde / src.stem / 'index.html', t.replace('<head>', '<head>' + ROBOTS, 1))
        n += 1
    return n


# ---------------------------------------------------------------- etusivu

def rakenna_etusivu():
    tuo(MALLIT / 'etusivu.html', ROOT / 'index.html')
    tuo(LAHDE / 'assets' / 'logo-valkoinen.png', ROOT / 'assets' / 'logo-valkoinen.png')
    (ROOT / '.nojekyll').write_text('', encoding='utf-8')


def main():
    canvas = json.loads(lue(LAHDE / 'canvas.json'))
    tyhjenna(ROOT / 'diat')
    n1, m1 = rakenna_diat(
        canvas, 'diat', 'diat', lambda k: k.startswith('dia-') or k == 'Main.dc.html', 'muistiinpano-%02d',
        ROOT / 'diat' / 'esittajat', 'Esittäjien diat · Kehotteesta automaatioon', 'Esittäjien diat')
    n2, m2 = rakenna_diat(
        canvas, 'luentodiat', 'luento', lambda k: k.startswith('luento-'), 'luento-puhe-%02d',
        ROOT / 'diat' / 'luennoija', 'Luennoijan diat · Kehotteesta automaatioon', 'Luennoijan diat')
    k = rakenna_kouluttaja()
    o = rakenna_osallistuja()
    v = rakenna_video()
    rakenna_etusivu()
    print('Esittäjien diat: %d (muistiinpano %d)' % (n1, m1))
    print('Luennoijan diat: %d (muistiinpano %d)' % (n2, m2))
    print('Kouluttajan sivut: %d' % k)
    print('Osallistujan liitteet: %d' % o)
    print('Videot: %d' % v)


if __name__ == '__main__':
    main()
