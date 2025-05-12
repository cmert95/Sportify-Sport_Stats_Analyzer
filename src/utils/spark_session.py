from pyspark.sql import SparkSession

from config import (
    SPARK_APP_NAME,
    SPARK_DRIVER_MEMORY,
    SPARK_EXECUTOR_MEMORY,
    SPARK_EXTRA_CONFIGS,
    SPARK_MASTER,
    SPARK_SHUFFLE_PARTITIONS,
)
from utils.logger import setup_logger

logger = setup_logger(name=__name__, log_name="spark_session")


def get_spark_session(app_name=SPARK_APP_NAME, master=SPARK_MASTER) -> SparkSession:
    """
    Creates and returns a SparkSession.

    Default settings are tuned for low-resource environments,
    such as AWS EC2 t2.micro or t3.micro instances (1 vCPU, 1 GiB RAM).

    To customize the Spark session, update `config/settings.yaml`.
    """
    try:
        builder = (
            SparkSession.builder.appName(app_name)
            .master(master)
            .config("spark.driver.memory", SPARK_DRIVER_MEMORY)
            .config("spark.executor.memory", SPARK_EXECUTOR_MEMORY)
            .config("spark.sql.shuffle.partitions", str(SPARK_SHUFFLE_PARTITIONS))
        )

        # Extra Spark config'leri uygula (varsa)
        for key, value in SPARK_EXTRA_CONFIGS.items():
            builder = builder.config(key, value)

        spark = builder.getOrCreate()
        spark.sparkContext.setLogLevel("WARN")

        logger.info(f"Spark session started: {app_name} ({master})")
        logger.info(f"Active shuffle partitions: {spark.conf.get('spark.sql.shuffle.partitions')}")
        logger.info(f"Driver memory: {spark.conf.get('spark.driver.memory')}")
        logger.info(f"Executor memory: {spark.conf.get('spark.executor.memory')}")
        return spark

    except Exception as e:
        logger.error(f"Failed to start Spark session: {e}")
        raise
