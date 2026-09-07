import pandas as pd

def latest_value(df, column):
    """Get each country's most recent NON-NULL value for one indicator."""
    sub = df.dropna(subset=[column]).sort_values("year")
    sub = sub.groupby("country").tail(1)
    return sub[["country", column]]

def main():
    df = pd.read_json("../data/processed/country_data.json")

    # Get each indicator's latest available value independently,
    # instead of forcing all 4 to come from the same year
    gdp = latest_value(df, "gdp_growth")
    inflation = latest_value(df, "inflation")
    debt = latest_value(df, "debt_to_gdp")
    unemployment = latest_value(df, "unemployment")

    # Merge them all together on country
    latest = gdp.merge(inflation, on="country", how="outer") \
                .merge(debt, on="country", how="outer") \
                .merge(unemployment, on="country", how="outer")

    # --- Normalize each indicator to a 0-100 scale ---
    # For gdp_growth: higher is SAFER, so we flip it (high growth = low risk)
    # For inflation, debt_to_gdp, unemployment: higher is RISKIER, so no flip

    def normalize(series, flip=False):
        norm = (series - series.min()) / (series.max() - series.min()) * 100
        return 100 - norm if flip else norm

    latest["gdp_risk"] = normalize(latest["gdp_growth"], flip=True)
    latest["inflation_risk"] = normalize(latest["inflation"])
    latest["debt_risk"] = normalize(latest["debt_to_gdp"])
    latest["unemployment_risk"] = normalize(latest["unemployment"])

    # --- Weighted composite score ---
    # Inflation and debt matter most for "country risk" in the real world, so we weight them higher
    latest["risk_score"] = (
        latest["gdp_risk"] * 0.20 +
        latest["inflation_risk"] * 0.30 +
        latest["debt_risk"] * 0.30 +
        latest["unemployment_risk"] * 0.20
    ).round(1)

    # --- Bucket into risk levels ---
    def bucket(score):
        if pd.isna(score):
            return "Insufficient Data"
        elif score < 33:
            return "Low Risk"
        elif score < 66:
            return "Moderate Risk"
        else:
            return "High Risk"

    latest["risk_level"] = latest["risk_score"].apply(bucket)

    # Sort riskiest first
    latest = latest.sort_values("risk_score", ascending=False)

    result = latest[["country", "gdp_growth", "inflation", "debt_to_gdp",
                      "unemployment", "risk_score", "risk_level"]]

    result.to_json("../data/processed/risk_scores.json", orient="records", indent=2)
    result.to_csv("../data/processed/risk_scores.csv", index=False)

    print(result.to_string(index=False))
    print("\nSaved to data/processed/risk_scores.json")

if __name__ == "__main__":
    main()