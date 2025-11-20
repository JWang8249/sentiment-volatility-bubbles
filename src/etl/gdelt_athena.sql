CREATE EXTERNAL TABLE IF NOT EXISTS gdelt_daily_parquet (
    date date,
    tone_mean double,
    goldstein_mean double,
    news_volume int,
    event_count int,
    extreme_negative int
)
STORED AS PARQUET
LOCATION 's3://gdelt-thesis-jingyi/processed/gdelt_daily/';

SELECT * FROM gdelt_daily_parquet ORDER BY date;