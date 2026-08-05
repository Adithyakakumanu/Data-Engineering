# Databricks notebook source
files=dbutils.fs.ls("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4")
display(files)

# COMMAND ----------

df=spark.read.csv("dbfs:/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/D_ICD_DIAGNOSES.csv",header=True,inferSchema=True)
df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC #Silver Layer

# COMMAND ----------

bronze_df = spark.table("bronze.d_icd_diagnoses")

# COMMAND ----------

silver_df = bronze_df.dropDuplicates()

# COMMAND ----------

silver_df.display()

# COMMAND ----------

silver_df.describe().display()

# COMMAND ----------

silver_df.select("long_title").distinct().count()

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

rows = [Row(column=k, null_count=v,null_percentage=round((v / total_rows), 2)) for k, v in null_counts.items()]

spark.createDataFrame(rows).display()


# COMMAND ----------

silver_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("silver.d_icd_diagnoses_clean")

# COMMAND ----------

silver_df = spark.table("silver.d_icd_diagnoses_clean")

# COMMAND ----------

from pyspark.sql.functions import count
gold_df = silver_df.groupBy("short_title", "long_title").agg(count("icd9_code").alias("total_diagnoses"))

# COMMAND ----------

gold_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.d_icd_diagnoses_summary")

# COMMAND ----------

df.write.format("delta").mode("overwrite").saveAsTable("D_ICD_DIAGNOSES_table")