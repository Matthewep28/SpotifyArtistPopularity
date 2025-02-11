# ID top non English speaking countries US audiences listen to
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = '/Users/matthewperez/Desktop/Spotify_Capstone/charts_with_main_genre.csv'  # Update with your file path
data = pd.read_csv(file_path)

# Convert the 'date' column to datetime format
data['date'] = pd.to_datetime(data['date'], errors='coerce')



# Step 2: Create a new column for unique song-artist combinations
data_filtered['song_artist'] = data_filtered['song'] + " - " + data_filtered['artist']

# Step 3: Count unique song-artist combinations per country_code
country_song_count = data_filtered.groupby('country_code')['song_artist'].nunique()



# Save the top 5 countries to a CSV file
top_5_countries.to_csv('/Users/matthewperez/Desktop/Spotify_Capstone/listner_map.csv', header=True)

# Step 5: Print unique artist names from South Korea (KR) in the terminal
unique_artists_kr = data_filtered[data_filtered['country_code'] == 'CU']['artist'].unique()
print("Unique artists from South Korea (KR):")
for artist in unique_artists_kr:
    print(artist)

# Step 6: Plot the results
plt.figure(figsize=(10, 6))
top_5_countries.plot(kind='bar', color='skyblue')
plt.title('Top 5 Countries with Most Songs on Billboard 100 (2015 and Onward)', fontsize=14)
plt.xlabel('Country', fontsize=12)
plt.ylabel('Number of Unique Songs', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
