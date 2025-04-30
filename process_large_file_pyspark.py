from itertools import count

from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode
from pyspark.sql.types import ArrayType, StringType, StructField, StructType

conf = SparkConf()
conf.set("spark.driver.memory", "4g")
conf.set("spark.executor.memory", "4g")
conf.set("spark.sql.shuffle.partitions", "100")

spark = (
    SparkSession.builder.appName("Large File Transaction Processor").config(conf=conf).getOrCreate()
)

schema = StructType(
    [
        StructField(
            "Stores",
            ArrayType(
                StructType(
                    [
                        StructField("StoreID", StringType(), True),
                        StructField("StoreName", StringType(), True),
                        StructField(
                            "Transactions",
                            ArrayType(
                                StructType(
                                    [
                                        StructField("TransactionID", StringType(), True),
                                        StructField("Date", StringType(), True),
                                        StructField("Amount", StringType(), True),
                                    ]
                                )
                            ),
                            True,
                        ),
                    ]
                )
            ),
            True,
        )
    ]
)

file_path = "/var/www/large_file.json"
df = spark.read.schema(schema).option("multiline", "true").json(file_path)

stores_df = df.select(explode(col("Stores")).alias("store"))
transactions_df = stores_df.select(
    col("store.StoreID").alias("StoreID"),
    col("store.StoreName").alias("StoreName"),
    explode(col("store.Transactions")).alias("transaction"),
)

transactions_df = transactions_df.repartition(100)


def process_partition(partition):

    for row in partition:
        store_id = row.StoreID
        store_name = row.StoreName
        transaction = row.transaction.asDict()
        print(
            f"Processing TransactionID {transaction['TransactionID']} for Store {store_id} - {store_name}"
        )


transactions_df.foreachPartition(process_partition)

spark.stop()
