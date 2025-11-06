# Ohje: Miten esittää avioerotilastot artikkelissa

## 📝 Mitä yritit selvittää?

Haluat vertailla samaa sukupuolta olevien ja eri sukupuolta olevien parien avioeroja artikkeliasi varten. Mietit kahdta vaihtoehtoa:

**Vaihtoehto A:** Näytä vain eroaste (avioerot suhteessa avioliittojen määrään)  
**Vaihtoehto B:** Näytä kaksi erillistä kaaviota (avioliittojen määrä + avioerojen määrä)

---

## ✅ Vastaus: Vaihtoehto A on parempi

**Sinun intuitiosi oli oikea!** Yleisölle on selkeintä näyttää **eroaste** (avioerot suhteessa avioliittojen määrään), ei pelkkiä absoluuttisia lukuja.

Miksi? Koska pelkät luvut eivät kerro mitään:
- "11,751 heteroeroa vs 89 naisparien eroa" → Ei kerro mitään, koska heteropareja on valtavasti enemmän
- "57% vs 21% eroaste" → Tämä kertoo suhteen, mutta vaatii kontekstia (ks. alla)

---

## ⚠️ TÄRKEÄ ONGELMA: Aika tekee vertailusta ongelmallisen

Tässä on **kriittinen tilastollinen ongelma**, joka sinun TÄYTYY mainita artikkelissa:

### Ongelma:
- **Samaa sukupuolta olevien avioliitot laillistettiin vasta maaliskuussa 2017**
- Tämä tarkoittaa, että samaa sukupuolta olevien parien avioerot tulevat VAIN vuosien 2017-2024 avioliitoista (max 7-8 vuotta vanhoja)
- **MUTTA** heteroparien avioerot tulevat avioliitoista, jotka voivat olla vuosilta 1990, 2000, 2010 jne. (jopa 30+ vuotta vanhoja)

### Miksi tämä on ongelma:
Avioerot ovat harvinaisia ensimmäisinä vuosina. Avioeron todennäköisyys **kasvaa ajan myötä**:
- 0-5 vuotta: vähän eroja
- 5-10 vuotta: enemmän eroja  
- 10-20 vuotta: paljon eroja
- 20+ vuotta: kaikista eniten eroja

Kun vertaat:
- **Samaa sukupuolta: 18.6% eroaste** (vain 0-8 vuotta vanhat avioliitot)
- **Eri sukupuolta: 57.0% eroaste** (mukana 0-30+ vuotta vanhat avioliitot)

→ **Tämä ei ole "apples to apples" -vertailu!**

---

## 📊 Mitä datasta voi OIKEASTI sanoa?

### ✅ TURVALLISIA VÄITTÄMIÄ:

1. **"Naisparit eroavat useammin kuin miesparit"**
   - Naisparit: 21.0% eroaste
   - Miesparit: 13.6% eroaste
   - Tämä on validi vertailu, koska molemmat ovat 2017-2024 dataa

2. **"Samaa sukupuolta olevien parien avioerot ovat toistaiseksi harvinaisempia, mutta trendi on kasvava"**
   - Vuonna 2017: 0.4% eroaste
   - Vuonna 2024: 27.8% eroaste (yhden vuoden suhde)
   - Tämä on odotettua, kun avioliitot vanhenevat

3. **"Vuosina 2017-2024 solmituista samaa sukupuolta olevien avioliitoista 18.6% on jo päättynyt eroon"**
   - Tämä on fakta, mutta mainitse että kyse on vain 7-8 vuoden ajanjaksosta

### ❌ VÄLTÄ NÄITÄ:

1. **"Samaa sukupuolta olevat parit eroavat harvemmin kuin heteroparit"**
   - Tämä EI ole totta - emme voi verrata lukuja suoraan ajan takia
   
2. **"Heteroparien avioeroaste on 57% ja samaa sukupuolta olevilla 19%"** (ilman kontekstia)
   - Harhaanjohtavaa ilman selitystä aikajänteestä

---

## 🎨 Mitä kaavioita käyttää artikkelissa?

Olen luonut sinulle 3 kaaviota. Suosittelen **yhtä** päävaihtoehdoista:

### PÄÄVAIHTOEHDOT (valitse yksi):

**1. `article_main_chart.png`** ⭐ SUOSITTELEN TÄTÄ
- Näyttää, miten eroasteet kehittyvät vuosittain (2017-2024)
- Näyttää, että trendi on nouseva (kuten pitääkin olla)
- Selkeä, informatiivinen, ja välttää harhaanjohtavaa suoraa vertailua

**2. `article_simple_comparison.png`**
- Yksinkertainen pylväskaavio: Miesparit 13.6%, Naisparit 21.0%, Heteroparit 57.0%
- Helppo lukea, mutta VAATII selityksen siitä, miksi heteroparien luku on suurempi

### TUKILOMATERIAL (valinnainen):

**3. `article_supporting_chart.png`**
- Näyttää absoluuttiset luvut (montako avioliittoa, montako eroa)
- Hyvä taustatietoksi, mutta ei ole pääpointti

---

## 📝 Esimerkkiteksti artikkeliin

```
Tilastokeskuksen mukaan vuosina 2017-2024 solmituista samaa sukupuolta 
olevien avioliitoista 18.6% on päättynyt eroon. Naisparien eroaste 
(21.0%) on selvästi korkeampi kuin miesparien (13.6%).

Suoraa vertailua eri sukupuolta olevien parien erosuhteseen (57.0%) 
on vaikea tehdä, sillä samaa sukupuolta olevien avioliitot laillistettiin 
Suomessa vasta vuonna 2017. Tämä tarkoittaa, että samaa sukupuolta olevien 
avioliitot ovat keskimäärin paljon nuorempia - vanhimmatkin vain 7-8 vuotta.

Tilastot osoittavat, että avioerot ovat yleisempiä avioliiton ensimmäisinä 
vuosikymmeninä, joten samaa sukupuolta olevien parien eroasteen odotetaan 
kasvavan tulevina vuosina, kun avioliitot vanhenevat.
```

---

## 📊 Data Datawrapperiin

Olen luonut sinulle CSV-tiedoston: **`datawrapper_export.csv`**

Tämä sisältää kaiken datan valmiiksi muotoiltuna Datawrapperia varten:
- Vuosittaiset eroasteet kaikille ryhmille
- Avioliittojen ja avioerojen määrät
- Valmis tuotavaksi suoraan Datawrapperiin

---

## 🎯 Yhteenveto: Mitä tehdä?

1. **Valitse kaavio:** Käytä `article_main_chart.png` (tai `article_simple_comparison.png`)

2. **Kirjoita selkeä teksti:**
   - Mainitse, että samaa sukupuolta olevien avioliitot laillistettiin 2017
   - Kerro, että naisparit eroavat useammin kuin miesparit (21% vs 14%)
   - Selitä, miksi suora heterovertailu ei ole oikeudenmukainen (aika)

3. **Käytä näitä lukuja:**
   - Naisparit: 21.0% eroaste (2,251 avioliittoa, 472 eroa)
   - Miesparit: 13.6% eroaste (1,057 avioliittoa, 144 eroa)
   - Yhteensä: 18.6% eroaste (3,308 avioliittoa, 616 eroa)

4. **Ole rehellinen rajoituksista:**
   - Data on uutta (vain 2017-2024)
   - Pienet otoskoot (3,000 vs 175,000)
   - Tarvitaan 20-30 vuotta luotettavaan vertailuun

---

## 🔗 Lähde

Lähde: Tilastokeskus, Siviilisäädyn muutokset  
https://pxdata.stat.fi/PxWeb/pxweb/fi/StatFin/StatFin__ssaaty/statfin_ssaaty_pxt_121e.px/

---

**Tsemppiä artikkelin kanssa! 💪**

Jos tarvitset jotain muuta tai haluat muokata kaavioita, kerro vaan!

