# Linear Regression of the amount of International Markets an artist is in compared to their populairty score. 
# Linear Regression to be done in Tableau 

import pandas as pd

# File path
spot_xmas_file = '/Users/matthewperez/Desktop/Spotify_Capstone/Spot_Xmas.csv'

# Load the dataset
spot_xmas_df = pd.read_csv(spot_xmas_file)

# Step 1: Filter for rows where 'country' is 'US'
us_artists = spot_xmas_df[spot_xmas_df['country'] == 'US']

# Step 2: Get unique 'artist_id' entries
unique_us_artists = us_artists['artist_id'].dropna().unique()

# Step 3: Count unique countries for each artist
artist_country_count = spot_xmas_df.groupby('artist_id')['country'].nunique()

# Filter the artist_country_count for artists in the US list
artist_country_count_us = artist_country_count.loc[artist_country_count.index.intersection(unique_us_artists)]

# Merge with artist names and popularity scores for clarity
artist_info = spot_xmas_df[['artist_id', 'artists', 'popularity']].drop_duplicates()
artist_country_count_us = artist_country_count_us.reset_index(name='country_count')
artist_country_count_us = artist_country_count_us.merge(artist_info, on='artist_id')

# Save the full dataset to a CSV file
csv_output_path = '/Users/matthewperez/Desktop/Spotify_Capstone/#ofIntMarkets_to_popScore.csv'
artist_country_count_us.to_csv(csv_output_path, index=False)

# Sort by the count of unique countries and select the top 10
top_10_artists = artist_country_count_us.nlargest(10, 'country_count')

# Print the top 10 artist_id, artist names, popularity scores, and country counts
print("Top 10 Artists by International Markets:")
print(top_10_artists[['artist_id', 'artists', 'popularity', 'country_count']])

# Save the top 10 artists to another CSV file (optional)
top_10_csv_output_path = '/Users/matthewperez/Desktop/Spotify_Capstone/USartists_Markets.csv'
top_10_artists.to_csv(top_10_csv_output_path, index=False)



