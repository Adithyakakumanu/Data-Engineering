# Databricks notebook source
a=dbutils.fs.ls("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4")
display(a)

# COMMAND ----------

db=spark.read.csv("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/NOTEEVENTS.csv",header=True,inferSchema=True)
display(db)

# COMMAND ----------

# MAGIC %md
# MAGIC #Silver Layer

# COMMAND ----------

silver_df = spark.table("bronze.noteevents")

# COMMAND ----------

silver_df.display()

# COMMAND ----------

silver_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("silver.noteevents_clean")

# COMMAND ----------

# MAGIC %md
# MAGIC #Gold Layer

# COMMAND ----------

gold_df = spark.table("silver.admissions_clean")

# COMMAND ----------

gold_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.noteevents_summary")