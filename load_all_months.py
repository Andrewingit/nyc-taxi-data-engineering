import pandas as pd
from sqlalchemy import create_engine

folder = r'C:\Users\USER\Documents\Data Engineering\DE Projects\NYC Taxi'

for month in range(2, 13):
    month_str = f"{month:02d}"
    table_name = f"yellow_taxi_2024_{month_str}"
    file_path = f"{folder}\\yellow_tripdata_2024-{month_str}.parquet"
 
    print(f"Loading month {month_str}...")
    engine = create_engine('postgresql://postgres:lavida%20loca@localhost:5432/postgres')
    df = pd.read_parquet(file_path)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    engine.dispose()
    print(f"Month {month_str} done! {len(df)} rows loaded.")

print("All months loaded!")