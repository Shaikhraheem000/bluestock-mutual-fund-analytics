-- Query 6: Top 5 schemes by 3-Year CAGR Return
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
