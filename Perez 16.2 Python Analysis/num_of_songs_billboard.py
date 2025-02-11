# of songs in billbord 100 a year

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = '/Users/matthewperez/Desktop/Spotify_Capstone/charts.csv'  # Update with your file path
data = pd.read_csv(file_path)

# Convert the 'date' column to datetime format
data['date'] = pd.to_datetime(data['date'], errors='coerce')

# Extract the year from the 'date' column
data['year'] = data['date'].dt.year

# Remove any rows with missing 'year', 'song', or 'artist' values
data = data.dropna(subset=['year', 'song', 'artist'])

# Filter for years 1990 and later
data = data[data['year'] >= 1990]

# Count the unique combinations of 'song' and 'artist' by 'year'
unique_combinations_by_year = (
    data.groupby('year')
    .apply(lambda x: x[['song', 'artist']].drop_duplicates().shape[0])
    .reset_index(name='unique_combinations')
)

# Save the results to a CSV file
csv_output_path = '/Users/matthewperez/Desktop/Spotify_Capstone/num_of_songs_billboard.csv'
unique_combinations_by_year.to_csv(csv_output_path, index=False)

# Plot the data as a line graph
plt.figure(figsize=(12, 6))
plt.plot(
    unique_combinations_by_year['year'],
    unique_combinations_by_year['unique_combinations'],
    label='Unique Song-Artist Combinations',
    linewidth=2,
    marker='o'
)

# Add titles and labels
plt.title("Unique Song-Artist Combinations Per Year (1990 and Later)", fontsize=16)
plt.xlabel("Year", fontsize=14)
plt.ylabel("Number of Unique Combinations", fontsize=14)
plt.grid(visible=True, linestyle="--", alpha=0.5)
plt.tight_layout()

# Show the plot
plt.show()

