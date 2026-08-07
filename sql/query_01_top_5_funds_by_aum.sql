-- Query 1: Top 5 funds by AUM
SELECT 
    amfi_code,
    scheme_name,
    fund_house,
    category,
    aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;
