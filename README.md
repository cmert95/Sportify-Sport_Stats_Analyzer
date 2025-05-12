## Sportify: Sport Stats Analyzer

This project showcases advanced engineering practices within the DevOps ecosystem by implementing a robust, modular ETL pipeline tailored for processing seasonal football data retrieved from an external API.

Built with scalability and future extensibility in mind, the pipeline produces ML- and DL-ready datasets, making it well-suited for downstream applications such as machine learning, deep learning model training, and advanced analytics.


### 📁 Project Structure

```bash
project22_football/
├── config/
│   └── settings.yaml           # Global configuration settings
├── data/
│   ├── raw/                    # Raw .json files fetched from API
│   ├── bronze/                 # Cleaned raw data (bronze layer)
│   ├── silver/                 # Processed and normalized data
│   ├── gold/                   # Final aggregated data for ML/DL
│   └── preview/                # CSV previews (first 20 rows, for quick view)
├── infra/                      # Infrastructure as Code (DevOps)
│   ├── ansible/                # Environment automation
│   └── terraform/              # Infrastructure provisioning
├── logs/                       # Application logs
├── src/
│   ├── pipeline/               # PySpark ETL steps
│   │   ├── load.py             # Creates raw data by ingesting from API
│   │   ├── combine_raw.py      # Generates bronze data by merging
│   │   ├── clean_data.py       # Creates silver data by cleaning
│   │   └── aggregate_data.py   # coming soon
│   ├── utils/                  # Shared utilities for pipeline
│   │   ├── logger.py           # Custom logging setup
│   │   ├── paths.py            # Centralized path definitions
│   │   ├── schema.py           # Data schema definitions
│   │   └── spark_session.py    # Initializes SparkSession
│   ├── config.py               # Python-side configuration
│   ├── fetch_api_data.py       # Fetches seasonal data from external API
│   ├── combine_raw_json.py     # Merges raw JSON files into one
│   ├── clean_bronze_data.py    # Cleans raw API data (bronze layer)
│   ├── clean_up.py             # Deletes unnecessary/temporary files
│   └── preview_generator.py    # Generates data previews for validation
├── docker-compose.yml          # (Planned) Dockerized environment setup
├── .gitignore
├── pyproject.toml
├── README.md
├── requirements.txt            # Core dependencies
├── requirements-dev.txt        # Dev/testing dependencies
```
