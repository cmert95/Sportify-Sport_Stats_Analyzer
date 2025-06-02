from data_pipeline.clean_bronze import run as silver_clean_data
from data_pipeline.fetch_seasons import run as raw_fetch_data
from data_pipeline.gold.generate_match_team_stats import run as gold_match_stats
from data_pipeline.gold.generate_team_season_summary import run as gold_team_summary
from data_pipeline.seasons_to_bronze import run as bronze_convert
from utils.logger import setup_logger

logger = setup_logger(__name__, log_name="main_pipeline")


def main():
    logger.info("Starting full football data pipeline")
    raw_fetch_data()
    bronze_convert()
    silver_clean_data()
    gold_match_stats()
    gold_team_summary()
    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()
