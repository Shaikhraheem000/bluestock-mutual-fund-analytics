-- Query 9: Top Held Stocks Across Portfolios by Total Weight
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
