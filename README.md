# GDELT Tech Bubble Analysis (Work in Progress)

This repository contains a work-in-progress, reproducible data engineering and machine learning pipeline studying how global news sentiment (GDELT) relates to technology stock volatility across two major eras—the Dot‑Com bubble (1995–2002) and the modern AI boom (2020–2025).

Although the project is **not yet completed**, the current repository includes a functional AWS-based data pipeline structure, prototype scripts, and early modeling experiments.

---

## 1. Project Overview

This project aims to:

- Collect **GDELT global event data** (1.0 & 2.0)
- Process it into **daily sentiment features** using AWS Glue (PySpark)
- Query processed datasets via **AWS Athena**
- Merge with **Yahoo Finance** stock data
- Train ML models to evaluate if global news sentiment affects tech‑stock volatility

The pipeline is still under active development.  
Many components are already implemented, but the full research and modeling are ongoing.

---

## 2. Repository Structure

```
config/
    project_config.yaml        ← Global configuration

data/
    sample/                    ← Small sample files (no large raw data)
    output/                    ← Example outputs (optional)

scripts/
    init_s3_structure.sh       ← Initialize S3 bucket structure
    run_glue_job.sh            ← Trigger Glue ETL
    run_athena_query.sh        ← Execute Athena query

src/
    data_download/
        gdelt_download.py      ← GDELT ingestion script

    etl/
        gdelt_athena.sql       ← Athena schema
        gdelt_glue_etl.py      ← Glue ETL (PySpark)
        gdelt_transform_csv.py ← Local preprocessing

    modeling/
        dot_com_test.py        ← Prototype ML model for Dot-Com era

LICENSE
requirements.txt
README.md
```

---

## 3. AWS Pipeline (Conceptual)

```
GDELT 15-min data → EC2 ingestion → S3 raw/
        ↓
AWS Glue ETL (PySpark) → S3 processed/ (daily Parquet)
        ↓
AWS Athena (sentiment metrics)
        ↓
Local ML modeling (XGBoost)
```

Daily features include:

- tone_mean  
- goldstein_mean  
- news_volume  
- event_count  
- extreme_negative  

---

## EC2 Ingestion Layer
A small EC2 instance acts as the ingestion layer for GDELT 2.0.  
It runs a cron-based Python script (`gdelt_download.py`) every 15 minutes:

    EC2 → download GDELT → validate → upload to S3 (raw/gdelt/)

This keeps the S3 bucket continuously updated with real-time global-event data.

## 4. Usage (Prototype Stage)

1. Install dependencies  
   ```
   pip install -r requirements.txt
   ```

2. Initialize S3 directory structure  
   ```
   bash scripts/init_s3_structure.sh
   ```

3. Run Glue ETL  
   ```
   bash scripts/run_glue_job.sh
   ```

4. Run Athena queries  
   ```
   bash scripts/run_athena_query.sh
   ```

5. Run the prototype ML model  
   ```
   python src/modeling/dot_com_test.py
   ```

---

## 5. Notes

- This project is **NOT a finished system** — it is under active development.
- No full GDELT datasets are included due to size. Only samples are provided.
- The pipeline is structured to ensure reproducibility once all components are completed.

---

## 6. License

MIT License.