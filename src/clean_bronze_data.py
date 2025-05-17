import os

from pyspark.sql.functions import col, to_timestamp, trim, when
from pyspark.sql.types import StringType, StructType

from utils.logger import setup_logger
from utils.paths import DATA_BRONZE_DIR, DATA_SILVER_DIR

logger = setup_logger(__name__, log_name="clean_data")


def normalize_all_strings_recursive(df, schema=None, prefix=""):
    """Recursively trims strings and replaces empty strings with nulls in StringType fields."""
    if schema is None:
        schema = df.schema

    for field in schema.fields:
        field_name = f"{prefix}.{field.name}" if prefix else field.name

        if isinstance(field.dataType, StringType):
            df = df.withColumn(
                field_name, when(trim(col(field_name)) == "", None).otherwise(trim(col(field_name)))
            )
        elif isinstance(field.dataType, StructType):
            df = normalize_all_strings_recursive(df, field.dataType, field_name)

    return df


def filter_invalid_rows(df):
    return df.filter(col("matchID").isNotNull() & col("matchDateTimeUTC").isNotNull())


def apply_transformations(df):
    df = normalize_all_strings_recursive(df)

    timestamp_cols = ["matchDateTime", "matchDateTimeUTC", "lastUpdateDateTime"]
    for ts_col in timestamp_cols:
        if ts_col in df.columns:
            df = df.withColumn(ts_col, to_timestamp(col(ts_col)))

    if "numberOfViewers" in df.columns:
        df = df.withColumn("numberOfViewers", col("numberOfViewers").cast("int"))
    if "matchIsFinished" in df.columns:
        df = df.withColumn("matchIsFinished", col("matchIsFinished").cast("boolean"))

    return df


def log_counts(before, after):
    logger.info(f"Rows before cleaning: {before}, after cleaning: {after}")


def clean_bronze_data(spark):
    input_path = os.path.join(DATA_BRONZE_DIR, "bundesliga_combined.parquet")
    output_path = os.path.join(DATA_SILVER_DIR, "clean_matches.parquet")

    try:
        df = spark.read.parquet(input_path)
        initial_count = df.count()

        df = apply_transformations(df)
        df = filter_invalid_rows(df)

        final_count = df.count()
        log_counts(initial_count, final_count)

        os.makedirs(DATA_SILVER_DIR, exist_ok=True)
        df.write.mode("overwrite").parquet(output_path)

        logger.info(f"Cleaned silver data written to: {output_path}")
        df.select("matchID", "matchDateTimeUTC", "numberOfViewers").show(5, truncate=False)

    except Exception as e:
        logger.error(f"Failed to clean bronze data: {e}")
