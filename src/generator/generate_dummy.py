import os
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_all_data():
    # Menggunakan seed agar data dummy acak yang dihasilkan konsisten setiap kali dijalankan
    np.random.seed(42)
    random.seed(42)
    
    # Pastikan folder output ada
    os.makedirs('data/staging', exist_ok=True)

    print("Generating dimension master data...")
    
    # Dim_Product (Diperluas menjadi 20 varian produk asli Indofood)
    df_product = pd.DataFrame({
        'product_id': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120],
        'product_name': [
            'Indomie Goreng Spesial', 'Indomie Kuah Rasa Ayam Bawang', 'Indomie Goreng Rendang', 'Indomie Kari Ayam Extra Bawang',
            'Pop Mie Rasa Ayam', 'Pop Mie Goreng Spesial', 'Pop Mie Rasa Baso',
            'Chitato Sapi Panggang', 'Chitato Ayam Bumbu', 'Chitato Lite Rumput Laut',
            'Qtela Singkong Original', 'Qtela Singkong Barbeque',
            'Chiki Balls Keju', 'JetZ Chocolate',
            'Indomilk Susu Cair Cokelat', 'Indomilk Susu Kental Manis Putih',
            'Ichi Ocha Green Tea', 'Club Air Mineral 600ml',
            'Bumbu Racik Ayam Goreng', 'Bumbu Racik Sayur Sop'
        ],
        'brand': [
            'Indomie', 'Indomie', 'Indomie', 'Indomie',
            'Pop Mie', 'Pop Mie', 'Pop Mie',
            'Chitato', 'Chitato', 'Chitato',
            'Qtela', 'Qtela',
            'Chiki', 'JetZ',
            'Indomilk', 'Indomilk',
            'Ichi Ocha', 'Club',
            'Racik', 'Racik'
        ],
        'category': [
            'Noodles', 'Noodles', 'Noodles', 'Noodles',
            'Noodles', 'Noodles', 'Noodles',
            'Snacks', 'Snacks', 'Snacks',
            'Snacks', 'Snacks',
            'Snacks', 'Snacks',
            'Dairy', 'Dairy',
            'Beverages', 'Beverages',
            'Food Ingredients', 'Food Ingredients'
        ],
        'pack_size': [
            '85g', '75g', '91g', '72g',
            '75g', '75g', '75g',
            '68g', '68g', '68g',
            '180g', '180g',
            '55g', '40g',
            '190ml', '370g',
            '350ml', '600ml',
            '20g', '20g'
        ],
        'base_price': [
            3100, 2900, 3300, 3100,
            5000, 5000, 5000,
            11500, 11500, 11000,
            8500, 8500,
            5500, 4500,
            6000, 12500,
            4000, 3000,
            2500, 2500
        ]
    })
    
    # Dim_Distributor
    df_distributor = pd.DataFrame({
        'distributor_id': [201, 202, 203, 204],
        'distributor_name': ['PT Indomarco Adi Prima Jakarta', 'PT Indomarco Adi Prima Bandung', 'PT Sukses Makmur Surabaya', 'PT Distribusi Nusantara Medan'],
        'distributor_type': ['Main Distributor', 'Main Distributor', 'Sub-Distributor', 'Regional Distributor']
    })

    # Dim_Region
    df_region = pd.DataFrame({
        'region_id': [301, 302, 303, 304, 305],
        'province': ['DKI Jakarta', 'Jawa Barat', 'Jawa Timur', 'Sumatera Utara', 'Sulawesi Selatan'],
        'city': ['Jakarta Pusat', 'Bandung', 'Surabaya', 'Medan', 'Makassar'],
        'island': ['Jawa', 'Jawa', 'Jawa', 'Sumatera', 'Sulawesi']
    })

    # Dim_Promotion
    df_promotion = pd.DataFrame({
        'promotion_id': [401, 402, 403, 404],
        'promotion_name': ['No Promotion', 'Promo Gajian Indomaret', 'Diskon Hari Raya', 'Bundling Merdeka'],
        'discount_percentage': [0.0, 0.10, 0.15, 0.05],
        'promo_type': ['None', 'Price Cut', 'Seasonal', 'Bundle']
    })

    # Dim_Customer_Segment
    df_customer_segment = pd.DataFrame({
        'segment_id': [501, 502, 503],
        'segment_name': ['Retail / Modern Market', 'Supermarket', 'Pasar Tradisional']
    })

    # Dim_Warehouse
    df_warehouse = pd.DataFrame({
        'warehouse_id': [601, 602, 603],
        'warehouse_name': ['Gudang Utama Ancol', 'Gudang Regional Leuwi Panjang', 'Gudang Hub Rungkut'],
        'warehouse_location': ['Jakarta', 'Bandung', 'Surabaya']
    })

    # Ekspor Master Dimensi ke Staging Area
    df_product.to_csv('data/staging/raw_products.csv', index=False)
    df_distributor.to_csv('data/staging/raw_distributors.csv', index=False)
    df_region.to_csv('data/staging/raw_regions.csv', index=False)
    df_promotion.to_csv('data/staging/raw_promotions.csv', index=False)
    df_customer_segment.to_csv('data/staging/raw_segments.csv', index=False)
    df_warehouse.to_csv('data/staging/raw_warehouses.csv', index=False)

    print("Generating 1500 raw sales transactions (Staging)...")
    num_sales = 1500
    start_date = datetime(2025, 1, 1)

    # Loop acak mengambil list product_id terbaru yang sudah berisi 20 item
    df_raw_sales = pd.DataFrame({
        'sales_id': [10000 + i for i in range(num_sales)],
        'raw_date': [(start_date + timedelta(days=int(np.random.randint(0, 540)))).strftime('%Y-%m-%d') for _ in range(num_sales)],
        'product_id': [random.choice(df_product['product_id'].tolist()) for _ in range(num_sales)],
        'distributor_id': [random.choice(df_distributor['distributor_id'].tolist()) for _ in range(num_sales)],
        'region_id': [random.choice(df_region['region_id'].tolist()) for _ in range(num_sales)],
        'promotion_id': [random.choice(df_promotion['promotion_id'].tolist()) for _ in range(num_sales)],
        'segment_id': [random.choice(df_customer_segment['segment_id'].tolist()) for _ in range(num_sales)],
        'warehouse_id': [random.choice(df_warehouse['warehouse_id'].tolist()) for _ in range(num_sales)],
        'quantity': [int(np.random.randint(10, 1000)) for _ in range(num_sales)]
    })
    
    df_raw_sales.to_csv('data/staging/raw_sales.csv', index=False)
    print(f"Berhasil memperbarui katalog menjadi 20 produk dan men-generate {num_sales} transaksi penjualan!")

if __name__ == '__main__':
    generate_all_data()