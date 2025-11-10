# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **statistical analysis project** examining Finnish marriage and divorce rates (2017-2024), specifically comparing same-sex and opposite-sex couples. The project includes:

- **Interactive Streamlit web application** (`app.py`) for data visualization and exploration
- **Statistical analysis scripts** for generating charts and performing statistical tests
- Data from Statistics Finland (Tilastokeskus) on marital status changes

**Critical Context**: Same-sex marriage was legalized in Finland in **March 2017**, which creates a fundamental time-horizon limitation when comparing same-sex and opposite-sex divorce rates. This limitation is central to the entire analysis.

## Development Commands

### Running the Application

```bash
# Run the interactive Streamlit app (primary interface)
streamlit run app.py

# The app will be available at http://localhost:8501
```

### Running Analysis Scripts

```bash
# Generate basic statistical analysis and charts
python3 divorce_analysis.py

# Generate article-focused analysis with Finnish labels
python3 article_analysis.py

# Generate advanced statistical analysis (confidence intervals, Bayesian analysis)
python3 advanced_statistical_analysis.py
```

### Environment Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Dependencies include:
# - streamlit (web app framework)
# - pandas (data manipulation)
# - plotly (interactive charts)
# - scipy (statistical tests)
# - numpy (numerical operations)
```

### Dev Container

This project includes a `.devcontainer/devcontainer.json` configuration that:
- Uses Python 3.11
- Auto-installs requirements
- Auto-starts Streamlit on port 8501
- Opens README.md and app.py by default

## Architecture & Code Structure

### Core Application (`app.py`)

**Multi-layered Structure**: The Streamlit app has two main sections:

1. **Public-Facing Section (lines 1-458)**:
   - Finnish language interface for general audience
   - Key metrics, interactive visualizations using Plotly
   - Cumulative divorce rate calculations
   - Critical disclaimers about data limitations
   - "Guided mode" helper to explain what different divorce rate metrics mean (lines 86-157)

2. **Advanced Statistical Section ("Tilastotieteilijän nurkkaus", lines 459-1255)**:
   - For statisticians and researchers
   - Four tabs covering:
     - Confidence intervals & significance testing (Wilson score intervals, Fisher's exact test)
     - Bayesian analysis (Beta posterior distributions)
     - Academic vs journalistic comparison
     - Data acquisition guidance

### Data Architecture

**In-app Data Structure** (`app.py` lines 25-33):
```python
data = {
    'Year': [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'Marriages_Opposite': [...],
    'Divorces_Opposite': [...],
    'Marriages_Male': [...],    # Male same-sex couples
    'Marriages_Female': [...],  # Female same-sex couples
    'Divorces_Male': [...],
    'Divorces_Female': [...]
}
```

**Computed Metrics** (lines 38-53):
- Cumulative totals since 2017
- Cumulative divorce rates = (Total divorces since 2017) / (Total marriages since 2017) × 100%
- Separate tracking for male couples, female couples, same-sex combined, and opposite-sex

### Statistical Methodology

**Key Calculation Pattern** (used throughout):
```python
# Cumulative approach (correct for this time-limited dataset)
df['Cum_Mar_Group'] = df['Marriages_Group'].cumsum()
df['Cum_Div_Group'] = df['Divorces_Group'].cumsum()
df['Rate_Group'] = (df['Cum_Div_Group'] / df['Cum_Mar_Group'] * 100)
```

**Why Not Simple Annual Ratios?**
- Annual divorce-to-marriage ratios (divorces/marriages in same year) are misleading
- Divorces in year X come from marriages in years X-1, X-2, ... X-30+
- For a dataset starting in 2017, cumulative rates are more appropriate

**Statistical Tests Implemented**:
- **Wilson Score Interval**: For confidence intervals on proportions (better than normal approximation for small samples) - `app.py:499-507`
- **Fisher's Exact Test**: For comparing male vs female same-sex divorce rates - `app.py:606-612`
- **Bayesian Posterior Distributions**: Using Beta priors for uncertainty quantification - `app.py:699-705`
- **Cohen's h**: Effect size measurement - `app.py:646-647`

### Analysis Scripts

**`divorce_analysis.py`**:
- Generates comprehensive visualizations (4-panel matplotlib charts)
- Outputs: `divorce_analysis.png`, `divorce_analysis_detailed.csv`
- Includes detailed statistical summaries to stdout

**`article_analysis.py`**:
- Finnish-language outputs for journalistic use
- Generates 3 charts optimized for articles: main cumulative chart, supporting absolute numbers, simple comparison bar chart
- Outputs: `article_main_chart.png`, `article_supporting_chart.png`, `article_simple_comparison.png`, `datawrapper_export.csv`

**`advanced_statistical_analysis.py`**:
- Deep statistical analysis with confidence intervals, Bayesian estimates, power analysis
- Educational/methodological focus
- Outputs: `advanced_statistical_analysis.png`

### Critical Data Limitation Pattern

**This pattern appears throughout the codebase** and must be preserved:

```python
# The "hetero indicator" problem (app.py:160-211)
# 57% figure for opposite-sex couples is MISLEADING because:
# - Numerator (divorces 2017-2024) includes divorces from marriages formed in 1990s-2010s
# - Denominator (marriages 2017-2024) only includes recent marriages
# - This creates an "apples to oranges" comparison with same-sex couples
```

**UI Pattern for Handling This**:
- Toggle to show/hide opposite-sex rate (defaults to hidden)
- Expandable section explaining the "57%" misleading interpretation
- Constant disclaimers about time-horizon incomparability

## Important Implementation Patterns

### 1. Precomputation for Performance

Lines 55-73 in `app.py` precompute frequently-used statistics to avoid recalculation in interactive sections:

```python
# Precompute group totals and core stats for reuse
male_marriages = df['Marriages_Male'].sum()
male_divorces = df['Divorces_Male'].sum()
# ... etc
p_male = male_divorces / male_marriages if male_marriages else 0
# ... Fisher's exact test, odds ratios
```

### 2. Guided UI Pattern

The "Ohjattu tila" (Guided Mode, lines 86-157) is a question-based interface that:
- Helps users understand what different divorce rate metrics mean
- Maps journalistic questions to valid statistical interpretations
- Provides copy-ready text snippets for articles

**When adding new metrics**: Follow this pattern - explain what the metric measures, what it requires, and what conclusions are valid.

### 3. Dual Language Strategy

- **UI**: Finnish (target audience is Finnish journalists/public)
- **Code**: English variable names, English comments for international collaboration
- **Statistical terms**: English technical terms with Finnish explanations

### 4. Transparency Architecture

Every major section includes:
- Clear explanation of what the metric measures
- What data it requires
- What conclusions are valid vs invalid
- Limitations and caveats

Example: The expandable "Mikä on '57 %' ja miksi se hämää?" section (lines 213-223)

## Data Update Workflow

When Statistics Finland releases new yearly data:

1. Update the data dictionary in `app.py` (lines 25-33)
   - Add new year to `Year` list
   - Add new marriage/divorce counts for all groups
   - Update the "Last Updated" caption (line 456)

2. Update corresponding data in analysis scripts if needed:
   - `divorce_analysis.py` (lines 16-24)
   - `article_analysis.py` (lines 24-32)
   - `advanced_statistical_analysis.py` (lines 23-31)

3. Re-run all analysis scripts to regenerate charts

4. The cumulative calculations will automatically incorporate new data

## Statistical Interpretation Guidelines

### Valid Claims (Can Say)
- "Female same-sex couples have a higher divorce rate than male same-sex couples (21% vs 14%, statistically significant)"
- "Of same-sex marriages formed 2017-2024, 18.6% have ended in divorce"
- "The divorce rate is increasing over time (expected as marriages age)"

### Invalid Claims (Cannot Say)
- ❌ "Same-sex couples divorce less than opposite-sex couples" - Time horizons are incomparable
- ❌ Any claim about "lifetime divorce probability" - Requires survival analysis with individual-level data
- ❌ "The final divorce rate will be X%" - Too early to project

### What Would Make Valid Comparison Possible
- **Survival analysis** with individual-level data (marriage date + divorce date for each couple)
- **20-30 year follow-up period** for same-sex marriages
- **Controlling for covariates** (age, education, income, children, location)
- **Cohort-based analysis** tracking specific marriage cohorts over time

## Collaboration with Statistics Finland

Data source: [Statistics Finland PxWeb API](https://pxdata.stat.fi/PxWeb/pxweb/fi/StatFin/StatFin__ssaaty/statfin_ssaaty_pxt_121e.px/)

See `api.md` for API usage documentation.

For research-grade analysis requiring individual-level data, see the "Puuttuvan Datan Hankkiminen" tab in the Streamlit app for detailed guidance on:
- Applying for microdata access from Statistics Finland
- Required ethical approvals
- Timeline (3-7 months)
- Costs (€500-2000/year)

## Deployment

The app is designed for deployment to Streamlit Cloud. See `DEPLOYMENT_GUIDE.md` for full instructions.

Quick deployment:
1. Push to GitHub
2. Connect repository to [Streamlit Cloud](https://share.streamlit.io/)
3. Select `app.py` as the main file
4. Deploy

## Testing Philosophy

This project doesn't have traditional unit tests because:
- It's primarily a data analysis/visualization tool
- Statistical correctness is verified through peer review and cross-checking with established methods
- Visual outputs require manual inspection

When modifying statistical calculations:
1. Verify against known statistical packages (scipy, statsmodels)
2. Check mathematical formulas against textbook definitions
3. Validate results against expected patterns (e.g., confidence intervals should widen with smaller samples)
4. Test edge cases (zero counts, single year data)

## File Output Patterns

All scripts save outputs to the repository root:
- PNG files for charts (300 DPI for publication quality)
- CSV files for data exports
- Naming convention: `{purpose}_{detail}.{ext}`
  - Example: `article_main_chart.png`, `divorce_analysis_detailed.csv`

When adding new outputs, follow this pattern and document in the relevant script's header.
