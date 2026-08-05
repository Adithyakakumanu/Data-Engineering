# Databricks notebook source
files = dbutils.fs.ls("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4")
display(files)

# COMMAND ----------

df=spark.read.csv(path="dbfs:/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/CPTEVENTS.csv",header="true",inferSchema="true")
df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC #Silver Layer

# COMMAND ----------

bronze_df=spark.read.table("bronze.cptevents")

# COMMAND ----------

bronze_df.display()

# COMMAND ----------

bronze_df.count()

# COMMAND ----------

bronze_describe().display()

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

bronze_df.select("ticket_id_seq").distinct().display()
bronze_df.select("description").distinct().display()
bronze_df.select("chartdate").distinct().display()
bronze_df.select("cpt_suffix").distinct().display()

# COMMAND ----------

bronze_df.select('sectionheader').distinct().display()
bronze_df.select('subsectionheader').distinct().display()
bronze_df.select('costcenter').distinct().display()

# COMMAND ----------

# DBTITLE 1,Untitled
from pyspark.sql.types import StringType
string_cols = [c for c in bronze_df.columns if isinstance(bronze_df.schema[c].dataType, StringType)]
silver_df = bronze_df.fillna("NA", subset=string_cols)

# COMMAND ----------

# df.display()
silver_df.limit(10).display()

# COMMAND ----------

# DBTITLE 1,Cell 13
# MAGIC %skip
# MAGIC from pyspark.ml.feature import OneHotEncoder, StringIndexer, MinMaxScaler, StandardScaler
# MAGIC from pyspark.sql.types import StringType, IntegerType, DoubleType
# MAGIC from pyspark.ml.linalg import Vectors, VectorUDT
# MAGIC from pyspark.sql.functions import udf
# MAGIC # Identify string columns to encode
# MAGIC string_cols = [c for c in df.columns if isinstance(df.schema[c].dataType, StringType)]
# MAGIC # Index string columns, skip if output column already exists
# MAGIC indexers = [StringIndexer(inputCol=c, outputCol=f"{c}_idx") for c in string_cols if f"{c}_idx" not in df.columns]
# MAGIC for indexer in indexers:
# MAGIC     df = indexer.fit(df).transform(df)
# MAGIC # Only use indexed columns with at least two distinct values for OneHotEncoder
# MAGIC indexed_cols = [f"{c}_idx" for c in string_cols if f"{c}_idx" in df.columns]
# MAGIC valid_ohe_cols = [col for col in indexed_cols if df.select(col).distinct().count() > 1]
# MAGIC if valid_ohe_cols:
# MAGIC     encoder = OneHotEncoder(inputCols=valid_ohe_cols,
# MAGIC                             outputCols=[f"{col[:-4]}_ohe" for col in valid_ohe_cols])
# MAGIC     df = encoder.fit(df).transform(df)
# MAGIC # Drop original string columns and index columns, keep one-hot encoded columns
# MAGIC if string_cols:
# MAGIC     drop_cols = string_cols + indexed_cols
# MAGIC     df = df.drop(*drop_cols)
# MAGIC # Scale numeric columns individually (no VectorAssembler)
# MAGIC numeric_cols = [c for c in df.columns if isinstance(df.schema[c].dataType, (IntegerType, DoubleType))]

# COMMAND ----------

# DBTITLE 1,Cell 14
# MAGIC %skip
# MAGIC for c in numeric_cols:
# MAGIC     # MinMaxScaler expects a vector, so create a single-element vector for each column
# MAGIC     to_vector_udf = udf(lambda x: Vectors.dense([float(x)]) if x is not None else Vectors.dense([0.0]), VectorUDT())
# MAGIC     df = df.withColumn(f"{c}_vec", to_vector_udf(df[c]))
# MAGIC     if f"{c}_minmax" not in df.columns:
# MAGIC         minmax = MinMaxScaler(inputCol=f"{c}_vec", outputCol=f"{c}_minmax")
# MAGIC         df = minmax.fit(df).transform(df)
# MAGIC     if f"{c}_standard" not in df.columns:
# MAGIC         scaler = StandardScaler(inputCol=f"{c}_vec", outputCol=f"{c}_standard", withMean=True, withStd=True)
# MAGIC         df = scaler.fit(df).transform(df)
# MAGIC     df = df.drop(f"{c}_vec")
# MAGIC # display(df)

# COMMAND ----------

df.display()

# COMMAND ----------

# DBTITLE 1,Cell 16
# MAGIC %skip
# MAGIC from pyspark.ml.classification import LogisticRegression
# MAGIC from pyspark.ml.evaluation import MulticlassClassificationEvaluator
# MAGIC from pyspark.ml import Pipeline
# MAGIC label_col = 'hadm_id'
# MAGIC final_df = df.select("features_standard", label_col).dropna().withColumnRenamed(label_col, "label")
# MAGIC final_df = final_df.filter((final_df.label >= 0) & (final_df.label < 100))
# MAGIC if final_df.count() == 0:
# MAGIC     print("ERROR: The dataset is empty after filtering. Cannot train model.\nRoot cause: No rows remain after filtering for label values in [0, 100).\nTo fix: Choose a different label column or adjust your filtering criteria so the dataset is not empty.")
# MAGIC else:
# MAGIC     train_df, test_df = final_df.randomSplit([0.8, 0.2], seed=42)
# MAGIC     lr = LogisticRegression(featuresCol="features_standard", labelCol="label")
# MAGIC     model = lr.fit(train_df)
# MAGIC     predictions = model.transform(test_df)
# MAGIC     evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
# MAGIC     accuracy = evaluator.evaluate(predictions)
# MAGIC     display(predictions.select("label", "prediction", "probability"))
# MAGIC     print(f"Test Accuracy: {accuracy}")
# MAGIC     new_data = df.limit(5).select("features_standard")
# MAGIC     new_predictions = model.transform(new_data)
# MAGIC     display(new_predictions.select("prediction", "probability"))

# COMMAND ----------

silver_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.cptevents_clean")

# COMMAND ----------

# MAGIC %md
# MAGIC #Gold Layer

# COMMAND ----------

silver_df=spark.read.table("gold.cptevents_clean")

# COMMAND ----------

from pyspark.sql.functions import to_date

cols_to_exclude = ['cpt_suffix','chartdate','cpt_cd']
value_cols = [c for c in silver_df.columns if c not in cols_to_exclude]

gold_df = silver_df.select(value_cols)

# timestamp_cols = [c for c, t in gold_df.dtypes if t in ("timestamp", "date")]
# for c in timestamp_cols:
#     gold_df = gold_df.withColumn(c, to_date(gold_df[c]))

gold_df = gold_df.dropna()

# COMMAND ----------

gold_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.cptevents_summary")

# COMMAND ----------

df.write.format("delta").mode("overwrite").saveAsTable("CPTEVENTS_Table")