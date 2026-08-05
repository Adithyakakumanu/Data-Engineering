# Databricks notebook source
files=dbutils.fs.ls("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4")
display(files)

# COMMAND ----------

df=spark.read.csv("dbfs:/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/DIAGNOSES_ICD.csv",header="true",inferSchema="true")
df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC #Silver Layer

# COMMAND ----------

bronze_df = spark.table("bronze.diagnoses_icd")

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

# DBTITLE 1,Fix NameError: import Row
from pyspark.sql.functions import col, when, sum
from pyspark.sql import Row

total_rows = silver_df.count()
null_counts = silver_df.select([
    sum(when(col(c).isNull(), 1).otherwise(0)).alias(c)
    for c in silver_df.columns
]).collect()[0].asDict()

rows = [Row(column=k, null_count=v,null_percentage=round((v / total_rows), 2)) for k, v in null_counts.items()]

spark.createDataFrame(rows).display()


# COMMAND ----------

silver_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("silver.diagnoses_icd_clean")

# COMMAND ----------

# MAGIC %md
# MAGIC #Gold Layer

# COMMAND ----------

silver_df = spark.table("silver.diagnoses_icd_clean")

# COMMAND ----------

gold_df = silver_df.dropDuplicates()

# COMMAND ----------

gold_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.diagnoses_icd_summary")

# COMMAND ----------

# DBTITLE 1,Cell 7
# from pyspark.ml.feature import MinMaxScaler, StandardScaler, VectorAssembler
# from pyspark.ml.regression import LinearRegression
# from pyspark.sql.functions import col

# feature_col = "seq_num"  # numeric column present in schema
# label_col = "row_id"     # numeric column present in schema

# df_clean = df.filter(col(feature_col).isNotNull() & col(label_col).isNotNull())

# # Use VectorAssembler to create feature vector
# assembler = VectorAssembler(inputCols=[feature_col], outputCol="feature_vec")
# df_vector = assembler.transform(df_clean).select(col(label_col).cast("double").alias("label"), "feature_vec")

# # Normalization (MinMaxScaler)
# scaler = MinMaxScaler(inputCol="feature_vec", outputCol="feature_scaled")
# scaler_model = scaler.fit(df_vector)
# df_scaled = scaler_model.transform(df_vector)

# # Standardization (StandardScaler)
# std_scaler = StandardScaler(inputCol="feature_vec", outputCol="feature_standardized", withMean=True, withStd=True)
# std_scaler_model = std_scaler.fit(df_vector)
# df_standardized = std_scaler_model.transform(df_vector)

# # Linear Regression using normalized feature
# lr = LinearRegression(featuresCol="feature_scaled", labelCol="label")
# lr_model = lr.fit(df_scaled)
# lr_results = lr_model.transform(df_scaled)
# display(lr_results.select("feature_scaled", "label", "prediction"))

# # Linear Regression using standardized feature
# lr_std = LinearRegression(featuresCol="feature_standardized", labelCol="label")
# lr_std_model = lr_std.fit(df_standardized)
# lr_std_results = lr_std_model.transform(df_standardized)
# display(lr_std_results.select("feature_standardized", "label", "prediction"))

# COMMAND ----------

df.write.format("delta").mode("overwrite").saveAsTable("DIAGNOSES_ICD_table")