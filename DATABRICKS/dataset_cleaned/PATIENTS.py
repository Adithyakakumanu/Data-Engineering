# Databricks notebook source
a=dbutils.fs.ls("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4")
display(a)

# COMMAND ----------

db=spark.read.csv("/Volumes/workspace/default/task/mimic-iii-clinical-database-demo-1.4/PATIENTS.csv",header=True,inferSchema=True)
display(db)

# COMMAND ----------

# MAGIC %md
# MAGIC #Silver Layer

# COMMAND ----------

bronze_df = spark.table("bronze.patients")

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

silver_df=silver_df.withColumn("age",(unix_timestamp("dod")-unix_timestamp("dob"))/365)

# COMMAND ----------

silver_df.select("dod_hosp").distinct().display()
silver_df.select("dod_ssn").distinct().display()

# COMMAND ----------

silver_df=silver_df.fillna("NA")

# COMMAND ----------

silver_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("silver.patients_clean")

# COMMAND ----------

# MAGIC %md
# MAGIC #Gold Layer

# COMMAND ----------

silver_df = spark.table("silver.patients_clean")

# COMMAND ----------

from pyspark.sql.functions import to_date

cols_to_exclude = ["dod", "dob"]
value_cols = [c for c in silver_df.columns if c not in cols_to_exclude]

gold_df = silver_df.select(value_cols)

# COMMAND ----------

gold_df.write.format("delta") \
.mode("overwrite") \
.saveAsTable("gold.patients_summary")

# COMMAND ----------

# DBTITLE 1,Show schemas in workspace
# MAGIC %sql
# MAGIC SHOW SCHEMAS FROM workspace;

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from workspace.gold.admission_summary join workspace.gold.patients_summary on workspace.gold.admission_summary.subject_id = workspace.gold.patients_summary.subject_id;

# COMMAND ----------

# DBTITLE 1,Untitled
admission_df = spark.table("workspace.default.admission_table")
joined_df = db.join(admission_df, db.subject_id == admission_df.subject_id, "left") \
    .select(
        db["row_id"].alias("row_id"),
        db["subject_id"].alias("subject_id"),
        *[db[c] for c in db.columns if c not in ["row_id", "subject_id"]],
        *[admission_df[c] for c in admission_df.columns if c not in ["row_id", "subject_id"]]
    )
display(joined_df)

# COMMAND ----------

joined_df=joined_df.withColumn("age",datediff(col("admittime"),col("dob"))/365)
joined_df=joined_df.withColumn("length_of_stay",datediff(col("dischtime"),col("admittime")))

joined_df = joined_df.withColumn(
    "age",
    round(when(col("age") > 100, 100).otherwise(col("age")), 0)
)


# COMMAND ----------

joined_df.write.mode("overwrite").saveAsTable("pat_adm_table")

# COMMAND ----------

joined_df.display()

# COMMAND ----------

spark.sql("drop table if exists workspace.default.admission_details")

# COMMAND ----------

spark.sql("drop table if exists workspace.default.admission_details")

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE workspace.default.admission_details AS
# MAGIC select pa.subject_id,pa.gender,pa.hospital_expire_flag,pa.admission_type,pa.admission_location,pa.discharge_location,pa.diagnosis,pa.insurance,pa.marital_status,pa.age,pa.length_of_stay,pa.hadm_id,d.drg_type,d.drg_code,d.description,icu.dbsource,icu.icustay_id,icu.first_careunit,icu.last_careunit,icu.los as stay_in_icu_in_days
# MAGIC from workspace.default.pat_adm_table pa 
# MAGIC inner join workspace.gold.drgcodes_summary d 
# MAGIC on pa.subject_id = d.subject_id inner join workspace.gold.icustays_summary icu on pa.subject_id=icu.subject_id;

# COMMAND ----------

admission_details = spark.table("workspace.default.admission_details")
display(admission_details.limit(100))

# COMMAND ----------

# DBTITLE 1,Cell 28
admission_details = spark.table("workspace.default.admission_details")
admission_details.write.mode("overwrite").option("header", "true").csv("/Volumes/workspace/default/task/admission_details_csv")

# COMMAND ----------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score, roc_curve

import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-whitegrid')

# =========================
# DATA LOADING
# =========================
# print("\n========== DATA LOADING ==========\n")

df = spark.table("workspace.default.admission_details").toPandas()

print("Shape:", df.shape)
display(df.head())

# =========================
# TARGET ANALYSIS
# =========================
# print("\n========== TARGET ANALYSIS ==========\n")

# sns.countplot(data=df, x='hospital_expire_flag')
# plt.title("Hospital Mortality Distribution")
# plt.subplots_adjust(hspace=0.5, wspace=0.5)
# plt.show()

# =========================
# NUMERICAL FEATURES
# =========================
# print("\n========== NUMERICAL FEATURES ==========\n")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

sns.histplot(df['age'], kde=True, ax=axes[0])
axes[0].set_title("Age Distribution")

sns.histplot(df['length_of_stay'], kde=True, ax=axes[1])
axes[1].set_title("Length of Stay Distribution")
plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.show()

# =========================
# CATEGORICAL FEATURES
# =========================
print("\n========== CATEGORICAL FEATURES ==========\n")

sns.countplot(data=df, x='gender')
plt.title("Gender Distribution")
plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.show()

sns.countplot(data=df, x='admission_type')
plt.title("Admission Type Distribution")
plt.xticks(rotation=45)
plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.show()

# =========================
# PREPROCESSING
# =========================
# print("\n========== DATA PREPROCESSING ==========\n")

df = df.drop_duplicates(subset=['subject_id', 'hadm_id'])

df['marital_status'] = df['marital_status'].fillna('UNKNOWN')

for col in df.columns:
    if df[col].isnull().sum() > 0:
        if df[col].dtype in ['int64', 'float64']:
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(df[col].mode()[0])

# print("Missing values handled")

# =========================
# FEATURE ENGINEERING
# =========================
# print("\n========== FEATURE ENGINEERING ==========\n")

df['diagnosis_sepsis'] = df['diagnosis'].str.lower().str.contains('sepsis', na=False).astype(int)
df['diagnosis_pneumonia'] = df['diagnosis'].str.lower().str.contains('pneumonia', na=False).astype(int)
df['diagnosis_failure'] = df['diagnosis'].str.lower().str.contains('failure', na=False).astype(int)
df['diagnosis_cardiac'] = df['diagnosis'].str.lower().str.contains('cardiac|heart|mi|cad', na=False).astype(int)
df['diagnosis_respiratory'] = df['diagnosis'].str.lower().str.contains('respiratory|pulmonary', na=False).astype(int)

df['age_over_80'] = (df['age'] >= 80).astype(int)
df['age_over_65'] = (df['age'] >= 65).astype(int)
df['short_stay'] = (df['length_of_stay'] <= 3).astype(int)
df['long_stay'] = (df['length_of_stay'] >= 14).astype(int)

# print("Feature engineering completed")

# =========================
# ENCODING
# =========================
# print("\n========== ENCODING ==========\n")

categorical_cols = ['gender', 'admission_type', 'admission_location', 
                    'discharge_location', 'insurance', 'marital_status', 'drg_type']

for col in categorical_cols:
    le = LabelEncoder()
    df[col + '_enc'] = le.fit_transform(df[col].astype(str))

# =========================
# MODEL DATA
# =========================
# print("\n========== MODEL PREPARATION ==========\n")

feature_cols = ['age', 'length_of_stay'] + \
               [col + '_enc' for col in categorical_cols] + \
               ['diagnosis_sepsis', 'diagnosis_pneumonia', 'diagnosis_failure',
                'diagnosis_cardiac', 'diagnosis_respiratory',
                'age_over_80', 'age_over_65', 'short_stay', 'long_stay']

X = df[feature_cols]
y = df['hospital_expire_flag']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# =========================
# MODEL TRAINING
# =========================
# print("\n========== MODEL TRAINING ==========\n")

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'Random Forest': RandomForestClassifier(),
    'Gradient Boosting': GradientBoostingClassifier(),
    'Decision Tree': DecisionTreeClassifier(),
    'KNN': KNeighborsClassifier(),
    'SVM': SVC(probability=True)
}

results = []

for name, model in models.items():
    if name in ['Logistic Regression', 'KNN', 'SVM']:
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        y_prob = model.predict_proba(X_test_scaled)[:, 1]
        cv = cross_val_score(model, X_train_scaled, y_train, cv=5)
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        cv = cross_val_score(model, X_train, y_train, cv=5)

    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)

    results.append([name, acc, auc, cv.mean()])

    print(f"\n{name}")
    print("Accuracy:", acc)
    print("ROC-AUC:", auc)
print("\n========== ADDITIONAL EDA PLOTS ==========\n")

# =========================
# AGE vs MORTALITY
# =========================
plt.figure(figsize=(6,4))
sns.boxplot(data=df, x='hospital_expire_flag', y='age')
plt.title("Age vs Mortality")
plt.xticks([0,1], ['Survived','Expired'])
plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.show()

# =========================
# LENGTH OF STAY vs MORTALITY
# =========================
plt.figure(figsize=(6,4))
sns.boxplot(data=df, x='hospital_expire_flag', y='length_of_stay')
plt.title("Length of Stay vs Mortality")
plt.xticks([0,1], ['Survived','Expired'])
plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.show()

# =========================
# GENDER vs MORTALITY (STACKED)
# =========================
gender_ct = pd.crosstab(df['gender'], df['hospital_expire_flag'])

gender_ct.plot(kind='bar', stacked=True)
plt.title("Gender vs Mortality")
plt.xticks(rotation=0)
plt.legend(['Survived','Expired'])
plt.tight_layout()
plt.show()

# =========================
# MORTALITY RATE BY GENDER
# =========================
(df.groupby('gender')['hospital_expire_flag'].mean()).plot(kind='bar')
plt.title("Mortality Rate by Gender")
plt.ylabel("Rate")
plt.xticks(rotation=0)
plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.show()

# =========================
# ADMISSION TYPE vs MORTALITY RATE
# =========================
(df.groupby('admission_type')['hospital_expire_flag'].mean().sort_values()) \
    .plot(kind='barh')

plt.title("Mortality Rate by Admission Type")
plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.show()

# =========================
# INSURANCE vs MORTALITY
# =========================
(df.groupby('insurance')['hospital_expire_flag'].mean().sort_values()) \
    .plot(kind='barh')

plt.title("Mortality Rate by Insurance")
plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.show()

# =========================
# AGE GROUP ANALYSIS
# =========================
df['age_group'] = pd.cut(df['age'], 
                        bins=[0,30,50,65,80,100,150],
                        labels=['<30','30-50','50-65','65-80','80-100','100+'])

(df.groupby('age_group')['hospital_expire_flag'].mean()).plot(kind='bar')
plt.title("Mortality Rate by Age Group")
plt.xticks(rotation=45)
plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.show()

# =========================
# TOP DIAGNOSIS MORTALITY
# =========================
top_diag = df['diagnosis'].value_counts().head(10).index

(df[df['diagnosis'].isin(top_diag)]
 .groupby('diagnosis')['hospital_expire_flag']
 .mean()
 .sort_values()) \
.plot(kind='barh')

plt.title("Top Diagnosis Mortality Rate")
plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.show()

# =========================
# CORRELATION HEATMAP
# =========================
df_corr = df.copy()

for col in ['gender','admission_type','insurance','marital_status','drg_type']:
    df_corr[col] = df_corr[col].astype('category').cat.codes

corr = df_corr[['age','length_of_stay','hospital_expire_flag',
                'gender','admission_type','insurance','marital_status','drg_type']].corr()

plt.figure(figsize=(10,8))
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Correlation Matrix")
plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.show()

# =========================
# LENGTH OF STAY DISTRIBUTION + LOG
# =========================
plt.figure(figsize=(10,4))

plt.subplot(1,2,1)
sns.histplot(df['length_of_stay'], bins=50)
plt.title("LOS Distribution")

plt.subplot(1,2,2)
sns.histplot(np.log1p(df['length_of_stay']), bins=50)
plt.title("Log LOS Distribution")
plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.show()

# =========================
# LOS CATEGORY vs MORTALITY
# =========================
df['los_category'] = pd.cut(df['length_of_stay'],
                           bins=[0,3,7,14,30,1000],
                           labels=['1-3','4-7','1-2w','2-4w','>4w'])

(df.groupby('los_category')['hospital_expire_flag'].mean()).plot(kind='bar')
plt.title("LOS Category vs Mortality")
plt.xticks(rotation=45)
plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.show()

plt.figure(figsize=(6,4))
sns.histplot(df['stay_in_icu_in_days'], bins=30, kde=True, color='purple')
plt.title("ICU Length of Stay Distribution")
plt.xlabel("Days in ICU")
plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.show()

plt.figure(figsize=(6,4))
df['first_careunit'].value_counts().plot(kind='bar', color='skyblue')
plt.title("ICU Type Distribution")
plt.xlabel("ICU Type")
plt.ylabel("Count")
plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.show()

# =========================
# MODEL COMPARISON
# =========================
# print("\n========== MODEL COMPARISON ==========\n")

# results_df = pd.DataFrame(results, columns=['Model', 'Accuracy', 'ROC-AUC', 'CV'])
# results_df = results_df.sort_values('ROC-AUC', ascending=False)
# display(results_df)

# sns.barplot(data=results_df, x='ROC-AUC', y='Model')
# plt.title("Model Comparison (ROC-AUC)")
# plt.subplots_adjust(hspace=0.5, wspace=0.5)
# plt.show()

# # =========================
# # BEST MODEL
# # =========================
# # print("\n========== BEST MODEL ==========\n")

# best_model_name = results_df.iloc[0]['Model']
# best_model = models[best_model_name]

# if best_model_name in ['Logistic Regression', 'KNN', 'SVM']:
#     y_pred = best_model.predict(X_test_scaled)
#     y_prob = best_model.predict_proba(X_test_scaled)[:, 1]
# else:
#     y_pred = best_model.predict(X_test)
#     y_prob = best_model.predict_proba(X_test)[:, 1]

# # Confusion Matrix
# sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d')
# plt.title(f"Confusion Matrix - {best_model_name}")
# plt.subplots_adjust(hspace=0.5, wspace=0.5)
# plt.show()

# # ROC Curve
# fpr, tpr, _ = roc_curve(y_test, y_prob)
# plt.plot(fpr, tpr, label=best_model_name)
# plt.plot([0,1],[0,1],'--')
# plt.title("ROC Curve")
# plt.legend()
# plt.show()
# plt.subplots_adjust(hspace=0.5, wspace=0.5)

# =========================
# FEATURE IMPORTANCE
# =========================
# # print("\n========== FEATURE IMPORTANCE ==========\n")

# rf = models['Random Forest']
# importance = pd.DataFrame({
#     'Feature': feature_cols,
#     'Importance': rf.feature_importances_
# }).sort_values('Importance', ascending=False)

# display(importance.head(10))

# sns.barplot(data=importance.head(10), x='Importance', y='Feature')
# plt.title("Top Feature Importance")
# plt.subplots_adjust(hspace=0.5, wspace=0.5)
# plt.show()

# COMMAND ----------

db.write.mode("overwrite").saveAsTable("patients_table")