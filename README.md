# NYC Yellow Taxi Data Engineering Project

A data engineering project that ingests, loads, transforms, and analyzes 
NYC Yellow Taxi trip data for the full year 2024 using Python and PostgreSQL.

## What this project does

- Automatically downloads all 12 months of NYC Yellow Taxi trip data (2024) in Parquet format directly from the NYC TLC public dataset
- Loads ~41 million trip records into a PostgreSQL database
- Combines 12 monthly tables into a single unified table for full-year analysis
- Performs data quality checks, identifying and filtering out records with impossible timestamps (trips dated outside 2024)
- Creates a clean, analysis-ready table as a separate layer from raw data
- Optimizes query performance using indexes, achieving 38x speed improvement

## Tech stack

- **Python** : automated data ingestion (urllib, pandas, SQLAlchemy)
- **PostgreSQL** : data storage and querying
- **psycopg2 / SQLAlchemy** : Python-to-database connection layer
- **SQL** : data transformation, cleaning, and analysis
- **Git / GitHub** :version control and project documentation

## Architecture

This project follows a layered ELT (Extract, Load, Transform) design:

[Source]        NYC TLC Public Dataset (Parquet files, hosted on public CDN)

↓

[Extract]       Python (urllib), automated download of 12 monthly files

↓

[Load]          pandas + SQLAlchemy + psycopg2, raw data loaded into PostgreSQL as 12 separate monthly tables (yellow_taxi_2024_01 through _12)

↓

[Transform]     SQL, two transformation layers:
Layer 1: UNION ALL combines 12 tables → yellow_taxi_2024_full

Layer 2: Date filter removes 56 bad records → yellow_taxi_2024_clean

↓

[Serve]         SQL queries against yellow_taxi_2024_clean, single source of truth for all downstream analysis

### Reliability decisions

| Decision | Reason |
|---|---|
| Fresh DB connection per month | Prevents one failed load from cascading into subsequent months |
| Raw layer preserved separately | Bad data decisions are always reversible |
| `IF NOT EXISTS` guards | Pipeline can be safely re-run without crashing |
| Raw data excluded from Git | Parquet files too large for version control, code tracked, data stays local |
| Descriptive commit history | Every pipeline change is auditable and recoverable |

### What would be added in production

- Automated scheduling (Apache Airflow or cron) to run monthly when new TLC data drops
- Row count validation checks after each load to confirm expected data volumes
- Structured error logging per pipeline step with timestamps
- PostgreSQL role-based access control
- Automated database backups
- Cloud storage (AWS S3, Azure Blob) to handle large data files at scale

## Project structure

NYC Taxi/

├── pipeline.py               # End-to-end automated pipeline (download → load → combine → clean)

├── download_taxi_data.py     # Standalone: downloads all 12 months of trip data

├── load_taxi_data.py         # Standalone: loads a single month into PostgreSQL

├── load_all_months.py        # Standalone: loads all 12 months into separate tables

├── combine_months.sql        # Combines all 12 monthly tables into one unified table

├── create_clean_table.sql    # Filters out bad data, creates analysis-ready clean table

├── add_indexes.sql           # Adds datetime index for query performance optimization

├── drop_monthly_tables.sql   # Drops redundant monthly tables to recover disk space

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

## Performance Optimization

Added a datetime index on `yellow_taxi_2024_clean` to dramatically improve query speed:

```sql
CREATE INDEX idx_pickup_datetime ON yellow_taxi_2024_clean (tpep_pickup_datetime);
```

| Metric | Before Index | After Index | Improvement |
|---|---|---|---|
| Query execution time | 23,261 ms | 601 ms | **38x faster** |
| Query type | Full table scan (41M rows) | Index seek (direct lookup) | |

> Tested against a date range filter on 41 million rows using `EXPLAIN ANALYZE`.

## Data quality

- Identified **56 records** with pickup timestamps outside of 2024 (future-dated entries)
- Raw data preserved in `yellow_taxi_2024_full` (41,169,720 rows)
- Clean data stored separately in `yellow_taxi_2024_clean` (41,169,664 rows)
- Filtering approach: `WHERE EXTRACT(YEAR FROM tpep_pickup_datetime) = 2024`

## Data source

[NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

## Status

Pipeline complete : data ingested, loaded, combined, cleaned, optimized and analyzed.
