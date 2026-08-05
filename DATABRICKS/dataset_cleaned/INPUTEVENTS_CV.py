# Databricks notebook source
db=spark.read.csv("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/INPUTEVENTS_CV.csv",header=True,inferSchema=True)
db.display()

# COMMAND ----------

# MAGIC %md
# MAGIC #Silver Layer

# COMMAND ----------

bronze_df = spark.table("bronze.inputevents_cv")

# COMMAND ----------

silver_df = bronze_df.dropDuplicates()

# COMMAND ----------

silver_df.display()

# COMMAND ----------

silver_df.describe().display()

# COMMAND ----------

silver_df.count()

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from workspace.gold.procedureevents_mv_summary  as cv join workspace.gold.outputevents_summary as mv on cv.hadm_id= mv.hadm_id;

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

rows = [Row(column=k, null_count=v,null_percentage=(v / total_rows)) for k, v in null_counts.items() if v > 0]

spark.createDataFrame(rows).display()


# COMMAND ----------

silver_df=silver_df.withColumn("duration",(unix_timestamp("storetime")-unix_timestamp("charttime"))/60)

# COMMAND ----------

silver_df.select("amount").distinct().display()
silver_df.select("amountuom").distinct().display()
silver_df.select("rate").distinct().display()
silver_df.select("rateuom").distinct().display()
silver_df.select("cgid").distinct().display()
silver_df.select("stopped").distinct().display()
silver_df.select("newbottle").distinct().display()
silver_df.select("originalamount").distinct().display()
silver_df.select("originalamountuom").distinct().display()
silver_df.select("originalroute").distinct().display()
silver_df.select("originalrate").distinct().display()
silver_df.select("originalrateuom").distinct().display()
silver_df.select("originalsite").distinct().display()

# COMMAND ----------

silver_df=silver_df.fillna("NA")

# COMMAND ----------

spark.sql("drop table if exists silver.inputevents_cv_clean")

# COMMAND ----------

silver_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("silver.inputevents_cv_clean")

# COMMAND ----------

# MAGIC %md
# MAGIC #Gold Layer

# COMMAND ----------

silver_df = spark.table("silver.inputevents_cv_clean")

# COMMAND ----------

gold_df = silver_df.drop('originalsite','newbottle','originalrateuom','storetime','charttime')

# COMMAND ----------

gold_df.display()

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from workspace.gold.inputevents_cv_summary where rate is not null;

# COMMAND ----------

# DBTITLE 1,Cell 18
gold_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.inputevents_cv_summary")

# COMMAND ----------

db.write.mode("overwrite").saveAsTable("inputevents_cv_table")