import pandas as pd
import json

def main():
    #Load the raw data we fetched in step 2
    with open("../data/raw/world_bank_raw.json","r") as f:
        raw_data = json.load(f)

    # Turn the list of records into a pandas table
    df = pd.DataFrame(raw_data)

    # Right now each row is: country, indicator, year, value
    # We want: each row = one country+year, with indicators as separate columns
    pivoted = df.pivot_table(
        index=["country","year"],
        columns="indicator",
        values="value"
    ).reset_index()

    # Sort nicely by country then year
    pivoted = pivoted.sort_values(["country","year"])

    # Drop rows where we're missing too much data(e.g less than 2 indicators present)
    indicator_cols = ["gdp_growth","inflation","debt_to_gdp","unemployment"]
    pivoted = pivoted.dropna(thresh=3, subset=indicator_cols)

    # Save as both CSV(easy to eyeball in Excel) and JSON (for the website later)
    pivoted.to_csv("../data/processed/country_data.csv",index=False)
    pivoted.to_json("../data/processed/country_data.json", orient="records", indent=2 ) 

    print(f"Cleaned data svaed. {len(pivoted)} rows across {pivoted['country'].nunique()} countries.")
    print("\nPreview:")
    print(pivoted.head(10))

if __name__ == "__main__":
    main()

                    
                    