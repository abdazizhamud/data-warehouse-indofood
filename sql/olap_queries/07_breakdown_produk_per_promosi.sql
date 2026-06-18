-- Melihat produk dan merek apa saja yang terlibat dalam setiap promosi
SELECT
    pr.promotion_name,
    pr.promo_type,
    pr.discount_percentage,
    p.brand,
    p.product_name,
    COUNT(f.sales_id)   AS total_transactions,
    SUM(f.quantity)     AS total_quantity_sold,
    SUM(f.revenue)      AS total_revenue
FROM Fact_Sales f
JOIN Dim_Promotion pr ON f.promotion_id = pr.promotion_id
JOIN Dim_Product p    ON f.product_id   = p.product_id
WHERE pr.promotion_id != 401  -- exclude No Promotion
GROUP BY pr.promotion_name, pr.promo_type, pr.discount_percentage, p.brand, p.product_name
ORDER BY pr.promotion_name, total_revenue DESC;