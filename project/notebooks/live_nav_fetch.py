import json
import urllib.request
import urllib.error 
import pandas as pd

# Define Schemes
HDFC_TOP_100_CODE = "125497"
BLUECHIP_SCHEMES = {
    "119551": "SBI Bluechip Direct Growth",
    "120503": "ICICI Bluechip Direct Growth",
    "118632": "Nippon Large Cap Direct Growth",
    "119092": "Axis Bluechip Direct Growth",
    "120841": "Kotak Bluechip Direct Growth"
}

def fetch_json(url):
    """Helper function to perform GET request and return parsed JSON."""
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None

# =====================================================================
# TASK 1: Fetch Live NAV (HDFC Top 100 Direct) and Save as Raw CSV
# =====================================================================
print("--- Task 1: Fetching HDFC Top 100 (125497) ---")
hdfc_url = f"https://api.mfapi.in/mf/{HDFC_TOP_100_CODE}"
hdfc_data = fetch_json(hdfc_url)

if hdfc_data and "data" in hdfc_data:
    # Extract historical NAV series
    df_hdfc = pd.DataFrame(hdfc_data["data"])
    df_hdfc["scheme_code"] = HDFC_TOP_100_CODE
    
    # Save raw CSV
    hdfc_csv_path = "hdfc_125497_raw.csv"
    df_hdfc.to_csv(hdfc_csv_path, index=False)
    print(f"Successfully saved {len(df_hdfc)} historical records to {hdfc_csv_path}\n")
else:
    print("Failed to fetch HDFC Top 100 data.\n")


# =====================================================================
# TASK 2: Fetch NAV for 5 Key Bluechip Schemes & Combine into CSV
# =====================================================================
print("--- Task 2: Fetching 5 Key Bluechip Schemes ---")
combined_records = []

for code, name in BLUECHIP_SCHEMES.items():
    print(f"Fetching NAV for {name} ({code})...")
    scheme_url = f"https://api.mfapi.in/mf/{code}"
    res = fetch_json(scheme_url)
    
    if res and "data" in res:
        # Get latest NAV entry (first element in the array is usually the latest)
        latest_entry = res["data"][0] 
        combined_records.append({
            "Scheme Code": code,
            "Scheme Name": name,
            "Latest Date": latest_entry.get("date"),
            "Latest NAV": latest_entry.get("nav")
        })

df_bluechips = pd.DataFrame(combined_records)
bluechips_csv_path = "bluechip_latest_nav.csv"
df_bluechips.to_csv(bluechips_csv_path, index=False)
print(f"Saved latest Bluechip NAVs to {bluechips_csv_path}\n")


# =====================================================================
# TASK 3: Explore Fund Master & AMFI Scheme Code Structure
# =====================================================================
print("--- Task 3: Exploring Fund Master ---")
# mfapi.in lists all schemes under GET /mf
all_funds_url = "https://api.mfapi.in/mf"
all_funds = fetch_json(all_funds_url)

if all_funds:
    df_master = pd.DataFrame(all_funds)
    print(f"Total schemes found in Master: {len(df_master)}")
    print("Sample Master Data Schema:")
    print(df_master.head(3))
else:
    print("Failed to fetch Fund Master list.")# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# Assuming you have a list of code values:
# fund_master_codes = set(df_master['schemeCode'].astype(str))

def validate_data_quality(fund_master_codes, sample_size=50):
    """
    Validates that a sample of AMFI codes from the fund master
    have active endpoints and returns status summaries.
    """
    sampled_codes = list(fund_master_codes)[:sample_size]
    results = []
    
    for code in sampled_codes:
        url = f"https://api.mfapi.in/mf/{code}/latest" # Lighter request than fetching full history
        try:
            with urllib.request.urlopen(url) as response:
                status = response.getcode()
                results.append({"scheme_code": code, "status": "Valid", "http_code": status})
        except urllib.error.HTTPError as e:
            results.append({"scheme_code": code, "status": f"Orphaned/Missing", "http_code": e.code})
        except Exception as e:
            results.append({"scheme_code": code, "status": f"Connection Error", "http_code": None})
            
    return pd.DataFrame(results)
