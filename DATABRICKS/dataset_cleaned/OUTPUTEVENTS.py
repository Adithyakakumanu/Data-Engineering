# Databricks notebook source
a=dbutils.fs.ls("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4")
display(a)

# COMMAND ----------

db=spark.read.csv("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/OUTPUTEVENTS.csv",header=True,inferSchema=True)
display(db)

# COMMAND ----------

# MAGIC %md
# MAGIC #Silver Layer

# COMMAND ----------

bronze_df = spark.table("bronze.outputevents")

# COMMAND ----------

silver_df = bronze_df.dropDuplicates()

# COMMAND ----------

silver_df.describe().display()

# COMMAND ----------

silver_df.count()

# COMMAND ----------

silver_df.printSchema()

# COMMAND ----------

silver_df.display()

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql import *

total_rows = silver_df.count()
null_counts = silver_df.select([
    sum(when(col(c).isNull(), 1).otherwise(0)).alias(c)
    for c in silver_df.columns
]).collect()[0].asDict()

rows = [Row(column=k, null_count=v,null_percentage=(v / total_rows)) for k, v in null_counts.items() if v > 0]

spark.createDataFrame(rows).display()


# COMMAND ----------

silver_df=silver_df.withColumn("duration",round((unix_timestamp("storetime")-unix_timestamp("charttime"))/60,2))

# COMMAND ----------

silver_df.select('valueuom').distinct().display()


# COMMAND ----------

silver_df=silver_df.fillna("NA")

# COMMAND ----------

silver_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("silver.outputevents_clean")

# COMMAND ----------

# MAGIC %md
# MAGIC #Gold Layer

# COMMAND ----------

silver_df = spark.table("silver.outputevents_clean")

# COMMAND ----------

from pyspark.sql.functions import to_date

cols_to_exclude = ['stopped','newbottle','iserror','charttime','storetime']
value_cols = [c for c in silver_df.columns if c not in cols_to_exclude]

gold_df = silver_df.select(value_cols)

# COMMAND ----------

# DBTITLE 1,Cell 17
gold_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.outputevents_summary")

# COMMAND ----------

db.write.mode("overwrite").saveAsTable("outputevents_table")