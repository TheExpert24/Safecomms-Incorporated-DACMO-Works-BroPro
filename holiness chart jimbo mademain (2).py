import pandas as pd

# Load the CSV data into a DataFrame
df = pd.read_csv('thissux.csv')
df1 = pd.read_csv('cleaned_output.csv')
df2 = pd.read_csv('an_and_rel.csv')

# Function to retrieve the values for Amusement, Religious, and Real Estate for a given state and county
def get_values_for_county_state(state, county):
    result = []
    if df['County Name'].str.contains(county).any() and df:
        # Filter the DataFrame based on state and county
        filtered_df = df[(df['State Name'] == state) & (df['County Name'] == county)]

        # Check if we have the three required NAICS descriptions (Real Estate, Amusement, Religious)
        required_values = ['Real Estate', 'Amusement', 'Religious']
        

        for value in required_values:
            # Get the establishments value for each description type
            matching_row = filtered_df[filtered_df['NAICS Description'] == value]
            if not matching_row.empty:
                result.append(int(matching_row['Establishments'].values[0]))
            else:
                result.append(0)  # If the county does not have that category, append 0

    else:
        total_row = df1[(df1["State Name"] == state) & (df1["County Name"] == county) & (df1["NAICS Description"] == "Total")]
        
        if not total_row.empty:
            result = [127, int(total_row["Establishments"].values[0])]
    return result

# Example usage
state = 'Alaska'
county = 'Yukon-Koyukuk Census Area'
values = get_values_for_county_state(state, county)
print(values)
if len(values) == 3:
    holiness = values[2]/(values[0]+values[1])
else:
    holiness = float((values[0]/values[1]))/0.30956


print(f"Values for {county}, {state}: {values}")
print("Holiness value: " + str(holiness))

