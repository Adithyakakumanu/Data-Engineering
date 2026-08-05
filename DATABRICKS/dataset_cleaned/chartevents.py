# Databricks notebook source
df=spark.read.csv("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/CHARTEVENTS.csv",header="true",inferSchema="true")
df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC #Silver Layer

# COMMAND ----------

bronze_df=spark.read.table("bronze.chartevents")

# COMMAND ----------

bronze_df.display()

# COMMAND ----------

bronze_df.count()

# COMMAND ----------

bronze_df.describe().display()

# COMMAND ----------

# DBTITLE 1,Untitled
from pyspark.sql.functions import sum,col,when
from pyspark.sql import Row
null_col = bronze_df.select([
    sum(when(col(c).isNull(), 1).otherwise(0)).alias(c)
    for c in bronze_df.columns
]).collect()[0].asDict()
rows = [Row(column=k, null_count=v,null_count_pct=v/bronze_df.count()) for k, v in null_col.items() if v > 0]

spark.createDataFrame(rows).display()

# COMMAND ----------

# DBTITLE 1,Untitled
from pyspark.sql.functions import unix_timestamp
bronze_df=bronze_df.withColumn('duration',(unix_timestamp(bronze_df['storetime'])-unix_timestamp(bronze_df['charttime']))/3600)

# COMMAND ----------

# DBTITLE 1,Cell 9
bronze_df.select('icustay_id').distinct().display()
bronze_df.select("value").distinct().display()
bronze_df.select("valueuom").distinct().display()
bronze_df.select("warning").distinct().display()
bronze_df.select("error").distinct().display()
bronze_df.select("resultstatus").distinct().display()
bronze_df.select("stopped").distinct().display()
bronze_df.select("valuenum").distinct().display()

# COMMAND ----------

# DBTITLE 1,Untitled
from pyspark.sql.functions import lit
string_cols = [c for c, dtype in bronze_df.dtypes if dtype == 'string']
silver_df = bronze_df.fillna('NA', subset=string_cols)

# COMMAND ----------

silver_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("silver.chartevents_clean")

# COMMAND ----------

# MAGIC %md
# MAGIC #Gold Layer

# COMMAND ----------

silver_df=spark.read.table("silver.chartevents_clean")

# COMMAND ----------


silver_df=silver_df.drop("storetime","charttime")

# COMMAND ----------

col_null_threshold = 0.5
total_rows=silver_df.count()
cols_to_drop = [
    c for c, nulls in null_col.items()
    if nulls / total_rows > col_null_threshold

]
# df=df.drop(*cols_to_drop)
# df=df.dropna()
gold_df=silver_df.dropna()

# COMMAND ----------

gold_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.chartevents_summary")

# COMMAND ----------

# MAGIC %skip
# MAGIC spark.sql("DROP TABLE IF EXISTS chartevents_Table")

# COMMAND ----------

df.write.format("delta").mode("overwrite").saveAsTable("chartevents_Table")

# COMMAND ----------

