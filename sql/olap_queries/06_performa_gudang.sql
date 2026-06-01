-- Menilai performa distribusi dan pendapatan dari setiap gudang
SELECT
    w.warehouse_name,
    w.warehouse_location,
    SUM(f.quantity) AS total_quantity_handled,
    SUM(f.revenue) AS total_revenue,
    COUNT(DISTINCT f.region_id) AS regions_served
FROM Fact_Sales f
JOIN Dim_Warehouse w ON f.warehouse_id = w.warehouse_id
GROUP BY w.warehouse_name, w.warehouse_location
ORDER BY total_revenue DESC;
