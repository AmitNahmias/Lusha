from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType

from conf import CSV_DB_PATH, DRIVER_PATH, DB_CONF
from country_code_parser import parse_country_code
from logger import setup_logger
from name_parser import extract_name
from phone_number_parser import parse_phone_number

LOGGER = setup_logger(__name__)

spark_session: SparkSession = (SparkSession.builder
                               .appName('TrueCaller')
                               .config("spark.executor.memory", "8g")
                               .config("spark.driver.memory", "8g")
                               .config("spark.master", "local[*]")
                               .config("spark.jars", DRIVER_PATH)
                               .getOrCreate())

extract_name_udf = udf(extract_name, StringType())
parse_phone_number_udf = udf(parse_phone_number, StringType())
parse_country_code_udf = udf(parse_country_code, StringType())

spark_df = spark_session.read.csv(CSV_DB_PATH, header=True, inferSchema=True)

# At first, parsing all the phone numbers
transformed_spark_df = spark_df.withColumn('parsed_phone_number',
                                           parse_phone_number_udf(spark_df['phone_number'], spark_df['location']))

# Filter out rows where parsed_phone_number is None to reduce work
transformed_spark_df = transformed_spark_df.filter(col("parsed_phone_number").isNotNull())

# Add the country code of the number
transformed_spark_df = transformed_spark_df.withColumn('country_code',
                                                       parse_country_code_udf(transformed_spark_df['phone_number']))

# Extracting the names of the people based on the text in 'name' column
transformed_spark_df = transformed_spark_df.withColumn('parsed_name', extract_name_udf(transformed_spark_df['name']))

# Filter out rows where parsed_name is None to reduce work
transformed_spark_df = transformed_spark_df.filter(col("parsed_name").isNotNull())

transformed_spark_df = transformed_spark_df.drop('num_of_records')
LOGGER.debug('Dropped column num_of_records')

LOGGER.info('Starting to write into the DB')
LOGGER.debug(f'Inserting to schema: {DB_CONF["schema"]} on table {DB_CONF["table"]}')

(transformed_spark_df.select("name", "phone_number", "source", "location", "work_email", "parsed_phone_number",
                             "country_code", "parsed_name")
 .write.format("jdbc")
 .option("url", DB_CONF['url'])
 .option("driver", DB_CONF['driver'])
 .option("dbtable", f'{DB_CONF["schema"]}.{DB_CONF["table"]}')
 .option("user", DB_CONF["user"])
 .option("password", DB_CONF["password"]).save(mode='append'))

LOGGER.info('Finished inserting to DB')
LOGGER.debug(f'Inserted to schema: {DB_CONF["schema"]} on table {DB_CONF["table"]}')