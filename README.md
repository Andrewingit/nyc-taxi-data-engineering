# NYC Yellow Taxi Data Engineering Project

A data engineering project that ingests, loads, transforms, and analyzes 
NYC Yellow Taxi trip data for the full year 2024 using Python and PostgreSQL.

## What this project does

- Automatically downloads all 12 months of NYC Yellow Taxi trip data (2024) 
  in Parquet format directly from the NYC TLC public dataset
- Loads ~41 million trip records into a PostgreSQL database
- Combines 12 monthly tables into a single unified table for full-year analysis
- Performs data quality checks — identifying and filtering out records with 
  impossible timestamps (trips dated outside 2024)
- Creates a clean, analysis-ready table as a separate layer from raw data
- Includes SQL queries for exploring patterns across the full dataset

## Tech stack

- **Python** — automated data ingestion (urllib, pandas, SQLAlchemy)
- **PostgreSQL** — data storage and querying
- **psycopg2 / SQLAlchemy** — Python-to-database connection layer
- **SQL** — data transformation, cleaning, and analysis
- **Git / GitHub** — version control and project documentation

## Project structure
NYC Taxi/

├── download_taxi_data.py     # Automatically downloads all 12 months of trip data

├── load_taxi_data.py         # Loads a single month into PostgreSQL

├── load_all_months.py        # Loads all 12 months into separate monthly tables

├── combine_months.sql        # Combines all 12 monthly tables into one unified table

├── create_clean_table.sql    # Filters out bad data, creates analysis-ready clean table

├── .gitignore                # Excludes large raw data files from version control

## Key findings (Full Year 2024)

Based on **41,169,664 cleaned taxi trips** across all 12 months:

| Metric | Result |
|---|---|
| Total trips | 41,169,664 |
| Average fare | $19.27 |
| Busiest month | October (3,833,780 trips) |
| Peak hours | 6PM, 5PM, 7PM, 3PM |
| #1 pickup zone | JFK Airport (1,989,986 trips) |
| Top 5 pickup zones | JFK Airport, Upper East Side South, Midtown Center, Upper East Side North, Midtown East |

## Data quality

- Identified **56 records** with pickup timestamps outside of 2024 (future-dated entries)
- Raw data preserved in `yellow_taxi_2024_full` (41,169,720 rows)
- Clean data stored separately in `yellow_taxi_2024_clean` (41,169,664 rows)
- Filtering approach: `WHERE EXTRACT(YEAR FROM tpep_pickup_datetime) = 2024`

## Data source

[NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

## Status

✅ Pipeline complete — data ingested, loaded, combined, cleaned and analyzed.