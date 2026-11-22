
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("ValidateProducts").getOrCreate()

hconf = spark.sparkContext._jsc.hadoopConfiguration()
hconf.set("fs.s3a.endpoint", "http://floci:4566")
hconf.set("fs.s3a.path.style.access", "true")
hconf.set("fs.s3a.connection.ssl.enabled", "false")
hconf.set("fs.s3a.access.key", "test")
hconf.set("fs.s3a.secret.key", "test")
hconf.set(
    "fs.s3a.aws.credentials.provider",
    "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider"
)

spark.conf.set(
    "spark.sql.catalog.lakehouse",
    "org.apache.iceberg.spark.SparkCatalog"
)
spark.conf.set("spark.sql.catalog.lakehouse.type", "hadoop")
spark.conf.set(
    "spark.sql.catalog.lakehouse.warehouse",
    "s3a://ucv-data-platform/products"
)

silver = spark.table("lakehouse.silver.products")
gold = spark.table("lakehouse.gold.product_category_summary")

silver_count = silver.count()
gold_count = gold.count()

duplicate_count = (
    silver.groupBy("product_id")
    .count()
    .filter(F.col("count") > 1)
    .count()
)

invalid_silver = silver.filter(
    F.col("product_id").isNull() |
    F.col("price").isNull() |
    (F.col("price") <= 0)
).count()

invalid_gold = gold.filter(
    F.col("category").isNull() |
    F.col("product_count").isNull() |
    (F.col("product_count") <= 0) |
    F.col("average_price").isNull() |
    (F.col("average_price") <= 0)
).count()

gold_total = gold.agg(
    F.sum("product_count").alias("total")
).first()["total"]

print("\n========== VALIDACION FINAL ==========")
print(f"Silver rows: {silver_count}")
print(f"Gold rows: {gold_count}")
print(f"Duplicated product IDs: {duplicate_count}")
print(f"Invalid Silver rows: {invalid_silver}")
print(f"Invalid Gold rows: {invalid_gold}")
print(f"Gold products total: {gold_total}")
duplicated_categories = (
    gold.groupBy("category")
    .count()
    .filter(F.col("count") > 1)
    .count()
)

print(f"Duplicated Gold categories: {duplicated_categories}")
assert duplicated_categories == 0

assert duplicate_count == 0
assert invalid_silver == 0
assert invalid_gold == 0
assert silver_count == gold_total

print("RESULTADO: VALIDACIONES OK")
spark.stop()
