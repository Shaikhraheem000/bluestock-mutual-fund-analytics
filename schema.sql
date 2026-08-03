-- SQLite Star Schema DDL for Bluestock Mutual Fund Analytics Platform
-- File: schema.sql

PRAGMA foreign_keys = ON;

-- 1. Dimension Table: Fund Master
DROP TABLE IF EXISTS dim_fund;
CREATE TABLE dim_fund (
    amfi_code TEXT PRIMARY KEY,
    fund_house TEXT NOT NULL,
    scheme_name TEXT NOT NULL,
    category TEXT NOT NULL,
    sub_category TEXT,
    plan TEXT,
    launch_date TEXT,
    benchmark TEXT,
    expense_ratio_pct REAL,
    exit_load_pct REAL,
    min_sip_amount REAL,
    min_lumpsum_amount REAL,
    fund_manager TEXT,
    risk_category TEXT,
    sebi_category_code TEXT
);

-- 2. Dimension Table: Date Dimension
DROP TABLE IF EXISTS dim_date;
CREATE TABLE dim_date (
    date TEXT PRIMARY KEY,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    is_weekday INTEGER NOT NULL
);

-- 3. Fact Table: NAV History
DROP TABLE IF EXISTS fact_nav;
CREATE TABLE fact_nav (
    amfi_code TEXT NOT NULL,
    date TEXT NOT NULL,
    nav REAL NOT NULL,
    daily_return_pct REAL DEFAULT 0.0,
    PRIMARY KEY (amfi_code, date),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date) REFERENCES dim_date(date)
);

-- 4. Fact Table: Investor Transactions
DROP TABLE IF EXISTS fact_transactions;
CREATE TABLE fact_transactions (
    tx_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id TEXT NOT NULL,
    transaction_date TEXT NOT NULL,
    amfi_code TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    amount_inr REAL NOT NULL,
    state TEXT,
    city TEXT,
    city_tier TEXT,
    age_group TEXT,
    gender TEXT,
    annual_income_lakh REAL,
    payment_mode TEXT,
    kyc_status TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (transaction_date) REFERENCES dim_date(date)
);

-- 5. Fact Table: Scheme Performance
DROP TABLE IF EXISTS fact_performance;
CREATE TABLE fact_performance (
    amfi_code TEXT PRIMARY KEY,
    scheme_name TEXT NOT NULL,
    fund_house TEXT NOT NULL,
    category TEXT NOT NULL,
    plan TEXT,
    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,
    benchmark_3yr_pct REAL,
    alpha REAL,
    beta REAL,
    sharpe_ratio REAL,
    sortino_ratio REAL,
    std_dev_ann_pct REAL,
    max_drawdown_pct REAL,
    aum_crore REAL,
    expense_ratio_pct REAL,
    morningstar_rating INTEGER,
    risk_grade TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- 6. Fact Table: AMC AUM History
DROP TABLE IF EXISTS fact_aum;
CREATE TABLE fact_aum (
    date TEXT NOT NULL,
    fund_house TEXT NOT NULL,
    aum_lakh_crore REAL,
    aum_crore REAL NOT NULL,
    num_schemes INTEGER,
    PRIMARY KEY (date, fund_house)
);

-- 7. Fact Table: Portfolio Holdings
DROP TABLE IF EXISTS fact_portfolio;
CREATE TABLE fact_portfolio (
    amfi_code TEXT NOT NULL,
    stock_symbol TEXT NOT NULL,
    stock_name TEXT NOT NULL,
    sector TEXT,
    weight_pct REAL,
    market_value_cr REAL,
    current_price_inr REAL,
    portfolio_date TEXT NOT NULL,
    PRIMARY KEY (amfi_code, stock_symbol, portfolio_date),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- 8. Fact Table: Industry Monthly SIP Inflows
DROP TABLE IF EXISTS fact_sip_industry;
CREATE TABLE fact_sip_industry (
    month TEXT PRIMARY KEY,
    sip_inflow_crore REAL NOT NULL,
    active_sip_accounts_crore REAL,
    new_sip_accounts_lakh REAL,
    sip_aum_lakh_crore REAL,
    yoy_growth_pct REAL
);

-- 9. Fact Table: Category Inflows
DROP TABLE IF EXISTS fact_category_inflows;
CREATE TABLE fact_category_inflows (
    month TEXT NOT NULL,
    category TEXT NOT NULL,
    net_inflow_crore REAL,
    PRIMARY KEY (month, category)
);

-- 10. Fact Table: Industry Folio Count
DROP TABLE IF EXISTS fact_industry_folios;
CREATE TABLE fact_industry_folios (
    month TEXT PRIMARY KEY,
    total_folios_crore REAL NOT NULL,
    equity_folios_crore REAL,
    debt_folios_crore REAL,
    hybrid_folios_crore REAL,
    others_folios_crore REAL
);

-- 11. Fact Table: Benchmark Indices Daily Prices
DROP TABLE IF EXISTS fact_benchmark_indices;
CREATE TABLE fact_benchmark_indices (
    date TEXT NOT NULL,
    index_name TEXT NOT NULL,
    close_value REAL NOT NULL,
    PRIMARY KEY (date, index_name)
);

-- Indices for optimized queries
CREATE INDEX IF NOT EXISTS idx_nav_amfi_date ON fact_nav(amfi_code, date);
CREATE INDEX IF NOT EXISTS idx_tx_amfi ON fact_transactions(amfi_code);
CREATE INDEX IF NOT EXISTS idx_tx_date ON fact_transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_tx_state ON fact_transactions(state);
