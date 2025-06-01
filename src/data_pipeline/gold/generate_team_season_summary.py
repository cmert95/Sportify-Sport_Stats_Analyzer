from pathlib import Path

from pyspark.sql.functions import count
from pyspark.sql.functions import sum as Fsum

from utils.logger import setup_logger
from utils.paths import DATA_GOLD_DIR
from utils.spark_session import get_spark_session

logger = setup_logger(__name__, log_name="generate_team_season_summary")


def read_gold_data(spark):
    """Reads the gold-layer match-level data as input for aggregation."""
    input_path = Path(DATA_GOLD_DIR) / "match_team_stats.parquet"
    logger.info(f"Reading gold data from {input_path}")
    return spark.read.parquet(str(input_path))


def generate_team_season_summary(df):
    logger.info("Aggregating season summary for each team")

    summary_df = df.groupBy("teamID", "matchYear").agg(
        count("*").alias("matchesPlayed"),
        Fsum((df.matchOutcome == "win").cast("int")).alias("wins"),
        Fsum((df.matchOutcome == "draw").cast("int")).alias("draws"),
        Fsum((df.matchOutcome == "loss").cast("int")).alias("losses"),
        Fsum("points").alias("totalPoints"),
    )

    return summary_df


def write_summary(df):
    """Writes the aggregated team-season summary to the gold layer."""
    output_path = Path(DATA_GOLD_DIR) / "team_season_summary.parquet"
    logger.info(f"Writing team season summary to {output_path}")
    df.write.mode("overwrite").parquet(str(output_path))


def run():
    spark = get_spark_session("Generate Team Season Summary")
    logger.info("Spark session started")

    try:
        gold_df = read_gold_data(spark)
        summary_df = generate_team_season_summary(gold_df)
        write_summary(summary_df)
        logger.info("Team_season_summary written successfully.")
    finally:
        spark.stop()
        logger.info("Spark session stopped")


if __name__ == "__main__":
    run()
