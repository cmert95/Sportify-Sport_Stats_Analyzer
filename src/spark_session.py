from pyspark.sql import SparkSession


def create_spark_session(app_name="FootballAPIProject", master="local[1]"):
    spark = (
        SparkSession.builder.appName(app_name)
        .master(master)
        .config("spark.driver.memory", "512m")
        .config("spark.executor.memory", "512m")
        .config("spark.sql.shuffle.partitions", "2")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")
    return spark
