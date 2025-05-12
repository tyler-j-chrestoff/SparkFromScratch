from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("BootstrapBronzeTables")
    .getOrCreate()
)

print("Bootstrapping dummy bronze.users table...")

df = spark.createDataFrame([
    (1, "Alice", True),
    (2, "Bob", False),
    (3, "Charlie", True),
], ["user_id", "name", "is_active"])

(
    df.writeTo("local.bronze.users")
    .using("iceberg")
    .tableProperty("format-version", "2")
    .createOrReplace()
)

print("Bootstrap complete.")