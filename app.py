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

# Header
st.title("💍 Avioerot Suomessa 2017-2024")
st.markdown("### Vertailu: Samaa sukupuolta vs. eri sukupuolta olevat parit")

st.info("""
**Huomio:** Samaa sukupuolta olevien avioliitot laillistettiin Suomessa maaliskuussa 2017. 
Tämä tarkoittaa, että samaa sukupuolta olevien parien data kattaa vain 7-8 vuotta, 
kun taas eri sukupuolta olevien parien avioerot voivat tulla vuosikymmeniä vanhoista avioliitoista.
""")

# Key metrics
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
    st.metric(
        "Eri sukupuolta",
        f"{df['Rate_Opposite'].iloc[-1]:.1f}%",
        help="Avioerojen osuus 2017-2024 solmituista avioliitoista (huom: monet avioerot tulevat vanhemmista avioliitoista)"
    )

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
st.header("🔬 Tilastotieteilijän Kulmaukseen")

st.info("""
**Tämä osio on tarkoitettu:**
- Tilastotieteilijöille ja tutkijoille
- Mariokselle oppimateriaali tilastollisesta ajattelusta
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
    st.markdown("### 🧪 Tilastollinen Merkitsevyys: Naisparit vs Miesparit")
    
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
            "Odds Ratio",
            f"{1/odds_ratio:.2f}x",
            help="Naisparilla on tämän verran suurempi todennäköisyys erota"
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
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Cohen's h", f"{h:.3f}")
    
    with col2:
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
        
        **Jos Marios (tai joku muu) haluaa tehdä tämän OIKEIN:**
        
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
    **Realistinen arvio Mariokselle:**
    
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

