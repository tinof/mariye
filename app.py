#!/usr/bin/env python3
"""
Streamlit Web App: Finnish Marriage and Divorce Statistics (2017-2024)
Author: Analysis for Marios's article

Deploy to: streamlit.io (free)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
from scipy.stats import beta

# Page config
st.set_page_config(
    page_title="Avioerot Suomessa 2017-2024",
    page_icon="💍",
    layout="wide"
)

# Data
data = {
    'Year': [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'Marriages_Opposite': [25988, 23412, 21920, 21687, 19204, 21519, 20320, 20995],
    'Divorces_Opposite': [13483, 13116, 13311, 13390, 12081, 11264, 11341, 11751],
    'Marriages_Male': [181, 145, 113, 123, 110, 132, 119, 134],
    'Marriages_Female': [373, 242, 263, 272, 265, 291, 254, 291],
    'Divorces_Male': [1, 6, 12, 25, 17, 26, 28, 29],
    'Divorces_Female': [1, 23, 42, 63, 68, 80, 106, 89],
}

df = pd.DataFrame(data)

# Calculate totals and rates
df['Marriages_SameSex'] = df['Marriages_Male'] + df['Marriages_Female']
df['Divorces_SameSex'] = df['Divorces_Male'] + df['Divorces_Female']

df['Cum_Mar_Opposite'] = df['Marriages_Opposite'].cumsum()
df['Cum_Div_Opposite'] = df['Divorces_Opposite'].cumsum()
df['Cum_Mar_Male'] = df['Marriages_Male'].cumsum()
df['Cum_Div_Male'] = df['Divorces_Male'].cumsum()
df['Cum_Mar_Female'] = df['Marriages_Female'].cumsum()
df['Cum_Div_Female'] = df['Divorces_Female'].cumsum()
df['Cum_Mar_SameSex'] = df['Marriages_SameSex'].cumsum()
df['Cum_Div_SameSex'] = df['Divorces_SameSex'].cumsum()

df['Rate_Opposite'] = (df['Cum_Div_Opposite'] / df['Cum_Mar_Opposite'] * 100)
df['Rate_Male'] = (df['Cum_Div_Male'] / df['Cum_Mar_Male'] * 100)
df['Rate_Female'] = (df['Cum_Div_Female'] / df['Cum_Mar_Female'] * 100)
df['Rate_SameSex'] = (df['Cum_Div_SameSex'] / df['Cum_Mar_SameSex'] * 100)

# Precompute group totals and core stats for reuse
male_marriages = df['Marriages_Male'].sum()
male_divorces = df['Divorces_Male'].sum()
female_marriages = df['Marriages_Female'].sum()
female_divorces = df['Divorces_Female'].sum()
opposite_marriages = df['Marriages_Opposite'].sum()
opposite_divorces = df['Divorces_Opposite'].sum()

p_male = male_divorces / male_marriages if male_marriages else 0
p_female = female_divorces / female_marriages if female_marriages else 0
p_same = (male_divorces + female_divorces) / (male_marriages + female_marriages)

contingency_table = np.array([
    [male_divorces, male_marriages - male_divorces],
    [female_divorces, female_marriages - female_divorces]
])
odds_ratio_tmp, p_value_fisher = stats.fisher_exact(contingency_table)
odds_ratio_female_vs_male = 1/odds_ratio_tmp if odds_ratio_tmp != 0 else np.inf
risk_ratio_female_vs_male = (p_female / p_male) if p_male > 0 else np.inf

# Header
st.title("💍 Avioerot Suomessa 2017-2024")
st.markdown("### Vertailu: Samaa sukupuolta vs. eri sukupuolta olevat parit")

# ============================================================================
# FOUNDATION: What is "eroaste" (divorce rate)?
# ============================================================================
st.markdown("---")
st.subheader("🧩 Mitä tarkoittaa 'eroaste'?")

col_a, col_b = st.columns([1, 1])

with col_a:
    st.markdown("""
    **💬 Puhekielessä:**

    "Puolet avioliitoista päättyy eroon"

    → Tämä tarkoittaa: *Kaikista koskaan solmituista avioliitoista, noin 50% päättyy lopulta eroon*
    (elinaikainen todennäköisyys).

    **Esimerkki:**
    - Jos 100 paria menee naimisiin
    - Seurataan heitä 30 vuotta
    - ~50 parista erotaan jossakin vaiheessa
    """)

with col_b:
    st.markdown("""
    **📊 Tässä analyysissa:**

    "21% (naisparit) ja 14% (miesparit)"

    → Tämä tarkoittaa: *Vuosina 2017-2024 solmituista avioliitoista, näin moni on JO eronnut*
    (kumulatiivinen osuus, ei lopullinen).

    **Esimerkki:**
    - 2,251 naisparia meni naimisiin 2017-2024
    - 472 heistä on jo eronnut (lokakuuhun 2024)
    - = 21% tähän mennessä (ei lopullinen luku!)
    """)

st.warning("""
⚠️ **Tärkeä ero:**

- **Puhekielen "puolet eroaa"** = Elinaikainen ennuste (vaatii 30+ vuoden seurannan)
- **Tämän analyysin "21%"** = Kuinka moni on JO eronnut 7-8 vuoden aikana (luku kasvaa vielä)

**Analogia:** Jos istutamme omenapuita vuonna 2017 ja laskemme tippuneita omenoita vuonna 2024,
emme voi sanoa "näin monta omenaa tippuu lopulta" - puut ovat vasta nuoria!
""")

st.markdown("---")

st.info("""
**⏰ Aikajänne-huomio:** Samaa sukupuolta olevien avioliitot laillistettiin Suomessa maaliskuussa 2017.
Siksi datamme kattaa vain 7-8 vuotta. Eri sukupuolta olevien parien avioerot voivat tulla
avioliitoista jotka solmittiin 1990-luvulla tai aikaisemmin.
""")

# ============================================================================
# JOURNALIST QUICK GUIDE - Direct answer for Marios
# ============================================================================
st.markdown("---")
st.subheader("📰 Toimittajan Pikaopas")

st.success("""
**❓ Miksi naisparit eroavat useammin kuin miesparit?**

✅ **Vastaus:** Vuosina 2017-2024 solmituista avioliitoista naisparien eroaste on **21%** ja miesparien **14%**.

**Tämä tarkoittaa:**
- 21% naisparien avioliitoista on jo päättynyt (472 eroa / 2,251 avioliittoa)
- 14% miesparien avioliitoista on jo päättynyt (144 eroa / 1,057 avioliittoa)
- Ero on tilastollisesti merkitsevä (ei sattumaa)
- Naisparilla on noin **1.5 kertaa** suurempi todennäköisyys erota
""")

st.markdown("**📋 Kopioi artikkeliisi (YKSINKERTAINEN VERSIO):**")

simple_copy = f"""
Vuosina 2017–2024 naisparien eroaste oli 21 prosenttia ja miesparien 14 prosenttia.
Naisparien avioliitoista on siis eronnut noin puolitoista kertaa useammin kuin miesparien.

Ero on tilastollisesti merkitsevä, eli se ei johdu sattumasta.

Huomioitavaa on, että nämä luvut eivät kerro lopullista eroastetta - monet avioliitot
ovat vasta muutaman vuoden ikäisiä, ja eroaste kasvaa todennäköisesti ajan myötä.
"""

st.code(simple_copy.strip(), language="markdown")

st.markdown("**📊 Kaaviot artikkeliisi:**")
st.caption("Scrollaa alemmas nähdäksesi vertailukuvaajia. Erityisesti osio '📊 Yksinkertainen vertailu' sopii hyvin artikkeli-käyttöön.")

st.markdown("---")

st.warning("""
⚠️ **TÄRKEÄ VAROITUS:**

**ÄLÄ** vertaa lukua 21% lukuun **57%** (eri sukupuolta olevien parien "eroaste").

**Miksi?** Ne mittaavat eri asioita:
- 21% = 2017-2024 solmittujen avioliittojen eroaste (kaikki avioerot tulevat 2017-2024 avioliitoista)
- 57% = 2017-2024 avioerot ÷ 2017-2024 solmitut (mutta avioerot tulevat myös 1990-2016 avioliitoista!)

**Katso tarkempi selitys alla** osiossa "Miksi 57% on harhaanjohtava?"
""")

# ============================================================================
# SIMPLE COMPARISON CHART - For article use
# ============================================================================
st.markdown("### 📊 Yksinkertainen vertailu")

# Create simple horizontal bar chart
fig_simple = go.Figure()

fig_simple.add_trace(go.Bar(
    x=[p_female*100, p_male*100],
    y=['Naisparit', 'Miesparit'],
    orientation='h',
    marker=dict(color=['#e74c3c', '#3498db']),
    text=[f'{p_female*100:.1f}%', f'{p_male*100:.1f}%'],
    textposition='outside',
    textfont=dict(size=20, color='black', family='Arial Black'),
    hovertemplate='<b>%{y}</b><br>Eroaste: %{x:.1f}%<br><extra></extra>'
))

fig_simple.update_layout(
    title=dict(
        text="Samaa sukupuolta olevien parien avioerot 2017-2024",
        font=dict(size=18, family='Arial', color='black')
    ),
    xaxis=dict(
        title="Eroaste (%)",
        range=[0, 30],
        tickfont=dict(size=14),
        titlefont=dict(size=16)
    ),
    yaxis=dict(
        tickfont=dict(size=16, family='Arial Black'),
        categoryorder='total ascending'
    ),
    height=300,
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=100, r=100, t=60, b=60)
)

st.plotly_chart(fig_simple, use_container_width=True)

st.caption("""
**Tulkinta:** Naisparien eroaste (21%) on noin 1.5-kertainen miespareihin (14%) verrattuna.
Tämä kuvaaja sopii hyvin artikkelikäyttöön.
""")

st.markdown("---")

# Guided helper: define what "eroaste" means
with st.expander("🧭 Lisäapu: Millaista lukua haet?"):
    st.markdown("""
    **Tämä osio auttaa sinua ymmärtämään, millaisia eri eroaste-lukuja voidaan laskea.**

    Valitse alla, mikä kysymys kuvaa parhaiten sitä mitä haluat tietää:
    """)

    choice = st.radio(
        "Valitse kysymyksesi:",
        (
            "📅 Kuinka moni tänä vuonna erosi? (vuosittainen rytmi)",
            "📊 Kuinka monesta 2017-2024 solmitusta avioliitosta on jo tullut ero? (SUOSITUS)",
            "🔮 Kuinka moni lopulta eroaa koskaan? (vaatii erikoisanalyysin, ei saatavilla)"
        ),
        index=1
    )

    if "tänä vuonna" in choice:
        year = st.slider("Valitse vuosi", int(df['Year'].min()), int(df['Year'].max()), int(df['Year'].max()))
        row = df.loc[df['Year'] == year].iloc[0]
        st.info("""
        **Mitä tämä mittaa:** Yhden vuoden eronneiden määrä jaettuna saman vuoden solmittujen määrällä.

        **Käyttötarkoitus:** Näyttää vuosittaisen "rytmin", mutta ei kerro pitkän aikavälin riskiä.

        **Huom:** Ei sovellu väittämiin "kuka eroaa useammin", koska vuoden erot eivät tule saman vuoden avioliitoista!
        """)
        st.metric("Naisparit", f"{row['Divorces_Female']/row['Marriages_Female']*100:.1f}%")
        st.metric("Miesparit", f"{row['Divorces_Male']/row['Marriages_Male']*100:.1f}%")
        st.metric("Eri sukupuolta", f"{row['Divorces_Opposite']/row['Marriages_Opposite']*100:.1f}%")
    elif "2017-2024 solmitusta" in choice:
        st.success("""
        **Mitä tämä mittaa:** Kuinka moni vuosina 2017-2024 solmituista avioliitoista on JO päättynyt eroon.

        **Käyttötarkoitus:** Vertailla samaa sukupuolta olevien pareja keskenään (nais- vs miesparit).

        **Huom:** Ei vertailukelpoinen heteropareihin (eri aikajänteet)!
        """)
        st.metric("Naisparit", f"{p_female*100:.1f}%")
        st.metric("Miesparit", f"{p_male*100:.1f}%")
        st.metric("Samaa sukupuolta (yht.)", f"{p_same*100:.1f}%")
        st.caption(f"✅ Ero on tilastollisesti merkitsevä (Fisher p-arvo: {p_value_fisher:.2e}, Riskisuhde: {risk_ratio_female_vs_male:.2f}x)")
    else:
        st.error("""
        **Tätä EI voi laskea tästä datasta!**

        "Kuinka moni lopulta eroaa" vaatii **survival-analyysin** (eloonjäämisanalyysi).
        """)
        st.markdown("""
        **Mitä tarvittaisiin:**
        - Jokaisen avioliiton solmimispäivä
        - Mahdollinen eropäivä TAI tieto että avioliitto on yhä voimassa
        - Kaplan-Meier -analyysi tai vastaava menetelmä

        **Katso lisätietoa:** Sivun alaosan "Tilastotieteilijän nurkkaus" -osiossa välilehdellä "Puuttuvan Datan Hankkiminen".
        """)

    st.markdown("---")
    st.markdown("### 📝 Valmiit vastaukset journalistisiin kysymyksiin")

    q = st.selectbox(
        "Valitse kysymyksesi:",
        (
            "❓ Eroavatko naisparit useammin kuin miesparit?",
            "❓ Voiko sanoa 'noin puolet avioliitoista päättyy eroon'?",
            "❓ Milloin eroja tapahtuu eniten avioliiton aikana?"
        )
    )
    if "naisparit useammin" in q:
        st.success(f"""
        **✅ KYLLÄ, naisparit eroavat useammin!**

        - Naisparit: **{p_female*100:.1f}%** ({female_divorces} eroa / {female_marriages} avioliittoa)
        - Miesparit: **{p_male*100:.1f}%** ({male_divorces} eroa / {male_marriages} avioliittoa)
        - Ero on tilastollisesti merkitsevä (ei sattumaa)
        - Naisparilla noin **{risk_ratio_female_vs_male:.1f} kertaa** suurempi todennäköisyys erota
        """)

        st.markdown("**📋 Kopioi artikkeliisi (tekninen versio):**")
        st.code(
            f"Vuosina 2017–2024 naisparien eroaste oli {p_female*100:.1f}% ja miesparien {p_male*100:.1f}%. "
            f"Ero on tilastollisesti merkitsevä (Fisher-testi p={p_value_fisher:.2e}), ja "
            f"naispareilla riski erota oli noin {risk_ratio_female_vs_male:.2f}-kertainen miespareihin verrattuna.",
            language="markdown"
        )
    elif "noin puolet" in q:
        st.warning("""
        **⚠️ EI voi sanoa (ainakaan tämän datan perusteella)**

        "Noin puolet avioliitoista päättyy eroon" on **elinaikainen ennuste**, joka vaatii:
        - 30+ vuoden seurannan
        - Survival-analyysin (Kaplan-Meier tai vastaava)
        - Yksilötason dataa (jokaisen avioliiton kesto)
        """)

        st.markdown("**📋 Mitä VOIT sanoa:**")
        st.code(
            f"Vuosina 2017–2024 solmituista samaa sukupuolta olevien avioliitoista {p_same*100:.1f}% on jo päättynyt eroon. "
            "Tämä luku tulee todennäköisesti kasvamaan, kun avioliitot vanhenevat. "
            "Lopullista eroastetta ei voi vielä arvioida luotettavasti, koska seuranta-aika on vasta 7-8 vuotta.",
            language="markdown"
        )
    else:
        st.warning("""
        **⚠️ EI voi vastata tällä datalla**

        "Milloin eroja tapahtuu eniten" vaatii tiedon avioliiton kestosta (kuinka monta vuotta vihkimisestä).

        Tämä data sisältää vain:
        - Vuosittaiset avioliittojen määrät
        - Vuosittaiset avioerojen määrät

        Ei tietoa yksittäisten avioliittojen kestosta.
        """)

        st.markdown("**💡 Yleinen tieto (ei tästä datasta):**")
        st.info(
            "Yleisesti tiedetään että avioerot ovat yleisimpiä 3.-5. avioliittovuoden aikana, "
            "mutta tämä vaatii yksilötason dataa vahvistukseksi."
        )

# Key metrics
st.markdown("### 📊 Avainluvut")

show_hetero_indicator = st.toggle(
    "Näytä heteroparien 2017–2024 'indikaattori' ⚠️ (VAROITUS: ei vertailukelpoinen!)",
    value=True,
    help=(
        "Luku = 2017–2024 avioerojen määrä / 2017–2024 solmittujen avioliittojen määrä. "
        "Se EI ole elinaikainen todennäköisyys, koska 2017–2024 avioeroihin sisältyy paljon "
        "vanhoja avioliittoja. Siksi luku ei ole vertailukelpoinen samaa sukupuolta olevien kanssa."
    )
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Naisparien eroaste",
        f"{df['Rate_Female'].iloc[-1]:.1f}%",
        help="Avioerojen osuus kaikista 2017-2024 solmituista naisparien avioliitoista"
    )

with col2:
    st.metric(
        "Miesparien eroaste",
        f"{df['Rate_Male'].iloc[-1]:.1f}%",
        help="Avioerojen osuus kaikista 2017-2024 solmituista miesparien avioliitoista"
    )

with col3:
    st.metric(
        "Samaa sukupuolta yhteensä",
        f"{df['Rate_SameSex'].iloc[-1]:.1f}%",
        help="Avioerojen osuus kaikista 2017-2024 solmituista samaa sukupuolta olevien avioliitoista"
    )

with col4:
    if show_hetero_indicator:
        st.metric(
            "Eri sukupuolta (indikaattori)",
            f"{df['Rate_Opposite'].iloc[-1]:.1f}%",
            help=(
                "2017–2024 avioerot / 2017–2024 solmitut heteroavioliitot. "
                "Ei vertailukelpoinen samaa sukupuolta olevien kanssa ajoitusvinouman vuoksi."
            )
        )
    else:
        st.metric(
            "Eri sukupuolta",
            "—",
            help=(
                "Heteroparien '57 %' ei ole vertailukelpoinen indikaattori. "
                "Avaa alta selitys: 'Mikä on 57 %?'."
            )
        )

with st.expander("⚠️ Miksi 57% on harhaanjohtava? (TÄRKEÄ - lue tämä!)", expanded=True):
    st.markdown("""
    ### 🍎 Hedelmäpuutarha-analogia

    Kuvittele kaksi omenapuutarhaa:
    """)

    col_orchard1, col_orchard2 = st.columns(2)

    with col_orchard1:
        st.markdown("""
        **🌳 Puutarha A: Samaa sukupuolta olevat parit**

        - Istutettu: 2017-2024 (kaikki puut)
        - Tippuneet omenat: 2017-2024
        - Laskemme: Tippuneet / Istutetut = **21%**

        → Oikeudenmukainen laskutapa! ✅
        """)

    with col_orchard2:
        st.markdown("""
        **🌳 Puutarha B: Eri sukupuolta olevat parit**

        - Istutettu: 1950-2024 (monet vanhat puut!)
        - Tippuneet omenat: 2017-2024
        - Laskemme: Tippuneet / **VAIN 2017-2024 istutetut** = **57%**

        → Epäreilu laskutapa! ❌
        """)

    st.error("""
    **❌ Ongelma:**

    Puutarhan B omenat tulevat **kaikista** vuosina 1950-2024 istutetuista puista,
    mutta laskemme vain vuosina 2017-2024 istutetut puut!

    Tämä saa 57%:n näyttämään suurelta, mutta se ei kerro totuutta.
    """)

    st.markdown("""
    ### 📊 Mitä tämä tarkoittaa numeroilla?

    **Heteroparien 57%:**
    - **Osoittaja** (erot 2017-2024): ~90,000 eroa
      - Näihin sisältyy eroja 1990-, 2000-, 2010-luvulla solmituista avioliitoista
    - **Nimittäjä** (avioliitot 2017-2024): ~155,000 avioliittoa
      - Vain viimeisen 7-8 vuoden avioliitot
    - **Tulos**: 90,000 / 155,000 ≈ 57%

    **Samaa sukupuolta olevien 21%:**
    - **Osoittaja** (erot 2017-2024): ~615 eroa
      - Kaikki erot tulevat 2017-2024 solmituista avioliitoista
    - **Nimittäjä** (avioliitot 2017-2024): ~3,300 avioliittoa
      - Kaikki avioliitot
    - **Tulos**: 615 / 3,300 ≈ 19%

    **Siksi**: 57% ja 21% eivät ole vertailukelpoisia!
    """)

    st.success("""
    **✅ Mitä voit sanoa turvallisesti:**

    - "Naisparit eroavat useammin kuin miesparit (21% vs 14%)" ✅
    - "Samaa sukupuolta olevien parien eroaste on 19%" ✅
    - "Heteroparien '57%' ei ole vertailukelpoinen luku" ✅

    **❌ Mitä et voi sanoa:**

    - "Samaa sukupuolta olevat eroavat harvemmin kuin heteroparit" ❌
    - "57% heteropareista eroaa" (ei pidä paikkaansa!) ❌
    """)

st.divider()

# Main chart: Cumulative divorce rates
st.subheader("📈 Kumulatiivinen eroaste vuosittain")

fig1 = go.Figure()

fig1.add_trace(go.Scatter(
    x=df['Year'], y=df['Rate_Male'],
    name='Miesparit',
    mode='lines+markers',
    line=dict(color='#3498db', width=3),
    marker=dict(size=8)
))

fig1.add_trace(go.Scatter(
    x=df['Year'], y=df['Rate_Female'],
    name='Naisparit',
    mode='lines+markers',
    line=dict(color='#e74c3c', width=3),
    marker=dict(size=8)
))

fig1.add_trace(go.Scatter(
    x=df['Year'], y=df['Rate_SameSex'],
    name='Samaa sukupuolta yhteensä',
    mode='lines+markers',
    line=dict(color='#9b59b6', width=3, dash='dash'),
    marker=dict(size=8)
))

fig1.add_trace(go.Scatter(
    x=df['Year'], y=df['Rate_Opposite'],
    name='Eri sukupuolta',
    mode='lines+markers',
    line=dict(color='#2ecc71', width=3, dash='dot'),
    marker=dict(size=8)
))

fig1.update_layout(
    xaxis_title="Vuosi",
    yaxis_title="Kumulatiivinen eroaste (%)",
    hovermode='x unified',
    height=500,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig1, use_container_width=True)

st.caption("""
**Kumulatiivinen eroaste** = (Avioerojen kokonaismäärä 2017-lähtien) / (Avioliittojen kokonaismäärä 2017-lähtien) × 100%  
Kaavio näyttää, miten eroaste kehittyy ajan myötä kun avioliitot vanhenevat.
""")

st.divider()

# Simple takeaways for non-experts
st.subheader("🧠 Kolme tärkeintä asiaa (selkokieli)")
st.success(
    """
    - Naisparit eroavat tässä datassa useammin kuin miesparit.
    - Heterolukua ("57 %") ei pidä verrata samaa sukupuolta oleviin – se mittaa eri asiaa.
    - Jos haluat sanoa "kuinka moni päätyy joskus eroon", tarvitset keston (eloonjäämisanalyysi).
    """
)

# Copy-ready blurb
copy_blurb = (
    f"Vuosina 2017–2024 naisparien eroaste oli {p_female*100:.1f}% "
    f"({female_divorces}/{female_marriages}) ja miesparien {p_male*100:.1f}% "
    f"({male_divorces}/{male_marriages}). Ero on hyvin epätodennäköisesti sattumaa "
    f"(Fisher p≈{p_value_fisher:.1e}). Naispareilla ero oli noin "
    f"{risk_ratio_female_vs_male:.2f}-kertainen verrattuna miespareihin. "
    f"Samaa sukupuolta olevien ja heteroparien suoraa vertailua ei voi tehdä reilusti, "
    f"koska samaa sukupuolta olevien avioliitot alkavat vasta vuodesta 2017."
)

st.markdown("**Kopioi juttuun:**")
st.code(copy_blurb, language="markdown")

st.caption("💡 **Vinkki:** Sanasto-termit löytyvät sivupalkin yläosasta!")

st.divider()

# Comparison chart
col1, col2 = st.columns(2)

with col1:
    st.subheader("💑 Solmitut avioliitot vuosittain")
    
    fig2 = go.Figure()
    
    fig2.add_trace(go.Bar(
        x=df['Year'],
        y=df['Marriages_Male'],
        name='Miesparit',
        marker_color='#3498db'
    ))
    
    fig2.add_trace(go.Bar(
        x=df['Year'],
        y=df['Marriages_Female'],
        name='Naisparit',
        marker_color='#e74c3c'
    ))
    
    fig2.update_layout(
        xaxis_title="Vuosi",
        yaxis_title="Avioliittojen määrä",
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("💔 Avioerot vuosittain")
    
    fig3 = go.Figure()
    
    fig3.add_trace(go.Bar(
        x=df['Year'],
        y=df['Divorces_Male'],
        name='Miesparit',
        marker_color='#3498db'
    ))
    
    fig3.add_trace(go.Bar(
        x=df['Year'],
        y=df['Divorces_Female'],
        name='Naisparit',
        marker_color='#e74c3c'
    ))
    
    fig3.update_layout(
        xaxis_title="Vuosi",
        yaxis_title="Avioerojen määrä",
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# Summary statistics
st.subheader("📊 Yhteenvetotaulukko (2017-2024)")

summary = pd.DataFrame({
    'Parityyppi': ['Miesparit', 'Naisparit', 'Samaa sukupuolta yhteensä', 'Eri sukupuolta'],
    'Avioliitot': [
        df['Marriages_Male'].sum(),
        df['Marriages_Female'].sum(),
        df['Marriages_SameSex'].sum(),
        df['Marriages_Opposite'].sum()
    ],
    'Avioerot': [
        df['Divorces_Male'].sum(),
        df['Divorces_Female'].sum(),
        df['Divorces_SameSex'].sum(),
        df['Divorces_Opposite'].sum()
    ],
    'Eroaste (%)': [
        df['Rate_Male'].iloc[-1],
        df['Rate_Female'].iloc[-1],
        df['Rate_SameSex'].iloc[-1],
        df['Rate_Opposite'].iloc[-1]
    ]
})

# Format numbers
summary['Avioliitot'] = summary['Avioliitot'].apply(lambda x: f"{x:,}".replace(',', ' '))
summary['Avioerot'] = summary['Avioerot'].apply(lambda x: f"{x:,}".replace(',', ' '))
summary['Eroaste (%)'] = summary['Eroaste (%)'].apply(lambda x: f"{x:.1f}%")

st.dataframe(summary, use_container_width=True, hide_index=True)

st.divider()

# Important notes
st.subheader("⚠️ Tärkeät huomiot")

st.warning("""
**Tilastollinen rajoitus:**

1. **Samaa sukupuolta olevien avioliitot** laillistettiin Suomessa maaliskuussa 2017
   - Data kattaa vain 7-8 vuoden ajanjakson
   - Kaikki avioerot tulevat maksimissaan 8 vuotta vanhoista avioliitoista

2. **Eri sukupuolta olevien parien avioerot** voivat tulla avioliitoista, jotka on solmittu 1990-luvulla tai aikaisemmin
   - Data kattaa vuosikymmeniä
   - Mukana paljon vanhempia avioliittoja

3. **Avioeron todennäköisyys kasvaa avioliiton keston myötä**
   - Tämä tekee suorasta vertailusta ongelmallisen
   - 57% vs 19% -lukuja ei voi suoraan verrata

**Mitä voimme sanoa:**
- ✅ Naisparit eroavat useammin kuin miesparit (21% vs 14%)
- ✅ Samaa sukupuolta olevien parien eroaste on kasvussa (odotetusti)
- ❌ Emme voi sanoa, että "samaa sukupuolta olevat eroavat harvemmin" - data on liian uutta
""")

with st.expander("Kysymyksiä ja vastauksia (journalistille)"):
    st.markdown(
        """
        **Onko 'noin puolet avioliitoista päättyy eroon' totta?**  
        – Se on elinaikainen ennuste, ei suora havaittu osuus yhden kalenterijakson sisällä. Tarvitsemme kohortti‑/eloonjäämisanalyysin sen arviointiin.

        **Miksi samaa sukupuolta olevien ja heteroparien lukuja ei voi suoraan verrata?**  
        – Samaa sukupuolta olevien avioliitot alkavat vasta 2017, heteroeroissa näkyy myös paljon aiempien vuosikymmenten avioliittoja. Aikajänteet ovat erilaiset.

        **Miksi naisparien eroaste näyttää korkeammalta kuin miesparien?**  
        – Havainto on tilastollisesti merkitsevä tässä datassa. Syy ei kuitenkaan ole tästä datasta pääteltävissä; ikä, perhetausta, lapset ja muut tekijät voivat vaikuttaa. Ne vaatisivat mikrodataa ja mallinnusta.
        """
    )

# Data source
st.divider()
st.caption("""
**Lähde:** Tilastokeskus, Siviilisäädyn muutokset  
https://pxdata.stat.fi/PxWeb/pxweb/fi/StatFin/StatFin__ssaaty/statfin_ssaaty_pxt_121e.px/

**Viimeksi päivitetty:** 24.4.2025
""")

# ============================================================================
# ADVANCED STATISTICAL SECTION
# ============================================================================
st.divider()
st.header("🔬 Tilastotieteilijän nurkkaus")

st.info("""
**Tämä osio on tarkoitettu:**
- Tilastotieteilijöille ja tutkijoille
- Opiskelijoille ja harrastelijoille, jotka haluavat oppia tilastollisesta ajattelusta
- Niille, jotka haluavat ymmärtää syvemmin, miten dataa tulisi analysoida

Perustilastot yllä ovat oikein, mutta tässä osiossa näytämme kehittyneempiä menetelmiä.
""")

# Tabs for different statistical topics
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Luottamusvälit & Merkitsevyys",
    "🎓 Bayesilainen Analyysi", 
    "📚 Akateeminen vs. Journalistinen",
    "💾 Puuttuvan Datan Hankkiminen"
])

# ============================================================================
# TAB 1: Confidence Intervals & Significance
# ============================================================================
with tab1:
    st.subheader("Luottamusvälit ja Tilastollinen Merkitsevyys")
    
    st.markdown("""
    **Miksi tämä on tärkeää?**
    
    Pelkkä prosenttiluku (esim. "21%") ei kerro:
    - Kuinka varma voimme olla luvusta
    - Onko ero ryhmien välillä todellinen vai sattumaa
    
    Tilastollinen analyysi vastaa näihin kysymyksiin.
    """)
    
    # Calculate confidence intervals using Wilson score method
    def wilson_score_interval(successes, trials, confidence=0.95):
        if trials == 0:
            return 0, 0, 0
        p = successes / trials
        z = stats.norm.ppf((1 + confidence) / 2)
        denominator = 1 + z**2 / trials
        center = (p + z**2 / (2 * trials)) / denominator
        margin = z * np.sqrt((p * (1 - p) / trials + z**2 / (4 * trials**2))) / denominator
        return p, max(0, center - margin), min(1, center + margin)
    
    # Calculate for each group
    male_marriages = df['Marriages_Male'].sum()
    male_divorces = df['Divorces_Male'].sum()
    female_marriages = df['Marriages_Female'].sum()
    female_divorces = df['Divorces_Female'].sum()
    opposite_marriages = df['Marriages_Opposite'].sum()
    opposite_divorces = df['Divorces_Opposite'].sum()
    
    groups_data = [
        ('Naisparit', female_marriages, female_divorces, '#e74c3c'),
        ('Miesparit', male_marriages, male_divorces, '#3498db'),
        ('Eri sukupuolta', opposite_marriages, opposite_divorces, '#2ecc71')
    ]
    
    ci_results = []
    for name, marriages, divorces, color in groups_data:
        rate, ci_lower, ci_upper = wilson_score_interval(divorces, marriages)
        ci_results.append({
            'Group': name,
            'Rate': rate * 100,
            'CI_Lower': ci_lower * 100,
            'CI_Upper': ci_upper * 100,
            'Color': color
        })
    
    # Visualization: Confidence Intervals
    fig_ci = go.Figure()
    
    for i, result in enumerate(ci_results):
        fig_ci.add_trace(go.Bar(
            y=[result['Group']],
            x=[result['Rate']],
            orientation='h',
            name=result['Group'],
            marker_color=result['Color'],
            error_x=dict(
                type='data',
                symmetric=False,
                array=[result['CI_Upper'] - result['Rate']],
                arrayminus=[result['Rate'] - result['CI_Lower']],
                thickness=2,
                width=10
            ),
            showlegend=False
        ))
    
    fig_ci.update_layout(
        title="Eroasteet 95% Luottamusvälein",
        xaxis_title="Eroaste (%) ± 95% Luottamusväli",
        yaxis_title="",
        height=300
    )
    
    st.plotly_chart(fig_ci, use_container_width=True)
    
    # Display numerical results
    st.markdown("### 📊 Numeeriset Tulokset")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Naisparit",
            f"{ci_results[0]['Rate']:.2f}%",
            delta=f"±{(ci_results[0]['CI_Upper'] - ci_results[0]['CI_Lower'])/2:.2f}%",
            help=f"95% Luottamusväli: [{ci_results[0]['CI_Lower']:.2f}% - {ci_results[0]['CI_Upper']:.2f}%]"
        )
    
    with col2:
        st.metric(
            "Miesparit",
            f"{ci_results[1]['Rate']:.2f}%",
            delta=f"±{(ci_results[1]['CI_Upper'] - ci_results[1]['CI_Lower'])/2:.2f}%",
            help=f"95% Luottamusväli: [{ci_results[1]['CI_Lower']:.2f}% - {ci_results[1]['CI_Upper']:.2f}%]"
        )
    
    with col3:
        st.metric(
            "Eri sukupuolta",
            f"{ci_results[2]['Rate']:.2f}%",
            delta=f"±{(ci_results[2]['CI_Upper'] - ci_results[2]['CI_Lower'])/2:.2f}%",
            help=f"95% Luottamusväli: [{ci_results[2]['CI_Lower']:.2f}% - {ci_results[2]['CI_Upper']:.2f}%]"
        )
    
    st.markdown("---")
    
    # Statistical significance test
    st.markdown("### 🧪 Tilastollinen merkitsevyys: Naisparit vs. miesparit")
    
    st.markdown("""
    **Kysymys:** Onko naisparien korkeampi eroaste (21% vs 14%) todellinen ero, 
    vai voisiko se johtua sattumasta?
    
    **Testit:**
    """)
    
    # Fisher's exact test
    contingency_table = np.array([
        [male_divorces, male_marriages - male_divorces],
        [female_divorces, female_marriages - female_divorces]
    ])
    
    odds_ratio, p_value_fisher = stats.fisher_exact(contingency_table)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Fisher's Exact Test (P-value)",
            f"{p_value_fisher:.6f}",
            delta="Merkitsevä!" if p_value_fisher < 0.05 else "Ei merkitsevä"
        )
    
    with col2:
        st.metric(
            "Odds‑suhde (naisparit / miesparit)",
            f"{1/odds_ratio:.2f}x",
            help=(
                "Odds‑suhde ei ole sama kuin riskisuhde, mutta pienillä prosenteilla ne ovat lähekkäin."
            )
        )
    
    if p_value_fisher < 0.05:
        st.success(f"""
        ✅ **ERO ON TILASTOLLISESTI MERKITSEVÄ** (p = {p_value_fisher:.6f} < 0.05)
        
        Tämä tarkoittaa:
        - Ero ei johdu sattumasta
        - Voimme luottavaisin mielin sanoa: "Naisparit eroavat useammin kuin miesparit"
        - Naisparilla on **{1/odds_ratio:.2f} kertaa** suurempi todennäköisyys erota
        """)
    else:
        st.warning("Ero ei ole tilastollisesti merkitsevä (p ≥ 0.05)")
    
    # Effect size
    st.markdown("### 📏 Efektikoko (Cohen's h)")
    
    def cohens_h(p1, p2):
        return 2 * (np.arcsin(np.sqrt(p1)) - np.arcsin(np.sqrt(p2)))
    
    p_female = female_divorces / female_marriages
    p_male = male_divorces / male_marriages
    h = cohens_h(p_female, p_male)
    risk_ratio = (p_female / p_male) if p_male > 0 else float('inf')
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Cohen's h", f"{h:.3f}")

    with col2:
        st.metric(
            "Riskisuhde (naisparit / miesparit)",
            f"{risk_ratio:.2f}x",
            help="Todennäköisyyksien suhde: p(ero | naispari) / p(ero | miespari)"
        )
        if abs(h) < 0.2:
            st.info("📊 **Pieni efekti** - Ero on olemassa, mutta ei valtava")
        elif abs(h) < 0.5:
            st.warning("📊 **Keskikokoinen efekti** - Merkittävä ero")
        else:
            st.error("📊 **Suuri efekti** - Hyvin suuri ero")
    
    st.markdown("""
    **Tulkinta:**
    - Cohen's h mittaa eron suuruuden (ei vain sen merkitsevyyden)
    - Pieni: < 0.2, Keskikokoinen: 0.2-0.5, Suuri: > 0.5
    - Meidän tapauksessamme: Ero ON merkitsevä, mutta efekti on pieni
    """)

# ============================================================================
# TAB 2: Bayesian Analysis
# ============================================================================
with tab2:
    st.subheader("Bayesilainen Lähestymistapa")
    
    st.markdown("""
    **Mikä on Bayesilainen analyysi?**
    
    Perinteinen (frekventistinen) tilastotiede:
    - "Todennäköisyys saada nämä tulokset, JOS nollahypoteesi on totta"
    - Vaikea tulkita
    
    Bayesilainen analyysi:
    - "Todennäköisyysjakauma sille, mikä TODELLINEN eroaste on"
    - Helpompi tulkita
    - Erityisen hyvä pienille otoksille (kuten miesparit, n=1,057)
    """)
    
    # Bayesian analysis
    def bayesian_estimate(successes, trials, prior_alpha=1, prior_beta=1):
        posterior_alpha = prior_alpha + successes
        posterior_beta = prior_beta + (trials - successes)
        mean = posterior_alpha / (posterior_alpha + posterior_beta)
        ci_lower = beta.ppf(0.025, posterior_alpha, posterior_beta)
        ci_upper = beta.ppf(0.975, posterior_alpha, posterior_beta)
        return mean, ci_lower, ci_upper, posterior_alpha, posterior_beta
    
    # Calculate for same-sex couples only
    mean_male, ci_lower_male, ci_upper_male, alpha_male, beta_male = bayesian_estimate(
        male_divorces, male_marriages
    )
    mean_female, ci_lower_female, ci_upper_female, alpha_female, beta_female = bayesian_estimate(
        female_divorces, female_marriages
    )
    
    # Visualize posterior distributions
    x = np.linspace(0, 0.35, 1000)
    y_male = beta.pdf(x, alpha_male, beta_male)
    y_female = beta.pdf(x, alpha_female, beta_female)
    
    fig_bayes = go.Figure()
    
    fig_bayes.add_trace(go.Scatter(
        x=x*100, y=y_male,
        mode='lines',
        name='Miesparit',
        fill='tozeroy',
        line=dict(color='#3498db', width=2),
        opacity=0.7
    ))
    
    fig_bayes.add_trace(go.Scatter(
        x=x*100, y=y_female,
        mode='lines',
        name='Naisparit',
        fill='tozeroy',
        line=dict(color='#e74c3c', width=2),
        opacity=0.7
    ))
    
    fig_bayes.update_layout(
        title="Bayesilainen Posteriorijakauma<br><sub>Todennäköisyysjakauma sille, mikä todellinen eroaste on</sub>",
        xaxis_title="Eroaste (%)",
        yaxis_title="Todennäköisyystiheys",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_bayes, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Miesparit:**")
        st.write(f"• Estimaatti: {mean_male*100:.2f}%")
        st.write(f"• 95% Credible Interval: [{ci_lower_male*100:.2f}% - {ci_upper_male*100:.2f}%]")
        st.write(f"• Otoskoko: n={male_marriages:,}")
    
    with col2:
        st.markdown("**Naisparit:**")
        st.write(f"• Estimaatti: {mean_female*100:.2f}%")
        st.write(f"• 95% Credible Interval: [{ci_lower_female*100:.2f}% - {ci_upper_female*100:.2f}%]")
        st.write(f"• Otoskoko: n={female_marriages:,}")
    
    st.markdown("---")
    
    st.markdown("""
    **Mitä jakauma kertoo?**
    
    - **Korkeampi huippu** = Varmempi estimaatti (naisparilla korkeampi, koska suurempi otos)
    - **Leveämpi jakauma** = Epävarmempi estimaatti (miesparilla leveämpi, koska pienempi otos)
    - **Ei päällekkäisyyttä** = Selvä ero ryhmien välillä
    
    **Johtopäätös:**
    Vaikka miesparien otoskoko on pienempi, ero naispareihin on niin selvä, että 
    voimme luottavaisin mielin sanoa että todellinen ero on olemassa.
    """)

# ============================================================================
# TAB 3: Academic vs Journalistic
# ============================================================================
with tab3:
    st.subheader("Akateeminen Julkaisu vs. Journalistinen Artikkeli")
    
    st.markdown("""
    **Tämä osio selittää:**
    - Mitä eroa on journalistisella ja akateemisella analyysillä
    - Mitä TÄMÄ analyysi on (ja mitä se ei ole)
    - Mitä tarvittaisiin tieteelliseen julkaisuun
    """)
    
    # Comparison table
    comparison = pd.DataFrame({
        'Kriteeri': [
            'Yleisö',
            'Datan taso',
            'Tilastolliset testit',
            'Luottamusvälit',
            'Survival analysis',
            'Kovariattien kontrollointi',
            'Seuranta-aika',
            'Peer review',
            'Rajoitusten maininta',
            'Yksinkertaisuus',
            'Lähdekoodin julkaisu',
            'Toistettavuus'
        ],
        'Journalistinen (TÄMÄ)': [
            '✅ Suuri yleisö',
            '✅ Aggregoitu data',
            '✅ Perustestit',
            '✅ Kyllä (tässä versiossa)',
            '❌ Ei',
            '❌ Ei',
            '⚠️ 7-8 vuotta (rajoite)',
            '❌ Ei tarvita',
            '✅ Kyllä, selkeästi',
            '✅ Yksinkertainen',
            '✅ GitHub (public)',
            '✅ Täysin toistettava'
        ],
        'Akateeminen Julkaisu': [
            '🎓 Tutkijat',
            '📊 Yksilödata (luvanvarainen)',
            '✅ Edistyneet testit',
            '✅ Pakollinen',
            '✅ Pakollinen (Kaplan-Meier)',
            '✅ Pakollinen (ikä, koulutus...)',
            '✅ 20-30 vuotta (suositus)',
            '✅ Pakollinen',
            '✅ Yksityiskohtaisesti',
            '⚠️ Monimutkainen',
            '✅ Supplementary materials',
            '✅ Täysin toistettava'
        ]
    })
    
    st.dataframe(comparison, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # What's missing
    st.markdown("### 🔍 Mitä Puuttuu Akateemiseen Julkaisuun?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **1. Survival Analysis (Eloonjäämisanalyysi)** ⭐⭐⭐
        
        *Mitä se on?*
        - Analysoi AIKAA avioeron tapahtumiseen
        - Huomioi "censored data" (avioliitot jotka eivät ole vielä päättyneet)
        - Kaplan-Meier käyrät
        
        *Mitä se vaatii?*
        - Yksilötason data
        - Jokaisen avioliiton solmimispäivä
        - Mahdollinen eropäivä
        
        *Esimerkki tuloksesta:*
        > "5 vuoden kohdalla 92% samaa sukupuolta olevien avioliitoista 
        > on edelleen voimassa (95% CI: 89-95%)"
        """)
        
        st.markdown("""
        **2. Cox Proportional Hazards Model**
        
        *Mitä se on?*
        - Regressiomalli joka kontrolloi sekoittavia tekijöitä
        - Antaa "adjusted hazard ratios"
        
        *Mitä se vaatii?*
        - Sama kuin survival analysis
        - PLUS: Kovariaarit (ikä, koulutus, tulot, lapset, alue)
        
        *Esimerkki tuloksesta:*
        > "Kontrolloituna iälle ja koulutukselle, naisparilla on 1.4x 
        > suurempi eroriski (95% CI: 1.2-1.7, p<0.001)"
        """)
    
    with col2:
        st.markdown("""
        **3. Pidempi Seuranta-aika**
        
        *Ongelma nyt:*
        - Vain 7-8 vuotta dataa samaa sukupuolta olevista
        - Monet avioerot tapahtuvat 10-20 vuoden aikana
        
        *Ratkaisu:*
        - Odottaa 15-20 vuotta lisää
        - TAI vertailla Ruotsiin/Norjaan (heillä pidempi data)
        
        *Miksi tärkeää?*
        - Eroaste kasvaa ajan myötä
        - Nykyinen 19% tulee varmasti kasvamaan
        """)
        
        st.markdown("""
        **4. Laajemmat Selittävät Muuttujat**
        
        *Mitä tarvittaisiin:*
        - Ikä avioliiton solmiessa
        - Koulutustaso
        - Tulotaso
        - Lasten määrä
        - Maantieteellinen sijainti
        - Aiemmat avioliitot
        
        *Miksi tärkeää?*
        - Voi selittää osaa eroista
        - Esim: Naispareiden suurempi eroaste voi johtua iästä tai 
          siitä että heillä on useammin lapsia edellisistä suhteista
        """)
    
    st.markdown("---")
    
    # What IS valid
    st.markdown("### ✅ Mitä Nykyinen Analyysi ON ja VOIDAAN sanoa")
    
    st.success("""
    **Tämä analyysi on:**
    
    1. **Metodologisesti pätevä perustasolla**
       - Oikeat tilastolliset menetelmät
       - Luottamusvälit laskettu (Wilson score)
       - Merkitsevyys testattu (Fisher's exact test)
       - Bayesilainen lähestymistapa huomioi otoskoon
    
    2. **Rehellinen rajoitustensa suhteen**
       - Aika-ongelma tunnistettu ja selitetty
       - Ei väitetä enempää kuin data sallii
       - Epävarmuus kvantifioitu (luottamusvälit)
    
    3. **Riittävä journalistiseen käyttöön**
       - Vastaa yleisön kysymyksiin
       - Ymmärrettävä ilman tilastotieteellistä koulutusta
       - Toistettava (koodi GitHubissa)
    
    4. **Opetustarkoituksellinen**
       - Näyttää oikeat menetelmät
       - Selittää rajoitukset
       - Opettaa tilastollista ajattelua
    
    **Voimme luottavaisin mielin sanoa:**
    - ✅ "Naisparit eroavat useammin kuin miesparit (21% vs 14%, p<0.001)"
    - ✅ "Ero on tilastollisesti merkitsevä"
    - ✅ "Vuosina 2017-2024 solmituista samaa sukupuolta olevien avioliitoista 18.6% on päättynyt eroon"
    - ✅ "Eroaste on kasvussa ajan myötä (odotettu)"
    
    **Emme voi sanoa:**
    - ❌ "Samaa sukupuolta olevat eroavat harvemmin kuin heteroparit" (aika-ongelma!)
    - ❌ "Ero johtuu sukupuolesta" (ei kontrolloitu muita tekijöitä)
    - ❌ "Lopullinen eroaste tulee olemaan 19%" (vielä liian aikaista)
    """)

# ============================================================================
# TAB 4: Data Availability
# ============================================================================
with tab4:
    st.subheader("Puuttuvan Datan Hankkiminen")
    
    st.markdown("""
    **Keskeiset kysymykset:**
    1. Onko yksilötason dataa saatavilla?
    2. Miten sitä voi hakea?
    3. Kuinka kauan se kestää?
    4. Mitä se maksaa?
    """)
    
    st.markdown("---")
    
    st.markdown("### 🗄️ Datan Saatavuus")
    
    tab_a, tab_b, tab_c = st.tabs([
        "📋 Tilastokeskuksen Mikrodata",
        "🌍 Pohjoismaiset Rekisterit",
        "💡 Käytännön Neuvot"
    ])
    
    with tab_a:
        st.markdown("""
        #### Tilastokeskuksen Tutkijakäyttö
        
        **Mitä dataa on saatavilla:**
        
        Tilastokeskuksella on yksilötason data avioliitoista ja avioeroista:
        - ✅ Jokaisen avioliiton solmimispäivä
        - ✅ Mahdollinen eropäivä
        - ✅ Puolisoiden sukupuoli
        - ✅ Ikä
        - ✅ Koulutus
        - ✅ Tulot
        - ✅ Asuinpaikka
        - ✅ Lasten määrä
        - ❌ Nimet (pseudonymisoitu)
        
        **Miten hakea:**
        
        1. **Tutkimussuunnitelma**
           - Kirjoita yksityiskohtainen suunnitelma
           - Perustele miksi tarvitset yksilödataa
           - Selitä tutkimuskysymykset ja menetelmät
        
        2. **Eettinen lupa**
           - Yliopiston eettinen toimikunta TAI
           - Tutkimuseettinen neuvottelukunta
        
        3. **Hakemus Tilastokeskukselle**
           - Täytä lomake: https://www.stat.fi/tup/mikroaineistot/index.html
           - Liitä tutkimussuunnitelma
           - Liitä eettinen lupa
        
        4. **Sopimus ja Käyttölupa**
           - Tilastokeskus arvioi hakemuksen
           - Allekirjoita käyttösopimus
           - Maksa käyttömaksu
        
        5. **Datan käyttö**
           - Turvatussa etäkäyttöympäristössä (FIONA)
           - EI saa ladata paikallisesti
           - Vain aggregoidut tulokset ulos
        """)
        
        st.info("""
        **Aikataulu:**
        - Tutkimussuunnitelma: 1-2 kuukautta
        - Eettinen lupa: 1-3 kuukautta
        - Tilastokeskuksen käsittely: 1-2 kuukautta
        - **Yhteensä: 3-7 kuukautta**
        
        **Kustannukset:**
        - Eettinen lupa: 0-500 € (riippuu instansista)
        - Tilastokeskuksen maksu: ~500-2,000 € per vuosi
        - Tutkijan palkka: 30,000-50,000 € per vuosi
        - **Yhteensä projekti: 40,000-100,000 € (2-3 vuotta)**
        """)
    
    with tab_b:
        st.markdown("""
        #### Pohjoismaiset Väestörekisterit
        
        **Miksi Pohjoismaat?**
        
        Ruotsi, Norja, Tanska ja Islanti ovat PARHAAT paikat tutkia avioeroja:
        - 🇸🇪 **Ruotsi:** Samaa sukupuolta olevien avioliitot laillistettu 2009
        - 🇳🇴 **Norja:** Laillistettu 2009
        - 🇩🇰 **Tanska:** Laillistettu 2012 (rekisteröidyt parisuhteet 1989!)
        - 🇮🇸 **Islanti:** Laillistettu 2010
        
        **Etuja:**
        - ✅ **Pidempi aikasarja** (15-35 vuotta)
        - ✅ **Laajempi data** (useampia muuttujia)
        - ✅ **Kattavat rekisterit** (100% väestöstä)
        - ✅ **Linkitettävyys** (voidaan yhdistää muihin rekistereihin)
        
        **Erityisesti Tanska:**
        
        Tanska on KULTAKAIVOS avioerotutkimukselle:
        - Rekisteröidyt parisuhteet samaa sukupuolta olevilla 1989 lähtien
        - 35 vuotta dataa!
        - Kattavat väestörekisterit
        - Aktiivinen tutkijayhteisö
        
        **Miten hakea:**
        
        1. **Tutkija-affiliaatio**
           - Tarvitset yhteyden pohjoismaiseen yliopistoon
           - TAI kansainvälinen yhteistyö
        
        2. **Statistics Denmark / Statistics Sweden**
           - Hae datan käyttölupaa
           - Prosessi samanlainen kuin Suomessa
        
        3. **Nordic Register Data Project**
           - Jos haluat dataa useasta maasta
           - Vaatii laajan tutkimussuunnitelman
        
        **Julkaistua tutkimusta Pohj osmaista:**
        
        - Andersson et al. (2006): Ruotsi
        - Wiik et al. (2014): Norja
        - Biblarz & Stacey (2010): Meta-analyysi
        """)
        
        st.success("""
        **Suositus akateemiseen tutkimukseen:**
        
        Jos haluat tehdä OIKEAN akateemisen tutkimuksen, suosittelen:
        
        1. **Yhteistyö Tanskan kanssa**
           - Pisin aikasarja (1989-)
           - Parhaat rekisterit
           - Aktiivinen tutkijayhteisö
        
        2. **Pohjoismainen vertailu**
        - Yhdistä Suomi + Ruotsi + Norja + Tanska
           - Suurempi otoskoko
           - Kulttuurinen vertailu
        
        3. **3 vuoden projekti**
           - Vuosi 1: Lupien haku
           - Vuosi 2: Analyysi
           - Vuosi 3: Kirjoittaminen ja julkaisu
        """)
    
    with tab_c:
        st.markdown("""
        #### Käytännön Neuvot

        **Jos haluat tehdä tämän OIKEIN (akateeminen tutkimus):**

        **Vaihtoehto 1: Itse (VAIKEA)**
        
        ✅ Edellytykset:
        - Tilastotieteen peruskurssit (tai parempi)
        - R tai Python osaaminen
        - Survival analysis koulutus
        - Aikaa 2-3 vuotta
        - Budjetti 40,000-100,000 €
        
        📝 Prosessi:
        1. Kirjoita tutkimussuunnitelma
        2. Hae eettinen lupa
        3. Hae data Tilastokeskukselta
        4. Analysoi (6-12 kuukautta)
        5. Kirjoita artikkeli
        6. Julkaise (peer review 6-12 kuukautta)
        
        ---
        
        **Vaihtoehto 2: Yhteistyö Yliopiston kanssa (SUOSITUS)**
        
        ✅ Ota yhteyttä:
        - Helsingin yliopisto, Sosiologia
        - Turun yliopisto, Sosiologia
        - Väestöliitto
        - Kansaneläkelaitos (Kela)
        
        💡 Ehdota:
        - Pro gradu -aihe opiskelijalle
        - Väitöskirjatutkimus
        - Yhteisartikkeli
        
        ⏱️ Aikataulu:
        - Pro gradu: 1-2 vuotta
        - Väitöskirja: 3-5 vuotta
        
        💰 Kustannus:
        - Sinulle: 0 € (yliopisto maksaa)
        - Saat: Co-authorship artikkeliin
        
        ---
        
        **Vaihtoehto 3: Pohjoismaiset Tutkijat (NOPEIN)**
        
        ✅ Ota yhteyttä:
        - **Tanska:** Statistics Denmark, Demografia-osasto
        - **Ruotsi:** Stockholm University, Demography Unit
        - **Norja:** Statistics Norway
        
        💡 Kysymykset:
        1. "Onko teillä julkaisemattomia tuloksia samaa sukupuolta olevien 
           parien avioeroista?"
        2. "Voisimmeko tehdä yhteistyötä - journalistinen artikkeli + 
           tieteellinen julkaisu?"
        
        ⏱️ Aikataulu:
        - Jos data on jo analysoitu: 3-6 kuukautta
        - Jos ei: 1-2 vuotta
        
        💰 Kustannus:
        - Heille: Tutkimusaika
        - Sinulle: Co-authorship + journalistinen julkaisu
        
        ---
        
        **Vaihtoehto 4: Käytä Nykyistä Analyysiä (REALISTINEN)**
        
        ✅ Miksi tämä on OK:
        - Tilastollisesti pätevä perustasolla
        - Rajoitukset selkeästi mainittu
        - Riittävä journalistiseen käyttöön
        - VOIT lisätä: "Tilastollisesti merkitsevä ero (p<0.001)"
        
        💡 Lisää artikkeliin:
        - Mainitse että survival analysis olisi parempi
        - Linkki tähän Streamlit-appiin (näyttää osaamista!)
        - "Tarvittaisiin pidempi seuranta-aika täydelliseen vertailuun"
        
        ⏱️ Aikataulu:
        - Valmis NYT! ✅
        
        💰 Kustannus:
        - 0 €
        """)
    
    st.markdown("---")
    
    st.markdown("### 📊 Yhteenveto: Datan Saatavuus")
    
    availability_summary = pd.DataFrame({
        'Data tyyppi': [
            'Aggregoitu data (nykyinen)',
            'Yksilödata (Suomi, survival)',
            'Yksilödata (Pohjoismaat)',
            'Kansainvälinen vertailu'
        ],
        'Saatavuus': [
            '✅ Julkinen, ilmainen',
            '🟡 Luvanvarainen, maksullinen',
            '🟡 Luvanvarainen, yhteistyö',
            '🟠 Monimutkainen, pitkä prosessi'
        ],
        'Aika': [
            'Heti',
            '3-7 kuukautta (luvat)',
            '6-12 kuukautta',
            '1-2 vuotta'
        ],
        'Kustannus': [
            '0 €',
            '500-2,000 € + tutkijan aika',
            '0 € (yliopiston kautta)',
            '50,000-100,000 € (projekti)'
        ],
        'Käyttötarkoitus': [
            'Journalismi, yleistajuinen',
            'Akateeminen tutkimus',
            'Akateeminen tutkimus',
            'Väitöskirja, tutkimushanke'
        ]
    })
    
    st.dataframe(availability_summary, use_container_width=True, hide_index=True)
    
    st.info("""
    **Realistinen arvio journalisteille:**

    **Nykyinen analyysi on:**
    - ✅ Riittävä journalistiseen artikkeliin
    - ✅ Tilastollisesti pätevä perustasolla
    - ✅ Rehellinen rajoitustensa suhteen
    - ✅ Valmis käyttöön NYT
    
    **Jos haluaa PAREMMAN analyysin:**
    - Ota yhteyttä Helsingin yliopiston sosiologian laitokseen
    - Ehdota pro gradu -aihetta opiskelijalle
    - TAI yhteistyötä Tanskan Statistics Denmarkin kanssa (heillä 35v dataa!)
    
    **Mutta:**
    - Tämä vie 1-3 vuotta
    - Jos artikkeli on ajankohtainen NYT, käytä nykyistä analyysiä
    - Se on rehellinen, pätevä, ja selittää rajoitukset
    """)

# Sidebar
with st.sidebar:
    st.header("Tietoja")

    st.markdown("""
    ### 📚 Sanasto (selkokieli)

    **Tärkeimmät termit ymmärrettävästi:**

    - **Eroaste**: Kuinka monesta 2017–2024 solmitusta avioliitosta on jo tullut ero.

    - **Kumulatiivinen**: "Kasautunyt" - lasketaan yhteen kaikki tapahtumat vuodesta 2017 alkaen.

    - **Tilastollisesti merkitsevä**: Ero ei johdu sattumasta, vaan on todellinen.

    - **Riskisuhde (RR)**: Kuinka monta kertaa suurempi todennäköisyys eroon ryhmässä A kuin B.

    - **p-arvo**: Mitä pienempi, sen varmempi että ero on todellinen (alle 0.05 = merkitsevä).

    - **Survival-analyysi**: Menetelmä joka seuraa tapahtumia ajan kuluessa (tarvitaan lopulliseen eroasteeseen).
    """)

    st.divider()

    st.markdown("""
    ### 📌 Projektin tarkoitus
    Tämä analyysi on tehty artikkelikäyttöön vertailemaan samaa sukupuolta
    ja eri sukupuolta olevien parien avioeroja Suomessa.
    
    ### 📅 Ajanjakso
    2017-2024 (samaa sukupuolta olevien avioliitot laillistettiin 3/2017)
    
    ### 🔍 Metodologia
    - Kumulatiivinen eroaste = Avioerojen kokonaismäärä / Avioliittojen kokonaismäärä
    - Kaikki luvut laskettu vuodesta 2017 alkaen
    
    ### ⚠️ Rajoitukset
    - Samaa sukupuolta: vain 7-8 vuoden data
    - Eri sukupuolta: mukana vuosikymmeniä vanhoja avioliittoja
    - Suora vertailu ei ole täysin oikeudenmukainen
    """)
    
    st.divider()
    
    st.markdown("""
    ### 📊 Lataa data
    """)
    
    # Download data
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Lataa CSV",
        data=csv,
        file_name="avioerot_2017_2024.csv",
        mime="text/csv",
    )
