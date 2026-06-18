import os
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_all_data():
    np.random.seed(42)
    random.seed(42)

    os.makedirs('data/staging', exist_ok=True)

    print("Generating dimension master data...")

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

    df_distributor = pd.DataFrame({
        'distributor_id': [201, 202, 203, 204],
        'distributor_name': ['PT Indomarco Adi Prima Jakarta', 'PT Indomarco Adi Prima Bandung', 'PT Sukses Makmur Surabaya', 'PT Distribusi Nusantara Medan'],
        'distributor_type': ['Main Distributor', 'Main Distributor', 'Sub-Distributor', 'Regional Distributor']
    })

    df_region = pd.DataFrame({
        'region_id': [301, 302, 303, 304, 305],
        'province': ['DKI Jakarta', 'Jawa Barat', 'Jawa Timur', 'Sumatera Utara', 'Sulawesi Selatan'],
        'city': ['Jakarta Pusat', 'Bandung', 'Surabaya', 'Medan', 'Makassar'],
        'island': ['Jawa', 'Jawa', 'Jawa', 'Sumatera', 'Sulawesi']
    })

    df_promotion = pd.DataFrame({
        'promotion_id': [401, 402, 403, 404],
        'promotion_name': ['No Promotion', 'Promo Gajian Indomaret', 'Diskon Hari Raya', 'Bundling Merdeka'],
        'discount_percentage': [0.0, 0.10, 0.15, 0.05],
        'promo_type': ['None', 'Price Cut', 'Seasonal', 'Bundle']
    })

    df_customer_segment = pd.DataFrame({
        'segment_id': [501, 502, 503],
        'segment_name': ['Retail / Modern Market', 'Supermarket', 'Pasar Tradisional']
    })

    df_warehouse = pd.DataFrame({
        'warehouse_id': [601, 602, 603],
        'warehouse_name': ['Gudang Utama Ancol', 'Gudang Regional Leuwi Panjang', 'Gudang Hub Rungkut'],
        'warehouse_location': ['Jakarta', 'Bandung', 'Surabaya']
    })

    # -------------------------------------------------------
    # PROMO ELIGIBILITY MAP — tentukan di sini, tidak random
    # -------------------------------------------------------
    # 401 = No Promotion     → semua produk bisa
    # 402 = Promo Gajian     → Indomie & Pop Mie (Noodles)
    # 403 = Diskon Hari Raya → Indomilk, Ichi Ocha, Club, Racik
    # 404 = Bundling Merdeka → Chitato, Qtela, Chiki, JetZ (Snacks)

    promo_eligible_products = {
        402: [101, 102, 103, 104, 105, 106, 107],        # Noodles
        403: [115, 116, 117, 118, 119, 120],              # Dairy, Beverages, Ingredients
        404: [108, 109, 110, 111, 112, 113, 114],         # Snacks
    }

    # Kebalikannya: tiap produk -> promo yang boleh
    # Semua produk selalu bisa dapat 401 (No Promo)
    product_to_eligible_promos = {}
    all_product_ids = df_product['product_id'].tolist()
    for pid in all_product_ids:
        eligible = [401]  # No Promo selalu tersedia
        for promo_id, products in promo_eligible_products.items():
            if pid in products:
                eligible.append(promo_id)
        product_to_eligible_promos[pid] = eligible

    # -------------------------------------------------------

    df_product.to_csv('data/staging/raw_products.csv', index=False)
    df_distributor.to_csv('data/staging/raw_distributors.csv', index=False)
    df_region.to_csv('data/staging/raw_regions.csv', index=False)
    df_promotion.to_csv('data/staging/raw_promotions.csv', index=False)
    df_customer_segment.to_csv('data/staging/raw_segments.csv', index=False)
    df_warehouse.to_csv('data/staging/raw_warehouses.csv', index=False)

    print("Generating 2000 raw sales transactions (Staging) dengan skewness...")
    num_sales = 2000
    start_date = datetime(2025, 1, 1)

    distributor_weights = [0.50, 0.15, 0.25, 0.10]
    warehouse_weights   = [0.50, 0.15, 0.35]
    segment_weights     = [0.35, 0.20, 0.45]
    region_weights      = [0.30, 0.15, 0.20, 0.15, 0.20]

    product_weights = [0.08, 0.07, 0.08, 0.07,
                       0.05, 0.05, 0.04,
                       0.10, 0.08, 0.09,
                       0.03, 0.03,
                       0.04, 0.02,
                       0.06, 0.07,
                       0.02, 0.01,
                       0.01, 0.01]
    product_weights = [w / sum(product_weights) for w in product_weights]

    # Promo weight per eligible slot — kalau produk eligible 2 promo,
    # peluang No Promo 50%, promo aktif 50%
    # Bisa diatur sesuai kebutuhan
    PROMO_ACTIVE_CHANCE = 0.60  # 60% chance kena promo kalau eligible

    sales_data = []

    for i in range(num_sales):
        sale_id = 10000 + i
        raw_date = (start_date + timedelta(days=int(np.random.randint(0, 540)))).strftime('%Y-%m-%d')

        product_id   = int(np.random.choice(all_product_ids, p=product_weights))
        distributor_id = int(np.random.choice(df_distributor['distributor_id'].tolist(), p=distributor_weights))
        region_id    = int(np.random.choice(df_region['region_id'].tolist(), p=region_weights))
        segment_id   = int(np.random.choice(df_customer_segment['segment_id'].tolist(), p=segment_weights))
        warehouse_id = int(np.random.choice(df_warehouse['warehouse_id'].tolist(), p=warehouse_weights))

        # Promo dipilih berdasarkan eligibility produk — bukan random bebas
        eligible_promos = product_to_eligible_promos[product_id]
        active_promos   = [p for p in eligible_promos if p != 401]  # selain No Promo

        if active_promos and random.random() < PROMO_ACTIVE_CHANCE:
            promotion_id = int(random.choice(active_promos))
        else:
            promotion_id = 401  # No Promotion

        # Quantity variance mengikuti promo
        if promotion_id == 404:
            quantity = int(np.random.normal(loc=250, scale=100))
        elif promotion_id == 401:
            quantity = int(np.random.normal(loc=150, scale=80))
        else:
            quantity = int(np.random.normal(loc=200, scale=90))

        quantity = max(10, quantity)

        sales_data.append({
            'sales_id':       sale_id,
            'raw_date':       raw_date,
            'product_id':     product_id,
            'distributor_id': distributor_id,
            'region_id':      region_id,
            'promotion_id':   promotion_id,
            'segment_id':     segment_id,
            'warehouse_id':   warehouse_id,
            'quantity':       quantity,
        })

    df_raw_sales = pd.DataFrame(sales_data)
    df_raw_sales.to_csv('data/staging/raw_sales.csv', index=False)

    print(f"✓ Berhasil generate {num_sales} transaksi!")
    print("  - Promo hanya berlaku untuk produk yang eligible (tidak random)")
    print("  - Jakarta distributor dominan (50% transaksi)")
    print("  - Chitato & Indomie best-sellers")
    print("  - Pasar Tradisional segment terbesar (45%)")
    print()
    print("=== PROMO ELIGIBILITY SUMMARY ===")
    for promo_id, products in promo_eligible_products.items():
        promo_name = df_promotion[df_promotion['promotion_id'] == promo_id]['promotion_name'].values[0]
        brands = df_product[df_product['product_id'].isin(products)]['brand'].unique().tolist()
        print(f"  [{promo_id}] {promo_name}: {', '.join(brands)}")

if __name__ == '__main__':
    generate_all_data()