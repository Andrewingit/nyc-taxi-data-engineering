import urllib.request

base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-{:02d}.parquet"
save_folder = r"C:\Users\USER\Documents\Data Engineering\DE Projects\NYC Taxi"

for month in range(1, 13):
    url = base_url.format(month)
    filename = f"{save_folder}\\yellow_tripdata_2024-{month:02d}.parquet"
    print(f"Downloading month {month}...")
    urllib.request.urlretrieve(url, filename)
    print(f"Month {month} done!")

print("All downloads Complete Andrew!")