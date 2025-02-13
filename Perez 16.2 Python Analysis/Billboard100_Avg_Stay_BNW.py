# Box and whiskers plot showing distribution of long a song averages on the Billboard 100

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = '/Users/matthewperez/Desktop/Spotify_Capstone/charts.csv'  # Update with your file path
data = pd.read_csv(file_path)

# Step 1: Convert the 'date' column to datetime format
data['date'] = pd.to_datetime(data['date'], errors='coerce')

# Step 2: Filter for entries from 1990 and onward
data_filtered = data[data['date'].dt.year >= 1990]

# Step 3: Create a new column for unique song-artist combinations
data_filtered.loc[:, 'song_artist'] = data_filtered['song'] + " - " + data_filtered['artist']  # Use .loc to avoid the warning

# Step 4: Count how many times each unique song-artist combination occurs (how long a song stays on the Billboard 100)
song_artist_count = data_filtered.groupby('song_artist').size()

# Step 5: Save the data to a CSV file
output_file_path = '/Users/matthewperez/Desktop/Spotify_Capstone/BoxNWhiskers_Billboard.csv'
song_artist_count.to_csv(output_file_path, header=['Weeks_on_Billboard'], index_label='Song_Artist')
print(f"Data saved to {output_file_path}")

# Step 5: Create a vertical box and whiskers plot to show the distribution of how long songs tend to stay
plt.figure(figsize=(10, 6))
plt.boxplot(song_artist_count, vert=True, patch_artist=True, 
            boxprops=dict(facecolor='skyblue', color='blue'),  # Set color for box
            flierprops=dict(markerfacecolor='red', marker='o', markersize=5))  # Set color for outliers
plt.title('Distribution of Song Durations on Billboard 100 (1990 and onward)', fontsize=14)
plt.ylabel('Number of Weeks on Billboard 100', fontsize=12)
plt.xticks([1], ['Songs'])
plt.tight_layout()
plt.show()

