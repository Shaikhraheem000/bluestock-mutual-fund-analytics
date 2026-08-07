-- Query 8: Investor Transaction Distribution by Payment Mode
SELECT 
    payment_mode,
    transaction_type,
    COUNT(tx_id) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr
FROM fact_transactions
GROUP BY payment_mode, transaction_type
ORDER BY total_amount_inr DESC;
