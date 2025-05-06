import pandas as pd

# Step 1: Read the CSV file
data = pd.read_csv('ty.csv')
df = pd.DataFrame(data)

# Step 2: Print original DataFrame
print("Original DataFrame with missing values and duplicates:\n", df)

# Step 3: Print column names to help identify correct names
print("\nColumn names in your CSV file:\n", df.columns.tolist())

# Step 4: Detect missing values
print("\nMissing value check (True = missing):\n", df.isnull())

# Step 5: Fill missing values (update column names based on actual ones)
df_filled = df.copy()

# Use actual column names shown in the print above
# Example: Replace 'statname' and 'Sum of area_sqkm' with your actual column names
if 'statname' in df.columns:
    df_filled['statname'] = df_filled['statname'].fillna('Unknown')

if 'Sum of area_sqkm' in df.columns:
    df_filled['Sum of area_sqkm'] = df_filled['Sum of area_sqkm'].fillna(0)

print("\nDataFrame after filling missing values:\n", df_filled)

# Step 6: Drop rows with any missing value
df_dropped = df.dropna()
print("\nDataFrame after dropping rows with any missing value:\n", df_dropped)

# Step 7: Remove duplicate rows
df_no_duplicates = df_filled.drop_duplicates()
print("\nDataFrame after removing duplicate rows:\n", df_no_duplicates)
