import requests

from config import OPENLIGADB_BASE_URL


def fetch_bundesliga_season_matches(season_year: int) -> list:
    url = f"{OPENLIGADB_BASE_URL}/getmatchdata/bl1/{season_year}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[{season_year}] Fetch failed: {e}")
        return []
