-- Query 4: Total Transaction Volume and Amount by State
SELECT 
    state,
    COUNT(tx_id) AS total_transactions,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr,
    ROUND(AVG(amount_inr), 2) AS avg_transaction_amount_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_amount_inr DESC;
