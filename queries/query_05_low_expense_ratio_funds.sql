-- Query 5: Funds with expense ratio < 1.0%
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
