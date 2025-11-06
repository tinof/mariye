# 💍 Finnish Marriage & Divorce Statistics Analysis (2017-2024)

Statistical analysis comparing same-sex and opposite-sex marriage divorce rates in Finland.

## 🌐 Live Demo

**Deploy this app online:** See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

**Test locally:**
```bash
streamlit run app.py
```

## 📊 What This Project Contains

### Files:

1. **`app.py`** - Interactive Streamlit web application
   - Interactive charts with Plotly
   - Statistical summaries
   - Data export functionality

2. **`api.md`** - Documentation for Statistics Finland PxWeb API
   - How to fetch data from Tilastokeskus
   - API usage examples

3. **`OHJE_MARIOKSELLE.md`** - Guide for article writing (Finnish)
   - Statistical methodology explanation
   - What claims are valid vs misleading
   - Example text for articles

4. **`DEPLOYMENT_GUIDE.md`** - How to deploy this app online
   - Streamlit Cloud (recommended)
   - GitHub Pages (static alternative)

5. **Generated files:**
   - `article_main_chart.png` - Main visualization for articles
   - `article_simple_comparison.png` - Simple bar chart comparison
   - `article_supporting_chart.png` - Supporting absolute numbers
   - `datawrapper_export.csv` - CSV for Datawrapper
   - `divorce_analysis_detailed.csv` - Full analysis data

### Python Scripts:

- **`divorce_analysis.py`** - Initial statistical analysis (generates charts)
- **`article_analysis.py`** - Article-focused analysis with Finnish labels

## 📈 Key Findings

**Data Period:** 2017-2024  
**Source:** [Statistics Finland (Tilastokeskus)](https://pxdata.stat.fi/PxWeb/pxweb/fi/StatFin/StatFin__ssaaty/statfin_ssaaty_pxt_121e.px/)

### Cumulative Divorce Rates (2017-2024):

| Couple Type | Marriages | Divorces | Divorce Rate |
|-------------|-----------|----------|--------------|
| **Female couples** | 2,251 | 472 | **21.0%** |
| **Male couples** | 1,057 | 144 | **13.6%** |
| **Same-sex (total)** | 3,308 | 616 | **18.6%** |
| **Opposite-sex** | 175,045 | 99,737 | **57.0%** |

### ⚠️ Important Statistical Note:

**Direct comparison is problematic:**
- Same-sex marriage was legalized in **March 2017**
- Same-sex divorces come from marriages max **7-8 years old**
- Opposite-sex divorces may come from marriages **30+ years old**
- Divorce probability **increases with marriage duration**

**Therefore:** The 57% vs 19% comparison is misleading!

## 🎯 Valid Conclusions

✅ **What we CAN say:**
1. Female same-sex couples divorce more than male same-sex couples (21% vs 14%)
2. Same-sex couple divorce rates are currently lower but growing (expected as marriages age)
3. Of same-sex marriages formed 2017-2024, 18.6% have ended in divorce

❌ **What we CANNOT say:**
1. ~~"Same-sex couples divorce less than opposite-sex couples"~~ - Not a fair comparison
2. Any conclusion comparing absolute rates without mentioning the time limitation

## 🚀 Quick Start

### 1. Run locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the web app
streamlit run app.py

# Or run the analysis scripts
python3 divorce_analysis.py
python3 article_analysis.py
```

### 2. Deploy online:

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

**Recommended:** Deploy to [Streamlit Cloud](https://share.streamlit.io/) (free)

## 📦 Requirements

```
streamlit==1.40.0
pandas==2.3.3
plotly==5.24.1
matplotlib==3.10.7  # For static charts
```

## 📚 Data Source

**Statistics Finland (Tilastokeskus)**  
Table: 121e - Changes in marital status, 1990-2024  
https://pxdata.stat.fi/PxWeb/pxweb/fi/StatFin/StatFin__ssaaty/statfin_ssaaty_pxt_121e.px/

**Last Updated:** April 24, 2025

## 🎨 Visualizations

The project generates multiple visualizations:

1. **Time series chart** - Shows how divorce rates evolve year by year
2. **Bar chart comparison** - Simple comparison of final rates
3. **Supporting charts** - Absolute numbers for context

All charts are available in both:
- Static PNG format (matplotlib)
- Interactive web format (plotly in Streamlit app)

## 📝 For Article Writers

See **`OHJE_MARIOKSELLE.md`** for:
- Detailed statistical methodology
- What to include in articles
- What to avoid (misleading claims)
- Example text snippets
- Chart selection guide

## 🤝 Contributing

This is an analytical project. To update:

1. Edit data in `app.py` (update the `data` dictionary)
2. Re-run analysis scripts
3. Regenerate charts
4. Deploy updated version

## 📄 License

Data: © Statistics Finland (Tilastokeskus)  
Analysis: Open for educational and journalistic use

## 📧 Contact

For questions about the analysis or methodology, refer to:
- [Statistics Finland](https://www.stat.fi)
- [PxWeb API Documentation](api.md)

---

**Note:** Same-sex marriage was legalized in Finland on March 1, 2017. This analysis covers the period from legalization through 2024.

