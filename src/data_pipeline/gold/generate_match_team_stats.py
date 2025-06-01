from pathlib import Path

from pyspark.sql.functions import col, dayofweek, lit, month, when, year
from pyspark.sql.utils import AnalysisException

from utils.logger import setup_logger
from utils.paths import DATA_GOLD_DIR, DATA_SILVER_DIR
from utils.spark_session import get_spark_session

logger = setup_logger(__name__, log_name="generate_match_team_stats")


def read_silver_data(spark):
    """Reads cleaned match-level data from the silver layer Parquet file."""
    try:
        input_path = Path(DATA_SILVER_DIR) / "clean_matches.parquet"
        logger.info(f"Reading silver data from {input_path}")
        df = spark.read.parquet(str(input_path))
        if df.rdd.isEmpty():
            logger.warning("Silver data is empty. Aborting pipeline.")
            return None
        return df
    except AnalysisException as e:
        logger.error(f"Failed to read silver data: {e}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error while reading silver data: {e}")
        return None


def transform_to_team_perspective(df):
    """
    Duplicates each match row to reflect both teams' perspectives in separate rows.
    Adds 'isHome' indicator to distinguish between team1 and team2 views.
    """
    logger.info("Transforming matches into team-based rows")

    base_cols = ["matchID", "matchDateTimeUTC"]

    team1_df = df.selectExpr(
        *base_cols,
        "team1_teamId as teamID",
        "team1_teamName as teamName",
        "team2_teamId as opponentID",
        "goal_scoreTeam1 as goalsFor",
        "goal_scoreTeam2 as goalsAgainst",
    ).withColumn("isHome", lit(True))

    team2_df = df.selectExpr(
        *base_cols,
        "team2_teamId as teamID",
        "team2_teamName as teamName",
        "team1_teamId as opponentID",
        "goal_scoreTeam2 as goalsFor",
        "goal_scoreTeam1 as goalsAgainst",
    ).withColumn("isHome", lit(False))

    return team1_df.unionByName(team2_df)


def add_additional_features(df):
    """
    Adds analytical and domain-specific features to each team-based row,
    including match outcome, goal difference, intensity classification, and more.
    """
    logger.info("Adding additional features to match data")
    df = (
        df
        # Goal difference for the team in the match (positive: win, negative: loss)
        .withColumn("goalDifference", col("goalsFor") - col("goalsAgainst"))
        # Match result classification based on goals: win / loss / draw
        .withColumn(
            "matchOutcome",
            when(col("goalsFor") > col("goalsAgainst"), "win")
            .when(col("goalsFor") < col("goalsAgainst"), "loss")
            .otherwise("draw"),
        )
        # Extract the year of the match
        .withColumn("matchYear", year("matchDateTimeUTC"))
        # Extract the month of the match
        .withColumn("matchMonth", month("matchDateTimeUTC"))
        # Determine whether the match was played on a weekend (1 = Sunday, 7 = Saturday)
        .withColumn(
            "isWeekend",
            when(dayofweek("matchDateTimeUTC").isin([1, 7]), lit(True)).otherwise(lit(False)),
        )
        # Categorize matches by total number of goals scored: high (≥5), low (≤1), or normal
        .withColumn(
            "scoringCategory",
            when((col("goalsFor") + col("goalsAgainst")) >= 5, "high")
            .when((col("goalsFor") + col("goalsAgainst")) <= 1, "low")
            .otherwise("normal"),
        )
        # Match type: 'derby' if both teams have same ID, else home or away
        .withColumn(
            "matchType",
            when(col("teamID") == col("opponentID"), "derby")
            .when(col("isHome"), "home")
            .otherwise("away"),
        )
        # Total number of goals in the match
        .withColumn("totalGoals", col("goalsFor") + col("goalsAgainst"))
        # Goalless draw: match ended 0–0
        .withColumn(
            "goallessDraw",
            when((col("goalsFor") == 0) & (col("goalsAgainst") == 0), lit(True)).otherwise(
                lit(False)
            ),
        )
        # Match intensity: combined goals + away indicator
        .withColumn(
            "matchIntensity",
            when((col("totalGoals") >= 5) & (~col("isHome")), "high_away")
            .when(col("totalGoals") >= 5, "high")
            .otherwise("normal"),
        )
        # Blowout: goal difference ≥ 3
        .withColumn(
            "isBlowout",
            when((col("goalDifference") >= 3) | (col("goalDifference") <= -3), lit(True)).otherwise(
                lit(False)
            ),
        )
        # Points awarded based on match outcome
        .withColumn(
            "points",
            when(col("matchOutcome") == "win", 3)
            .when(col("matchOutcome") == "draw", 1)
            .otherwise(0),
        )
    )
    return df


def write_gold_data(df):
    """Writes the transformed and enriched team-level data to the gold layer."""
    try:
        if df is None or df.rdd.isEmpty():
            logger.warning("Gold DataFrame is empty. Skipping write.")
            return

        output_path = Path(DATA_GOLD_DIR) / "match_team_stats.parquet"
        logger.info(f"Writing gold data to {output_path}")
        df.write.mode("overwrite").parquet(str(output_path))
    except Exception as e:
        logger.exception(f"Failed to write gold data: {e}")


def run():
    spark = get_spark_session("Generate Match Team Stats")
    logger.info("Spark session started")

    try:
        silver_df = read_silver_data(spark)
        if silver_df is None:
            logger.error("Silver data is missing. Terminating process.")
            return

        gold_df = transform_to_team_perspective(silver_df)
        enriched_df = add_additional_features(gold_df)
        write_gold_data(enriched_df)

        logger.info("Match_team_stats written successfully.")
    finally:
        spark.stop()
        logger.info("Spark session stopped")


if __name__ == "__main__":
    run()
