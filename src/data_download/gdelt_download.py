import requests
import boto3
import zipfile
import io
from datetime import datetime, timedelta

BUCKET = "gdelt-thesis-jingyi"
s3 = boto3.client("s3")

START = datetime(2025, 10, 1, 0, 0)
END   = datetime(2025, 10, 1, 23, 45)
delta = timedelta(minutes=15)

current = START

while current <= END:
    dt_str = current.strftime("%Y%m%d%H%M%S")
    url = f"http://data.gdeltproject.org/gdeltv2/{dt_str}.export.CSV.zip"

    print("Downloading:", url)
    r = requests.get(url, timeout=30)

    if r.status_code == 200:
        try:
            z = zipfile.ZipFile(io.BytesIO(r.content))
            tsv_name = z.namelist()[0]

            print("Extracting:", tsv_name)
            tsv_bytes = z.read(tsv_name)

            key = f"raw/gdelt/{dt_str}.csv"
            print("Uploading to S3:", key)

            s3.put_object(
                Bucket=BUCKET,
                Key=key,
                Body=tsv_bytes
            )

        except Exception as e:
            print("Error extracting zip:", e)

    else:
        print("Skip (HTTP", r.status_code, "):", url)

    current += delta

print("Finished!")
