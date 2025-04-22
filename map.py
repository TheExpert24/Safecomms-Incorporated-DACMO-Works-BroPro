import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm
import matplotlib.ticker as ticker
from shapely.strtree import STRtree


# Load the CSV data into a DataFrame
df = pd.read_csv('thissux.csv')
df1 = pd.read_csv('cleaned_output.csv')
df2 = pd.read_csv('ar.csv')
df3 = pd.read_csv('rr.csv')


result = [1,1,1]

def get_values_for_county_state(state, county):
    global result
    if not df[(df['County Name'] == county) & (df['State Name'] == state)].empty:
        result = []
        #filter based on state and county
        filtered_df = df[(df['State Name'] == state) & (df['County Name'] == county)] #THIS APPLIES TO COUNTIES THAT HAVE REALTORS, GAMBLING, AND CHURCHES

        #three required descriptions
        required_values = ['Real Estate', 'Amusement', 'Religious']
        
        for value in required_values:
            #establishments number (number of businesses) for each NAICS description
            matching_row = filtered_df[filtered_df['NAICS Description'] == value]
            if not matching_row.empty:
                result.append(int(matching_row['Establishments'].values[0]))
            else:
                result.append(0)  #basically not applicable

    elif not df2[(df2['County Name'] == county) & (df2['State Name'] == state)].empty: #THIS APPLIES TO COUNTIES THAT HAVE ONLY GAMBLING AND CHURCHES
        result = []
        # Filter the DataFrame based on state and county
        filtered_df = df2[(df2['State Name'] == state) & (df2['County Name'] == county)]

        #
        required_values = ['Real Estate', 'Amusement', 'Religious']
        
        for value in required_values:
            # Get the establishments value for each description type
            matching_row = filtered_df[filtered_df['NAICS Description'] == value]
            if not matching_row.empty:
                result.append(int(matching_row['Establishments'].values[0]))
            else:
                result.append(0)  # If the county does not have that category, append 0

    elif not df3[(df3['County Name'] == county) & (df3['State Name'] == state)].empty: #THIS APPLIES TO COUNTIES THAT ONLY HAVE REALTORS AND CHURCHES
        result = []
        # Filter the DataFrame based on state and county
        filtered_df = df3[(df3['State Name'] == state) & (df3['County Name'] == county)] #df3 is the list of counties that have at least realtors and churches, but don't necessarily have other stuff

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
        
        #if not total_row.empty:
            #result = [1,1,1]# [127, int(total_row["Establishments"].values[0])]
    #print(f"{county}, {state}: {result}")
    result1 = result
    return result1

# Function to calculate holiness for a given county
def calculate_holiness(values):
    if len(values) == 3:
        holiness = (values[2]/(values[1]+values[0]))
    else:
        holiness = float((values[0]/values[1]))/0.30956
    return holiness

# Get all unique counties in the DataFrame
all_counties = df1[['State Name', 'County Name']].drop_duplicates()

# List to store holiness values
holiness_values = []

# Loop through all counties and calculate holiness
for _, row in all_counties.iterrows():
    state = row['State Name']
    county = row['County Name']
    values = get_values_for_county_state(state, county)
    holiness = calculate_holiness(values)
    holiness_values.append((state, county, holiness))

# Convert holiness values to a DataFrame for merging with the shapefile
holiness_df = pd.DataFrame(holiness_values, columns=['State Name', 'County Name', 'Holiness'])

# Load the U.S. counties shapefile using GeoPandas
# Replace with the path to your shapefile
shapefile_path = 'cb_2021_us_county_20m.shp'
gdf = gpd.read_file(shapefile_path)
print(gdf.columns)  # Columns in the GeoDataFrame (gdf)
print(holiness_df.columns)  # Columns in the holiness data (holiness_df)




# Clean up county and state names by stripping spaces and standardizing the case
gdf['NAME'] = gdf['NAME'].str.strip().str.title()  # Strip and title-case county names in shapefile
holiness_df['County Name'] = holiness_df['County Name'].str.strip().str.title()  # Clean county names
holiness_df['State Name'] = holiness_df['State Name'].str.strip().str.title()  # Clean state names



# Merge the shapefile with the holiness data based on county and state names
gdf = gdf.rename(columns={"COUNTYFP": "County Code", "STUSPS": "State Abbreviation"})
# Make sure the county and state names are consistent in both the DataFrame and shapefile






gdf = gdf.merge(holiness_df, left_on=["STATE_NAME", "NAME"], right_on=["State Name", "County Name"])

# Apply square root or log transformation to exaggerate lower values
gdf['Holiness_transformed'] = gdf['Holiness']  # Applying square root to exaggerate low values

# Use LogNorm for emphasizing the lower range
norm = LogNorm(vmin=gdf['Holiness'].quantile(0.1), vmax=gdf['Holiness'].max())

# Use a color map with higher contrast, like 'plasma', 'viridis', or 'RdYlBu'
cmap = plt.get_cmap("plasma")  # You can also try 'viridis', 'RdYlBu', etc.

# Create the plot
fig, ax = plt.subplots(1, 1, figsize=(15, 15))

# Add a colorbar axis (cax) for the legend
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)

# Plot the counties with the transformed holiness values
gdf.plot(column='Holiness_transformed', ax=ax, legend=True, cax=cax, cmap=cmap, norm=norm, 
         legend_kwds={'label': "Holiness", 'orientation': "vertical"})

# Adjust ticks to have better clarity
# Adjust the colorbar ticks for clarity (optional)
cax.tick_params(axis="y", labelsize=10)

ax.set_xlim(-190, -60)


# Add a title
ax.set_title("US Counties by Holiness", fontsize=16)


# Create an annotation (tooltip)
annot = ax.annotate("", xy=(0,0), xytext=(10,10), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

# Build spatial index for fast lookup
shapes = gdf['geometry'].tolist()
tree = STRtree(shapes)
shape_to_index = {shape: idx for idx, shape in enumerate(shapes)}

# Function to update tooltip
def update_annot(event):
    if event.inaxes == ax:
        point = gpd.points_from_xy([event.xdata], [event.ydata])[0]
        nearest = tree.query(point, predicate="intersects")

        if nearest.size > 0:  # Ensure there's at least one result
            county_index = nearest[0]  # Use the integer index directly
            if county_index in gdf.index:  # Ensure index is valid
                row = gdf.loc[county_index]

                annot.xy = (event.xdata, event.ydata)
                text = f"{row['NAME']}, {row['STATE_NAME']}\nHoliness: {row['Holiness']:.4f}"
                annot.set_text(text)
                annot.set_visible(True)
                fig.canvas.draw_idle()
                return

    annot.set_visible(False)
    fig.canvas.draw_idle()

# Connect the hover event
fig.canvas.mpl_connect("motion_notify_event", update_annot)

# Show the plot
plt.show()
