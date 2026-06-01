-- Mengukur kontribusi setiap segmen pelanggan terhadap volume dan pendapatan
SELECT
    s.segment_name,
    SUM(f.quantity) AS total_quantity_sold,
    SUM(f.revenue) AS total_revenue,
    ROUND(100.0 * SUM(f.revenue) / SUM(SUM(f.revenue)) OVER (), 2) AS revenue_share_pct
FROM Fact_Sales f
JOIN Dim_Customer_Segment s ON f.segment_id = s.segment_id
GROUP BY s.segment_name
ORDER BY total_revenue DESC;
