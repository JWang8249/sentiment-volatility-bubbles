📘 GDELT Tech Bubble Analysis

A reproducible AWS data pipeline for analyzing how global news sentiment impacts technology stock volatility across the Dot-Com (1995–2002) and AI Boom (2020–2025) eras.

⭐ 1. Project Overview
This project builds a full data engineering + machine learning pipeline that:
downloads GDELT global event data
processes it into daily sentiment metrics via AWS Glue (PySpark)
queries aggregated data using Athena
merges GDELT sentiment with stock market data (Yahoo Finance)
trains ML models (XGBoost) to study
whether global news affects tech stock volatility
The pipeline is entirely reproducible using the scripts in this repository.

⭐ 2. Repository Structure
SENTIMENT-VOLATILITY-BUBBLE/
│
├── config/
│   └── project_config.yaml            # Global config (paths, AWS, stocks)
│
├── data/
│   ├── sample/                        # Small samples only (not full GDELT)
│   └── output/                        # Example output (optional)
│
├── scripts/
│   ├── init_s3_structure.sh           # Initialize S3 bucket folders
│   ├── run_glue_job.sh                # Trigger Glue ETL job
│   └── run_athena_query.sh            # Run Athena queries
│
├── src/
│   ├── data_download/
│   │   └── gdelt_download.py          # GDELT ingestion script
│   │
│   ├── etl/
│   │   ├── gdelt_athena.sql           # Table schema
│   │   ├── gdelt_glue_etl.py          # Glue PySpark ETL logic
│   │   └── gdelt_transform_csv.py     # Local preprocessing
│   │
│   └── modeling/
│       └── dot_com_test.py            # ML prototype for Dot-Com era
│
├── LICENSE
├── requirements.txt
└── README.md

⭐ 3. AWS Pipeline
GDELT 15-min exports
          ↓
EC2 ingestion (gdelt_download.py)
          ↓
S3 raw/
          ↓
AWS Glue PySpark ETL (gdelt_glue_etl.py)
          ↓
S3 processed/ (Parquet: daily sentiment)
          ↓
Athena SQL analytics
          ↓
Local modeling (dot_com_test.py)


Daily sentiment fields extracted:
tone_mean
goldstein_mean
news_volume
event_count
extreme_negative

⭐ 4. Usage
1) Install dependencies
pip install -r requirements.txt
2) Initialize S3 bucket
bash scripts/init_s3_structure.sh
3) Run Glue ETL job
bash scripts/run_glue_job.sh
4) Query Athena
bash scripts/run_athena_query.sh
5) Run ML prototype
python src/modeling/dot_com_test.py

⭐ 5. Notes
No raw GDELT data is included (too large).
Only small samples are provided in data/sample/.
The full pipeline can be fully reproduced via the scripts.
Suitable for thesis research, data engineering, and financial sentiment analysis.

⭐ 6. License
MIT License.

🟦 Done!