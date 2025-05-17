from pathlib import Path

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

Path(DATA_PREVIEW_DIR).mkdir(parents=True, exist_ok=True)

FILES = {
    "bronze": {
        "path": Path(DATA_BRONZE_DIR) / "bundesliga_combined.parquet",
        "limit": 20,
    },
    "silver": {
        "path": Path(DATA_SILVER_DIR) / "clean_matches.parquet",
        "limit": 20,
    },
    "gold": {
        "path": Path(DATA_GOLD_DIR) / "match_team_stats.parquet",
        "limit": 100,
    },
}


def export_preview(input_path: Path, output_csv_name: str, limit_count: int):
    try:
        df = spark.read.parquet(str(input_path)).limit(limit_count)
        output_path = Path(DATA_PREVIEW_DIR) / output_csv_name
        df.toPandas().to_csv(output_path, index=False)
        logger.info(f"Preview created: {output_csv_name}")
    except Exception as e:
        logger.error(f"Failed to create preview for {output_csv_name}: {e}")


def run_preview_generation():
    for name, info in FILES.items():
        output_file = f"{name}_preview.csv"
        export_preview(info["path"], output_file, info["limit"])


if __name__ == "__main__":
    run_preview_generation()
