-- Query 3: Monthly SIP Inflows and YoY Growth
SELECT 
    month,
    sip_inflow_crore,
    active_sip_accounts_crore,
    yoy_growth_pct
FROM fact_sip_industry
ORDER BY month ASC;
