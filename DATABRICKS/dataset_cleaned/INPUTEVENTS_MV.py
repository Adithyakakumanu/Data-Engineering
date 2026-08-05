# Databricks notebook source
a=dbutils.fs.ls("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4")
display(a)

# COMMAND ----------

db=spark.read.csv("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/INPUTEVENTS_MV.csv",header=True,inferSchema=True)
display(db)
db.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC #Silver Layer

# COMMAND ----------

bronze_df = spark.table("bronze.inputevents_mv")

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

rows = [Row(column=k, null_count=v,null_percentage=(v / total_rows)) for k, v in null_counts.items() if v > 0]

spark.createDataFrame(rows).display()


# COMMAND ----------

silver_df.select("rate").distinct().display()
silver_df.select("rateuom").distinct().display()
silver_df.select("secondaryordercategoryname").distinct().display()
silver_df.select("totalamount").distinct().display()
silver_df.select("totalamountuom").distinct().display()
silver_df.select("comments_editedby").distinct().display()
silver_df.select("comments_canceledby").distinct().display()
silver_df.select("comments_date").distinct().display()

# COMMAND ----------

silver_df=silver_df.withColumn('duration',(unix_timestamp('endtime')-unix_timestamp('starttime'))/3600)


# COMMAND ----------

silver_df=silver_df.fillna("NA")

# COMMAND ----------

silver_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("silver.inputevents_mv_clean")

# COMMAND ----------

# MAGIC %md
# MAGIC #Gold Layer

# COMMAND ----------

silver_df = spark.table("silver.inputevents_mv_clean")

# COMMAND ----------

from pyspark.sql.functions import to_date

cols_to_exclude = ["starttime", "endtime","comments_editedby","comments_canceledby","totalamountuom"]
value_cols = [c for c in silver_df.columns if c not in cols_to_exclude]

gold_df = silver_df.select(value_cols)



gold_df = gold_df.dropna()

# COMMAND ----------

gold_df.display()

# COMMAND ----------

gold_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.inputevents_mv_summary")

# COMMAND ----------

silver_df.write.mode("overwrite").saveAsTable("inputevents_mv_table")