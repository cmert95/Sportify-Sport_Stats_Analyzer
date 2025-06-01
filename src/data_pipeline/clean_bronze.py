from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, explode, to_timestamp, trim, when
from pyspark.sql.types import ArrayType, StringType, StructType

from utils.logger import setup_logger
from utils.paths import DATA_BRONZE_DIR, DATA_SILVER_DIR
from utils.spark_session import get_spark_session

logger = setup_logger(__name__, log_name="clean_bronze")


def normalize_all_strings_recursive(
    df: DataFrame, schema: StructType | None = None, prefix: str = ""
) -> DataFrame:
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


def flatten_struct_column(df: DataFrame, col_name: str, prefix: str) -> DataFrame:
    """Moves fields of a struct column to top-level columns with prefixed names."""
    logger.info(f"Flattening struct column: {col_name}")
    for field in df.select(f"{col_name}.*").columns:
        df = df.withColumn(f"{prefix}_{field}", col(f"{col_name}.{field}"))
    return df.drop(col_name)


def explode_and_flatten_array(df: DataFrame, col_name: str, prefix: str) -> DataFrame:
    """Explodes an array<struct> column and flattens the resulting struct fields."""
    logger.info(f"Exploding and flattening array column: {col_name}")
    df = df.withColumn(col_name, explode(col(col_name)))
    for field in df.select(f"{col_name}.*").columns:
        df = df.withColumn(f"{prefix}_{field}", col(f"{col_name}.{field}"))
    return df.drop(col_name)


def filter_invalid_rows(df: DataFrame) -> DataFrame:
    logger.info("Filtering out rows with null matchID or matchDateTimeUTC")
    return df.filter(col("matchID").isNotNull() & col("matchDateTimeUTC").isNotNull())


def apply_transformations(df: DataFrame) -> DataFrame:
    logger.info("Applying data transformations...")

    df = normalize_all_strings_recursive(df)

    # Convert string columns to timestamp where applicable
    timestamp_cols = ["matchDateTime", "matchDateTimeUTC", "lastUpdateDateTime"]
    for ts_col in timestamp_cols:
        if ts_col in df.columns:
            logger.info(f"Converting column to timestamp: {ts_col}")
            df = df.withColumn(ts_col, to_timestamp(col(ts_col)))

    # Cast specific fields to appropriate types
    if "numberOfViewers" in df.columns:
        logger.info("Casting numberOfViewers to int")
        df = df.withColumn("numberOfViewers", col("numberOfViewers").cast("int"))
    if "matchIsFinished" in df.columns:
        logger.info("Casting matchIsFinished to boolean")
        df = df.withColumn("matchIsFinished", col("matchIsFinished").cast("boolean"))

    # Flatten struct fields
    for struct_col in ["team1", "team2", "location", "group"]:
        if struct_col in df.columns:
            logger.info(f"Flattening struct column: {struct_col}")
            df = flatten_struct_column(df, struct_col, struct_col)

    # Flatten exploded array<struct> fields
    for array_col, prefix in [("goals", "goal"), ("matchResults", "result")]:
        if array_col in df.columns and isinstance(df.schema[array_col].dataType, ArrayType):
            logger.info(f"Exploding and flattening array column: {array_col}")
            df = explode_and_flatten_array(df, array_col, prefix)

    if "timeZoneID" in df.columns:
        logger.info("Dropping column: timeZoneID")
        df = df.drop("timeZoneID")

    # Drop columns with more than 80% missing values
    threshold = 0.8
    total_rows = df.count()
    for column in df.columns:
        null_count = df.filter(col(column).isNull()).count()
        logger.info(f"Dropping column due to missing value threshold: {column}")
        if null_count / total_rows > threshold:
            df = df.drop(column)

    # Remove duplicates based on matchID
    df = df.dropDuplicates(["matchID"])
    logger.info("Dropped duplicate rows based on matchID")
    return df


def log_counts(before: int, after: int) -> None:
    logger.info(f"Rows before cleaning: {before}, after cleaning: {after}")


def clean_bronze_data(spark: SparkSession) -> None:
    input_path = Path(DATA_BRONZE_DIR) / "bundesliga_combined.parquet"
    output_path = Path(DATA_SILVER_DIR) / "clean_matches.parquet"

    try:
        df = spark.read.parquet(str(input_path))
        initial_count = df.count()

        df = apply_transformations(df)
        df = filter_invalid_rows(df)

        final_count = df.count()
        log_counts(initial_count, final_count)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.write.mode("overwrite").parquet(str(output_path))

        logger.info(f"Cleaned silver data written to: {output_path}")
        df.select(
            "matchID", "matchDateTimeUTC", "team1_teamName", "team2_teamName", "numberOfViewers"
        ).show(5, truncate=False)

    except Exception as e:
        logger.error(f"Failed to clean bronze data: {e}")


def run() -> None:
    spark = get_spark_session("Clean Bronze Data")
    logger.info("Spark session started")

    try:
        clean_bronze_data(spark)
    finally:
        spark.stop()
        logger.info("Spark session stopped")


if __name__ == "__main__":
    run()
