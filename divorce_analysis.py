#!/usr/bin/env python3
"""
Analysis of Marriage and Divorce Rates in Finland (2017-2024)
Comparing opposite-sex and same-sex couples

Data source: Statistics Finland (Tilastokeskus)
https://pxdata.stat.fi/PxWeb/pxweb/fi/StatFin/StatFin__ssaaty/statfin_ssaaty_pxt_121e.px/
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data from Statistics Finland (2017-2024)
# Note: Same-sex marriage was legalized in Finland in March 2017
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

# Calculate total same-sex marriages and divorces
df['Marriages_SameSex'] = df['Marriages_Male'] + df['Marriages_Female']
df['Divorces_SameSex'] = df['Divorces_Male'] + df['Divorces_Female']

# Calculate same-year divorce-to-marriage ratios (crude indicator)
# CAVEAT: Divorces come from previous years' marriages, so this is just a rough indicator
df['Ratio_Opposite'] = (df['Divorces_Opposite'] / df['Marriages_Opposite'] * 100)
df['Ratio_Male'] = (df['Divorces_Male'] / df['Marriages_Male'] * 100)
df['Ratio_Female'] = (df['Divorces_Female'] / df['Marriages_Female'] * 100)
df['Ratio_SameSex'] = (df['Divorces_SameSex'] / df['Marriages_SameSex'] * 100)

# Calculate cumulative totals (better for recent same-sex marriage data)
df['Cumulative_Marriages_Opposite'] = df['Marriages_Opposite'].cumsum()
df['Cumulative_Divorces_Opposite'] = df['Divorces_Opposite'].cumsum()
df['Cumulative_Marriages_SameSex'] = df['Marriages_SameSex'].cumsum()
df['Cumulative_Divorces_SameSex'] = df['Divorces_SameSex'].cumsum()
df['Cumulative_Marriages_Male'] = df['Marriages_Male'].cumsum()
df['Cumulative_Divorces_Male'] = df['Divorces_Male'].cumsum()
df['Cumulative_Marriages_Female'] = df['Marriages_Female'].cumsum()
df['Cumulative_Divorces_Female'] = df['Divorces_Female'].cumsum()

# Calculate cumulative divorce rates (divorces as % of total marriages since 2017)
df['Cumulative_Rate_Opposite'] = (df['Cumulative_Divorces_Opposite'] / df['Cumulative_Marriages_Opposite'] * 100)
df['Cumulative_Rate_SameSex'] = (df['Cumulative_Divorces_SameSex'] / df['Cumulative_Marriages_SameSex'] * 100)
df['Cumulative_Rate_Male'] = (df['Cumulative_Divorces_Male'] / df['Cumulative_Marriages_Male'] * 100)
df['Cumulative_Rate_Female'] = (df['Cumulative_Divorces_Female'] / df['Cumulative_Marriages_Female'] * 100)

# Print summary statistics
print("=" * 80)
print("MARRIAGE AND DIVORCE ANALYSIS IN FINLAND (2017-2024)")
print("=" * 80)
print("\n1. TOTAL COUNTS (2017-2024)")
print("-" * 80)
print(f"Opposite-sex couples:")
print(f"  Total Marriages: {df['Marriages_Opposite'].sum():,}")
print(f"  Total Divorces:  {df['Divorces_Opposite'].sum():,}")
print(f"\nSame-sex couples (combined):")
print(f"  Total Marriages: {df['Marriages_SameSex'].sum():,}")
print(f"  Total Divorces:  {df['Divorces_SameSex'].sum():,}")
print(f"\nMale couples:")
print(f"  Total Marriages: {df['Marriages_Male'].sum():,}")
print(f"  Total Divorces:  {df['Divorces_Male'].sum():,}")
print(f"\nFemale couples:")
print(f"  Total Marriages: {df['Marriages_Female'].sum():,}")
print(f"  Total Divorces:  {df['Divorces_Female'].sum():,}")

print("\n2. CUMULATIVE DIVORCE RATES (as of 2024)")
print("-" * 80)
print("(Divorces as % of total marriages since same-sex marriage legalization in 2017)")
print(f"\nOpposite-sex couples: {df['Cumulative_Rate_Opposite'].iloc[-1]:.2f}%")
print(f"Same-sex couples:     {df['Cumulative_Rate_SameSex'].iloc[-1]:.2f}%")
print(f"  Male couples:       {df['Cumulative_Rate_Male'].iloc[-1]:.2f}%")
print(f"  Female couples:     {df['Cumulative_Rate_Female'].iloc[-1]:.2f}%")

print("\n3. AVERAGE ANNUAL SAME-YEAR RATIO (2017-2024)")
print("-" * 80)
print("(CAUTION: This is a crude indicator as divorces come from previous years' marriages)")
print(f"\nOpposite-sex couples: {df['Ratio_Opposite'].mean():.2f}%")
print(f"Same-sex couples:     {df['Ratio_SameSex'].mean():.2f}%")
print(f"  Male couples:       {df['Ratio_Male'].mean():.2f}%")
print(f"  Female couples:     {df['Ratio_Female'].mean():.2f}%")

print("\n4. YEAR-BY-YEAR DATA")
print("-" * 80)
print(df[['Year', 'Marriages_Opposite', 'Divorces_Opposite', 'Ratio_Opposite', 
          'Marriages_SameSex', 'Divorces_SameSex', 'Ratio_SameSex']].to_string(index=False))

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Marriage and Divorce Analysis in Finland (2017-2024)\nSame-sex marriage legalized March 2017', 
             fontsize=16, fontweight='bold')

# Plot 1: Cumulative Divorce Rates Over Time
ax1 = axes[0, 0]
ax1.plot(df['Year'], df['Cumulative_Rate_Opposite'], marker='o', linewidth=2, 
         label='Opposite-sex couples', color='#2E86AB')
ax1.plot(df['Year'], df['Cumulative_Rate_SameSex'], marker='s', linewidth=2, 
         label='Same-sex couples (combined)', color='#A23B72')
ax1.plot(df['Year'], df['Cumulative_Rate_Male'], marker='^', linewidth=1.5, 
         label='Male couples', color='#F18F01', linestyle='--')
ax1.plot(df['Year'], df['Cumulative_Rate_Female'], marker='v', linewidth=1.5, 
         label='Female couples', color='#C73E1D', linestyle='--')
ax1.set_xlabel('Year', fontsize=11, fontweight='bold')
ax1.set_ylabel('Cumulative Divorce Rate (%)', fontsize=11, fontweight='bold')
ax1.set_title('Cumulative Divorce Rate\n(Divorces as % of all marriages since 2017)', 
              fontsize=12, fontweight='bold')
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)
ax1.set_xticks(df['Year'])

# Plot 2: Annual Marriages by Type
ax2 = axes[0, 1]
width = 0.25
x = np.arange(len(df['Year']))
ax2.bar(x - width, df['Marriages_Opposite']/1000, width, label='Opposite-sex', color='#2E86AB')
ax2.bar(x, df['Marriages_Male'], width, label='Male couples', color='#F18F01')
ax2.bar(x + width, df['Marriages_Female'], width, label='Female couples', color='#C73E1D')
ax2.set_xlabel('Year', fontsize=11, fontweight='bold')
ax2.set_ylabel('Number of Marriages', fontsize=11, fontweight='bold')
ax2.set_title('Annual Marriages by Couple Type\n(Opposite-sex in thousands)', 
              fontsize=12, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(df['Year'])
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')

# Plot 3: Annual Divorces by Type
ax3 = axes[1, 0]
ax3.bar(x - width, df['Divorces_Opposite']/1000, width, label='Opposite-sex', color='#2E86AB')
ax3.bar(x, df['Divorces_Male'], width, label='Male couples', color='#F18F01')
ax3.bar(x + width, df['Divorces_Female'], width, label='Female couples', color='#C73E1D')
ax3.set_xlabel('Year', fontsize=11, fontweight='bold')
ax3.set_ylabel('Number of Divorces', fontsize=11, fontweight='bold')
ax3.set_title('Annual Divorces by Couple Type\n(Opposite-sex in thousands)', 
              fontsize=12, fontweight='bold')
ax3.set_xticks(x)
ax3.set_xticklabels(df['Year'])
ax3.legend()
ax3.grid(True, alpha=0.3, axis='y')

# Plot 4: Comparison of Cumulative Rates (2024)
ax4 = axes[1, 1]
categories = ['Opposite-sex', 'Same-sex\n(combined)', 'Male\ncouples', 'Female\ncouples']
rates = [
    df['Cumulative_Rate_Opposite'].iloc[-1],
    df['Cumulative_Rate_SameSex'].iloc[-1],
    df['Cumulative_Rate_Male'].iloc[-1],
    df['Cumulative_Rate_Female'].iloc[-1]
]
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
bars = ax4.bar(categories, rates, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
ax4.set_ylabel('Cumulative Divorce Rate (%)', fontsize=11, fontweight='bold')
ax4.set_title('Cumulative Divorce Rates by Couple Type (2024)\n(Total divorces / Total marriages since 2017)', 
              fontsize=12, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bar, rate in zip(bars, rates):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
             f'{rate:.2f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)

plt.tight_layout()
plt.savefig('/Users/konstantinosfotiou/Documents/mariye/divorce_analysis.png', dpi=300, bbox_inches='tight')
print("\n" + "=" * 80)
print("Visualization saved as: divorce_analysis.png")
print("=" * 80)

# Save detailed data to CSV
df.to_csv('/Users/konstantinosfotiou/Documents/mariye/divorce_analysis_detailed.csv', index=False)
print("Detailed data saved as: divorce_analysis_detailed.csv")

# Create a summary table
summary = pd.DataFrame({
    'Couple Type': ['Opposite-sex', 'Same-sex (combined)', 'Male couples', 'Female couples'],
    'Total Marriages (2017-2024)': [
        df['Marriages_Opposite'].sum(),
        df['Marriages_SameSex'].sum(),
        df['Marriages_Male'].sum(),
        df['Marriages_Female'].sum()
    ],
    'Total Divorces (2017-2024)': [
        df['Divorces_Opposite'].sum(),
        df['Divorces_SameSex'].sum(),
        df['Divorces_Male'].sum(),
        df['Divorces_Female'].sum()
    ],
    'Cumulative Divorce Rate (%)': [
        df['Cumulative_Rate_Opposite'].iloc[-1],
        df['Cumulative_Rate_SameSex'].iloc[-1],
        df['Cumulative_Rate_Male'].iloc[-1],
        df['Cumulative_Rate_Female'].iloc[-1]
    ]
})

print("\n5. SUMMARY TABLE")
print("-" * 80)
print(summary.to_string(index=False))

print("\n" + "=" * 80)
print("IMPORTANT NOTES:")
print("=" * 80)
print("1. Same-sex marriage was legalized in Finland in March 2017")
print("2. The cumulative divorce rate is calculated as total divorces / total marriages")
print("   since 2017, which is appropriate for the newer same-sex marriage data")
print("3. For opposite-sex couples, this only covers 2017-2024, while many existing")
print("   marriages were formed before 2017, so the true rate would be different")
print("4. The data shows divorces in a given year come from marriages of all previous")
print("   years, not just that year's marriages")
print("5. Sample sizes for same-sex couples are much smaller, leading to higher")
print("   statistical variability")
print("=" * 80)

plt.show()

