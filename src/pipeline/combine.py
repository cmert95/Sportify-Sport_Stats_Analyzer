from combine_raw_json import combine_raw_json_to_bronze
from utils.logger import setup_logger
from utils.spark_session import get_spark_session

logger = setup_logger(__name__, log_name="combine_seasons")


def main():
    spark = get_spark_session("Combine Raw JSON to Bronze")
    logger.info("Spark session started")
    combine_raw_json_to_bronze(spark)
    spark.stop()
    logger.info("Spark session stopped")


if __name__ == "__main__":
    main()
