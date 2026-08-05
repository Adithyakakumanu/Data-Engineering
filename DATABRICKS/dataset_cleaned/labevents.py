# Databricks notebook source
a=dbutils.fs.ls("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4")
display(a)

# COMMAND ----------

db=spark.read.csv("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/LABEVENTS.csv",header=True,inferSchema=True)
# db.write.format('parquet').save("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/LABEVENTS1.parquet")

# COMMAND ----------

# MAGIC %md
# MAGIC #Silver Layer

# COMMAND ----------

bronze_df = spark.table("bronze.labevents")

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

silver_df.select("hadm_id").distinct().display()
silver_df.select("value").distinct().display()
silver_df.select("valueuom").distinct().display()
silver_df.select("flag").distinct().display()
silver_df.select("valuenum").distinct().display()

# COMMAND ----------

silver_df=silver_df.fillna("NA")

# COMMAND ----------

silver_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("silver.labevents_clean")

# COMMAND ----------

# MAGIC %md
# MAGIC #Gold Layer

# COMMAND ----------

silver_df = spark.table("silver.labevents_clean")

# COMMAND ----------

from pyspark.sql.functions import to_date

cols_to_exclude = ["value"]
value_cols = [c for c in silver_df.columns if c not in cols_to_exclude]

gold_df = silver_df.filter(col("flag")!="NA")

# gold_df = gold_df.dropna()

# COMMAND ----------

gold_df.display()

# COMMAND ----------

# DBTITLE 1,Cell 18
gold_df.select(*dict.fromkeys(gold_df.columns)).write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.labevents_summary")

# COMMAND ----------

silver_df.write.mode("overwrite").saveAsTable("labevents_table")