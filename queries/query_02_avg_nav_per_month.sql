-- Query 2: Average NAV per month across all schemes
SELECT 
    strftime('%Y-%m', date) AS month,
    ROUND(AVG(nav), 4) AS avg_nav,
    ROUND(MIN(nav), 4) AS min_nav,
    ROUND(MAX(nav), 4) AS max_nav
FROM fact_nav
GROUP BY strftime('%Y-%m', date)
ORDER BY month ASC;
