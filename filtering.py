import pandas as pd

# Load the CSV file
file_path = "filtered_file.csv"  # Change this to your actual file path
df = pd.read_csv(file_path, dtype=str)

# Keep only relevant columns
df = df[["State Name", "County Name", "NAICS Description", "Establishments"]]

# Define required NAICS descriptions and their new names
required_naics = {
    "Real Estate": "Real Estate",
    "Religious, Grantmaking, Civic, Professional, and Similar Organizations": "Religious"
}

# Filter rows for only required NAICS descriptions
df_filtered = df[df["NAICS Description"].isin(required_naics.keys())].copy()

# Rename NAICS descriptions
df_filtered["NAICS Description"] = df_filtered["NAICS Description"].map(required_naics)

# Pivot to check which counties have both categories
county_pivot = df_filtered.pivot_table(index=["State Name", "County Name"], 
                                       columns="NAICS Description", 
                                       values="Establishments", 
                                       aggfunc="first")  # Uses 'first' to avoid duplicate values

# Drop counties missing either Amusement or Religious
county_pivot = county_pivot.dropna(subset=["Real Estate", "Religious"])

# Convert back to long format
df_filtered = county_pivot.reset_index().melt(id_vars=["State Name", "County Name"], 
                                              var_name="NAICS Description", 
                                              value_name="Establishments")

# Sort to ensure counties appear together
df_filtered = df_filtered.sort_values(by=["State Name", "County Name", "NAICS Description"])

# Save the cleaned file
df_filtered.to_csv("rr.csv", index=False)

print("Filtered CSV saved as 'ar.csv'")
