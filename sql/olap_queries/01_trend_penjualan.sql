-- Analisis tren penjualan bulanan/tahunan berdasarkan brand dan produk
SELECT 
    t.year,
    t.month,
    p.brand,
    p.product_name,
    SUM(f.quantity) AS total_quantity_sold,
    SUM(f.revenue) AS total_revenue
FROM Fact_Sales f
JOIN Dim_Time t ON f.date_id = t.date_id
JOIN Dim_Product p ON f.product_id = p.product_id
GROUP BY t.year, t.month, p.brand, p.product_name
ORDER BY t.year DESC, t.month DESC, total_revenue DESC;