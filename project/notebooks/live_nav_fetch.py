import json
import urllib.request
from urllib.error import HTTPError, URLError
import pandas as pd
import numpy as np

# Config & Constants
HDFC_TOP_100_CODE = "125497"
BLUECHIP_SCHEMES = {
    "119551": "SBI Bluechip Direct Growth",
    "120503": "ICICI Bluechip Direct Growth",
    "118632": "Nippon Large Cap Direct Growth",
    "119092": "Axis Bluechip Direct Growth",
    "120841": "Kotak Bluechip Direct Growth"
}

def fetch_json(url):
    """Safely fetch and parse JSON from a URL."""
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None

# =====================================================================
# STEP 1: Fetch Live NAV (HDFC Top 100) & Save Raw CSV
# =====================================================================
print("\n=== STEP 1: Fetching HDFC Top 100 Direct ===")
hdfc_url = f"https://api.mfapi.in/mf/{HDFC_TOP_100_CODE}"
hdfc_payload = fetch_json(hdfc_url)

if hdfc_payload and "data" in hdfc_payload:
    meta = hdfc_payload.get("meta", {})
    raw_data = hdfc_payload["data"]
    
    # Map to DataFrame and inject metadata
    df_hdfc = pd.DataFrame(raw_data)
    df_hdfc["scheme_code"] = meta.get("scheme_code")
    df_hdfc["scheme_name"] = meta.get("scheme_name")
    
    # Save as Raw CSV
    df_hdfc.to_csv("hdfc_125497_raw.csv", index=False)
    print(f"✔ Saved {len(df_hdfc)} historical records to 'hdfc_125497_raw.csv'")
else:
    print("❌ Failed to fetch HDFC 125497.")

# =====================================================================
# STEP 2: Fetch Live NAV for 5 Key Schemes & Save Combined CSV
# =====================================================================
print("\n=== STEP 2: Fetching 5 Key Bluechip Schemes ===")
bluechip_list = []

for code, name in BLUECHIP_SCHEMES.items():
    print(f"Fetching NAV for: {name} ({code})...")
    payload = fetch_json(f"https://api.mfapi.in/mf/{code}")
    if payload and "data" in payload and "meta" in payload:
        latest = payload["data"][0]  # mfapi.in historical arrays are ordered [newest -> oldest]
        bluechip_list.append({
            "scheme_code": code,
            "scheme_name": payload["meta"].get("scheme_name"),
            "date": latest.get("date"),
            "nav": latest.get("nav")
        })

df_bluechips = pd.DataFrame(bluechip_list)
df_bluechips.to_csv("bluechip_latest_nav.csv", index=False)
print("✔ Saved combined latest NAVs to 'bluechip_latest_nav.csv'")

# =====================================================================
# STEP 3: Explore Fund Master & Analyze AMFI Scheme Code Structure
# =====================================================================
print("\n=== STEP 3: Exploring Fund Master Structure ===")
master_url = "https://api.mfapi.in/mf"
master_payload = fetch_json(master_url)

if master_payload:
    df_master = pd.DataFrame(master_payload)
    print(f"Total Unique Schemes in Master List: {len(df_master):,}")
    
    # Demystifying why metadata attributes (Risk, Categories) are missing in raw master:
    print("\n🔍 Note on Fund Master Metadata:")
    print("The raw `mfapi.in/mf` master list returns ONLY `schemeCode` and `schemeName`.")
    print("Metadata (Fund House, Category, Risk Grade) must be parsed programmatically from the text patterns.")
    
    # Parse Fund House & Plan options from the Scheme Name pattern
    df_master['fund_house'] = df_master['schemeName'].apply(lambda x: x.split("Mutual Fund")[0].strip() if "Mutual Fund" in x else x.split()[0])
    df_master['is_direct'] = df_master['schemeName'].str.contains('Direct', case=False)
    df_master['is_growth'] = df_master['schemeName'].str.contains('Growth', case=False)
    
    print("\n--- Structural Analysis Sample ---")
    print(f"Unique Fund Houses Identified: {df_master['fund_house'].nunique()}")
    print(f"Percentage of Direct Plans: {df_master['is_direct'].mean() * 100:.2f}%")
    print(f"Percentage of Growth Schemes: {df_master['is_growth'].mean() * 100:.2f}%")
else:
    print("❌ Failed to pull Master registry.")

# import time  # <--- Import time for introducing sleep delays

# =====================================================================
# STEP 4: Validating AMFI Codes (DQ Audit) - SAFE VERSION
# =====================================================================
print("\n=== STEP 4: Validating AMFI Codes (DQ Audit) ===")

# Reduce sample size to 15-20 to test quickly without getting blocked
dq_sample = df_master.sample(n=20, random_state=42) if 'df_master' in locals() else pd.DataFrame()
validation_results = []

for idx, row in dq_sample.iterrows():
    code = str(row['schemeCode'])
    url = f"https://api.mfapi.in/mf/{code}/latest" 
    
    print(f"Auditing code {code}...", end="", flush=True)
    
    try:
        # Added 'timeout=3' to prevent infinite hanging if api.mfapi.in is slow
        with urllib.request.urlopen(url, timeout=3) as response:
            payload = json.loads(response.read().decode())
            if payload and "data" in payload and len(payload["data"]) > 0:
                validation_results.append({"code": code, "status": "PASS", "details": "Active & Valid"})
                print(" [PASS]")
            else:
                validation_results.append({"code": code, "status": "FAIL", "details": "Null data payload"})
                print(" [FAIL - Empty]")
                
    except HTTPError as e:
         validation_results.append({"code": code, "status": "FAIL", "details": f"Orphaned Code (HTTP {e.code})"})
         print(f" [FAIL - HTTP {e.code}]")
    except URLError as e:
         validation_results.append({"code": code, "status": "ERROR", "details": f"Network Error ({e.reason})"})
         print(" [ERROR - Timeout/DNS]")
    except Exception as e:
         validation_results.append({"code": code, "status": "ERROR", "details": str(e)})
         print(" [ERROR]")
    
    # Crucial: Sleep for 0.5 seconds to respect the API limits and prevent blocking
    time.sleep(0.5)


df_dq = pd.DataFrame(validation_results)
pass_rate = (df_dq['status'] == 'PASS').mean() * 100

print(f"\nAudit completed on {len(df_dq)} sampled registry items.")
print(f"Referential Integrity Pass Rate: {pass_rate:.1f}%")



from pathlib import Path

# Safely establish the destination directory
reports_dir = Path("./reports")
reports_dir.mkdir(parents=True, exist_ok=True)

# Define file destination
pdf_path = reports_dir / "mutual_fund_dq_report.pdf"
