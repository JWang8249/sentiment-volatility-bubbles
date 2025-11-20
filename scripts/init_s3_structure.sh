#!/bin/bash

BUCKET="gdelt-thesis-jingyi"

echo "Initializing S3 folder structure for bucket: $BUCKET"

aws s3api head-bucket --bucket $BUCKET 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Bucket does not exist. Creating S3 bucket..."
    aws s3api create-bucket \
        --bucket $BUCKET \
        --region eu-west-1 \
        --create-bucket-configuration LocationConstraint=eu-west-1
fi

echo "Creating folder prefixes..."
aws s3api put-object --bucket $BUCKET --key "raw/gdelt/"
aws s3api put-object --bucket $BUCKET --key "processed/gdelt_daily/"
aws s3api put-object --bucket $BUCKET --key "glue_temp/"
aws s3api put-object --bucket $BUCKET --key "athena_query_results/"
aws s3api put-object --bucket $BUCKET --key "sample/"

echo "S3 initialization complete!"
