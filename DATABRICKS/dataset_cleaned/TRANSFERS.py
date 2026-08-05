# Databricks notebook source
a=dbutils.fs.ls("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4")
display(a)

# COMMAND ----------

db=spark.read.csv("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/TRANSFERS.csv",header=True,inferSchema=True)
display(db)

# COMMAND ----------

# MAGIC %md
# MAGIC #Silver Layer

# COMMAND ----------

bronze_df = spark.table("bronze.transfers")

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

silver_df.select("icustay_id").distinct().display()
silver_df.select("curr_careunit").distinct().display()
silver_df.select("prev_careunit").distinct().display()
silver_df.select("curr_wardid").distinct().display()
silver_df.select("prev_wardid").distinct().display()
silver_df.select("outtime").distinct().display()
silver_df.select("los").distinct().display()


# COMMAND ----------

silver_df=silver_df.fillna("NA")

# COMMAND ----------

silver_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("silver.transfers_clean")

# COMMAND ----------

# MAGIC %md
# MAGIC #Gold Layer

# COMMAND ----------

silver_df = spark.table("silver.transfers_clean")

# COMMAND ----------

from pyspark.sql.functions import to_date

cols_to_exclude = ["intime", "outtime"]
value_cols = [c for c in silver_df.columns if c not in cols_to_exclude]

gold_df = silver_df.select(value_cols)

# timestamp_cols = [c for c, t in gold_df.dtypes if t in ("timestamp", "date")]
# for c in timestamp_cols:
#     gold_df = gold_df.withColumn(c, to_date(gold_df[c]))


# COMMAND ----------

gold_df.display()

# COMMAND ----------

gold_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.transfers_summary")

# COMMAND ----------

# DBTITLE 1,Join tables with unambiguous column selection
# Load tables
icustays = spark.read.table("workspace.default.icustays_table")
services = spark.read.table("workspace.default.services_table")
transfers = db
callout = spark.read.table("workspace.default.callout_table")

tables = [
    ("icustays", icustays),
    ("services", services),
    ("transfers", transfers),
    ("callout", callout)
]

def smart_join(tables, join_key="subject_id", join_type="inner"):
    
    base_name, base_df = tables[0]
    joined_df = base_df
    
    for name, df in tables[1:]:
        
        # Find duplicate columns
        common_cols = set(joined_df.columns).intersection(set(df.columns))
        
        # Remove join key from renaming
        if join_key in common_cols:
            common_cols.remove(join_key)
        
        # Rename duplicate columns from right table
        for col_name in common_cols:
            df = df.withColumnRenamed(col_name, f"{name}_{col_name}")
        
        # Perform join safely
        joined_df = joined_df.join(df, [join_key], join_type)
    
    return joined_df


# Execute
final_df = smart_join(tables)

display(final_df)

# COMMAND ----------

final_df.columns

# COMMAND ----------

final_df.write.mode('overwrite').saveAsTable('icu_stc_table')

# COMMAND ----------


    db.write.mode('overwrite').saveAsTable('transfers_table')