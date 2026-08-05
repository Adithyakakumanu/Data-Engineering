# Databricks notebook source
# DBTITLE 1,Cell 1
files = dbutils.fs.ls("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4")
display(files)

# COMMAND ----------

df=spark.read.csv("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/CALLOUT.csv",header="true",inferSchema="true")
df.display()

# COMMAND ----------

# from pyspark.ml.feature import Imputer

# imputer = Imputer(
#     inputCols=["glucose", "blood_pressure"],
#     outputCols=["glucose_imputed", "blood_pressure_imputed"]
# ).setStrategy("mean")

# df = imputer.fit(df).transform(df)

# from pyspark.sql.functions import when, col

# df = df.withColumn(
#     "death_flag",
#     when(col("death_date").isNotNull(), 1).otherwise(0)
# )
# from pyspark.ml.feature import StringIndexer

# indexer = StringIndexer(
#     inputCol="gender",
#     outputCol="gender_index"
# )
# df = indexer.fit(df).transform(df)

# from pyspark.ml.feature import OneHotEncoder

# encoder = OneHotEncoder(
#     inputCol="gender_index",
#     outputCol="gender_ohe"
# )
# df = encoder.fit(df).transform(df)
# from pyspark.ml.feature import MinMaxScaler

# scaler = MinMaxScaler(
#     inputCol="features",
#     outputCol="normalized_features"
# )

# df = scaler.fit(df).transform(df)



# COMMAND ----------

# MAGIC %skip
# MAGIC from pyspark.sql.functions import year, month, dayofmonth, hour, minute, second
# MAGIC
# MAGIC df.withColumn("year", year("event_time")) \
# MAGIC        .withColumn("month", month("event_time")) \
# MAGIC        .withColumn("day", dayofmonth("event_time")) \
# MAGIC        .withColumn("hour", hour("event_time")) \
# MAGIC        .withColumn("minute", minute("event_time")) \
# MAGIC        .withColumn("second", second("event_time"))
# MAGIC
# MAGIC
# MAGIC from pyspark.sql.functions import to_date
# MAGIC
# MAGIC df.withColumn(
# MAGIC     "event_date",
# MAGIC     to_date("event_timestamp")
# MAGIC )
# MAGIC
# MAGIC from pyspark.sql.functions import date_format
# MAGIC
# MAGIC df.withColumn(
# MAGIC     "event_time",
# MAGIC     date_format("event_timestamp", "HH:mm:ss")
# MAGIC )
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC #Silver Layer

# COMMAND ----------

bronze_df=spark.table("bronze.callout")

# COMMAND ----------

bronze_df.count()

# COMMAND ----------

silver_df=bronze_df.dropDuplicates()

# COMMAND ----------

silver_df.describe().display()

# COMMAND ----------

from pyspark.sql.functions import when, col, sum

null_counts = silver_df.select([
    sum(when(col(c).isNull(), 1).otherwise(0)).alias(c)
    for c in silver_df.columns
])

# Filter columns with at least one null value
null_columns = [c for c in null_counts.columns if null_counts.collect()[0][c] > 0]
display(null_counts.select(null_columns))

# COMMAND ----------

from pyspark.sql.functions import unix_timestamp,col

silver_df=silver_df.withColumn("stay_duration_hours",
    (unix_timestamp("outcometime") - unix_timestamp("firstreservationtime")) / 3600
)


# COMMAND ----------


silver_df = silver_df.fillna("NA")

# COMMAND ----------

silver_df.select('submit_careunit').distinct().display()
silver_df.select('discharge_wardid').distinct().display()
silver_df.select('acknowledgetime').distinct().display()
silver_df.select('firstreservationtime').distinct().display()
silver_df.select('currentreservationtime').distinct().display()


# COMMAND ----------

silver_df= silver_df.withColumnRenamed("curr_careunit", "ccurr_careunit")

# COMMAND ----------

silver_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("silver.callout_clean")

# COMMAND ----------

# MAGIC %md
# MAGIC #Gold Layer

# COMMAND ----------

silver_df = spark.table("silver.callout_clean")

# COMMAND ----------

from pyspark.sql.functions import to_date

cols_to_exclude = ['firstreservationtime','currentreservationtime']
value_cols = [c for c in silver_df.columns if c not in cols_to_exclude]

gold_df = silver_df.select(value_cols)

# timestamp_cols = [c for c, t in gold_df.dtypes if t in ("timestamp", "date")]
# for c in timestamp_cols:
#     gold_df = gold_df.withColumn(c, to_date(gold_df[c]))


# COMMAND ----------

# DBTITLE 1,Untitled
gold_df.display()

# COMMAND ----------

# Gold layer: Aggregate and enrich data for analytics
from pyspark.sql.functions import count, avg

# Example: Aggregate callouts per ward and average response/request times
gold_df = df.groupBy("callout_wardid").agg(
    count("row_id").alias("callout_count"),
    avg("request_resp").alias("avg_request_resp"),
    avg("request_tele").alias("avg_request_tele")
)

display(gold_df)

# Visualization: Plot callout counts per ward
import matplotlib.pyplot as plt

callout_counts = gold_df.select("callout_wardid", "callout_count").toPandas()
plt.figure(figsize=(10,6))
plt.bar(callout_counts["callout_wardid"], callout_counts["callout_count"])
plt.xlabel("Callout Ward ID")
plt.ylabel("Callout Count")
plt.title("Callout Counts per Ward")
plt.show()

# COMMAND ----------

gold_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.callout_summary")

# COMMAND ----------

df.write.format("delta").mode("overwrite").saveAsTable("callout_Table")