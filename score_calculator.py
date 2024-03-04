from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import count, col, DataFrame

from conf import DRIVER_PATH


def add_score(df: DataFrame) -> DataFrame:
    """
    Calculating score for record.
    The calculation is how many times the name occurs + how many times the phone occurs.

    :param df: Input pyspark dataframe.
    :return: Dataframe with new column 'score'.
    """
    df_with_score = df.withColumn("score",
                                  count("parsed_phone_number").over(Window.partitionBy("parsed_phone_number")) + count(
                                      "parsed_name").over(Window.partitionBy("parsed_name")))
    return df_with_score
