import yaml

from utils.paths import SETTINGS_PATH

with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
    settings = yaml.safe_load(f)

# API SEttings
API = settings["api"]
OPENLIGADB_BASE_URL = API["base_url"]
LEAGUE_SHORTCUT = API["league_shortcut"]
SEASON_COUNT = API["season_count"]
LATEST_SEASON = API["latest_season"]

# Spark Settings
SPARK = settings["spark"]
SPARK_APP_NAME = SPARK["app_name"]
SPARK_MASTER = SPARK["master"]
SPARK_DRIVER_MEMORY = SPARK["driver_memory"]
SPARK_EXECUTOR_MEMORY = SPARK["executor_memory"]
SPARK_SHUFFLE_PARTITIONS = SPARK["shuffle_partitions"]
SPARK_EXTRA_CONFIGS = SPARK.get("extra_configs", {})
