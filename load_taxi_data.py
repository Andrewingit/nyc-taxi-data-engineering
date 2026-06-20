import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Connect to PostgreSQL
engine = create_engine('postgresql://postgres:lavida%20loca@localhost:5432/postgres')

# Load January 2024 parquet file
print("I dey Read parquet file...")
df = pd.read_parquet(r'C:\Users\USER\Documents\Data Engineering\DE Projects\NYC Taxi\yellow_tripdata_2024-01.parquet')

# Load into PostgreSQL
print("I dey Load for PostgreSQL...")
df.to_sql('yellow_taxi_2024_01', engine, if_exists='replace', index=False)

print(f"Hello! Get down {len(df)} rows loaded. E don complete")