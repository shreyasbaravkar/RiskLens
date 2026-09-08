# RiskLens — Country Risk & Economic Intelligence Platform

A data pipeline and interactive dashboard that scores and visualizes sovereign
economic risk across 10 major economies, using real World Bank data.

**Live demo:** https://magnificent-banoffee-f35a2a.netlify.app

## What it does

- Pulls GDP growth, inflation, debt-to-GDP, and unemployment data for 10
  countries from the World Bank API
- Cleans and reshapes the data into a country-year indicator table
- Computes a weighted composite **Risk Score (0–100)** per country, normalizing
  indicators onto a common scale and weighting inflation/debt highest
- Flags countries with incomplete data as "Insufficient Data" rather than
  silently guessing
- Renders an interactive dashboard: risk scorecard, bar chart, risk
  distribution donut, inflation-vs-debt scatter plot, high-risk/low-risk
  spotlights, and auto-generated takeaways
- Dashboard is fully filterable by risk level (All / High / Moderate / Low)

## Why these weights

Inflation and debt-to-GDP are weighted highest (30% each) since they're the
indicators sovereign risk analysts weight most heavily in practice; GDP growth
and unemployment are weighted 20% each.

## Tech stack

- **Data pipeline:** Python (pandas, requests) — `scripts/`
- **Frontend:** HTML, CSS, JavaScript, Chart.js — `site/`
- **Data source:** [World Bank Open Data API](https://data.worldbank.org/)

## Project structure
risklens/
├── scripts/
│ ├── fetch_data.py # pulls raw data from World Bank API
│ ├── clean_data.py # reshapes into tidy country-year table
│ └── risk_score.py # computes composite risk scores
├── data/
│ ├── raw/ # untouched API output
│ └── processed/ # cleaned data + final scores
└── site/
├── index.html
├── style.css
└── script.js


## Running it locally

```bash
pip install requests pandas
cd scripts
python fetch_data.py
python clean_data.py
python risk_score.py
```

Then open `site/index.html` with a local server (e.g. VS Code's Live Server
extension) — `fetch()` requires a server, not a direct file open.

## Notes

Risk scores are a modeled estimate for demonstration purposes, not an
official sovereign risk rating.
