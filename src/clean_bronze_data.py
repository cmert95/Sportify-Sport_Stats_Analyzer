import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, trim, when
from pyspark.sql.types import StringType, StructType

from utils.paths import DATA_BRONZE_DIR, DATA_SILVER_DIR


def normalize_all_strings_recursive(df, schema=None, prefix=""):
    """
    Recursively converts empty strings to null in all StringType columns.
    Works for both flat and nested struct fields.
    """
    if schema is None:
        schema = df.schema

    for field in schema.fields:
        field_name = f"{prefix}.{field.name}" if prefix else field.name

        if isinstance(field.dataType, StringType):
            df = df.withColumn(
                field_name, when(trim(col(field_name)) == "", None).otherwise(col(field_name))
            )

        elif isinstance(field.dataType, StructType):
            df = normalize_all_strings_recursive(df, field.dataType, field_name)

    return df


def filter_invalid_rows(df):
    return df.filter(
        col("matchID").isNotNull()
        & col("matchDateTimeUTC").isNotNull()
        & col("team1.teamName").isNotNull()
        & col("team2.teamName").isNotNull()
    )


def apply_transformations(df):
    df = df.withColumn("matchDateTimeUTC", to_timestamp("matchDateTimeUTC"))

    df = df.withColumn(
        "numberOfViewers",
        when(col("numberOfViewers").isNull(), 0).otherwise(col("numberOfViewers")),
    )

    df = df.dropDuplicates(["matchID"])
    df = df.drop("timeZoneID")

    return df


def log_counts(before, after):
    print(f"Rows before cleaning: {before}, after cleaning: {after}")


def clean_bronze_data():
    spark = SparkSession.builder.appName("Clean Bronze Data").getOrCreate()

    input_path = os.path.join(DATA_BRONZE_DIR, "bundesliga_combined.parquet")
    output_path = os.path.join(DATA_SILVER_DIR, "clean_matches.parquet")

    df = spark.read.parquet(input_path)
    initial_count = df.count()

    df = normalize_all_strings_recursive(df)
    df = filter_invalid_rows(df)
    df = apply_transformations(df)

    final_count = df.count()
    log_counts(initial_count, final_count)

    os.makedirs(DATA_SILVER_DIR, exist_ok=True)
    df.write.mode("overwrite").parquet(output_path)

    print(f"Cleaned silver data written to: {output_path}")
    df.select(
        "matchID", "matchDateTimeUTC", "team1.teamName", "team2.teamName", "numberOfViewers"
    ).show(3, truncate=False)
