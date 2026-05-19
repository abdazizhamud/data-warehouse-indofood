import os
import pandas as pd
from sqlalchemy import create_engine, text

def run_etl_load():
    print("=== Memulai Proses ETL Load ke Postgres Docker ===")
    
    # 1. Konfigurasi Koneksi Database (Sesuaikan dengan setup Docker-mu)
    DB_USER = "postgres"
    DB_PASSWORD = "password"  # Ganti dengan password Postgres Docker-mu
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "indofood_dwh"             # Ganti dengan nama database-mu
    DB_ADMIN_NAME = "postgres"           # Database admin default untuk membuat DB baru
    
    # Membuat koneksi string SQLAlchemy
    connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(connection_string)

    # Pastikan database target ada; jika belum, buat dulu.
    try:
        admin_connection_string = (
            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_ADMIN_NAME}"
        )
        admin_engine = create_engine(admin_connection_string)
        with admin_engine.connect() as admin_conn:
            admin_conn = admin_conn.execution_options(isolation_level="AUTOCOMMIT")
            exists = admin_conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
                {"dbname": DB_NAME},
            ).scalar()
            if not exists:
                print(f"Database '{DB_NAME}' belum ada. Membuat database...")
                admin_conn.execute(text(f'CREATE DATABASE "{DB_NAME}"'))
    except Exception as e:
        print(f"\n❌ Gagal memastikan database '{DB_NAME}': {e}")
        return
    
    # 2. Daftar file yang akan di-load (Urutan krusial: Dimensi dulu, baru Fakta!)
    files_to_load = {
        'dim_product': 'data/warehouse/dim_product.csv',
        'dim_time': 'data/warehouse/dim_time.csv',
        'dim_distributor': 'data/warehouse/dim_distributor.csv',
        'dim_region': 'data/warehouse/dim_region.csv',
        'dim_promotion': 'data/warehouse/dim_promotion.csv',
        'dim_customer_segment': 'data/warehouse/dim_customer_segment.csv',
        'dim_warehouse': 'data/warehouse/dim_warehouse.csv',
        'fact_sales': 'data/warehouse/fact_sales.csv' # Terakhir karena butuh Foreign Key dari dimensi
    }
    
    # 3. Eksekusi Load menggunakan pandas.to_sql
    try:
        with engine.connect() as connection:
            for table_name, file_path in files_to_load.items():
                if os.path.exists(file_path):
                    print(f"Loading data dari {file_path} ke tabel '{table_name}'...")
                    
                    # Baca CSV
                    df = pd.read_csv(file_path)
                    
                    # Insert ke Postgres. 
                    # if_exists='append' memastikan data masuk ke struktur tabel yang sudah dibuat lewat schema.sql
                    df.to_sql(name=table_name.lower(), con=engine, if_exists='append', index=False)
                else:
                    print(f"⚠️ Warning: File {file_path} tidak ditemukan. Skip.")
            
        print("\n🎉 Sukses! Semua data berhasil di-load ke Star Schema Postgres Docker-mu.")
        
    except Exception as e:
        print(f"\n❌ Terjadi kesalahan saat loading data: {e}")

if __name__ == '__main__':
    run_etl_load()