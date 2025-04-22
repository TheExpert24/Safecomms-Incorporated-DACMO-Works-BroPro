import pandas as pd

# Load the CSV file
file_path = "real_and_rel.csv"  # Replace with your actual file path
df = pd.read_csv(file_path)

# Ensure the column names are correct
columns_to_keep = ["State Name", "County Name", "NAICS Description", "Establishments"]

# Filter rows for only "Total" and "Religious, Grantmaking, Civic, Professional, and Similar Organizations"
filtered_df = df[df["NAICS Description"].isin(["Religious, Grantmaking, Civic, Professional, and Similar Organizations", "Amusement, Gambling, and Recreation Industries"])]

# Keep only the specified columns
filtered_df = filtered_df[columns_to_keep]

# Save the cleaned dataset (optional)
filtered_df.to_csv("rel_and_rel.csv", index=False)

print("Filtered dataset saved as 'cleaned_output.csv'.")
