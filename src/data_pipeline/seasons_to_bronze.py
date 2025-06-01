from pathlib import Path

from pyspark.sql import SparkSession

from utils.logger import setup_logger
from utils.paths import DATA_BRONZE_DIR, DATA_RAW_DIR
from utils.schema import match_schema
from utils.spark_session import get_spark_session

logger = setup_logger(name=__name__, log_name="seasons_to_bronze")


def convert_seasons_to_bronze(spark: SparkSession) -> None:
    """
    Reads all raw JSON files containing season match data from the raw data directory, applies the defined schema, and writes a combined Parquet file to the bronze data directory.
    """
    input_pattern = str(Path(DATA_RAW_DIR) / "bundesliga_*.json")
    output_path = str(Path(DATA_BRONZE_DIR) / "bundesliga_combined.parquet")

    try:
        logger.info(f"Reading raw JSON files from: {input_pattern}")
        df = spark.read.schema(match_schema).json(input_pattern)
    except Exception as e:
        logger.error(f"Failed to read JSON files: {e}")
        raise

    try:
        Path(DATA_BRONZE_DIR).mkdir(parents=True, exist_ok=True)
        df.write.mode("overwrite").parquet(output_path)
        logger.info(f"Combined parquet written to: {output_path}")
    except Exception as e:
        logger.error(f"Failed to write combined parquet: {e}")
        raise


def run() -> None:
    spark = get_spark_session("Combine Raw JSON to Bronze")
    logger.info("Spark session started")

    try:
        convert_seasons_to_bronze(spark)
    finally:
        spark.stop()
        logger.info("Spark session stopped")


if __name__ == "__main__":
    run()
