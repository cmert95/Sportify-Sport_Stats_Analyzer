## Sportify: Sport Stats Analyzer

This project showcases advanced engineering practices within the DevOps ecosystem by implementing a robust, modular ETL pipeline tailored for processing seasonal football data retrieved from an external API.

Built with scalability and future extensibility in mind, the pipeline produces ML- and DL-ready datasets, making it well-suited for downstream applications such as machine learning, deep learning model training, and advanced analytics.


### 📁 Project Structure

```bash
sportify/
├── config/
│   └── settings.yaml           # Global configuration settings
├── data/
│   ├── raw/                    # Raw .json files fetched from API
│   ├── bronze/                 # Cleaned raw data
│   ├── silver/                 # Processed and normalized data
│   ├── gold/                   # Final aggregated datasets for downstream use
│   └── preview/                # CSV previews (for Quick View)
├── infra/                      # Infrastructure as Code (DevOps)
│   ├── terraform/              # AWS provisioning
│   └── ansible/                # Automates Python, Java, Spark etc. setup
├── logs/                       # Application logs
├── src/
│   ├── pipeline/
│   │   ├── load.py             # Ingests raw data from API (Raw Layer)
│   │   ├── combine.py          # Combines raw JSON into one file (Bronze Layer)
│   │   ├── clean.py            # Cleans and normalizes bronze data (Silver Layer)
│   │   └── gold.py             # Runs full gold pipeline (Gold Layer)
│   ├── utils/
│   │   ├── logger.py           # Custom logging setup
│   │   ├── paths.py            # Centralized path definitions
│   │   ├── schema.py           # Data schema definitions
│   │   └── spark_session.py    # Initializes SparkSession
│   ├── config.py               # Python-side configuration
│   ├── fetch_api_data.py       # Fetches seasonal data from external API
│   ├── combine_seasons.py      # Saves each season to a separate JSON (Raw Layer)
│   ├── combine_raw_json.py     # Merges raw JSON files into one (Bronze Layer)
│   ├── clean_bronze_data.py    # Cleans raw API data (Silver Layer)
│   ├── generate_match_team...  # Generates enriched match-level dataset
│   ├── generate_team_seaso...  # Aggregates team-level seasonal stats
│   ├── clean_up.py             # Deletes unnecessary/temporary files
│   └── preview_generator.py    # Generates data previews for validation
├── docker-compose.yml          # (Planned) Dockerized environment setup
├── .gitignore
├── pyproject.toml
├── README.md
├── requirements.txt            # Core dependencies
├── requirements-dev.txt        # Dev/testing dependencies
```

### 📊 Gold Datasets

- **`match_team_stats.parquet`** – Match-level team performance metrics (e.g., goals, result, points); used for analytics and ML feature engineering
- **`team_season_summary.parquet`** – Season-level aggregated stats per team; supports season evaluation and BI dashboards *(in progress)*
- **`rolling_team_stats.parquet`** – Rolling averages over recent matches; useful for trend analysis and time-aware modeling *(planned)*
- **`head_to_head_summary.parquet`** – Historical summaries between teams; supports rivalry insights and predictive modeling *(planned)*
