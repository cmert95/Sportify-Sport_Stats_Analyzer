import requests

from config import LEAGUE_SHORTCUT, OPENLIGADB_BASE_URL
from utils.logger import setup_logger

logger = setup_logger(__name__, log_name="fetch_data")


def fetch_bundesliga_season_matches(season):
    url = f"{OPENLIGADB_BASE_URL}/getmatchdata/{LEAGUE_SHORTCUT}/{season}"
    logger.info(f"[{season}] Fetching match data from: {url}")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        matches = response.json()
        logger.info(f"[{season}] Successfully fetched {len(matches)} matches")
        return matches

    except requests.exceptions.RequestException as e:
        logger.error(f"[{season}] Failed to fetch match data: {e}")
        return []

    except Exception as e:
        logger.error(f"[{season}] Unexpected error: {e}")
        return []
