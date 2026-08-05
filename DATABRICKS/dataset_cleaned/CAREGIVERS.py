# Databricks notebook source
a=dbutils.fs.ls('/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4')
display(a)

# COMMAND ----------

df=spark.read.csv('/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/CAREGIVERS.csv',header="true",inferSchema="true")
df.printSchema()

# COMMAND ----------

df.display()

# COMMAND ----------

bronze_df=spark.table("bronze.caregivers")

# COMMAND ----------

bronze_df.count()

# COMMAND ----------

bronze_df.describe().display()

# COMMAND ----------

bronze_df.distinct().count()

# COMMAND ----------

# DBTITLE 1,Untitled
from pyspark.sql.functions import sum,when,col
null_col=bronze_df.select([
    sum(when(col(c).isNull(),1).otherwise(0)).alias(c) for c in bronze_df.columns])
#null_col.display()
row_count = bronze_df.count()
null_counts = null_col.collect()[0].asDict()
null_percent_df = spark.createDataFrame(
    [(col_name, count, (count / row_count) * 100) for col_name, count in null_counts.items() if count > 0],
    ["column", "null_count", "null_percentage"]
)
display(null_percent_df)

# COMMAND ----------

bronze_df.select("description").distinct().display()
bronze_df.select("label").distinct().display()

# COMMAND ----------

from pyspark.sql.functions import col, when

str_cols = [c for c, t in bronze_df.dtypes if t == "string"]
silver_df = bronze_df.select([
    when(col(c).isNull(), "NA").otherwise(col(c)).alias(c) if c in str_cols else col(c) 
    for c in bronze_df.columns
])

# COMMAND ----------

silver_df.display()

# COMMAND ----------

silver_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("silver.caregivers_clean")

# COMMAND ----------

# MAGIC %md
# MAGIC #Gold Layer

# COMMAND ----------

silver_df=spark.table("silver.caregivers_clean")

# COMMAND ----------

# DBTITLE 1,Cell 15
from pyspark.sql.functions import count, avg, first

gold_df = silver_df.groupBy("label").agg(
    count("cgid").alias("count_cgid"),
    first("description").alias("description")
)

# COMMAND ----------

gold_df.display()

# COMMAND ----------

gold_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.caregivers_summary")

# COMMAND ----------

# DBTITLE 1,Untitled
df.write.format("delta").mode("overwrite").saveAsTable("CARGIVERS_Table")