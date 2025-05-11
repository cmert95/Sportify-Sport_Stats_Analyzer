import os

# Project base file dir
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Data file dir
DATA_RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
DATA_BRONZE_DIR = os.path.join(PROJECT_ROOT, "data", "bronze")
DATA_SILVER_DIR = os.path.join(PROJECT_ROOT, "data", "silver")
DATA_GOLD_DIR = os.path.join(PROJECT_ROOT, "data", "gold")
DATA_PREVIEW_DIR = os.path.join(PROJECT_ROOT, "data", "preview")

# Logs dir
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
