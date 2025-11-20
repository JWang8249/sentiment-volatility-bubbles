import sys
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import functions as F

# -------------------------
# Init
# -------------------------
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# -------------------------
# Load raw GDELT 2.0 data
# -------------------------
raw = spark.read.text("s3://gdelt-thesis-jingyi/raw/gdelt/")
df = raw.withColumn("cols", F.split(F.col("value"), "\t"))

# Only keep rows with at least 40 columns (your data has ~ 40+)
df = df.withColumn("col_count", F.size("cols"))
df = df.filter(F.col("col_count") >= 40)

# -------------------------
# Field mapping - STRICTLY based on your real data
#
# Verified from your dataset:
#  Index 1  = SQLDATE ("20251001000000")
#  Index 6  = Actor1Name
#  Index 27 = GoldsteinScale
#  Index 30 = NumArticles
#  Index 31 = AvgTone
# -------------------------
df = df.select(
    F.col("cols")[1].alias("SQLDATE"),
    F.col("cols")[6].alias("Actor1Name"),
    F.col("cols")[27].alias("Goldstein"),
    F.col("cols")[30].alias("NumArticles"),
    F.col("cols")[31].alias("AvgTone")
)

# -------------------------
# Clean and convert types
# -------------------------
df = df.withColumn("NumArticles", F.col("NumArticles").cast("int"))
df = df.withColumn("Goldstein", F.col("Goldstein").cast("double"))
df = df.withColumn("AvgTone", F.col("AvgTone").cast("double"))
df = df.withColumn("date", F.to_date("SQLDATE", "yyyyMMdd"))

# Drop invalid date
df = df.filter(F.col("date").isNotNull())

# -------------------------
# Filter tech companies (case-insensitive)
# -------------------------
companies = [
    "nvidia", "amd", "intel", "tsmc",
    "microsoft", "meta", "amazon",
    "apple", "tesla", "google", "alphabet"
]
regex = "|".join(companies)

df = df.withColumn("Actor1Name", F.lower("Actor1Name"))
df_tech = df.filter(F.col("Actor1Name").rlike(regex))

# -------------------------
# Daily Aggregation
# -------------------------
daily = df_tech.groupBy("date").agg(
    F.avg("AvgTone").alias("tone_mean"),
    F.avg("Goldstein").alias("goldstein_mean"),
    F.sum("NumArticles").alias("news_volume"),
    F.count("*").alias("event_count"),
    F.sum(F.when(F.col("AvgTone") < -5, 1).otherwise(0)).alias("extreme_negative")
)

# -------------------------
# Save to S3
# -------------------------
daily.write.mode("overwrite").parquet(
    "s3://gdelt-thesis-jingyi/processed/gdelt_daily/"
)

job.commit()
print("Job finished successfully.")