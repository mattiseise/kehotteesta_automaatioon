# Asiakasviestin käsittelyohje

Tällä ohjeella tekoäly käsittelee yhden asiakasviestin kolmessa vaiheessa: se luokittelee viestin, poimii siitä tiedot ja kirjoittaa vastausluonnoksen. Tuloste on joka kerta samanlainen JSON-muotoinen lomake, jossa on samat kentät samassa järjestyksessä.

Ohje on tämän tiedoston lopussa koodilohkossa. Koodilohko alkaa rivistä, jolla on kolme heittomerkin näköistä merkkiä ja sana text, ja päättyy riviin, jolla on pelkästään samat kolme merkkiä. Kopioi näiden kahden rivin välissä oleva teksti ja jätä itse rivit kopioimatta. Jos ohjelmasi näyttää koodilohkon harmaana laatikkona, kopioi laatikon sisältö.

Kopioi ohje kokonaan uuteen keskusteluun, liitä asiakkaan viesti ohjeen viimeisen rivin tilalle ja lähetä.

## Nämä kohdat voit muokata

Kopioitava ohje on kirjoitettu Virtaaman koulutuspyynnöille. Kaksi ensimmäistä kohtaa voit muuttaa jo silloin, kun käsittelet Virtaaman viestejä. Loput kohdat vaihdat omiin, kun teet ohjeesta version omalle viestityypillesi, esimerkiksi kurssin peruutuksille tai tiedusteluille.

- **Vastausluonnoksen sävy ja allekirjoitus.** Vaiheessa 3 kerrotaan, miten asiakkaalle kirjoitetaan ja kenen nimellä. Muuta nämä oman työpaikkasi tavan mukaisiksi. Omassa versiossasi allekirjoitukseen tulee oma nimesi ja yrityksesi.
- **Tavoite.** Kohdassa "TAVOITE" kerrotaan, mitä vastauksella halutaan saada aikaan. Kun otat ohjeen omaan käyttöösi, kirjoita tähän, mitä omalla vastauksellasi haluat saada aikaan.
- **Taustatiedot.** Kohdassa "TAUSTATIEDOT" kerrotaan, minkä yrityksen viestejä käsitellään. Kun otat ohjeen omaan käyttöösi, kirjoita tilalle oma organisaatiosi kahdella tai kolmella virkkeellä.
- **Luokat.** Vaiheessa 1 on neljä luokkaa. Voit vaihtaa niiden tilalle ne viestityypit, joita omassa työssäsi tulee, esimerkiksi tiedustelu, peruutus ja tarjouspyyntö. Kirjoita jokaiselle luokalle yksi virke siitä, milloin se valitaan.
- **Poimittavat tiedot.** Vaiheen 2 kentät "organisaatio", "osallistujia", "ajankohta" ja "toteutustapa" kuuluvat koulutuspyyntöön. Vaihda niiden tilalle ne tiedot, joita omassa viestityypissäsi tarvitaan, ja tee sama muutos ohjeen lopussa olevaan JSON-rakenteeseen. Pidä aina nämä viisi kenttää: "luokka", "asiakas", "asiakkaan_tarve", "puuttuvat_tiedot" ja "vastausluonnos".
- **Kolme tarkistettavaa tietoa.** Ohjeen mukaan tekoäly tarkistaa koulutuspyynnöstä aina osallistujamäärän, ajankohdan ja sen, pidetäänkö koulutus lähi- vai etäkoulutuksena. Päätä itse, mitkä kaksi tai kolme tietoa sinulla pitää aina olla, ennen kuin viestiin voi vastata, ja kirjoita ne ohjeeseen näiden kolmen tilalle. Kurssin peruutuksessa ne voivat olla esimerkiksi nämä: mikä kurssi on kyseessä, monesko kerta on menossa ja haluaako asiakas hyvityksen vai siirron.
- **Kielto mainita hintoja.** Vaiheessa 3 lukee "Älä mainitse hintoja", koska tässä ohjeessa ei ole Virtaaman hinnastoa. Jos liität omaan versioosi hinnastosi, voit poistaa kiellon ja pyytää tekoälyä kertomaan hinnan täsmälleen niin kuin se on hinnastossa. Jos hinnasto ei ole mukana, pidä kielto.

## Näitä älä muuta

Kun käsittelet Virtaaman viestejä, pidä nämä kaksi kohtaa ennallaan. Kouluttajan demossa ja iltapäivän agentissa viestistä poimitaan samat tiedot samoilla nimillä.

- **Kenttien nimet ja järjestys.** Jos muutat kentän nimeä kesken harjoituksen, et voi enää verrata tulostetta odotettuun tulokseen etkä eri viestien tulosteita keskenään. Omassa versiossasi saat vaihtaa kentät niin kuin edellä kerrotaan. Pidä sen jälkeen omatkin kenttäsi samoina kerrasta toiseen.
- **Sääntö puuttuvista tiedoista.** Ohje käskee tekoälyä kirjaamaan puuttuvan tiedon puuttuvaksi. Jos poistat säännön, tekoäly täyttää aukon helposti arvauksella. Pidä tämä sääntö myös omassa versiossasi, vaikka vaihdat tarkistettavat tiedot omiin.

## Kopioitava ohje

```text
Käsittele tämän ohjeen lopussa oleva asiakasviesti. Tee kolme vaihetta tässä järjestyksessä ja palauta tulos JSON-muodossa.

TAUSTATIEDOT
Virtaama Oy on tamperelainen koulutus- ja konsultointiyritys. Se auttaa pieniä ja keskisuuria organisaatioita sujuvoittamaan toimistotyötä kolmella alueella: tekoäly työssä, Excel ja raportointi sekä työn prosessit. Koulutukset pidetään tilauksesta lähi- tai etäkoulutuksina. Asiakasviesteihin vastaa asiakaskoordinaattori Riikka Lahtela.

TAVOITE
Tavoitteena on, että asiakas saa selkeän vastauksen ja että Virtaamalla on tarjouksen tekemiseen tarvittavat tiedot. Asiakaskoordinaattorin pitää pystyä lähettämään vastausluonnos pienin korjauksin.

TÄRKEIN SÄÄNTÖ
Käytä vain tietoja, jotka ovat asiakkaan viestissä tai tässä ohjeessa. Jos tieto puuttuu viestistä, kirjaa se puuttuvaksi äläkä arvaa.

1 Luokittele
Valitse viestille yksi luokka näistä neljästä.
- tarjouspyyntö: asiakas haluaa tilata koulutuksen tai muun palvelun, pyytää tarjousta tai kysyy hintaa koulutukselle, jota hän on tilaamassa.
- kysymys: asiakas kysyy yleistä tietoa eikä ole tilaamassa mitään.
- reklamaatio: asiakas on tyytymätön laskuun tai palveluun tai vaatii hyvitystä.
- muu: viesti ei sovi mihinkään edellisistä.
Jos viestissä on useita asioita, valitse luokka sen asian mukaan, jonka asiakas mainitsee ensimmäisenä.

2 Poimi tiedot
Poimi viestistä tiedot näihin kenttiin. Jos viestissä ei ole kentän tietoa, kentän arvo on null.
- asiakas: viestin lähettäjän nimi.
- organisaatio: lähettäjän yritys tai muu organisaatio.
- asiakkaan_tarve: mitä asiakas haluaa, yhdellä lyhyellä virkkeellä. Jos viestissä on useita asioita, mainitse ne kaikki.
- osallistujia: koulutukseen tulevien määrä lukuna. Luvuksi käy myös organisaation tai ryhmän koko, jos asiakas pyytää koulutusta koko joukolle. Jos määrä on likimääräinen, kirjoita pelkkä luku. Jos määrää ei kerrota, arvo on null.
- ajankohta: asiakkaan toivoma ajankohta samoin sanoin kuin viestissä. Jos ajankohtaa ei kerrota, arvo on null.
- toteutustapa: lähi, etä tai null. Arvo on lähi, jos asiakas pyytää lähikoulutusta tai kertoo paikan, jossa koulutus pidetään, esimerkiksi oman toimistonsa. Arvo on etä, jos asiakas pyytää etäkoulutusta. Muuten arvo on null.
- puuttuvat_tiedot: lista tiedoista, jotka pitää kysyä asiakkaalta.

Täytä kenttä puuttuvat_tiedot näin.
- Jos asiakas pyytää koulutusta tai tarjousta koulutuksesta, tarkista aina nämä kolme tietoa: osallistujamäärä, ajankohta ja lähi vai etä. Koulutuspyynnöstä ei tarkisteta muita tietoja.
- Osallistujamäärä puuttuu, jos kentän osallistujia arvo on null.
- Ajankohta puuttuu, jos sitä ei kerrota tai se kerrotaan epätarkemmin kuin viikon tarkkuudella. Viikon numero tai päivämäärä riittää, eikä vuotta tarvitse mainita. Pelkkä kuukausi, vuodenaika tai juhlapyhä ei riitä.
- Lähi vai etä puuttuu, jos kentän toteutustapa arvo on null.
- Kirjoita nämä kolme tietoa listaan aina näillä nimillä: "osallistujamäärä", "ajankohta", "lähi vai etä".
- Jos viestissä on reklamaatio tai jokin muu asia kuin koulutuspyyntö, lisää listaan myös ne tiedot, joita ilman asiaa ei voi selvittää.
- Jos mitään ei puutu, lista on tyhjä.

3 Kirjoita vastausluonnos
Kirjoita asiakkaalle vastaus kenttään vastausluonnos. Virtaaman asiakaskoordinaattori lukee ja korjaa luonnoksen ennen kuin se lähetetään.
- Sinuttele asiakasta. Sävy on ystävällinen ja asiallinen.
- Aloita tervehdyksellä ja kiitä yhteydenotosta.
- Jos kentässä puuttuvat_tiedot on tietoja, kysy ne kaikki asiakkaalta.
- Jos viesti on tarjouspyyntö eikä tietoja puutu, kertaa asiakkaan antamat tiedot lyhyesti ja kerro, että tarjous lähetetään hänelle.
- Älä mainitse hintoja. Jos asiakas kysyy hintaa tai sitä, mitä hintaan sisältyy, kerro, että ne ovat tarjouksessa.
- Älä lupaa päivämääriä, hyvityksiä tai alennuksia.
- Lopeta allekirjoitukseen: Riikka Lahtela, Virtaama Oy

TULOSTE
Palauta pelkkä JSON tässä rakenteessa. Kenttien nimet ja järjestys ovat aina nämä.

{
  "luokka": "yksi luokka vaiheesta 1",
  "asiakas": "lähettäjän nimi",
  "organisaatio": "lähettäjän organisaatio",
  "asiakkaan_tarve": "mitä asiakas haluaa",
  "osallistujia": null,
  "ajankohta": null,
  "toteutustapa": null,
  "puuttuvat_tiedot": [],
  "vastausluonnos": "vastauksen teksti"
}

Rakenteessa näkyvät arvot ovat malleja. Korvaa jokainen arvo tämän viestin tiedoilla vaiheiden 1, 2 ja 3 mukaan. Kirjoita tekstit lainausmerkkeihin. Kirjoita luku ja null ilman lainausmerkkejä.
Älä kirjoita JSONin eteen tai perään selityksiä, otsikoita tai muuta tekstiä. Vastauksesi ensimmäinen merkki on avaava aaltosulku ja viimeinen merkki sulkeva aaltosulku.

ASIAKKAAN VIESTI
LIITÄ ASIAKKAAN VIESTI TÄHÄN
```
