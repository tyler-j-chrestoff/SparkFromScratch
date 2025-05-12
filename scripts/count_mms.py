import sys

from pyspark.sql import SparkSession


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: count_mms <file>", file=sys.stderr)
        sys.exit(-1)


    spark = (SparkSession
      .builder
      .appName("PythonMnMCount")
      .getOrCreate())

    mnm_file = sys.argv[1]

    mnm_df = (spark.read.format("csv")
      .option("header", "true")
      .option("inferSchema", "true")
      .load(mnm_file))

    count_mnm_df = (mnm_df
      .select("State", "Color", "Count")
      .groupBy("State", "Color")
      .sum("Count")
      .orderBy("sum(Count)", ascending=False))

    count_mnm_df.show(n=60, truncate=False)
    print("Total Rows = %d" % (count_mnm_df.count()))


    ca_count_mnm_df = (mnm_df
      .select("State", "Color", "Count")
      .where(mnm_df.State == "CA")
      .groupBy("State", "Color")
      .sum("Count")
      .orderBy("sum(Count)", ascending=False))

    ca_count_mnm_df.show(n=10, truncate=False)

    spark.stop()
