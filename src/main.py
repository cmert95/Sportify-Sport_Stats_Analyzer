from fetch_api_data import fetch_leagues


def main():
    data = fetch_leagues()

    print("Top-level keys:", data.keys())
    print("Sample:", data["response"][0])


if __name__ == "__main__":
    main()
