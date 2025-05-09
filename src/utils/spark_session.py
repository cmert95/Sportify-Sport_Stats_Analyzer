from pyspark.sql import SparkSession

from utils.logger import setup_logger

logger = setup_logger(name=__name__, log_name="spark_session")


def get_spark_session(app_name="MyProject", master="local[1]") -> SparkSession:
    """
    Creates and returns a SparkSession with configuration tailored for low-resource environments.
    Specifically optimized for AWS EC2 t2.micro/t3.micro instances:
    - 1 vCPU
    - 1 GiB RAM
    """
    try:
        spark = (
            SparkSession.builder.appName(app_name)
            .master(master)
            .config("spark.driver.memory", "512m")
            .config("spark.executor.memory", "512m")
            .config("spark.sql.shuffle.partitions", "2")
            .getOrCreate()
        )

        spark.sparkContext.setLogLevel("WARN")
        logger.info(f"Spark session started: {app_name} ({master})")
        return spark

    except Exception as e:
        logger.error(f"Failed to start Spark session: {e}")
        raise
