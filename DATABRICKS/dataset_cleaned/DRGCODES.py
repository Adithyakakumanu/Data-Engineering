# Databricks notebook source
files=dbutils.fs.ls("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4")
display(files)

# COMMAND ----------

df=spark.read.csv("dbfs:/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/DRGCODES.csv",header=True,inferSchema=True)
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC #Silver Layer

# COMMAND ----------

bronze_df = spark.table("bronze.drgcodes")

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

silver_df=silver_df.fillna("NA")

# COMMAND ----------

silver_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("silver.drgcodes_clean")

# COMMAND ----------

# MAGIC %md
# MAGIC #Gold Layer

# COMMAND ----------

silver_df = spark.table("silver.drgcodes_clean")

# COMMAND ----------

gold_df = silver_df.dropDuplicates()

# COMMAND ----------

gold_df.display()

# COMMAND ----------

gold_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.drgcodes_summary")

# COMMAND ----------

df.write.format("delta").mode("overwrite").saveAsTable("DRGCODES_Table")