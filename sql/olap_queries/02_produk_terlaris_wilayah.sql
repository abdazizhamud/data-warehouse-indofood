-- Mencari produk yang paling banyak mendominasi kuantitas penjualan di setiap provinsi
WITH RankedProducts AS (
    SELECT 
        r.province,
        p.product_name,
        SUM(f.quantity) AS total_quantity,
        DENSE_RANK() OVER (PARTITION BY r.province ORDER BY SUM(f.quantity) DESC) AS product_rank
    FROM Fact_Sales f
    JOIN Dim_Region r ON f.region_id = r.region_id
    JOIN Dim_Product p ON f.product_id = p.product_id
    GROUP BY r.province, p.product_name
)
SELECT 
    province,
    product_name,
    total_quantity
FROM RankedProducts
WHERE product_rank = 1;