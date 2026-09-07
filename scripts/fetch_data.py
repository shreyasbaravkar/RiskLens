import requests
import pandas as pd
import json

# Countries we care about for the risk platform (mix of stable + volatile economies)
COUNTRIES = ["USA","GBR","IND","CHN","BRA","ZAF","NGA","PAK","TUR","ARG"]

# World Bank Indicator codes we want 
INDICATORS = {
    "NY.GDP.MKTP.KD.ZG": "gdp_growth",  # GDP growth (annual %)
    "FP.CPI.TOTL.ZG": "inflation",     # Inflation(annual %)
    "GC.DOD.TOTL.GD.ZS": "debt_to_gdp", # Central govt debt(% of gdp)
    "SL.UEM.TOTL.ZS": "unemployment",  # Unemployment(%)
}

def fetch_indicator(country, indicator_code):
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator_code}"
    params = {"format": "json", "per_page": 20, "date": "2015:2024"}
    response = requests.get(url, params=params)
    data = response.json()

    # World Bank API returns[metadata, actual_data] - we want index 1 
    if len(data) < 2 or data[1] is None:
        return[]
    return data[1]

def main():
    all_records = []

    for country in COUNTRIES:
        for code , name in INDICATORS.items():
            print(f"Fetching {name} for {country}...")
            records = fetch_indicator(country,code)
            for r in records:
                if r["value"] is not None:
                    all_records.append({
                        "country": country,
                        "indicator": name,
                        "year": r["date"],
                        "value": r["value"]
                    })

# Save raw JSON as a backup
    with open("../data/raw/world_bank_raw.json","w") as f:
        json.dump(all_records, f, indent=2)

    print(f"\n Done. Fetched {len(all_records)} records.")
    print("Saved to data/raw/world_bank_raw.json")

if __name__ == "__main__":
    main()
