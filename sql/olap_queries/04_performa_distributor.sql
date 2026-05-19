-- Menilai performa volume distribusi dan revenue yang dihasilkan oleh setiap mitra distributor
SELECT 
    d.distributor_name,
    d.distributor_type,
    SUM(f.quantity) AS total_volume_distributed,
    SUM(f.revenue) AS total_sales_value,
    COUNT(DISTINCT f.region_id) AS regional_coverage_count
FROM Fact_Sales f
JOIN Dim_Distributor d ON f.distributor_id = d.distributor_id
GROUP BY d.distributor_name, d.distributor_type
ORDER BY total_sales_value DESC;