import json
import os
import time

from config import LATEST_SEASON, SEASON_COUNT
from fetch_api_data import fetch_bundesliga_season_matches
from utils.logger import setup_logger
from utils.paths import DATA_RAW_DIR

logger = setup_logger(__name__, log_name="combine_seasons")


def save_all_seasons_to_json():
    for year in range(LATEST_SEASON - SEASON_COUNT + 1, LATEST_SEASON + 1):
        logger.info(f"[{year}] Requesting match data from API module...")
        matches = fetch_bundesliga_season_matches(year)

        if not matches:
            logger.warning(f"[{year}] No matches returned. Skipping save.")
            continue

        try:
            os.makedirs(DATA_RAW_DIR, exist_ok=True)
            file_path = os.path.join(DATA_RAW_DIR, f"bundesliga_{year}.json")

            with open(file_path, "w", encoding="utf-8") as f:
                for match in matches:
                    json.dump(match, f)
                    f.write("\n")

            logger.info(f"[{year}] Saved {len(matches)} matches to {file_path}")

        except Exception as e:
            logger.error(f"[{year}] Failed to save matches: {e}")

        time.sleep(0.3)  # Gentle pause between requests


if __name__ == "__main__":
    save_all_seasons_to_json()
