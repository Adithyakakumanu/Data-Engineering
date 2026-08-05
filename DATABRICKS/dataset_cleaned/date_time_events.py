# Databricks notebook source
files = dbutils.fs.ls("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4")
display(files)

# COMMAND ----------

# DBTITLE 1,Cell 2
df = spark.read.csv("dbfs:/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/DATETIMEEVENTS.csv", header=True, inferSchema=True)
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC #Silver Layer

# COMMAND ----------

bronze_df = spark.table("bronze.datetimeevents")

# COMMAND ----------

silver_df = bronze_df.dropDuplicates()

# COMMAND ----------

silver_df.display()

# COMMAND ----------

silver_df.describe().display()

# COMMAND ----------

silver_df.count()

# COMMAND ----------

silver_df.printSchema()

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

silver_df.select("warning").distinct().display()
silver_df.select("error").distinct().display()
silver_df.select("stopped").distinct().display()
# df.filter(col("column_name") == "value_to_count").count()
# df.groupBy("stopped").count().display()

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql import *
silver_df=silver_df.withColumn("duration",unix_timestamp(col("storetime"))-unix_timestamp(col("charttime")))


# COMMAND ----------

silver_df=silver_df.fillna("NA")

# COMMAND ----------

silver_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("silver.datetimeevents_clean")

# COMMAND ----------

# MAGIC %md
# MAGIC #Gold Layer

# COMMAND ----------

silver_df = spark.table("silver.datetimeevents_clean")

# COMMAND ----------

from pyspark.sql.functions import to_date

cols_to_exclude = ["warning", "error","resultstatus","storetime","charttime"]
value_cols = [c for c in silver_df.columns if c not in cols_to_exclude]

gold_df = silver_df.select(value_cols)

timestamp_cols = [c for c, t in gold_df.dtypes if t in ("timestamp", "date")]
for c in timestamp_cols:
    gold_df = gold_df.withColumn(c, to_date(gold_df[c]))

# gold_df = gold_df.dropna()

# COMMAND ----------

gold_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.datetimeevents_summary")

# COMMAND ----------

# MAGIC %skip
# MAGIC spark.sql("drop table if exists datetimeevents_Table")

# COMMAND ----------

df.write.format("delta").mode("overwrite").saveAsTable("datetimeevents_Table")