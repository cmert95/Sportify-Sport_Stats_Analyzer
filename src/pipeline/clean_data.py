from clean_bronze_data import clean_bronze_data
from utils.spark_session import get_spark_session


def main():
    spark = get_spark_session("Clean Bronze Data")
    clean_bronze_data(spark)
    spark.stop()


if __name__ == "__main__":
    main()
