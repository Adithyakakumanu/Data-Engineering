# Databricks notebook source
a=dbutils.fs.ls("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4")
display(a)

# COMMAND ----------

db=spark.read.csv("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/D_ICD_PROCEDURES.csv",header="true",inferSchema="true")
db.display()

# COMMAND ----------

# MAGIC %md
# MAGIC #Silver Layer

# COMMAND ----------

bronze_df = spark.table("bronze.d_icd_procedures")

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

# DBTITLE 1,Fix NameError: import Row
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

silver_df.select("long_title").distinct().count()

# COMMAND ----------

silver_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("silver.d_icd_procedures_clean")

# COMMAND ----------

silver_df = spark.table("silver.d_icd_procedures_clean")

# COMMAND ----------

gold_df = silver_df.groupBy("short_title", "long_title").count()
gold_df.display()

# COMMAND ----------

gold_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.d_icd_procedures_summary")

# COMMAND ----------

db.write.mode("overwrite").saveAsTable("d_icd_procedures_table")