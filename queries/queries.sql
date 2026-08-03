-- Day 02 Analytical SQL Queries
-- Database: bluestock_mf.db

-- ============================================================
-- Query 1: Top 5 funds by AUM
-- ============================================================
SELECT 
    amfi_code,
    scheme_name,
    fund_house,
    category,
    aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;

-- ============================================================
-- Query 2: Average NAV per month across all schemes
-- ============================================================
SELECT 
    strftime('%Y-%m', date) AS month,
    ROUND(AVG(nav), 4) AS avg_nav,
    ROUND(MIN(nav), 4) AS min_nav,
    ROUND(MAX(nav), 4) AS max_nav
FROM fact_nav
GROUP BY strftime('%Y-%m', date)
ORDER BY month ASC;

-- ============================================================
-- Query 3: Monthly SIP Inflows and YoY Growth
-- ============================================================
SELECT 
    month,
    sip_inflow_crore,
    active_sip_accounts_crore,
    yoy_growth_pct
FROM fact_sip_industry
ORDER BY month ASC;

-- ============================================================
-- Query 4: Total Transaction Volume and Amount by State
-- ============================================================
SELECT 
    state,
    COUNT(tx_id) AS total_transactions,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr,
    ROUND(AVG(amount_inr), 2) AS avg_transaction_amount_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_amount_inr DESC;

-- ============================================================
-- Query 5: Funds with expense ratio < 1.0%
-- ============================================================
SELECT 
    amfi_code,
    scheme_name,
    fund_house,
    category,
    expense_ratio_pct,
    return_3yr_pct
FROM fact_performance
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- ============================================================
-- Query 6: Top 5 schemes by 3-Year CAGR Return
-- ============================================================
SELECT 
    amfi_code,
    scheme_name,
    fund_house,
    category,
    return_3yr_pct,
    benchmark_3yr_pct,
    alpha
FROM fact_performance
ORDER BY return_3yr_pct DESC
LIMIT 5;

-- ============================================================
-- Query 7: High Sharpe Ratio Schemes (> 2.0)
-- ============================================================
SELECT 
    amfi_code,
    scheme_name,
    fund_house,
    sharpe_ratio,
    sortino_ratio,
    risk_grade
FROM fact_performance
WHERE sharpe_ratio > 2.0
ORDER BY sharpe_ratio DESC;

-- ============================================================
-- Query 8: Investor Transaction Distribution by Payment Mode
-- ============================================================
SELECT 
    payment_mode,
    transaction_type,
    COUNT(tx_id) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr
FROM fact_transactions
GROUP BY payment_mode, transaction_type
ORDER BY total_amount_inr DESC;

-- ============================================================
-- Query 9: Top Held Stocks Across Portfolios by Total Weight
-- ============================================================
SELECT 
    stock_symbol,
    stock_name,
    sector,
    COUNT(DISTINCT amfi_code) AS num_funds_holding,
    ROUND(AVG(weight_pct), 2) AS avg_portfolio_weight_pct
FROM fact_portfolio
GROUP BY stock_symbol, stock_name, sector
ORDER BY avg_portfolio_weight_pct DESC
LIMIT 10;

-- ============================================================
-- Query 10: Category-wise Total Net Inflows Summary
-- ============================================================
SELECT 
    category,
    ROUND(SUM(net_inflow_crore), 2) AS total_net_inflow_crore,
    ROUND(AVG(net_inflow_crore), 2) AS avg_monthly_net_inflow_crore
FROM fact_category_inflows
GROUP BY category
ORDER BY total_net_inflow_crore DESC;
