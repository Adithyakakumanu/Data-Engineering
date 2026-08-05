# Databricks notebook source
a=dbutils.fs.ls("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4")
display(a)

# COMMAND ----------

db=spark.read.csv("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/PROCEDUREEVENTS_MV.csv",header=True,inferSchema=True)
display(db)

# COMMAND ----------

# MAGIC %md
# MAGIC #Silver Layer

# COMMAND ----------

bronze_df = spark.table("bronze.procedureevents_mv")

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
.saveAsTable("silver.procedureevents_mv_clean")

# COMMAND ----------

# MAGIC %md
# MAGIC #Gold Layer

# COMMAND ----------

silver_df = spark.table("silver.procedureevents_mv_clean")

# COMMAND ----------

from pyspark.sql.functions import to_date

cols_to_exclude = [ "secondaryordercategoryname","comments_edited","comments_date","comments_cancelled"]
value_cols = [c for c in silver_df.columns if c not in cols_to_exclude]

gold_df = silver_df.select(value_cols)
gold_df = gold_df.dropna()

# COMMAND ----------

gold_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.procedureevents_mv_summary")

# COMMAND ----------

db.write.mode("overwrite").saveAsTable("procedureevents_mv_table")