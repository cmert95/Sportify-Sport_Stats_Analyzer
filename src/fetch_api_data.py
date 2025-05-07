import requests

from config import API_BASE_URL, API_KEY


def fetch_leagues():
    url = f"{API_BASE_URL}/leagues"
    headers = {"x-apisports-key": API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")
