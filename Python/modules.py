import numpy as np
arr = np.array([10, 20, 30, 40])
# print(arr) #
# print(arr.dtype) #Shows datatype

import pandas as pd
data = {
    "id": [1, 2, 3, 4, 4],
    "name": ["Ram", "Sita", "Ravi", "Amit", "Amit"],
    "marks": [85, None, 78, 90, 90],
    "city": ["Delhi", "Mumbai", None, "Chennai", "Chennai"]
}

df = pd.DataFrame(data)
#print(df)
df.head()      # First 5 rows
df.tail()      # Last 5 rows
df.shape      # Rows, Columns
df.columns     # Column names
df.info()      # Datatypes & null info
df.isnull()
df.isnull().sum()
df_no_duplicates = df.drop_duplicates()
df_unique_id = df.drop_duplicates(subset="id") #remove based on the column
#print(df_no_duplicates)
df["marks"] = df["marks"].fillna(0)
df["marks"] = df["marks"].fillna(df["marks"].mean())
df["city"] = df["city"].fillna(df["city"].mode()[0])
df_drop = df.dropna()
df.dtypes
df["marks"] = df["marks"].astype(int) #convert to another datatype
df["date"] = pd.to_datetime("2024-01-01") #convert to datetime
df.sort_values(by="total_marks", ascending=False)
df["city"].value_counts()
