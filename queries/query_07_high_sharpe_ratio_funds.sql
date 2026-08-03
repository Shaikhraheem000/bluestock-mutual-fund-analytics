-- Query 7: High Sharpe Ratio Schemes (> 2.0)
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
