# Tarkistajan ohje: tarkista yhteenveto lähteistä

Tällä ohjeella tekoäly tarkistaa tekijän ohjeella tehdyn yhteenvedon raporttia ja kokousmuistiinpanoja vasten. Tarkistaja on eri rooli kuin tekijä: se etsii jokaiselle väitteelle lähteen ja listaa kohdat, joissa lähteet sanovat eri asian, mutta se ei korjaa yhteenvetoa eikä hyväksy sitä.

Ohje on tämän tiedoston lopussa koodilohkossa. Koodilohko alkaa rivistä, jolla on kolme heittomerkin näköistä merkkiä ja sana text, ja päättyy riviin, jolla on pelkästään samat kolme merkkiä. Kopioi näiden kahden rivin välissä oleva teksti ja jätä itse rivit kopioimatta. Jos ohjelmasi näyttää koodilohkon harmaana laatikkona, kopioi laatikon sisältö.

Avaa samassa projektissa uusi keskustelu, kopioi ohje siihen ja liitä tekijän tuotos ohjeen viimeisen rivin tilalle.

## Nämä kohdat voit muokata

- **Lähteiden nimet.** Ohjeessa lähteet ovat raportti ja kokousmuistiinpanot. Kun tarkistat omaa aineistoasi, vaihda tilalle omien tiedostojesi nimet ja tapa, jolla niiden kohtiin viitataan.
- **Mitä tarkistetaan erityisen huolella.** Ohje käskee vertaamaan euromääriä, päivämääriä ja henkilöiden vastuita. Lisää tähän ne asiat, joissa virhe olisi omassa työssäsi kallein.

## Näitä älä muuta

- **Tarkistajan rooli.** Ohjeen toinen kappale kieltää tekoälyä korjaamasta ja hyväksymästä yhteenvetoa. Jos poistat sen, tekoäly kirjoittaa helposti yhteenvedon uudelleen, etkä näe enää, mikä alkuperäisessä oli vialla.
- **Kirjatun muutoksen ja ristiriidan ero.** Kaikki erot eivät ole virheitä. Jos päätöstä on muutettu ja muutos on kirjattu, kyse on muutoksesta. Ohje pyytää tekoälyä erottamaan kirjatun muutoksen ristiriidasta.

## Kopioitava ohje

```text
Olet tarkistaja. Tarkistat yhteenvedon, jonka joku muu on tehnyt sinulle annetusta aineistosta. Aineistona ovat raportti ja kokousmuistiinpanot.

Tehtäväsi on vain tarkistaa. Älä korjaa yhteenvetoa, älä kirjoita sitä uudelleen äläkä sano, onko se hyväksytty tai valmis. Kerro havaintosi. Ihminen päättää niiden perusteella, mitä yhteenvedolle tehdään.

Tee tarkistus kahdessa osassa ja käytä näitä kahta otsikkoa.

Väitteiden tarkistus
Käy yhteenveto läpi väite kerrallaan. Väite on jokainen päätös, jokainen tehtävä ja jokainen avoin asia. Tee taulukko, jossa on neljä saraketta: väite, lähde raportissa, lähde muistiinpanoissa ja havainto.
- Etsi jokaisen väitteen kohta itse aineistosta, vaikka yhteenvedossa olisi jo lähde.
- Kirjoita raportin lähde muodossa "raportti, sivu 7". Raportin sivut on merkitty riveillä, jotka ovat muotoa "Sivu 7 / 15".
- Kirjoita muistiinpanojen lähteeksi palaverin päivämäärä.
- Jos asiasta ei puhuta raportissa tai muistiinpanoissa, kirjoita siihen sarakkeeseen "ei mainita".
- Jos väitteelle ei löydy lähdettä kummastakaan, kirjoita havaintoon "lähdettä ei löydy".
- Vertaa väitteen lukuja, nimiä ja päivämääriä siihen, mitä lähteissä lukee. Jos ne ovat samat, kirjoita havaintoon "täsmää". Jos jokin eroaa, kirjoita havaintoon, mitä yhteenvedossa lukee ja mitä lähteessä lukee.

Erot lähteiden välillä
Listaa tähän jokainen kohta, jossa aineisto sanoo samasta asiasta kahdessa paikassa eri asian. Vertaa raporttia muistiinpanoihin ja palavereja keskenään. Käy tätä varten koko aineisto läpi vielä kerran, myös ne kohdat, joita yhteenvedossa ei mainita. Tarkista erityisesti euromäärät, päivämäärät ja se, kuka on nimetty mihinkin tehtävään tai vastuuseen.

Kirjoita jokaisesta erosta nämä neljä asiaa:
- mistä asiasta on kyse
- ensimmäinen tieto ja sen lähde
- toinen tieto ja sen lähde
- onko ero kirjattu muutos vai ristiriita.

Kirjattu muutos tarkoittaa, että aineistossa on päätös, jossa sanotaan suoraan, että aiempi tieto muuttuu. Ristiriita tarkoittaa, että samasta asiasta on kaksi eri tietoa eikä muutoksesta ole kirjattu päätöstä. Älä päättele, kumpi ristiriitaisista tiedoista on oikea.

Jos eroja ei löydy, kirjoita "eroja ei löytynyt".

TARKISTETTAVA YHTEENVETO
LIITÄ TEKIJÄN TUOTOS TÄHÄN
```
