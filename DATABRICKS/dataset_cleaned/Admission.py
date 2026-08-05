# Databricks notebook source
# spark.conf.set(
#   "fs.azure.account.key.mimicstorage12345.dfs.core.windows.net",
#   "YOUR_ACCESS_KEY")

# COMMAND ----------

files = [
"ADMISSIONS",
"PATIENTS",
"CALLOUT",
"CAREGIVERS",
"CHARTEVENTS",
"CPTEVENTS",
"DIAGNOSES_ICD",
"D_CPT",
"DRGCODES",
"OUTPUTEVENTS",
"D_ICD_DIAGNOSES",
"D_ICD_PROCEDURES",
"DATETIMEEVENTS",
"INPUTEVENTS_CV",
"INPUTEVENTS_MV",
"MICROBIOLOGYEVENTS",
"NOTEEVENTS",
"PROCEDUREEVENTS_MV",
"PROCEDURES_ICD",
"SERVICES",
"TRANSFERS",
"D_ITEMS",
"D_LABITEMS",
"ICUSTAYS",
"LABEVENTS",
"PRESCRIPTIONS"
]
base_path = "/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/"

for file in files:

    df = spark.read.csv(
        base_path + file + ".csv",
        header=True,
        inferSchema=True
    )

    table_name = "bronze." + file.lower()

    df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable(table_name)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE IF NOT EXISTS bronze;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE IF NOT EXISTS silver;
# MAGIC CREATE DATABASE IF NOT EXISTS gold;

# COMMAND ----------

# MAGIC %md
# MAGIC #Bronze Layer

# COMMAND ----------

df=spark.read.csv("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/ADMISSIONS.csv",header=True,inferSchema=True)
#display(df)
df.show()

# COMMAND ----------

df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("bronze.admissions")

# COMMAND ----------

# MAGIC %md
# MAGIC #Silver Layer

# COMMAND ----------

bronze_df = spark.table("bronze.admissions")

# COMMAND ----------

silver_df = bronze_df.dropDuplicates()

# COMMAND ----------

silver_df.describe().display()

# COMMAND ----------

# from pyspark.sql.functions import to_date
# df = df.withColumn("date", to_date("timestamp_col"))
# from pyspark.sql.functions import date_format
# df = df.withColumn("time", date_format("timestamp_col", "HH:mm:ss"))
# from pyspark.sql.functions import year, month, dayofmonth, hour
# df = df.withColumn("year", year("timestamp_col")) \
#        .withColumn("month", month("timestamp_col")) \
#        .withColumn("day", dayofmonth("timestamp_col")) \
#        .withColumn("hour", hour("timestamp_col"))

# COMMAND ----------

# from pyspark.ml.feature import StringIndexer,OneHotEncoder
# from pyspark.ml.feature import MinMaxScaler
# from pyspark.ml.feature import StandardScaler

# scaler = StandardScaler(
#     inputCol="numeric_vector",
#     outputCol="standardized_features",
#     withMean=True,
#     withStd=True
# )

# df = scaler.fit(df).transform(df)

# scaler = MinMaxScaler(
#     inputCol="numeric_vector",
#     outputCol="normalized_features"
# )

# df = scaler.fit(df).transform(df)

# encoder = OneHotEncoder(
#     inputCol="category_index",
#     outputCol="category_ohe"
# )
# indexer = StringIndexer(
#     inputCol="category_column",
#     outputCol="category_index"
# )
# df = encoder.fit(df).transform(df)

# df = indexer.fit(df).transform(df)


# COMMAND ----------

silver_df.count()

# COMMAND ----------

silver_df.printSchema()

# COMMAND ----------

schema = """
row_id INT,
subject_id INT,
hadm_id INT,
admittime TIMESTAMP,
dischtime TIMESTAMP,
deathtime TIMESTAMP,
admission_type STRING,
admission_location STRING,
discharge_location STRING,
insurance STRING,
language STRING,
religion STRING,
marital_status STRING,
ethnicity STRING,
edregtime TIMESTAMP,
edouttime TIMESTAMP,
diagnosis STRING,
hospital_expire_flag INT,
has_chartevents_data INT
"""
silver_df = spark.read \
    .option("header", "true") \
    .schema(schema).csv("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/ADMISSIONS.csv")
silver_df.printSchema()

#df.withColumn("salary", col("salary").cast("double"))
#schema = StructType([
#     StructField("name", StringType(), True),
#     StructField("age", IntegerType(), True)
# ])

# COMMAND ----------

silver_df.display()

# COMMAND ----------

silver_df.columns

# COMMAND ----------

# %sql
# -- Bronze Layer: raw admissions data
# CREATE LIVE TABLE bronze_admissions
# TBLPROPERTIES ("pipelines.autoOptimize.managed" = "true")
# AS
# SELECT *
# FROM cloud_files(
#   '/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/ADMISSIONS.csv',
#   'csv',
#   header=true,
#   inferSchema=true
# );
# -- Silver Layer: clean admissions data
# CREATE LIVE TABLE silver_admissions
# TBLPROPERTIES ("pipelines.autoOptimize.managed" = "true")
# AS
# SELECT
#     admission_id,
#     subject_id,
#     hadm_id,
#     coalesce(admission_type,'Unknown') AS admission_type,
#     coalesce(insurance,'Unknown') AS insurance,
#     coalesce(admission_location,'Unknown') AS admission_location,
#     coalesce(discharge_location,'Unknown') AS discharge_location,
#     coalesce(language,'Unknown') AS language,
#     coalesce(marital_status,'Unknown') AS marital_status,
#     coalesce(religion,'Unknown') AS religion,
#     coalesce(ethnicity,'Unknown') AS ethnicity,
#     admittime,
#     dischtime,
#     deathtime,
#     hospital_expire_flag
# FROM live.bronze_admissions
# WHERE admission_id IS NOT NULL
# ;
# -- Gold Layer: admissions analytics
# CREATE LIVE TABLE gold_admissions_summary
# TBLPROPERTIES ("pipelines.autoOptimize.managed" = "true")
# AS
# SELECT
#     admission_type,
#     COUNT(*) AS total_admissions,
#     SUM(hospital_expire_flag) AS deaths
# FROM live.silver_admissions
# GROUP BY admission_type
# ;

# COMMAND ----------

from pyspark.sql.functions import col, when, sum
from pyspark.sql import Row

total_rows = silver_df.count()
null_counts = silver_df.select([
    sum(when(col(c).isNull(), 1).otherwise(0)).alias(c)
    for c in silver_df.columns
]).collect()[0].asDict()

rows = [Row(column=k, null_count=v,null_percentage=round((v / total_rows), 2)) for k, v in null_counts.items() if v > 0]

spark.createDataFrame(rows).display()


# COMMAND ----------

col_null_threshold = 0.5
cols_to_drop = [
    c for c, nulls in null_counts.items()
    if nulls / total_rows > col_null_threshold

]
#df=df.drop(*cols_to_drop)

# COMMAND ----------

# DBTITLE 1,Untitled
# from pyspark.sql.functions import to_date
# df = df.withColumn("admitdate", to_date(col("admittime"),"dd-mm-yyy"))
# df = df.withColumn("dischdate", to_date(col("dischtime"),"dd-mm-yyy"))
# df = df.withColumn("deathdate", to_date(col("deathtime"),"dd-mm-yyy"))
# df = df.withColumn("edregdate", to_date(col("edregtime"),"dd-mm-yyy"))
# df = df.withColumn("edoutdate", to_date(col("edouttime"),"dd-mm-yyy"))
# df = df.withColumn("edoutdate", to_date(col("edouttime"),"dd-mm-yyy"))

# COMMAND ----------

# from pyspark.sql.functions import date_format

# df = df.withColumn("admittime", date_format(col("admittime"), "HH:mm:ss"))
# df = df.withColumn("dischtime", date_format(col("dischtime"), "HH:mm:ss"))
# df = df.withColumn("deathtime", date_format(col("deathtime"), "HH:mm:ss"))
# df = df.withColumn("edregtime", date_format(col("edregtime"), "HH:mm:ss"))
# df = df.withColumn("edouttime", date_format(col("edouttime"), "HH:mm:ss"))


# COMMAND ----------


silver_df.select('marital_status').distinct().display()
silver_df.select('language').distinct().display()

# COMMAND ----------

silver_df=silver_df.fillna("NA")

# COMMAND ----------

silver_df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC # fill null values as mean
# MAGIC

# COMMAND ----------

# from pyspark.sql.functions import avg

# numeric_cols = [c for c, t in df.dtypes if t.startswith(("int", "bigint", "double", "float", "decimal"))]

# means = df.select([
#     avg(c).alias(c) for c in numeric_cols
# ]).collect()[0].asDict()

# df = df.fillna(means)


# COMMAND ----------

# MAGIC %md
# MAGIC # fill null values as mode

# COMMAND ----------

# from pyspark.sql.functions import desc
# string_cols = [c for c, t in df.dtypes if t == "string"]
# modes = {}
# for c in string_cols:
#     mode_val = (
#         df.filter(df[c].isNotNull())
#           .groupBy(c)
#           .count()
#           .orderBy(desc("count"))
#           .first()
#     )
#     if mode_val:
#         modes[c] = mode_val[0]
# df = df.fillna(modes)

# COMMAND ----------

display(silver_df.limit(10))

# COMMAND ----------

# df = df.fillna({"event_time": "1970-01-01 00:00:00"})
# timestamp_cols = [c for c, t in df.dtypes if t in ("timestamp", "date")]
# fill_dict = {c: "1970-01-01 00:00:00" for c in timestamp_cols}
# df = df.fillna(fill_dict)

# COMMAND ----------

# df.dropna(how="all",thresh=None)
# cols_to_check = ["deathtime", "edouttime"]

# df_clean = df
# for c in cols_to_check:
#     df_clean = df_clean.filter(
#         (col(c).isNotNull()) & (col(c) != "") & (col(c).lower() != "null")
#     )



# COMMAND ----------

#df.dropna(subset=["language","edregtime","marital_status","edouttime"]) #drop rows
#df=df.drop("deathtime","language","edregtime","marital_status","edouttime") #drop columns



# COMMAND ----------

silver_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("silver.admissions_clean")

# COMMAND ----------

# MAGIC %md
# MAGIC #Gold Layer

# COMMAND ----------

silver_df = spark.table("silver.admissions_clean")

# COMMAND ----------

from pyspark.sql.functions import to_date

cols_to_exclude = ["language", "religion"]
value_cols = [c for c in silver_df.columns if c not in cols_to_exclude]
gold_df = silver_df.select(value_cols)

# COMMAND ----------

# DBTITLE 1,Untitled
gold_df.write.format("delta") \
.mode("overwrite") \
.option("overwriteSchema", "true") \
.saveAsTable("gold.admission_summary")

# COMMAND ----------

gold_df.display()

# COMMAND ----------

# spark.sql("drop table if exists admission_table")

# COMMAND ----------

# DBTITLE 1,Write DataFrame as Delta Table (fixed)
df.write.format("delta").mode("overwrite").saveAsTable("admission_table")