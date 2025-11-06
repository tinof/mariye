#!/usr/bin/env python3
"""
Streamlit Web App: Finnish Marriage and Divorce Statistics (2017-2024)
Author: Analysis for Marios's article

Deploy to: streamlit.io (free)
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

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

