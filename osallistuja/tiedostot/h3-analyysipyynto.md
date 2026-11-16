# Taulukon analyysipyyntö: tulos, poikkeamat ja kuvaaja

Tällä pyynnöllä tekoäly laskee taulukosta myynnin, kulut ja tuloksen, nimeää poikkeavat kuukaudet ja piirtää kuvaajan, jos palvelusi osaa piirtää. Pyyntö käskee tekoälyä näyttämään laskunsa, jotta voit tarkistaa tuloksen itse taulukkolaskennan kaavalla.

Pyyntö on tämän tiedoston lopussa koodilohkossa. Koodilohko alkaa rivistä, jolla on kolme heittomerkin näköistä merkkiä ja sana text, ja päättyy riviin, jolla on pelkästään samat kolme merkkiä. Kopioi näiden kahden rivin välissä oleva teksti ja jätä itse rivit kopioimatta. Jos ohjelmasi näyttää koodilohkon harmaana laatikkona, kopioi laatikon sisältö.

Lisää ensin keskusteluun tiedosto "talous_6kk.csv". Kopioi sitten pyyntö ja liitä se samaan viestiin.

Jos tiedoston lisääminen ei onnistu, avaa tiedosto, kopioi sen sisältö ja liitä se tekstinä samaan viestiin pyynnön perään.

## Nämä kohdat voit muokata

- **Mitä pidetään poikkeamana.** Kohdassa 3 poikkeama on tappiollinen kuukausi tai kuukausi, jonka myynti tai kulut eroavat selvästi muista. Omassa työssäsi raja voi olla toinen, esimerkiksi tietty euromäärä tai prosentti.
- **Mitä kuvaajassa näytetään.** Kohdassa 4 pyydetään myynti ja kulut kuukausittain. Voit pyytää tilalle esimerkiksi pelkän tuloksen.
- **Aineiston kuvaus.** Pyynnön ensimmäisessä kappaleessa kerrotaan, mitä taulukossa on. Kun käytät pyyntöä omaan taulukkoosi, kirjoita tähän sen sarakkeet ja mitä luvut ovat.

## Näitä älä muuta

- **Lasku näkyviin.** Kohdassa 2 tekoälyä pyydetään näyttämään lasku. Ilman sitä saat pelkän luvun, etkä näe, mistä se on laskettu.
- **Syytä ei arvata.** Kohdan 3 kaksi viimeistä virkettä kieltävät tekoälyä arvaamasta poikkeaman syytä. Taulukossa on vain lukuja, joten syy ei voi löytyä siitä.

## Kopioitava pyyntö

```text
Tässä viestissä on taulukko joko tiedostona tai tekstinä. Siinä on Virtaama Oy:n koulutuspalveluiden myynti ja kulut euroina kuudelta kuukaudelta, tammikuusta kesäkuuhun 2026. Sarakkeet ovat Kuukausi, Myynti ja Kulut, ja ne on erotettu puolipisteellä.

Tee näistä luvuista analyysi neljässä osassa. Käytä vain taulukon lukuja äläkä pyöristä niitä.

1. Tulos kuukausittain
Tee taulukko, jossa on jokaiselta kuukaudelta myynti, kulut ja tulos. Tulos on myynti miinus kulut. Lisää viimeiseksi riviksi luvut yhteensä.

2. Lasku näkyviin
Näytä, miten laskit koko jakson tuloksen: myynti yhteensä, kulut yhteensä ja niiden erotus. Kirjoita lasku niin, että voin tarkistaa sen itse taulukkolaskennassa. Kerro myös, kuinka monta prosenttia tulos on myynnistä.

3. Poikkeavat kuukaudet
Nimeä kuukaudet, jotka poikkeavat muista. Poikkeava kuukausi on tappiollinen, tai sen myynti tai kulut eroavat selvästi muiden kuukausien tasosta. Perustele jokainen poikkeama taulukon luvuilla. Jos poikkeaman syy ei selviä taulukosta, sano se suoraan. Älä arvaa syytä äläkä esitä mahdollista syytä tietona.

4. Kuvaaja
Piirrä kuvaaja, jossa näkyvät myynti ja kulut kuukausittain. Jos et voi piirtää kuvaajaa, sano se. Silloin kohdan 1 taulukko riittää.
```
