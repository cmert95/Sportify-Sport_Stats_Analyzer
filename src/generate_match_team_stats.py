import os

from pyspark.sql.functions import col, dayofweek, lit, month, when, year

from utils.logger import setup_logger
from utils.paths import DATA_GOLD_DIR, DATA_SILVER_DIR

logger = setup_logger(__name__, log_name="generate_gold")


def read_silver_data(spark):
    input_path = os.path.join(DATA_SILVER_DIR, "clean_matches.parquet")
    logger.info(f"Reading silver data from {input_path}")
    return spark.read.parquet(input_path)


def transform_to_team_perspective(df):
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
    df = (
        df
        # Goal difference for the team in the match
        .withColumn("goalDifference", col("goalsFor") - col("goalsAgainst"))
        # Match result classification based on goals
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
        # Determine whether the match was played on a weekend
        .withColumn(
            "isWeekend",
            when(dayofweek("matchDateTimeUTC").isin([1, 7]), lit(True)).otherwise(lit(False)),
        )
        # Categorize matches by goals scored (high, low, normal)
        .withColumn(
            "scoringCategory",
            when((col("goalsFor") + col("goalsAgainst")) >= 5, "high")
            .when((col("goalsFor") + col("goalsAgainst")) <= 1, "low")
            .otherwise("normal"),
        )
    )
    return df


def write_gold_data(df):
    output_path = os.path.join(DATA_GOLD_DIR, "match_team_stats.parquet")
    logger.info(f"Writing gold data to {output_path}")
    df.write.mode("overwrite").parquet(output_path)


def run_gold_generation(spark):
    silver_df = read_silver_data(spark)
    gold_df = transform_to_team_perspective(silver_df)
    enriched_df = add_additional_features(gold_df)
    write_gold_data(enriched_df)
    logger.info("Gold data successfully written.")
