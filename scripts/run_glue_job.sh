#!/bin/bash

JOB_NAME="gdelt_daily_etl"
REGION="eu-west-1"

echo "Starting Glue job: $JOB_NAME ..."

aws glue start-job-run \
    --job-name $JOB_NAME \
    --region $REGION \
    > glue_job_run.json

echo "Glue ETL Job triggered."
echo "Job run ID saved to glue_job_run.json"
