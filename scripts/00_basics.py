from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SparkBasics").getOrCreate()

df = spark.range(1, 11)
df.show()

df_filtered = df.filter("id % 2 = 0")
df_filtered.show()
