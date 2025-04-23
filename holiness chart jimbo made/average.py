import pandas as pd

# Load the CSV file
file_path = "filtered_file.csv"  # Replace with your actual file path
df = pd.read_csv(file_path)

# Ensure the column name is correct (check your CSV for exact column names)
establishment_col = "Establishments"  # Update if needed

# Convert the "Establishments" column to numeric, forcing errors to NaN
df[establishment_col] = pd.to_numeric(df[establishment_col], errors="coerce")

# Filter rows with the specific NAICS Description
filtered_df = df[df["NAICS Description"] == "Total"]

# Group by county and sum establishments
county_establishments = filtered_df.groupby("County Name")[establishment_col].sum()

# Compute the average across counties
average_establishments = county_establishments.mean()

print(f"Average establishments per county: {average_establishments:.2f}")
