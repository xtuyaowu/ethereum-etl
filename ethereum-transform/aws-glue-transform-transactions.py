import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
## @type: DataSource
## @args: [database = "lab1", table_name = "transactions", transformation_ctx = "datasource0"]
## @return: datasource0
## @inputs: []
datasource0 = glueContext.create_dynamic_frame.from_catalog(database="lab1", table_name="transactions",
                                                            transformation_ctx="datasource0")
## @type: ApplyMapping
## @args: [mapping = [("tx_hash", "string", "tx_hash", "string"), ("tx_nonce", "long", "tx_nonce", "long"), ("tx_block_hash", "string", "tx_block_hash", "string"), ("tx_block_number", "long", "tx_block_number", "long"), ("tx_index", "long", "tx_index", "long"), ("tx_from", "string", "tx_from", "string"), ("tx_to", "string", "tx_to", "string"), ("tx_value", "long", "tx_value", "long"), ("tx_gas", "long", "tx_gas", "long"), ("tx_gas_price", "long", "tx_gas_price", "long"), ("tx_input", "string", "tx_input", "string")], transformation_ctx = "applymapping1"]
## @return: applymapping1
## @inputs: [frame = datasource0]
applymapping1 = ApplyMapping.apply(frame=datasource0, mappings=[
    ("start_block", "long", "start_block", "long"),
    ("end_block", "long", "end_block", "long"),
    ("tx_hash", "string", "tx_hash", "string"),
    ("tx_nonce", "long", "tx_nonce", "long"),
    ("tx_block_hash", "string", "tx_block_hash", "string"),
    ("tx_block_number", "long", "tx_block_number", "long"),
    ("tx_index", "long", "tx_index", "long"),
    ("tx_from", "string", "tx_from", "string"),
    ("tx_to", "string", "tx_to", "string"),
    ("tx_value", "long", "tx_value", "long"),
    ("tx_gas", "long", "tx_gas", "long"),
    ("tx_gas_price", "long", "tx_gas_price", "long"),
    ("tx_input", "string", "tx_input", "string")],
                                   transformation_ctx="applymapping1")
## @type: ResolveChoice
## @args: [choice = "make_struct", transformation_ctx = "resolvechoice2"]
## @return: resolvechoice2
## @inputs: [frame = applymapping1]
resolvechoice2 = ResolveChoice.apply(frame=applymapping1, choice="make_struct", transformation_ctx="resolvechoice2")
## @type: DropNullFields
## @args: [transformation_ctx = "dropnullfields3"]
## @return: dropnullfields3
## @inputs: [frame = resolvechoice2]
dropnullfields3 = DropNullFields.apply(frame=resolvechoice2, transformation_ctx="dropnullfields3")
## @type: DataSink
## @args: [connection_type = "s3", connection_options = {"path": "s3://<your_bucket>/glue/transactions"}, format = "parquet", transformation_ctx = "datasink4"]
## @return: datasink4
## @inputs: [frame = dropnullfields3]
datasink4 = glueContext.write_dynamic_frame.from_options(frame=dropnullfields3, connection_type="s3",
                                                         connection_options={
                                                             "path": "s3://<your_bucket>/glue/transactions",
                                                             "partitionKeys": ["start_block", "end_block"]},
                                                         format="parquet", transformation_ctx="datasink4")
job.commit()
