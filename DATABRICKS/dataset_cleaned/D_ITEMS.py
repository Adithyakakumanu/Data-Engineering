# Databricks notebook source
  a=dbutils.fs.ls("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4")
display(a)

# COMMAND ----------

db=spark.read.csv("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/D_ITEMS.csv",header=True,inferSchema=True)
db.describe().display()

# COMMAND ----------

# MAGIC %md
# MAGIC #Silver Layer

# COMMAND ----------

bronze_df = spark.table("bronze.d_items")

# COMMAND ----------

silver_df = bronze_df.dropDuplicates()

# COMMAND ----------

silver_df.display()

# COMMAND ----------

silver_df.select('label').distinct().display()
silver_df.select('dbsource').distinct().display()
silver_df.select('linksto').distinct().display()
silver_df.select('unitname').distinct().display()
silver_df.select('param_type').distinct().display()
silver_df.select('category').distinct().display()


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

rows = [Row(column=k, null_count=v,null_percentage=round((v / total_rows), 2)) for k, v in null_counts.items() if v > 0]

spark.createDataFrame(rows).display()


# COMMAND ----------

silver_df=silver_df.fillna("NA")

# COMMAND ----------

silver_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("silver.d_items_clean")

# COMMAND ----------

silver_df = spark.table("silver.d_items_clean")

# COMMAND ----------

silver_df = silver_df.drop("conceptid")
gold_df = silver_df.filter(~(
    (col("abbreviation") == "NA") &
    (col("category") == "NA") &
    (col("unitname") == "NA") &
    (col("param_type") == "NA")
))

# COMMAND ----------

gold_df.distinct().display()

# COMMAND ----------

gold_df.count()

# COMMAND ----------

gold_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.d_items_summary")

# COMMAND ----------

db.write.mode("overwrite").saveAsTable("d_items_table")

# COMMAND ----------

# db.write.mode("overwrite").parquet("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/ICUSTAYS.parquet")