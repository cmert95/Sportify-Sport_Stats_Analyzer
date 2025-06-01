import os

from utils.logger import setup_logger
from utils.paths import DATA_BRONZE_DIR, DATA_RAW_DIR
from utils.schema import match_schema

logger = setup_logger(name=__name__, log_name="combine_raw")


def combine_raw_json_to_bronze(spark):
    input_pattern = os.path.join(DATA_RAW_DIR, "bundesliga_*.json")
    output_path = os.path.join(DATA_BRONZE_DIR, "bundesliga_combined.parquet")

    try:
        logger.info(f"Reading raw JSON files from: {input_pattern}")
        df = spark.read.schema(match_schema).json(input_pattern)
    except Exception as e:
        logger.error(f"Failed to read JSON files: {e}")
        raise

    try:
        os.makedirs(DATA_BRONZE_DIR, exist_ok=True)
        df.write.mode("overwrite").parquet(output_path)
        logger.info(f"Combined parquet written to: {output_path}")
    except Exception as e:
        logger.error(f"Failed to write combined parquet: {e}")
        raise
