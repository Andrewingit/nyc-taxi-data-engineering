import urllib.request
import pandas as pd
from sqlalchemy import create_engine, text

# ============================================================
# CONFIGURATION
# ============================================================
DB_URL = 'postgresql://postgres:lavida%20loca@localhost:5432/postgres'
FOLDER = r'C:\Users\USER\Documents\Data Engineering\DE Projects\NYC Taxi'
YEAR = 2024
MONTHS = range(1, 13)

# ============================================================
# STEP 1: DOWNLOAD
# ============================================================
def download_data():
    print("\n--- STEP 1: DOWNLOADING DATA ---")
    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet"
    for month in MONTHS:
        url = base_url.format(year=YEAR, month=month)
        filename = f"{FOLDER}\\yellow_tripdata_{YEAR}-{month:02d}.parquet"
        print(f"Downloading month {month:02d}...")
        urllib.request.urlretrieve(url, filename)
        print(f"Month {month:02d} downloaded!")
    print("All files downloaded!")

# ============================================================
# STEP 2: LOAD INTO POSTGRESQL
# ============================================================
def load_data():
    print("\n--- STEP 2: LOADING INTO POSTGRESQL ---")
    for month in MONTHS:
        month_str = f"{month:02d}"
        table_name = f"yellow_taxi_{YEAR}_{month_str}"
        file_path = f"{FOLDER}\\yellow_tripdata_{YEAR}-{month_str}.parquet"
        print(f"Loading month {month_str}...")
        engine = create_engine(DB_URL)
        df = pd.read_parquet(file_path)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        engine.dispose()
        print(f"Month {month_str} done! {len(df)} rows loaded.")
    print("All months loaded!")

# ============================================================
# STEP 3: COMBINE INTO ONE TABLE
# ============================================================
def combine_data():
    print("\n--- STEP 3: COMBINING INTO ONE TABLE ---")
    engine = create_engine(DB_URL)
    union_parts = " UNION ALL ".join(
        [f"SELECT * FROM yellow_taxi_{YEAR}_{month:02d}" for month in MONTHS]
    )
    sql = f"CREATE TABLE IF NOT EXISTS yellow_taxi_{YEAR}_full AS {union_parts};"
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
    engine.dispose()
    print(f"Combined table yellow_taxi_{YEAR}_full created!")

# ============================================================
# STEP 4: CLEAN THE DATA
# ============================================================
def clean_data():
    print("\n--- STEP 4: CLEANING DATA ---")
    engine = create_engine(DB_URL)
    sql = f"""
        CREATE TABLE IF NOT EXISTS yellow_taxi_{YEAR}_clean AS
        SELECT * FROM yellow_taxi_{YEAR}_full
        WHERE EXTRACT(YEAR FROM tpep_pickup_datetime) = {YEAR};
    """
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
    engine.dispose()
    print(f"Clean table yellow_taxi_{YEAR}_clean created!")

# ============================================================
# RUN THE PIPELINE
# ============================================================
if __name__ == "__main__":
    print("========================================")
    print("   NYC TAXI DATA PIPELINE STARTING...   ")
    print("========================================")
    download_data()
    load_data()
    combine_data()
    clean_data()
    print("\n========================================")
    print("   PIPELINE COMPLETE!                   ")
    print("========================================")