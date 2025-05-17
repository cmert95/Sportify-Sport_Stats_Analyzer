import os

from pyspark.sql.functions import col, explode, to_timestamp, trim, when
from pyspark.sql.types import ArrayType, StringType, StructType

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


def flatten_struct_column(df, col_name, prefix):
    """Moves fields of a struct column to top-level columns with prefixed names."""
    for field in df.select(f"{col_name}.*").columns:
        df = df.withColumn(f"{prefix}_{field}", col(f"{col_name}.{field}"))
    return df.drop(col_name)


def explode_and_flatten_array(df, col_name, prefix):
    """Explodes an array<struct> column and flattens the resulting struct fields."""
    df = df.withColumn(col_name, explode(col(col_name)))
    for field in df.select(f"{col_name}.*").columns:
        df = df.withColumn(f"{prefix}_{field}", col(f"{col_name}.{field}"))
    return df.drop(col_name)


def filter_invalid_rows(df):
    return df.filter(col("matchID").isNotNull() & col("matchDateTimeUTC").isNotNull())


def apply_transformations(df):
    df = normalize_all_strings_recursive(df)

    # Convert datetime strings to timestamp
    timestamp_cols = ["matchDateTime", "matchDateTimeUTC", "lastUpdateDateTime"]
    for ts_col in timestamp_cols:
        if ts_col in df.columns:
            df = df.withColumn(ts_col, to_timestamp(col(ts_col)))

    # Cast fields
    if "numberOfViewers" in df.columns:
        df = df.withColumn("numberOfViewers", col("numberOfViewers").cast("int"))
    if "matchIsFinished" in df.columns:
        df = df.withColumn("matchIsFinished", col("matchIsFinished").cast("boolean"))

    # Flatten struct fields
    for struct_col in ["team1", "team2", "location", "group"]:
        if struct_col in df.columns:
            df = flatten_struct_column(df, struct_col, struct_col)

    # Explode + flatten array<struct> fields
    for array_col, prefix in [("goals", "goal"), ("matchResults", "result")]:
        if array_col in df.columns and isinstance(df.schema[array_col].dataType, ArrayType):
            df = explode_and_flatten_array(df, array_col, prefix)

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
        df.select(
            "matchID", "matchDateTimeUTC", "team1_teamName", "team2_teamName", "numberOfViewers"
        ).show(5, truncate=False)

    except Exception as e:
        logger.error(f"Failed to clean bronze data: {e}")
