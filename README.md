## Sportify: Sport Stats Analyzer

This project showcases advanced engineering practices within the DevOps ecosystem by implementing a robust, modular ETL pipeline tailored for processing seasonal football data retrieved from an external API.

Built with scalability and future extensibility in mind, the pipeline produces ML- and DL-ready datasets, making it well-suited for downstream applications such as machine learning, deep learning model training, and advanced analytics.


## 📁 Project Structure

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
├── infra/
│   ├── terraform/              # AWS provisioning
│   └── ansible/                # Automates Python, Java, Spark etc. setup
├── logs/                       # Application logs
├── src/
│   ├── data_pipeline/
│   │   └── gold/
│   │   │   ├──match_team...    # Generates enriched match-level dataset
│   │   │   └──team_season...   # Aggregates team-level seasonal stats
│   │   ├── fetch_seasons.py    # Fetches seasonal data from API (Raw Layer)
│   │   ├── seasons_to_brnze.py # Combines raw JSON into one file (Bronze Layer)
│   │   └── clean_bronze.py     # Cleans and normalizes bronze data (Silver Layer)
│   ├── utils/
│   │   ├── logger.py           # Custom logging setup
│   │   ├── paths.py            # Centralized path definitions
│   │   ├── schema.py           # Data schema definitions
│   │   └── spark_session.py    # Initializes SparkSession
│   ├── utils/
│   │   └── openligadb_cli.py   # Fetches seasonal data from openligadb API
│   ├── config.py               # Python-side configuration
│   ├── clean_up.py             # Deletes unnecessary/temporary files
│   └── preview_generator.py    # Generates data previews for validation
├── .gitignore
├── pyproject.toml
├── README.md
├── requirements.txt            # Core dependencies
├── requirements-dev.txt        # Dev/testing dependencies
```


## ✅ Project Progress Overview

### Phase 1: Foundational Development

| Status | Task                                                                 |
|--------|----------------------------------------------------------------------|
| ✅     | Set up project structure with formatting and linting tools.          |
| ✅     | Created infrastructure scaffolding using Terraform and Ansible.      |
| ✅     | Installed and configured Apache Spark for local processing.          |
| ✅     | Integrated OpenLigaDB API for seasonal match data.                   |
| ✅     | Built bronze layer with schema-aware JSON ingestion.                 |
| ✅     | Created `settings.yaml` for centralized and flexible configuration.  |
| ✅     | Developed silver layer with normalization and type casting.          |
| ✅     | Added CSV preview generator for quick validation.                    |
| ✅     | Engineered gold features for matches and team seasons.               |
| 🟡     | Extend gold outputs with new views and metrics.                      |

### Phase 2: Infra & Scalability

| Status | Task                                                                 |
|--------|----------------------------------------------------------------------|
| 🟡     | Create a `main.py` to orchestrate the full pipeline.                 |
| 🔜     | Create a `Makefile` to streamline common dev and pipeline tasks.     |
| 🔜     | Add dynamic IP handling to Ansible inventory.                        |
| 🔜     | Containerize project with Docker & Compose.                          |

### Phase 3: Testing & Deployment

| Status | Task                                                                 |
|--------|----------------------------------------------------------------------|
| 🟡     | Add unit and integration tests.                                      |
| 🔜     | Set up CI/CD with GitHub Actions or Jenkins.                         |
| 🔜     | Export final data to PostgreSQL or S3.                               |
| 🔜     | Build dashboards with Power BI, Tableau, or Streamlit.               |


## 📊 Gold Datasets

- **`match_team_stats.parquet`** – Match-level team performance metrics (e.g., goals, result, points); used for analytics and ML feature engineering
- **`team_season_summary.parquet`** – Season-level aggregated stats per team; supports season evaluation and BI dashboards *(in progress)*
- **`rolling_team_stats.parquet`** – Rolling averages over recent matches; useful for trend analysis and time-aware modeling *(planned)*
- **`head_to_head_summary.parquet`** – Historical summaries between teams; supports rivalry insights and predictive modeling *(planned)*
