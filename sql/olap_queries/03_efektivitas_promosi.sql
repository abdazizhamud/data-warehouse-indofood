-- Mengevaluasi performa finansial yang dihasilkan oleh setiap jenis promosi
SELECT 
    pr.promotion_name,
    pr.promo_type,
    COUNT(f.sales_id) AS total_transactions,
    SUM(f.quantity) AS total_items_sold,
    SUM(f.revenue) AS total_revenue_generated,
    ROUND(AVG(f.revenue), 2) AS average_transaction_value
FROM Fact_Sales f
JOIN Dim_Promotion pr ON f.promotion_id = pr.promotion_id
GROUP BY pr.promotion_name, pr.promo_type
ORDER BY total_revenue_generated DESC;