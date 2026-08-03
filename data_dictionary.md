# Bluestock Mutual Fund Analytics Platform — Data Dictionary

This document provides complete technical specifications, schema definitions, business logic, data types, key constraints, and source mappings for all tables in the `bluestock_mf.db` SQLite star schema.

---

## Star Schema Overview

```
                          ┌────────────────┐
                          │   dim_date     │
                          └───────┬────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
          ▼                       ▼                       ▼
   ┌──────────────┐       ┌───────────────┐       ┌──────────────┐
   │   fact_nav   │       │fact_transact. │       │fact_benchmark│
   └──────┬───────┘       └───────┬───────┘       └──────────────┘
          │                       │
          └───────────┬───────────┘
                      ▼
              ┌──────────────┐
              │   dim_fund   │
              └───────┬──────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
   ┌──────────────┐       ┌───────────────┐
   │fact_perform. │       │fact_portfolio │
   └──────────────┘       └───────────────┘
```

---

## 1. Table: `dim_fund` (Fund Master Dimension)

- **Description**: Master dimension containing scheme-level metadata for 40 mutual fund schemes across top Indian AMCs.
- **Source Dataset**: `data/raw/01_fund_master.csv` -> `data/processed/01_fund_master.csv`
- **Primary Key**: `amfi_code`

| Column Name | SQL Type | Key | Business Definition | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `amfi_code` | TEXT | **PK** | Unique 6-digit AMFI code assigned by AMFI India. | `119551` |
| `fund_house` | TEXT | None | Asset Management Company (AMC) name. | `SBI Mutual Fund` |
| `scheme_name` | TEXT | None | Official scheme name registered with SEBI. | `SBI Bluechip Fund - Direct - Growth` |
| `category` | TEXT | None | Broad asset category (Equity, Debt, Hybrid, Solution Oriented). | `Equity` |
| `sub_category` | TEXT | None | SEBI scheme sub-category (Large Cap, Mid Cap, Small Cap, Liquid, etc.). | `Large Cap` |
| `plan` | TEXT | None | Investment plan route (`Direct` or `Regular`). | `Direct` |
| `launch_date` | TEXT | None | Inception date of the scheme (`YYYY-MM-DD`). | `2013-01-01` |
| `benchmark` | TEXT | None | Official benchmark index for performance comparison. | `NIFTY 100 TRI` |
| `expense_ratio_pct` | REAL | None | Total Expense Ratio (TER) expressed as annual percentage. | `0.85` |
| `exit_load_pct` | REAL | None | Exit load penalty percentage for early redemptions. | `1.0` |
| `min_sip_amount` | REAL | None | Minimum monthly SIP installment amount in INR. | `500.0` |
| `min_lumpsum_amount`| REAL | None | Minimum single lumpsum investment amount in INR. | `5000.0` |
| `fund_manager` | TEXT | None | Primary fund manager responsible for portfolio strategy. | `Sohini Andani` |
| `risk_category` | TEXT | None | Riskometer risk level (Low, Moderate, High, Very High). | `Very High` |
| `sebi_category_code`| TEXT | None | Internal SEBI category mapping code. | `EC01` |

---

## 2. Table: `dim_date` (Date Dimension)

- **Description**: Central calendar date dimension supporting temporal aggregations, day-of-week analysis, and holiday filtering.
- **Source**: Dynamically generated from full contiguous date range spanning Jan 2022 to May 2026.
- **Primary Key**: `date`

| Column Name | SQL Type | Key | Business Definition | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `date` | TEXT | **PK** | ISO calendar date (`YYYY-MM-DD`). | `2024-01-15` |
| `year` | INTEGER | None | Four-digit calendar year. | `2024` |
| `month` | INTEGER | None | Month number (1 to 12). | `1` |
| `quarter` | INTEGER | None | Calendar quarter (1 to 4). | `1` |
| `day_of_week` | INTEGER | None | Day of week index (0=Monday, 6=Sunday). | `0` |
| `is_weekday` | INTEGER | None | Binary flag: `1` if Monday–Friday, `0` if weekend. | `1` |

---

## 3. Table: `fact_nav` (Daily Scheme NAV History Fact)

- **Description**: Daily Net Asset Value (NAV) history for all schemes. Includes forward-filled weekend and market holiday values.
- **Source Dataset**: `data/raw/02_nav_history.csv` -> `data/processed/02_nav_history.csv`
- **Primary Key**: `(amfi_code, date)`
- **Foreign Keys**: `amfi_code` -> `dim_fund(amfi_code)`, `date` -> `dim_date(date)`

| Column Name | SQL Type | Key | Business Definition | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `amfi_code` | TEXT | **PK, FK** | AMFI scheme identifier. | `119551` |
| `date` | TEXT | **PK, FK** | Business date of the NAV entry (`YYYY-MM-DD`). | `2024-01-15` |
| `nav` | REAL | None | Per-unit Net Asset Value in Indian Rupees (INR). | `89.4521` |
| `daily_return_pct` | REAL | None | Calculated daily NAV percentage change vs previous day. | `0.45` |

---

## 4. Table: `fact_transactions` (Investor Transactions Fact)

- **Description**: Granular investor transaction log covering SIPs, Lumpsum investments, and Redemptions for 5,000 investors.
- **Source Dataset**: `data/raw/08_investor_transactions.csv` -> `data/processed/08_investor_transactions.csv`
- **Primary Key**: `tx_id`
- **Foreign Keys**: `amfi_code` -> `dim_fund(amfi_code)`, `transaction_date` -> `dim_date(date)`

| Column Name | SQL Type | Key | Business Definition | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `tx_id` | INTEGER | **PK** | Auto-incremented primary transaction sequence number. | `1001` |
| `investor_id` | TEXT | None | Unique investor identifier (`INV000001` to `INV005000`). | `INV002952` |
| `transaction_date` | TEXT | **FK** | Date when transaction occurred (`YYYY-MM-DD`). | `2024-01-15` |
| `amfi_code` | TEXT | **FK** | Target scheme AMFI code. | `119551` |
| `transaction_type` | TEXT | None | Standardised type (`SIP`, `Lumpsum`, `Redemption`). | `SIP` |
| `amount_inr` | REAL | None | Transaction value in Indian Rupees (INR). Must be > 0. | `10000.0` |
| `state` | TEXT | None | Indian state location of the investor. | `Maharashtra` |
| `city` | TEXT | None | City location of the investor. | `Mumbai` |
| `city_tier` | TEXT | None | AMFI classification: Top 30 (`T30`) or Beyond 30 (`B30`). | `T30` |
| `age_group` | TEXT | None | Investor age bracket (`18-25`, `26-35`, `36-45`, `46-55`, `56+`). | `26-35` |
| `gender` | TEXT | None | Investor gender (`Male`, `Female`). | `Male` |
| `annual_income_lakh`| REAL | None | Self-reported annual income in Lakh INR. | `15.5` |
| `payment_mode` | TEXT | None | Channel (`UPI`, `Net Banking`, `Mandate`, `Cheque`). | `UPI` |
| `kyc_status` | TEXT | None | Compliance status (`Verified`, `Pending`). | `Verified` |

---

## 5. Table: `fact_performance` (Scheme Performance & Risk Metrics Fact)

- **Description**: Key risk-adjusted metrics, annualized returns, benchmark comparisons, and ratings per scheme.
- **Source Dataset**: `data/raw/07_scheme_performance.csv` -> `data/processed/07_scheme_performance.csv`
- **Primary Key**: `amfi_code`
- **Foreign Keys**: `amfi_code` -> `dim_fund(amfi_code)`

| Column Name | SQL Type | Key | Business Definition | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `amfi_code` | TEXT | **PK, FK** | AMFI scheme identifier. | `119551` |
| `scheme_name` | TEXT | None | Scheme name. | `SBI Bluechip Fund - Direct - Growth` |
| `fund_house` | TEXT | None | Asset Management Company name. | `SBI Mutual Fund` |
| `category` | TEXT | None | Asset category. | `Equity` |
| `plan` | TEXT | None | Investment route (`Direct` or `Regular`). | `Direct` |
| `return_1yr_pct` | REAL | None | 1-year absolute return percentage. | `18.52` |
| `return_3yr_pct` | REAL | None | 3-year Compound Annual Growth Rate (CAGR %). | `16.24` |
| `return_5yr_pct` | REAL | None | 5-year Compound Annual Growth Rate (CAGR %). | `15.10` |
| `benchmark_3yr_pct`| REAL | None | Benchmark index 3-year CAGR %. | `14.80` |
| `alpha` | REAL | None | Excess return over benchmark (OLS intercept * 252). | `1.44` |
| `beta` | REAL | None | Sensitivity to benchmark movement (OLS slope). | `0.92` |
| `sharpe_ratio` | REAL | None | Risk-adjusted return ratio using 6.5% risk-free rate. | `1.85` |
| `sortino_ratio` | REAL | None | Downside risk-adjusted return ratio. | `2.45` |
| `std_dev_ann_pct` | REAL | None | Annualized standard deviation of daily returns (%). | `13.80` |
| `max_drawdown_pct` | REAL | None | Worst historical peak-to-trough decline percentage. | `-14.50` |
| `aum_crore` | REAL | None | Scheme Assets Under Management in INR Crore. | `42500.0` |
| `expense_ratio_pct` | REAL | None | Total Expense Ratio (TER %). | `0.85` |
| `morningstar_rating`| INTEGER | None | Simulated rating score (1 to 5 stars). | `5` |
| `risk_grade` | TEXT | None | Risk grade classification. | `Very High` |

---

## 6. Table: `fact_aum` (AMC AUM History Fact)

- **Description**: Quarterly Assets Under Management (AUM) history for top 10 AMC fund houses (2022–2025).
- **Source Dataset**: `data/raw/03_aum_by_fund_house.csv` -> `data/processed/03_aum_by_fund_house.csv`
- **Primary Key**: `(date, fund_house)`

| Column Name | SQL Type | Key | Business Definition | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `date` | TEXT | **PK** | Quarter-end date (`YYYY-MM-DD`). | `2025-12-31` |
| `fund_house` | TEXT | **PK** | AMC fund house name. | `SBI Mutual Fund` |
| `aum_lakh_crore` | REAL | None | Total AUM in Lakh INR Crore. | `12.50` |
| `aum_crore` | REAL | None | Total AUM in INR Crore. | `1250000.0` |
| `num_schemes` | INTEGER | None | Total active mutual fund schemes offered. | `186` |

---

## 7. Table: `fact_portfolio` (Portfolio Holdings Fact)

- **Description**: Top equity stock holdings, sector exposure, and portfolio weights as of Dec 2025.
- **Source Dataset**: `data/raw/09_portfolio_holdings.csv` -> `data/processed/09_portfolio_holdings.csv`
- **Primary Key**: `(amfi_code, stock_symbol, portfolio_date)`
- **Foreign Keys**: `amfi_code` -> `dim_fund(amfi_code)`

| Column Name | SQL Type | Key | Business Definition | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `amfi_code` | TEXT | **PK, FK** | AMFI scheme identifier. | `119551` |
| `stock_symbol` | TEXT | **PK** | NSE/BSE stock ticker symbol. | `HDFCBANK` |
| `stock_name` | TEXT | None | Full company name. | `HDFC Bank Ltd` |
| `sector` | TEXT | None | Industry sector classification. | `Banking` |
| `weight_pct` | REAL | None | Portfolio weight allocation percentage. | `9.45` |
| `market_value_cr` | REAL | None | Market value of holding in INR Crore. | `4016.25` |
| `current_price_inr`| REAL | None | Stock closing price as of portfolio date. | `1685.50` |
| `portfolio_date` | TEXT | **PK** | Reporting snapshot date (`YYYY-MM-DD`). | `2025-12-31` |

---

## 8. Table: `fact_sip_industry` (Industry Monthly SIP Inflows Fact)

- **Description**: Industry-wide monthly SIP inflow statistics published by AMFI India.
- **Source Dataset**: `data/raw/04_monthly_sip_inflows.csv` -> `data/processed/04_monthly_sip_inflows.csv`
- **Primary Key**: `month`

| Column Name | SQL Type | Key | Business Definition | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `month` | TEXT | **PK** | Year-Month string (`YYYY-MM`). | `2025-12` |
| `sip_inflow_crore` | REAL | None | Total monthly SIP contribution in INR Crore. | `31002.0` |
| `active_sip_accounts_crore`| REAL | None | Total active SIP accounts in Crore. | `9.35` |
| `new_sip_accounts_lakh`| REAL | None | New SIP registrations in that month (Lakh). | `68.5` |
| `sip_aum_lakh_crore`| REAL | None | Total SIP Assets Under Management in Lakh Crore. | `13.85` |
| `yoy_growth_pct` | REAL | None | Year-over-Year growth percentage of SIP inflow. | `24.5` |

---

## 9. Table: `fact_category_inflows` (Category Inflows Fact)

- **Description**: Monthly net inflows broken down by SEBI fund category (FY 2024-25).
- **Source Dataset**: `data/raw/05_category_inflows.csv` -> `data/processed/05_category_inflows.csv`
- **Primary Key**: `(month, category)`

| Column Name | SQL Type | Key | Business Definition | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `month` | TEXT | **PK** | Year-Month string (`YYYY-MM`). | `2024-04` |
| `category` | TEXT | **PK** | Mutual fund category name. | `Small Cap` |
| `net_inflow_crore` | REAL | None | Net monthly inflow in INR Crore (Inflows - Outflows). | `3897.0` |

---

## 10. Table: `fact_industry_folios` (Industry Folio Milestones Fact)

- **Description**: Industry total and asset-class specific investor folio counts (2022-2025).
- **Source Dataset**: `data/raw/06_industry_folio_count.csv` -> `data/processed/06_industry_folio_count.csv`
- **Primary Key**: `month`

| Column Name | SQL Type | Key | Business Definition | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `month` | TEXT | **PK** | Year-Month string (`YYYY-MM`). | `2025-12` |
| `total_folios_crore` | REAL | None | Total mutual fund folios across all categories (Crore). | `26.12` |
| `equity_folios_crore`| REAL | None | Equity scheme folios (Crore). | `18.45` |
| `debt_folios_crore` | REAL | None | Debt scheme folios (Crore). | `0.72` |
| `hybrid_folios_crore`| REAL | None | Hybrid scheme folios (Crore). | `1.45` |
| `others_folios_crore`| REAL | None | Passive, Index, and Solution-oriented folios (Crore). | `5.50` |

---

## 11. Table: `fact_benchmark_indices` (Benchmark Indices Fact)

- **Description**: Daily closing prices for market benchmark indices (Nifty 50, Nifty 100, BSE SmallCap, etc.).
- **Source Dataset**: `data/raw/10_benchmark_indices.csv` -> `data/processed/10_benchmark_indices.csv`
- **Primary Key**: `(date, index_name)`

| Column Name | SQL Type | Key | Business Definition | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `date` | TEXT | **PK** | ISO calendar date (`YYYY-MM-DD`). | `2024-01-15` |
| `index_name` | TEXT | **PK** | Official benchmark index name (e.g. `NIFTY50`, `NIFTY100`). | `NIFTY50` |
| `close_value` | REAL | None | End of day closing index value. | `22097.45` |
