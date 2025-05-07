import json
import os
import time

from config import LATEST_SEASON, SEASON_COUNT
from fetch_api_data import fetch_bundesliga_season_matches
from utils.paths import DATA_RAW_DIR


def fetch_and_save_all_seasons():
    for year in range(LATEST_SEASON - SEASON_COUNT + 1, LATEST_SEASON + 1):
        matches = fetch_bundesliga_season_matches(year)
        if not matches:
            continue

        os.makedirs(DATA_RAW_DIR, exist_ok=True)
        path = os.path.join(DATA_RAW_DIR, f"bundesliga_{year}.json")
        with open(path, "w", encoding="utf-8") as f:
            for match in matches:
                json.dump(match, f)
                f.write("\n")
        print(f"[{year}] Saved {len(matches)} matches to {path}")
        time.sleep(0.3)  # gentle delay between reqs
