import json
import time
from pathlib import Path
from typing import Any

from config import LATEST_SEASON, SEASON_COUNT
from fetch_api_data import fetch_bundesliga_season_matches
from utils.logger import setup_logger
from utils.paths import DATA_RAW_DIR

logger = setup_logger(__name__, log_name="fetch_seasons")


def fetch_and_save_season_data() -> None:
    """
    Fetches football match data for multiple seasons and saves each season's data as a separate JSON file in the raw data directory.
    """
    for year in range(LATEST_SEASON - SEASON_COUNT + 1, LATEST_SEASON + 1):
        logger.info(f"[{year}] Requesting match data from API module...")
        matches: list[dict[str, Any]] = fetch_bundesliga_season_matches(year)

        if not matches:
            logger.warning(f"[{year}] No matches returned. Skipping save.")
            continue

        try:
            Path(DATA_RAW_DIR).mkdir(parents=True, exist_ok=True)
            file_path = Path(DATA_RAW_DIR) / f"bundesliga_{year}.json"

            with file_path.open("w", encoding="utf-8") as f:
                for match in matches:
                    json.dump(match, f)
                    f.write("\n")

            logger.info(f"[{year}] Saved {len(matches)} matches to {file_path}")

        except Exception as e:
            logger.error(f"[{year}] Failed to save matches: {e}")

        time.sleep(0.3)


def run() -> None:
    logger.info("Starting season data fetch process...")
    fetch_and_save_season_data()
    logger.info("Season data fetch process completed.")


if __name__ == "__main__":
    run()
