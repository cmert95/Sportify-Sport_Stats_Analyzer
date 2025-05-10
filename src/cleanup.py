import os

from utils.paths import DATA_RAW_DIR


def clean_bundesliga_json_files():
    for filename in os.listdir(DATA_RAW_DIR):
        if filename.endswith(".json"):
            path = os.path.join(DATA_RAW_DIR, filename)
            try:
                os.remove(path)
                print(f"Deleted {filename}")
            except Exception as e:
                print(f"Failed to delete {filename}: {e}")


if __name__ == "__main__":
    clean_bundesliga_json_files()
