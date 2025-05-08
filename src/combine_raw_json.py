import os

from pyspark.sql import SparkSession

from utils.paths import DATA_BRONZE_DIR, DATA_RAW_DIR
from utils.schema import match_schema


def combine_raw_json_to_bronze():
    spark = SparkSession.builder.appName("Combine Raw JSON to Bronze").getOrCreate()

    input_pattern = os.path.join(DATA_RAW_DIR, "bundesliga_*.json")
    output_path = os.path.join(DATA_BRONZE_DIR, "bundesliga_combined.parquet")

    print(f"Reading from: {input_pattern}")
    df = spark.read.schema(match_schema).json(input_pattern)

    os.makedirs(DATA_BRONZE_DIR, exist_ok=True)
    df.write.mode("overwrite").parquet(output_path)

    print(f"Combined Parquet written to: {output_path}")
    print("Schema preview:")
    df.printSchema()
