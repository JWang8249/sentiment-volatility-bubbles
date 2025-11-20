#!/bin/bash

QUERY="SELECT * FROM gdelt_daily_parquet ORDER BY date LIMIT 20;"
DATABASE="gdelt_db"
OUTPUT="s3://gdelt-thesis-jingyi/athena_query_results/"
REGION="eu-west-1"

echo "Running Athena query..."

QUERY_EXECUTION_ID=$(aws athena start-query-execution \
    --query-string "$QUERY" \
    --query-execution-context Database=$DATABASE \
    --result-configuration OutputLocation=$OUTPUT \
    --region $REGION \
    --query "QueryExecutionId" \
    --output text)

echo "QueryExecutionId: $QUERY_EXECUTION_ID"
echo "Waiting for Athena execution..."

STATUS="RUNNING"

while [ "$STATUS" = "RUNNING" ] || [ "$STATUS" = "QUEUED" ]
do
    sleep 2
    STATUS=$(aws athena get-query-execution \
        --query-execution-id $QUERY_EXECUTION_ID \
        --query "QueryExecution.Status.State" \
        --output text)
    echo "Status: $STATUS"
done

if [ "$STATUS" = "SUCCEEDED" ]; then
    echo "Query succeeded."
    echo "Results stored at: ${OUTPUT}${QUERY_EXECUTION_ID}.csv"
else
    echo "Query failed or cancelled."
fi
