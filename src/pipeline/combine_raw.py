from combine_raw_json import combine_raw_json_to_bronze
from utils.spark_session import get_spark_session


def main():
    spark = get_spark_session("Combine Raw JSON to Bronze")
    combine_raw_json_to_bronze(spark)
    spark.stop()


if __name__ == "__main__":
    main()
