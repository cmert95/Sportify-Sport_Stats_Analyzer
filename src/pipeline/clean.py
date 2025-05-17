from clean_bronze_data import clean_bronze_data
from utils.logger import setup_logger
from utils.spark_session import get_spark_session

logger = setup_logger(__name__, log_name="clean_data")


def main():
    spark = get_spark_session("Clean Bronze Data")
    logger.info("Spark session started")
    clean_bronze_data(spark)
    spark.stop()
    logger.info("Spark session stopped")


if __name__ == "__main__":
    main()
