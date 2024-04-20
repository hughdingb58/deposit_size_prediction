from fredapi import Fred
import requests

import numpy as np
import pandas as pd

from pyarrow.feather import read_feather, write_feather

# ***************
# FRED
# ***************

print("Gathering FRED data")

# Read in FRED API key
f = open("../fred_api_key.txt", "r")
api_key = f.read().strip()
fred_con = Fred(api_key=api_key)

# Loop through each series code and pull data
fred_series = {
    "GDPC1": "gdp",
    "CPIAUCNS": "cpi",
    "UNRATE": "unemployment_rate",
    "FEDFUNDS": "fed_fund_rate",
    "GS10": "treasury_10yr_constant_maturity_rate",
    "GPDIC1": "private_domestic_investment",
    "GPDIC96": "private_domestic_investment_excl_iva_ccadj",
    "FGEXPND": "fed_govt_expenditures",
    "SLEXPND": "state_local_govt_expenditures",
    "NETEXP": "net_exports_good_services",
    "HOUST": "housing_starts",
    "HSN1F": "new_one_family_houses_sold",
    "CSUSHPINSA": "case_shiller_us_national_home_price_index",
    "RETAILMPCSMSA": "advance_real_retail_food_services_sales",
    "INDPRO": "industrial_production_index",
    "DSPIC96": "disposable_personal_income",
    "RRSFS": "retail_food_services_sales",
    "PSAVERT": "personal_savings_rate",
    "UMCSENT": "umich_consumer_sentiment_index",
    "TDSP": "household_debt_service_payments_pct_disposable_income",
    "DRCCLACBS": "credit_card_delinquency_rate",
    "TOTALSL": "consumer_credit_owned_securitized_outstanding",
    "CPILFESL": "cpi_urban_consumers_less_food_energy",
    "AHETPI": "avg_hrly_earnings_production_nonsupervisory_employees",
    "MEHOINUSA672N": "real_median_household_income",
    "PCEC96": "pce",
    "TOTALSA": "total_vehicle_sales",
}

econ_full = pd.DataFrame()

for code in fred_series.keys():
    series = fred_con.get_series(
        code, observation_start="2000-01-01", observation_end="2023-12-31"
    )
    econ_full[code] = series

# Rename columns to be more descriptive
econ = econ_full.rename(columns=fred_series)

# Keep date as column
econ = econ.reset_index().rename(columns={"index": "date"})
# Add year and quarter columns for merging
econ["year"] = econ["date"].dt.year
econ["quarter"] = econ["date"].dt.quarter

# Cache values
write_feather(econ, "../data/fred_econ.feather")

# ***************
# FDIC
# ***************

print("Gathering FDIC data (approx. 30 min)")

# FDIC data is gathered from its API - https://banks.data.fdic.gov/docs/
fdic_url = "https://banks.data.fdic.gov/api/"

institutions_url = fdic_url + "institutions"

# Get list of institutions from API
institutions_params = {
    "filters": "ACTIVE:1",
    "sort_by": "OFFICES",
    "sort_order": "DESC",
    "limit": 10000,
    "format": "json",
}

res = requests.get(institutions_url, params=institutions_params)
institutions_data = res.json()["data"]

# Read data into list
institutions_list = []
for row in institutions_data:
    curr_bank = pd.DataFrame(row["data"], index=[0])
    institutions_list.append(curr_bank)

# Bind list into table
institutions_full = pd.concat(institutions_list, axis=0).reset_index(drop=True)

# Keep only relevant columns
institutions = institutions_full[["NAMEHCR", "ZIP"]].drop_duplicates()
institutions = institutions[institutions["NAMEHCR"] != ""].reset_index(drop=True)
institutions["ZIP"] = institutions["ZIP"].astype(str)
institutions.head()

# Create string of needed fields for API call
fdic_series = {
    "NAMEHCR": "name",
    "ZIP": "zip",
    "REPDTE": "date",
    "CLCODE": "classcode",
    "ASSET": "total_assets",
    "NETINCQ": "net_income_quarterly",
    "OFFOA": "offices_us",
    "OFFFOR": "offices_foreign",
    "ROAQ": "roa_quarterly",
    "ROEQ": "roe_quarterly",
    "EINTXQA": "total_interest_expense_quarterly",
    "NONIXQA": "non_interest_expense_quarterly",
    "DEP": "total_deposits",
    "SC1LES": "debt_securities_maturity_1yr_or_less",
}

fields_str = ",".join(fdic_series.keys())
fields_sum_str = ",".join(list(fdic_series.keys())[4:])

financials_url = fdic_url + "financials"

financials_list = []

# Loop through banks
for i in range(institutions.shape[0]):
    institution_row = institutions.iloc[i]
    financials_params = {
        "filters": 'NAMEHCR:"'
        + str(institution_row["NAMEHCR"])
        + '",ZIP:"'
        + str(institution_row["ZIP"])
        + '"',
        "fields": fields_str,
        "sort_by": "REPDTE",
        "sort_order": "DESC",
        "limit": 10000,
        "agg_term_fields": "NAMEHCR,ZIP,REPDTE",
        "agg_sum_fields": fields_sum_str,
        "format": "json",
    }

    # Get list of institutions from API
    res = requests.get(financials_url, params=financials_params)
    financials_data = res.json()["data"]

    # Read data into list
    for row in financials_data:
        curr_bank = pd.DataFrame(row["data"], index=[0])
        financials_list.append(curr_bank)

# Bind list into table
financials_full = pd.concat(financials_list, axis=0).reset_index(drop=True)

# Set more descriptive column names
financials = financials_full.rename(columns=fdic_series)
# Clean column data types
financials["date"] = pd.to_datetime(financials["date"], format="%Y%m%d")
financials["zip"] = financials["zip"].astype(str)
# Filter to holding companies only
financials = financials[financials["classcode"] <= 65]
# Filter to data after 2000 only, to match FRED data time frame
financials = financials[financials["date"] >= "2000-01-01"]
# Add year and quarter columns for merging
financials["year"] = financials["date"].dt.year
financials["quarter"] = financials["date"].dt.quarter
# Sort data
financials = financials.sort_values(["name", "zip", "date"])

# Remove unneeded columns:
# The ID doesn't seem to be immediately meaningful.
# The office counts don't seem to be properly filled in.
# RoA and RoE are ratios, so they will be difficult to aggregate.
# We no longer need classcode.
financials = financials.drop(
    [
        "ID",
        "offices_foreign",
        "offices_us",
        "roe_quarterly",
        "roa_quarterly",
        "zip",
        "classcode",
    ],
    axis=1,
)
# Aggregate by bank name
financials = (
    financials.groupby(["name", "date", "year", "quarter"]).agg("sum").reset_index()
)
# Cache values
write_feather(financials, "../data/fdic_financials.feather")
