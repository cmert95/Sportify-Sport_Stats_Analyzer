from generate_match_team_stats import run_match_team_stats
from generate_team_season_summary import run_team_season_summary
from utils.logger import setup_logger
from utils.spark_session import get_spark_session

logger = setup_logger(__name__, log_name="generate_gold_pipeline")


def main():
    spark = get_spark_session("Generate Gold Data")
    logger.info("Spark session started")
    run_match_team_stats(spark)
    run_team_season_summary(spark)
    spark.stop()
    logger.info("Spark session stopped")


if __name__ == "__main__":
    main()
