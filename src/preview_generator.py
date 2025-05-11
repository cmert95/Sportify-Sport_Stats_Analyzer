import os

from utils.logger import setup_logger
from utils.paths import (
    DATA_BRONZE_DIR,
    DATA_GOLD_DIR,
    DATA_PREVIEW_DIR,
    DATA_SILVER_DIR,
)
from utils.spark_session import get_spark_session

logger = setup_logger(__name__, log_name="preview_generator")
spark = get_spark_session("Preview Generator")

os.makedirs(DATA_PREVIEW_DIR, exist_ok=True)

FILES = {
    "bronze": os.path.join(DATA_BRONZE_DIR, "bundesliga_combined.parquet"),
    "silver": os.path.join(DATA_SILVER_DIR, "clean_matches.parquet"),
    "gold": os.path.join(DATA_GOLD_DIR, "team_stats.parquet"),
}


def export_preview(input_path, output_csv_name):
    try:
        df = spark.read.parquet(input_path).limit(20)
        df.toPandas().to_csv(os.path.join(DATA_PREVIEW_DIR, output_csv_name), index=False)
        logger.info(f"Preview created: {output_csv_name}")
    except Exception as e:
        logger.error(f"Failed to create preview for {output_csv_name}: {e}")


def run_preview_generation():
    for name, path in FILES.items():
        output_file = f"{name}_preview.csv"
        export_preview(path, output_file)


if __name__ == "__main__":
    run_preview_generation()
