from pathlib import Path

# Project root directory (2 seviye yukarı: utils → src → project root)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Data directories
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_BRONZE_DIR = PROJECT_ROOT / "data" / "bronze"
DATA_SILVER_DIR = PROJECT_ROOT / "data" / "silver"
DATA_GOLD_DIR = PROJECT_ROOT / "data" / "gold"
DATA_PREVIEW_DIR = PROJECT_ROOT / "data" / "preview"

# Logs directory
LOG_DIR = PROJECT_ROOT / "logs"

# Settings file
SETTINGS_PATH = PROJECT_ROOT / "config" / "settings.yaml"
