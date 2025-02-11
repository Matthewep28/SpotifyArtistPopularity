

# box and whiskers for Spotify dataset, how long a song tends to last on the Spotify Daily 50 in the US

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
uni_file_path = "/Users/matthewperez/Desktop/Spotify_Capstone/universal_top_spotify_songs.csv"
df = pd.read_csv(uni_file_path)

# Filter for entries with "US" as the country
us_df = df[df['country'] == 'US']

# Count how many times each song is listed
song_counts = us_df[' "spotify_id"'].value_counts()

# Convert to a DataFrame for easier plotting
song_counts_df = song_counts.reset_index()
song_counts_df.columns = ['song', 'count']

# Save the data to a CSV file
csv_output_path = "/Users/matthewperez/Desktop/Spotify_Capstone/BoxNWhiskers_Spotify.csv"
song_counts_df.to_csv(csv_output_path, index=False)


# Plot a vertical box-and-whisker plot of the counts
plt.figure(figsize=(8, 10))  # Adjusted dimensions for a vertical plot
sns.set_theme(style="whitegrid")
sns.boxplot(y=song_counts_df['count'], color="skyblue", width=0.6)  # Note: 'y' is used for vertical orientation

# Add labels and title
plt.title("Spread of How Many Times a Song Stays on the List (US)", fontsize=16)
plt.ylabel("Number of Appearances", fontsize=12)
plt.xlabel("Density", fontsize=12)

# Adjust the y-axis range to focus on the main spread
plt.ylim(0, 75)

# Save and show the plot
output_path = "/Users/matthewperez/Desktop/Spotify_Capstone/box_and_whisker_song_counts_vertical.png"
plt.tight_layout()
plt.show()
plt.savefig(output_path)



