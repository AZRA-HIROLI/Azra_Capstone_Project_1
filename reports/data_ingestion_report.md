# 📊 Data Ingestion Report

## 📂 01_fund_master.csv
- **Shape:** (40, 15)
- **Dtypes:**
```
amfi_code               int64
fund_house             object
scheme_name            object
category               object
sub_category           object
plan                   object
launch_date            object
benchmark              object
expense_ratio_pct     float64
exit_load_pct         float64
min_sip_amount          int64
min_lumpsum_amount      int64
fund_manager           object
risk_category          object
sebi_category_code     object
dtype: object
```
- **Head:**
```
   amfi_code       fund_house  ... risk_category sebi_category_code
0     119551  SBI Mutual Fund  ...      Moderate               EC01
1     119552  SBI Mutual Fund  ...      Moderate               EC01
2     119598  SBI Mutual Fund  ...     Very High               EC03
3     119599  SBI Mutual Fund  ...     Very High               EC03
4     119120  SBI Mutual Fund  ...           Low               DC02

[5 rows x 15 columns]
```

- ✅ No missing values detected
- ✅ No duplicate rows detected

## 📂 02_nav_history.csv
- **Shape:** (46000, 3)
- **Dtypes:**
```
amfi_code      int64
date          object
nav          float64
dtype: object
```
- **Head:**
```
   amfi_code        date      nav
0     119551  2022-01-03  54.3856
1     119551  2022-01-04  54.3474
2     119551  2022-01-05  54.6869
3     119551  2022-01-06  55.4550
4     119551  2022-01-07  55.3692
```

- ✅ No missing values detected
- ✅ No duplicate rows detected

## 📂 03_aum_by_fund_house.csv
- **Shape:** (90, 5)
- **Dtypes:**
```
date               object
fund_house         object
aum_lakh_crore    float64
aum_crore           int64
num_schemes         int64
dtype: object
```
- **Head:**
```
         date           fund_house  aum_lakh_crore  aum_crore  num_schemes
0  2022-03-31      SBI Mutual Fund            6.05     605000          186
1  2022-03-31  ICICI Prudential MF            4.65     465000          216
2  2022-03-31     HDFC Mutual Fund            4.35     435000          195
3  2022-03-31      Nippon India MF            2.70     270000          177
4  2022-03-31    Kotak Mahindra MF            2.70     270000          168
```

- ✅ No missing values detected
- ✅ No duplicate rows detected

## 📂 04_monthly_sip_inflows.csv
- **Shape:** (48, 6)
- **Dtypes:**
```
month                         object
sip_inflow_crore               int64
active_sip_accounts_crore    float64
new_sip_accounts_lakh        float64
sip_aum_lakh_crore           float64
yoy_growth_pct               float64
dtype: object
```
- **Head:**
```
     month  sip_inflow_crore  ...  sip_aum_lakh_crore  yoy_growth_pct
0  2022-01             11517  ...                4.80             NaN
1  2022-02             11438  ...                4.85             NaN
2  2022-03             12328  ...                5.01             NaN
3  2022-04             11863  ...                5.12             NaN
4  2022-05             12286  ...                5.15             NaN

[5 rows x 6 columns]
```

- ⚠️ **Missing values per column:**
```
month                         0
sip_inflow_crore              0
active_sip_accounts_crore     0
new_sip_accounts_lakh         0
sip_aum_lakh_crore            0
yoy_growth_pct               12
dtype: int64
```
- ✅ No duplicate rows detected

## 📂 05_category_inflows.csv
- **Shape:** (144, 3)
- **Dtypes:**
```
month                object
category             object
net_inflow_crore    float64
dtype: object
```
- **Head:**
```
     month         category  net_inflow_crore
0  2024-04        Large Cap            2413.0
1  2024-04          Mid Cap            3897.0
2  2024-04        Small Cap            3533.0
3  2024-04        Flexi Cap            4947.0
4  2024-04  Large & Mid Cap            4214.0
```

- ✅ No missing values detected
- ✅ No duplicate rows detected

## 📂 06_industry_folio_count.csv
- **Shape:** (21, 6)
- **Dtypes:**
```
month                   object
total_folios_crore     float64
equity_folios_crore    float64
debt_folios_crore      float64
hybrid_folios_crore    float64
others_folios_crore    float64
dtype: object
```
- **Head:**
```
     month  total_folios_crore  ...  hybrid_folios_crore  others_folios_crore
0  2022-01               13.26  ...                 0.80                 1.33
1  2022-04               13.91  ...                 0.83                 1.39
2  2022-07               13.85  ...                 0.83                 1.38
3  2022-10               14.12  ...                 0.85                 1.41
4  2023-01               14.81  ...                 0.89                 1.48

[5 rows x 6 columns]
```

- ✅ No missing values detected
- ✅ No duplicate rows detected

## 📂 07_scheme_performance.csv
- **Shape:** (40, 19)
- **Dtypes:**
```
amfi_code               int64
scheme_name            object
fund_house             object
category               object
plan                   object
return_1yr_pct        float64
return_3yr_pct        float64
return_5yr_pct        float64
benchmark_3yr_pct     float64
alpha                 float64
beta                  float64
sharpe_ratio          float64
sortino_ratio         float64
std_dev_ann_pct       float64
max_drawdown_pct      float64
aum_crore               int64
expense_ratio_pct     float64
morningstar_rating      int64
risk_grade             object
dtype: object
```
- **Head:**
```
   amfi_code  ... risk_grade
0     119551  ...   Moderate
1     119552  ...   Moderate
2     119598  ...  Very High
3     119599  ...  Very High
4     119120  ...        Low

[5 rows x 19 columns]
```

- ✅ No missing values detected
- ✅ No duplicate rows detected

## 📂 08_investor_transactions.csv
- **Shape:** (32778, 13)
- **Dtypes:**
```
investor_id            object
transaction_date       object
amfi_code               int64
transaction_type       object
amount_inr              int64
state                  object
city                   object
city_tier              object
age_group              object
gender                 object
annual_income_lakh    float64
payment_mode           object
kyc_status             object
dtype: object
```
- **Head:**
```
  investor_id transaction_date  ...  payment_mode kyc_status
0   INV003054       2024-01-01  ...           UPI   Verified
1   INV002952       2024-01-01  ...        Cheque   Verified
2   INV003420       2024-01-01  ...       Mandate   Verified
3   INV003436       2024-01-01  ...        Cheque    Pending
4   INV004691       2024-01-01  ...   Net Banking    Pending

[5 rows x 13 columns]
```

- ✅ No missing values detected
- ✅ No duplicate rows detected

## 📂 09_portfolio_holdings.csv
- **Shape:** (322, 8)
- **Dtypes:**
```
amfi_code              int64
stock_symbol          object
stock_name            object
sector                object
weight_pct           float64
market_value_cr      float64
current_price_inr    float64
portfolio_date        object
dtype: object
```
- **Head:**
```
   amfi_code stock_symbol  ... current_price_inr portfolio_date
0     119551    POWERGRID  ...           6011.08     2025-12-31
1     119551     HDFCBANK  ...           1074.65     2025-12-31
2     119551       GRASIM  ...           5964.59     2025-12-31
3     119551      DRREDDY  ...           3748.82     2025-12-31
4     119551   ASIANPAINT  ...           1321.45     2025-12-31

[5 rows x 8 columns]
```

- ✅ No missing values detected
- ✅ No duplicate rows detected

## 📂 10_benchmark_indices.csv
- **Shape:** (8050, 3)
- **Dtypes:**
```
date            object
index_name      object
close_value    float64
dtype: object
```
- **Head:**
```
         date index_name  close_value
0  2022-01-03    NIFTY50     17492.79
1  2022-01-04    NIFTY50     17689.64
2  2022-01-05    NIFTY50     17835.05
3  2022-01-06    NIFTY50     17878.51
4  2022-01-07    NIFTY50     17759.15
```

- ✅ No missing values detected
- ✅ No duplicate rows detected
