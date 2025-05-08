from pyspark.sql.types import (
    ArrayType,
    BooleanType,
    LongType,
    StringType,
    StructField,
    StructType,
)

match_schema = StructType(
    [
        StructField(
            "goals",
            ArrayType(
                StructType(
                    [
                        StructField("comment", StringType(), True),
                        StructField("goalGetterID", LongType(), True),
                        StructField("goalGetterName", StringType(), True),
                        StructField("goalID", LongType(), True),
                        StructField("isOvertime", BooleanType(), True),
                        StructField("isOwnGoal", BooleanType(), True),
                        StructField("isPenalty", BooleanType(), True),
                        StructField("matchMinute", LongType(), True),
                        StructField("scoreTeam1", LongType(), True),
                        StructField("scoreTeam2", LongType(), True),
                    ]
                )
            ),
            True,
        ),
        StructField(
            "group",
            StructType(
                [
                    StructField("groupID", LongType(), True),
                    StructField("groupName", StringType(), True),
                    StructField("groupOrderID", LongType(), True),
                ]
            ),
            True,
        ),
        StructField("lastUpdateDateTime", StringType(), True),
        StructField("leagueId", LongType(), True),
        StructField("leagueName", StringType(), True),
        StructField("leagueSeason", LongType(), True),
        StructField("leagueShortcut", StringType(), True),
        StructField(
            "location",
            StructType(
                [
                    StructField("locationCity", StringType(), True),
                    StructField("locationID", LongType(), True),
                    StructField("locationStadium", StringType(), True),
                ]
            ),
            True,
        ),
        StructField("matchDateTime", StringType(), True),
        StructField("matchDateTimeUTC", StringType(), True),
        StructField("matchID", LongType(), True),
        StructField("matchIsFinished", BooleanType(), True),
        StructField(
            "matchResults",
            ArrayType(
                StructType(
                    [
                        StructField("pointsTeam1", LongType(), True),
                        StructField("pointsTeam2", LongType(), True),
                        StructField("resultDescription", StringType(), True),
                        StructField("resultID", LongType(), True),
                        StructField("resultName", StringType(), True),
                        StructField("resultOrderID", LongType(), True),
                        StructField("resultTypeID", LongType(), True),
                    ]
                )
            ),
            True,
        ),
        StructField("numberOfViewers", LongType(), True),
        StructField(
            "team1",
            StructType(
                [
                    StructField("shortName", StringType(), True),
                    StructField("teamGroupName", StringType(), True),
                    StructField("teamIconUrl", StringType(), True),
                    StructField("teamId", LongType(), True),
                    StructField("teamName", StringType(), True),
                ]
            ),
            True,
        ),
        StructField(
            "team2",
            StructType(
                [
                    StructField("shortName", StringType(), True),
                    StructField("teamGroupName", StringType(), True),
                    StructField("teamIconUrl", StringType(), True),
                    StructField("teamId", LongType(), True),
                    StructField("teamName", StringType(), True),
                ]
            ),
            True,
        ),
        StructField("timeZoneID", StringType(), True),
    ]
)
