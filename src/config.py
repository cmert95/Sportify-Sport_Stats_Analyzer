import os

from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = "https://v3.football.api-sports.io"
API_KEY = os.getenv("API_KEY")
