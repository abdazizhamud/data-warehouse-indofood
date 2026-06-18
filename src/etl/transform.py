import os
from pathlib import Path
import pandas as pd

def run_etl_transform():
    print("Memulai proses ETL Extract & Transform...")

    # Root proyek adalah dua level di atas folder src/etl
    base_dir = Path(__file__).resolve().parents[2]
    staging_dir = base_dir / 'data' / 'staging'
    warehouse_dir = base_dir / 'data' / 'warehouse'

    # EXTRACT: Membaca file dari staging area
    df_raw_sales = pd.read_csv(staging_dir / 'raw_sales.csv')
    df_product = pd.read_csv(staging_dir / 'raw_products.csv')
    df_promotion = pd.read_csv(staging_dir / 'raw_promotions.csv')
    df_distributor = pd.read_csv(staging_dir / 'raw_distributors.csv')
    df_region = pd.read_csv(staging_dir / 'raw_regions.csv')
    df_segment = pd.read_csv(staging_dir / 'raw_segments.csv')
    df_warehouse = pd.read_csv(staging_dir / 'raw_warehouses.csv')

    # TRANSFORM 1: Membuat Dim_Time secara dinamis berdasarkan data penjualan unik
    print("Mentransformasi Dim_Time...")
    unique_dates = pd.to_datetime(df_raw_sales['raw_date'].unique()).sort_values()
    df_time = pd.DataFrame({
        'date_id': [int(dt.strftime('%Y%m%d')) for dt in unique_dates],
        'date': unique_dates.strftime('%Y-%m-%d'),
        'month': [dt.month for dt in unique_dates],
        'quarter': [((dt.month - 1) // 3) + 1 for dt in unique_dates],
        'year': [dt.year for dt in unique_dates]
    })

    # TRANSFORM 2: Memproses Fact_Sales (Lookup Data & Penghitungan Kalkulatif)
    print("Mentransformasi Fact_Sales & menghitung revenue bersih...")
    # Lookup Base Price produk
    df_fact = df_raw_sales.merge(df_product[['product_id', 'base_price']], on='product_id', how='left')
    # Lookup Persentase Diskon dari Promosi
    df_fact = df_fact.merge(df_promotion[['promotion_id', 'discount_percentage']], on='promotion_id', how='left')
    
    # Mengubah format tanggal mentah menjadi date_id (integer YYYYMMDD) pendukung join Star Schema
    df_fact['date_id'] = pd.to_datetime(df_fact['raw_date']).dt.strftime('%Y%m%d').astype(int)
    
    # Penghitungan Rumus Bisnis: Revenue = Qty * Price * (1 - Discount)
    df_fact['revenue'] = df_fact['quantity'] * df_fact['base_price'] * (1 - df_fact['discount_percentage'])
    df_fact['revenue'] = df_fact['revenue'].round(2)

    # Memilah field akhir yang akan di-load sesuai arsitektur skema DWH Fact_Sales
    df_fact_sales = df_fact[[
        'sales_id', 'date_id', 'product_id', 'distributor_id', 
        'region_id', 'promotion_id', 'segment_id', 'warehouse_id', 
        'quantity', 'revenue'
    ]]

    # Drop kolom internal 'base_price' dari master data produk sebelum di-load ke database target
    df_product_final = df_product.drop(columns=['base_price'])

    # LOAD SIMULATION: Simpan versi clean & ready ke folder lokal / siap di-push ke database
    print(f"Menyimpan hasil transformasi ke '{warehouse_dir}/'...")
    warehouse_dir.mkdir(parents=True, exist_ok=True)
    
    df_fact_sales.to_csv(warehouse_dir / 'fact_sales.csv', index=False)
    df_time.to_csv(warehouse_dir / 'dim_time.csv', index=False)
    df_product_final.to_csv(warehouse_dir / 'dim_product.csv', index=False)
    df_distributor.to_csv(warehouse_dir / 'dim_distributor.csv', index=False)
    df_region.to_csv(warehouse_dir / 'dim_region.csv', index=False)
    df_promotion.to_csv(warehouse_dir / 'dim_promotion.csv', index=False)
    df_segment.to_csv(warehouse_dir / 'dim_customer_segment.csv', index=False)
    df_warehouse.to_csv(warehouse_dir / 'dim_warehouse.csv', index=False)
    
    print("Proses ETL Transformasi Selesai!")

if __name__ == '__main__':
    run_etl_transform()