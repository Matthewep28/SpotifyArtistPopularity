# number of songs with multiple artists over time (since 1990)
# Avg number of appearances for songs with one artist: 8.285891440865294
# Avg number of appearances for songs with more than one artist: 9.331905541602497

import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the data
file_path = '/Users/matthewperez/Desktop/Spotify_Capstone/12-20-24-grand-charts-no-audio-feats.csv'  # Update with your actual file path
data = pd.read_csv(file_path)

# Step 2: Filter for entries from 1990 onwards
data['date'] = pd.to_datetime(data['date'], errors='coerce')  # Ensure 'date' is in datetime format
data = data[data['date'].dt.year >= 1990]

# Step 3: Filter for songs with more than one artist
filtered_data = data[data['num_artists'] > 1]

# Step 4: Group by year and count unique spotify_id per year
filtered_data['year'] = filtered_data['date'].dt.year  # Extract year from the date
unique_songs_per_year = filtered_data.groupby('year')['spotify_id'].nunique()

unique_songs_per_year.to_csv('/Users/matthewperez/Desktop/Spotify_Capstone/Number_of_Songs_With_Multiple_Artists.csv', header=True)

# Step 5: Plot the results in a line graph
plt.figure(figsize=(10, 6))
plt.plot(unique_songs_per_year.index, unique_songs_per_year.values, marker='o', linestyle='-', color='b')
plt.title('Number of Unique Songs with More Than One Artist per Year')
plt.xlabel('Year')
plt.ylabel('Number of Unique Songs')
plt.grid(True)
plt.show()
