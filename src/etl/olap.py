import glob
import os
from pathlib import Path

import duckdb

BASE_DIR = Path(__file__).resolve().parents[2]
WAREHOUSE_DIR = BASE_DIR / "data" / "warehouse"
QUERY_DIR = BASE_DIR / "sql" / "olap_queries"
OUTPUT_DIR = BASE_DIR / "data" / "olap_results"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

con = duckdb.connect()

# Map CSV file names to SQL view names
csv_to_view = {
    "fact_sales.csv": "Fact_Sales",
    "dim_time.csv": "Dim_Time",
    "dim_product.csv": "Dim_Product",
    "dim_distributor.csv": "Dim_Distributor",
    "dim_region.csv": "Dim_Region",
    "dim_promotion.csv": "Dim_Promotion",
    "dim_customer_segment.csv": "Dim_Customer_Segment",
    "dim_warehouse.csv": "Dim_Warehouse",
}

for csv_name, view_name in csv_to_view.items():
    csv_path = WAREHOUSE_DIR / csv_name
    con.execute(
        f"""
        CREATE OR REPLACE VIEW {view_name} AS
        SELECT * FROM read_csv_auto('{csv_path.as_posix()}')
        """
    )

sql_files = sorted(glob.glob(str(QUERY_DIR / "*.sql")))

for sql_path in sql_files:
    sql_text = Path(sql_path).read_text(encoding="utf-8")
    result_df = con.execute(sql_text).df()

    out_name = Path(sql_path).stem + ".csv"
    out_path = OUTPUT_DIR / out_name
    result_df.to_csv(out_path, index=False)

print(f"Saved {len(sql_files)} result files to {OUTPUT_DIR}")