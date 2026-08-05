# Databricks notebook source
a=dbutils.fs.ls("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4")
display(a)

# COMMAND ----------

df=spark.read.csv("dbfs:/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/MICROBIOLOGYEVENTS.csv",header=True,inferSchema=True)
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC #Silver Layer

# COMMAND ----------

bronze_df = spark.table("bronze.microbiologyevents")

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

# DBTITLE 1,Cell 7
silver_df = silver_df.withColumn("duration", round((unix_timestamp("charttime") - unix_timestamp("chartdate")) / 3600, 2))

# COMMAND ----------

silver_df.select('org_itemid').distinct().display()
silver_df.select('ab_itemid').distinct().display()
silver_df.select('ab_name').distinct().display()
silver_df.select('org_name').distinct().display()
silver_df.select('isolate_num').distinct().display()
silver_df.select('duration').distinct().display()
silver_df.select('dilution_value').distinct().display()
silver_df.select('dilution_comparison').distinct().display()
silver_df.select('interpretation').distinct().display()

# COMMAND ----------

silver_df=silver_df.fillna("NA")

# COMMAND ----------

silver_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("silver.microbiologyevents_clean")

# COMMAND ----------

# MAGIC %md
# MAGIC #Gold Layer

# COMMAND ----------

silver_df = spark.table("silver.microbiologyevents_clean")

# COMMAND ----------

from pyspark.sql.functions import to_date

cols_to_exclude = ['dilution_text', 'dilution_comparison','chartdate','charttime']
value_cols = [c for c in silver_df.columns if c not in cols_to_exclude]

gold_df = silver_df.select(value_cols)

# COMMAND ----------

gold_df.display()

# COMMAND ----------

# DBTITLE 1,Cell 18
gold_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.microbiologyevents_summary")

# COMMAND ----------

df.write.mode("overwrite").saveAsTable("microbiologyevents_table")