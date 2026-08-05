# Databricks notebook source
a=dbutils.fs.ls("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4")
display(a)

# COMMAND ----------

db=spark.read.csv("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/PRESCRIPTIONS.csv",header=True,inferSchema=True)
display(db)

# COMMAND ----------

# MAGIC %md
# MAGIC #Silver Layer

# COMMAND ----------

bronze_df = spark.table("bronze.prescriptions")

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

silver_df = silver_df.withColumn("duration", (unix_timestamp("enddate") - unix_timestamp("startdate")) / 3600)

# COMMAND ----------

silver_df.select("icustay_id").distinct().display()
silver_df.select("enddate").distinct().display()
silver_df.select("drug_name_poe").distinct().display()
silver_df.select("formulary_drug_cd").distinct().display()
silver_df.select("drug_name_generic").distinct().display()
silver_df.select("gsn").distinct().display()
silver_df.select("ndc").distinct().display()
silver_df.select("form_unit_disp").distinct().display()

# COMMAND ----------

silver_df=silver_df.fillna("NA")

# COMMAND ----------

silver_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("silver.prescriptions_clean")

# COMMAND ----------

# MAGIC %md
# MAGIC #Gold Layer

# COMMAND ----------

silver_df = spark.table("silver.prescriptions_clean")

# COMMAND ----------

from pyspark.sql.functions import to_date

cols_to_exclude = ["enddate", "startdate"]
value_cols = [c for c in silver_df.columns if c not in cols_to_exclude]

gold_df = silver_df.select(value_cols)
gold_df = gold_df.dropna()

# COMMAND ----------

gold_df.display()

# COMMAND ----------

gold_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.prescriptions_summary")

# COMMAND ----------

db.write.mode("overwrite").saveAsTable("predcriptions_table")