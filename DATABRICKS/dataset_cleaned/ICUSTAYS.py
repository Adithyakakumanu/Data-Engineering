# Databricks notebook source
a=dbutils.fs.ls("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4")
display(a)

# COMMAND ----------

db=spark.read.csv("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/ICUSTAYS.csv",header=True,inferSchema=True)
db.display()

# COMMAND ----------

# MAGIC %md
# MAGIC #Silver Layer

# COMMAND ----------

bronze_df = spark.table("bronze.icustays")

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

from pyspark.sql.functions import *
from pyspark.sql import *

total_rows = silver_df.count()
null_counts = silver_df.select([
    sum(when(col(c).isNull(), 1).otherwise(0)).alias(c)
    for c in silver_df.columns
]).collect()[0].asDict()

rows = [Row(column=k, null_count=v,null_percentage=(v / total_rows)) for k, v in null_counts.items()]

spark.createDataFrame(rows).display()


# COMMAND ----------

silver_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("silver.icustays_clean")

# COMMAND ----------

# MAGIC %md
# MAGIC #Gold Layer

# COMMAND ----------

silver_df = spark.table("silver.icustays_clean")

# COMMAND ----------

gold_df = silver_df.drop('intime','outtime','stay_time')

# COMMAND ----------

gold_df.display()

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE workspace.default.combined_summary AS
# MAGIC SELECT mv.curr_service,mv.prev_service,cv.curr_careunit,cv.eventtype,cv.prev_careunit,cv.hadm_id,cv.subject_id,cv.los as time_in_services
# MAGIC FROM workspace.gold.services_summary AS mv
# MAGIC inner JOIN workspace.gold.transfers_summary AS cv ON cv.subject_id = mv.subject_id;

# COMMAND ----------

gold_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.icustays_summary")

# COMMAND ----------

# DBTITLE 1,Join icustays_table and pat_adm_table
joined_df = spark.sql("""
SELECT 
    icustays_table.subject_id AS subject_id,
    icustays_table.row_id AS row_id,
    icustays_table.hadm_id AS hadm_id,
    pat_adm_table.* EXCEPT (subject_id, row_id, hadm_id)
FROM icustays_table
JOIN pat_adm_table ON icustays_table.hadm_id = pat_adm_table.hadm_id
""")
joined_df.display()

# COMMAND ----------

db.write.mode("overwrite").saveAsTable("icu_pat_adm_table")

# COMMAND ----------

db.write.format("delta").mode("overwrite").saveAsTable("icustays_table")

# COMMAND ----------

# db.write.format("parquet").mode("overwrite").saveAsTable("icustays_parquet_table")
# db.write.mode("overwrite").parquet("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/ICUSTAYS.parquet")