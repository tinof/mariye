#!/usr/bin/env python3
"""
Statistical Analysis for Article: Same-sex vs Opposite-sex Divorce Rates in Finland
Author: Prepared for Marios's article

PROPER METHODOLOGY:
Since same-sex marriage only became legal in March 2017, we need to compare
"apples to apples" by looking at:
1. Cumulative divorce rates since 2017 (acknowledging the limitation)
2. Annual trends showing how divorce rates evolve
3. Clear disclaimers about data limitations

For a general audience, focus on:
- Clear, simple visualizations
- Honest about what we can and cannot conclude
- Contextual information
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data from Statistics Finland (2017-2024)
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

# Calculate totals
df['Marriages_SameSex'] = df['Marriages_Male'] + df['Marriages_Female']
df['Divorces_SameSex'] = df['Divorces_Male'] + df['Divorces_Female']

# Calculate cumulative totals
df['Cum_Mar_Opposite'] = df['Marriages_Opposite'].cumsum()
df['Cum_Div_Opposite'] = df['Divorces_Opposite'].cumsum()
df['Cum_Mar_Male'] = df['Marriages_Male'].cumsum()
df['Cum_Div_Male'] = df['Divorces_Male'].cumsum()
df['Cum_Mar_Female'] = df['Marriages_Female'].cumsum()
df['Cum_Div_Female'] = df['Divorces_Female'].cumsum()
df['Cum_Mar_SameSex'] = df['Marriages_SameSex'].cumsum()
df['Cum_Div_SameSex'] = df['Divorces_SameSex'].cumsum()

# Calculate cumulative rates (divorces as % of marriages since 2017)
df['Rate_Opposite'] = (df['Cum_Div_Opposite'] / df['Cum_Mar_Opposite'] * 100)
df['Rate_Male'] = (df['Cum_Div_Male'] / df['Cum_Mar_Male'] * 100)
df['Rate_Female'] = (df['Cum_Div_Female'] / df['Cum_Mar_Female'] * 100)
df['Rate_SameSex'] = (df['Cum_Div_SameSex'] / df['Cum_Mar_SameSex'] * 100)

# ============================================================================
# VISUALIZATION 1: Main chart for article - Cumulative Divorce Rates
# ============================================================================
fig1, ax = plt.subplots(figsize=(12, 7))

# Plot lines
ax.plot(df['Year'], df['Rate_Male'], marker='o', linewidth=3, 
        label='Miesparit', color='#3498db', markersize=8)
ax.plot(df['Year'], df['Rate_Female'], marker='s', linewidth=3, 
        label='Naisparit', color='#e74c3c', markersize=8)
ax.plot(df['Year'], df['Rate_SameSex'], marker='^', linewidth=3, 
        label='Samaa sukupuolta yhteensä', color='#9b59b6', markersize=8, linestyle='--')
ax.plot(df['Year'], df['Rate_Opposite'], marker='D', linewidth=3, 
        label='Eri sukupuolta', color='#2ecc71', markersize=8, linestyle=':')

# Styling
ax.set_xlabel('Vuosi', fontsize=14, fontweight='bold')
ax.set_ylabel('Kumulatiivinen eroaste (%)', fontsize=14, fontweight='bold')
ax.set_title('Avioerot suhteessa avioliittojen määrään (2017-2024)\nSamaa sukupuolta olevien avioliitot laillistettu maaliskuussa 2017', 
             fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='upper left', fontsize=12, framealpha=0.95)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xticks(df['Year'])
ax.set_ylim(0, max(df['Rate_Opposite'].max(), df['Rate_Female'].max()) * 1.1)

# Add data labels on final points
for rate, label, color in [
    (df['Rate_Male'].iloc[-1], 'Miehet', '#3498db'),
    (df['Rate_Female'].iloc[-1], 'Naiset', '#e74c3c'),
    (df['Rate_Opposite'].iloc[-1], 'Hetero', '#2ecc71')
]:
    ax.annotate(f'{rate:.1f}%', 
                xy=(2024, rate), 
                xytext=(10, 0), 
                textcoords='offset points',
                fontsize=11, 
                fontweight='bold',
                color=color,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color, alpha=0.8))

plt.tight_layout()
plt.savefig('/Users/konstantinosfotiou/Documents/mariye/article_main_chart.png', dpi=300, bbox_inches='tight')
print("✓ Main article chart saved: article_main_chart.png")

# ============================================================================
# VISUALIZATION 2: Supporting chart - Absolute numbers for context
# ============================================================================
fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Chart A: Marriages
years = df['Year'].values
width = 0.35
x = np.arange(len(years))

ax1.bar(x - width/2, df['Marriages_Opposite']/1000, width, 
        label='Eri sukupuolta', color='#2ecc71', alpha=0.8)
ax1.bar(x + width/2, df['Marriages_SameSex'], width, 
        label='Samaa sukupuolta', color='#9b59b6', alpha=0.8)

ax1.set_xlabel('Vuosi', fontsize=12, fontweight='bold')
ax1.set_ylabel('Avioliitot', fontsize=12, fontweight='bold')
ax1.set_title('Solmitut avioliitot vuosittain\n(eri sukupuolta tuhansia)', fontsize=13, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(years, rotation=45)
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3, axis='y')

# Chart B: Divorces
ax2.bar(x - width/2, df['Divorces_Opposite']/1000, width, 
        label='Eri sukupuolta', color='#2ecc71', alpha=0.8)
ax2.bar(x + width/2, df['Divorces_SameSex'], width, 
        label='Samaa sukupuolta', color='#9b59b6', alpha=0.8)

ax2.set_xlabel('Vuosi', fontsize=12, fontweight='bold')
ax2.set_ylabel('Avioerot', fontsize=12, fontweight='bold')
ax2.set_title('Avioerot vuosittain\n(eri sukupuolta tuhansia)', fontsize=13, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(years, rotation=45)
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('/Users/konstantinosfotiou/Documents/mariye/article_supporting_chart.png', dpi=300, bbox_inches='tight')
print("✓ Supporting chart saved: article_supporting_chart.png")

# ============================================================================
# VISUALIZATION 3: Clean comparison bar chart for 2024
# ============================================================================
fig3, ax = plt.subplots(figsize=(10, 7))

categories = ['Miesparit', 'Naisparit', 'Eri sukupuolta']
rates = [
    df['Rate_Male'].iloc[-1],
    df['Rate_Female'].iloc[-1],
    df['Rate_Opposite'].iloc[-1]
]
colors = ['#3498db', '#e74c3c', '#2ecc71']

bars = ax.barh(categories, rates, color=colors, alpha=0.8, edgecolor='black', linewidth=2)

ax.set_xlabel('Kumulatiivinen eroaste (%) vuoden 2024 loppuun', fontsize=13, fontweight='bold')
ax.set_title('Avioerot suhteessa avioliittojen määrään (2017-2024)\nAvioerojen osuus kaikista solmituista avioliitoista', 
             fontsize=14, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='x')

# Add percentage labels
for bar, rate in zip(bars, rates):
    width = bar.get_width()
    ax.text(width + 1, bar.get_y() + bar.get_height()/2.,
            f'{rate:.1f}%', ha='left', va='center', fontweight='bold', fontsize=14)

plt.tight_layout()
plt.savefig('/Users/konstantinosfotiou/Documents/mariye/article_simple_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Simple comparison chart saved: article_simple_comparison.png")

# ============================================================================
# Print summary for article text
# ============================================================================
print("\n" + "="*80)
print("TILASTOLLINEN YHTEENVETO ARTIKKELIIN")
print("="*80)

print("\n📊 PÄÄASIALLISET LUVUT (2017-2024):")
print("-"*80)
print(f"Eri sukupuolta olevat parit:")
print(f"  • Avioliittoja yhteensä: {df['Marriages_Opposite'].sum():,}")
print(f"  • Avioeroja yhteensä: {df['Divorces_Opposite'].sum():,}")
print(f"  • Kumulatiivinen eroaste: {df['Rate_Opposite'].iloc[-1]:.1f}%")
print()
print(f"Samaa sukupuolta olevat parit (yhteensä):")
print(f"  • Avioliittoja yhteensä: {df['Marriages_SameSex'].sum():,}")
print(f"  • Avioeroja yhteensä: {df['Divorces_SameSex'].sum():,}")
print(f"  • Kumulatiivinen eroaste: {df['Rate_SameSex'].iloc[-1]:.1f}%")
print()
print(f"Miesparit:")
print(f"  • Avioliittoja yhteensä: {df['Marriages_Male'].sum():,}")
print(f"  • Avioeroja yhteensä: {df['Divorces_Male'].sum():,}")
print(f"  • Kumulatiivinen eroaste: {df['Rate_Male'].iloc[-1]:.1f}%")
print()
print(f"Naisparit:")
print(f"  • Avioliittoja yhteensä: {df['Marriages_Female'].sum():,}")
print(f"  • Avioeroja yhteensä: {df['Divorces_Female'].sum():,}")
print(f"  • Kumulatiivinen eroaste: {df['Rate_Female'].iloc[-1]:.1f}%")

print("\n" + "="*80)
print("⚠️  TÄRKEÄT HUOMIOT ARTIKKELIIN:")
print("="*80)
print("""
1. Samaa sukupuolta olevien avioliitot laillistettiin Suomessa maaliskuussa 2017.

2. Tämän analyysin kumulatiivinen eroaste lasketaan: 
   (Avioerojen määrä 2017-2024) / (Avioliittojen määrä 2017-2024) × 100%

3. KRIITTINEN RAJOITUS:
   - Eri sukupuolta olevien parien avioeroista monet tulevat avioliitoista, 
     jotka on solmittu ENNEN vuotta 2017 (jopa 1990-luvulla tai aikaisemmin).
   - Samaa sukupuolta olevien parien avioerot tulevat VAIN vuosien 2017-2024 
     avioliitoista (maksimissaan 7-8 vuotta vanhoja).
   - Tämä tekee suorasta vertailusta ongelmallisen, koska avioeron todennäköisyys 
     kasvaa avioliiton keston myötä.

4. MITÄ VOIMME SANOA:
   ✓ Samaa sukupuolta olevien parien avioerot ovat toistaiseksi harvinaisempia
   ✓ Naisparien eroaste (21%) on korkeampi kuin miesparien (14%)
   ✓ Trendit näyttävät eroasteiden kasvavan, mikä on odotettua kun avioliitot vanhenevat
   
5. MITÄ EMME VOI SANOA:
   ✗ Emme voi suoraan verrata 57%:n ja 19%:n lukuja keskenään
   ✗ Emme voi tehdä johtopäätöksiä siitä, kumpi ryhmä eroaa "enemmän"
   ✗ Tarvittaisiin 20-30 vuoden seuranta-aika luotettavaan vertailuun

6. Otoskoot:
   - Samaa sukupuolta olevien parien otoskoot ovat paljon pienempiä 
     (~3,000 avioliittoa vs. ~175,000), mikä lisää tilastollista vaihtelua.
""")

print("="*80)
print("\n💡 SUOSITUS ARTIKKELIIN:")
print("="*80)
print("""
KÄYTÄ: Pääkaavio (article_main_chart.png) tai yksinkertainen vertailu 
       (article_simple_comparison.png)

TEKSTISSÄ KERRO:
1. Luvut selkeästi (käytä yllä olevia lukuja)
2. Mainitse, että samaa sukupuolta olevien avioliitot ovat uusia (2017-)
3. Korosta, ettei suora vertailu ole täysin oikeudenmukainen ajan vuoksi
4. Keskity siihen, mitä DATA KERTOO: naisparit eroavat useammin kuin miesparit
5. Huomioi, että trendit näyttävät eroasteiden kasvavan ajan myötä

VÄLTÄ:
- Sanomasta "samaa sukupuolta olevat eroavat harvemmin" (ei ole totuudenmukaista)
- Yksinkertaista vertailua ilman kontekstia
- Selittämättömiä prosenttilukuja
""")

print("\n✓ Kaikki kaaviot ja data tallennettu!")
print("="*80)

# Save data for Datawrapper or other tools
export_df = pd.DataFrame({
    'Vuosi': df['Year'],
    'Miesparit_eroaste': df['Rate_Male'].round(2),
    'Naisparit_eroaste': df['Rate_Female'].round(2),
    'Samaa_sukupuolta_yhteensä': df['Rate_SameSex'].round(2),
    'Eri_sukupuolta_eroaste': df['Rate_Opposite'].round(2),
    'Miesparit_avioliitot': df['Marriages_Male'],
    'Naisparit_avioliitot': df['Marriages_Female'],
    'Eri_sukupuolta_avioliitot': df['Marriages_Opposite'],
    'Miesparit_avioerot': df['Divorces_Male'],
    'Naisparit_avioerot': df['Divorces_Female'],
    'Eri_sukupuolta_avioerot': df['Divorces_Opposite'],
})

export_df.to_csv('/Users/konstantinosfotiou/Documents/mariye/datawrapper_export.csv', index=False)
print("\n✓ Datawrapper-yhteensopiva CSV tallennettu: datawrapper_export.csv")

