import numpy as np
arr = np.array([10, 20, 30, 40])
np.array([1, 2, 3])          # Create array
np.zeros(5)                  # [0,0,0,0,0]
np.ones(5)                   # [1,1,1,1,1]
np.arange(1, 10, 2)          # Range
np.linspace(1, 10, 5)        # Equal intervals
np.eye(3)                    # Identity matrix
np.random.rand(3)            # Random floats
np.random.randint(1, 10, 5)  # Random integers
arr = np.array([[1,2],[3,4]])

arr.ndim     # Number of dimensions
arr.shape    # Rows, columns
arr.size     # Total elements
arr.dtype    # Data type
arr.reshape(4,1)
arr.flatten()
arr.ravel()
arr.T            # Transpose
np.sum(arr)
np.mean(arr)
np.median(arr)
np.std(arr)
np.var(arr)
np.min(arr)
np.max(arr)
np.sqrt(arr)
np.log(arr)
np.exp(arr)
np.sort(arr)
np.argsort(arr)
np.argmax(arr)
np.argmin(arr)
np.percentile(arr, 50)
np.corrcoef(arr)
np.unique(arr)

# print(arr) #
# print(arr.dtype) #Shows datatype

import pandas as pd
pd.Series([1,2,3,4])
data = {
    "id": [1, 2, 3, 4, 4],
    "name": ["Ram", "Sita", "Ravi", "Amit", "Amit"],
    "marks": [85, None, 78, 90, 90],
    "city": ["Delhi", "Mumbai", None, "Chennai", "Chennai"]
}
pd.read_csv("data.csv")
pd.read_excel("data.xlsx")
df = pd.DataFrame(data)
#print(df)
df.head()      # First 5 rows
df.tail()      # Last 5 rows
df.shape      # Rows, Columns
df.columns 
df.describe()
df.index    # Column names
df.info()      # Datatypes & null info
df.isnull()
df.notnull()
df.isnull().sum()
df.fillna(0)
df.fillna(method="ffill")
df.fillna(method="bfill")
df.dropna()
df.dropna(subset=["col"])

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
df["name"].str.upper()
df["name"].str.lower()
df["name"].str.strip()
df["name"].str.contains("a")
df["name"].str.replace("a", "A")
df.groupby("class").mean()
df.groupby("class").sum()
df.groupby("class").count()
df.groupby("class").agg(["min","max","mean"])
