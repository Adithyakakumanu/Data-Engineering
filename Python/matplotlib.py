import matplotlib.pyplot as plt
import pandas as pd

# Step 1: Create the DataFrame
data = {
    "names": ["Ram", "Sita", "Ravi", "Amit", "Amit"],
    "marks": [85, None, 78, 90, 90]
}

df = pd.DataFrame(data)

# Step 2: Clean the data
df.drop_duplicates(inplace=True)  # Remove duplicate rows
df["marks"].fillna(df["marks"].mean(), inplace=True)  # Fill missing marks with mean

# Step 3: Extract variables for plotting
x = df["names"]        # x-axis: names
y = df["marks"]        # y-axis: marks
values = df["marks"]   # values for bar, pie, histogram
labels = df["names"]   # labels for pie chart

# Step 4: Line plot
plt.plot(x, y)
plt.title("Simple Line Plot")
plt.xlabel("Names")
plt.ylabel("Marks")
plt.show()

# Step 5: Line plot with style
plt.plot(x, y, color="red", linestyle="--", marker="o")
plt.title("Styled Line Plot")
plt.xlabel("Names")
plt.ylabel("Marks")
plt.show()

# Step 6: Bar plot
plt.bar(x, values, color="skyblue")
plt.title("Bar Plot of Marks")
plt.xlabel("Names")
plt.ylabel("Marks")
plt.show()

# Step 7: Histogram
plt.hist(values, bins=5, color="green", edgecolor="black")
plt.title("Histogram of Marks")
plt.xlabel("Marks")
plt.ylabel("Frequency")
plt.show()

# Step 8: Scatter plot
plt.scatter(x, y, color="purple")
plt.title("Scatter Plot of Marks")
plt.xlabel("Names")
plt.ylabel("Marks")
plt.show()

# Step 9: Pie chart
plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
plt.title("Pie Chart of Marks")
plt.show()

# Step 10: Subplots
plt.figure(figsize=(10,5))  # Figure size

plt.subplot(1,2,1)
plt.plot(x, y, color="blue", marker="o")
plt.title("Line Plot in Subplot")

plt.subplot(1,2,2)
plt.bar(x, values, color="orange")
plt.title("Bar Plot in Subplot")

plt.tight_layout()  # Adjust spacing
plt.show()
