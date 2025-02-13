# pie chart of 2005 vs 2021 to show global region distrubtion

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = '/Users/matthewperez/Desktop/Spotify_Capstone/charts_with_main_genre.csv'  # Update with your file path
data = pd.read_csv(file_path)

# Convert the 'date' column to datetime format
data['date'] = pd.to_datetime(data['date'], errors='coerce')

# Step 1: Filter data for the years 2005 and 2021
data_2005 = data[data['date'].dt.year == 2005]
data_2021 = data[data['date'].dt.year == 2021]

# Step 2: Remove groups 'Unknown' and 'Other' for both years
data_2005_filtered = data_2005[~data_2005['group'].isin(['Unknown', 'Other'])]
data_2021_filtered = data_2021[~data_2021['group'].isin(['Unknown', 'Other'])]

# Step 3: Count the unique artists per group
artists_2005 = data_2005_filtered.groupby('group')['artist_id'].nunique()
artists_2021 = data_2021_filtered.groupby('group')['artist_id'].nunique()

# Step 4: Combine data into a single DataFrame for "long format"
# Add year information and convert Series to DataFrame
artists_2005_df = artists_2005.reset_index().rename(columns={'artist_id': 'unique_artists'})
artists_2005_df['year'] = 2005

artists_2021_df = artists_2021.reset_index().rename(columns={'artist_id': 'unique_artists'})
artists_2021_df['year'] = 2021

# Concatenate both years
long_format_df = pd.concat([artists_2005_df, artists_2021_df], ignore_index=True)

# Step 5: Calculate total artists per year for percentage calculation
total_artists_per_year = long_format_df.groupby('year')['unique_artists'].sum()
long_format_df = long_format_df.merge(total_artists_per_year, on='year', suffixes=('', '_total'))

# Add a column for the percentage of total artists per group
long_format_df['percentage'] = (long_format_df['unique_artists'] / long_format_df['unique_artists_total']) * 100

# Step 6: Save the "long format" data to CSV
csv_output_path = '/Users/matthewperez/Desktop/Spotify_Capstone/region_pieChart.csv'
long_format_df[['year', 'group', 'percentage']].to_csv(csv_output_path, index=False)

# Plot Pie Charts (Optional)
# Pie chart for 2005
plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)
artists_2005.plot(kind='pie', autopct='%1.1f%%', startangle=90, legend=False, title='Artist Distribution (2005)')
plt.ylabel('')  # Hide the ylabel

# Pie chart for 2021
plt.subplot(1, 2, 2)
artists_2021.plot(kind='pie', autopct='%1.1f%%', startangle=90, legend=False, title='Artist Distribution (2021)')
plt.ylabel('')  # Hide the ylabel

plt.tight_layout()
plt.show()

# Step 7: Print percentage growth/decline per group
growth_percentage = ((artists_2021 - artists_2005) / artists_2005) * 100
print("Percentage Growth/Decline (2005 to 2021):")
print(growth_percentage)

# Optional: Save growth percentages to CSV
growth_csv_output_path = '/Users/matthewperez/Desktop/Spotify_Capstone/Billboard_Region_Growth.csv'
growth_percentage.to_csv(growth_csv_output_path, header=True)


