-- Query 10: Category-wise Total Net Inflows Summary
SELECT 
    category,
    ROUND(SUM(net_inflow_crore), 2) AS total_net_inflow_crore,
    ROUND(AVG(net_inflow_crore), 2) AS avg_monthly_net_inflow_crore
FROM fact_category_inflows
GROUP BY category
ORDER BY total_net_inflow_crore DESC;
