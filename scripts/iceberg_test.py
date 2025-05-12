from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException



spark = (
    SparkSession
      .builder
      .appName("IcebergTransformJob")
      .getOrCreate()
)


source_table = "local.bronze.users"
target_table = "local.silver.active_users"


df = spark.read.table(source_table)

transform_logic = lambda df: df.filter("is_active = true")
df_transformed = transform_logic(df)

(
    df_transformed.writeTo(target_table)
    .using("iceberg")
    .tableProperty("format-version", "2")
    .createOrReplace()
)