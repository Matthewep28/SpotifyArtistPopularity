

#Linear graph of the change of genres present in Billboard 100 over time
#smoothed over with a 5 year rolling window


import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = "/Users/matthewperez/Desktop/Spotify_Capstone/charts_with_main_genre.csv"
df = pd.read_csv(file_path)

# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Extract the year from the 'date' column
df['year'] = df['date'].dt.year

# Filter for entries from 1975 onward and exclude 'Other' genre
filtered_df = df[(df['year'] >= 1975) & (df['Main_Genre'] != 'Other')]

# Group by 'year' and 'Main_Genre', and count occurrences
genre_counts = filtered_df.groupby(['year', 'Main_Genre']).size().reset_index(name='count')

# Pivot the data to make it easier for percentage calculations (one column per genre)
genre_pivot = genre_counts.pivot(index='year', columns='Main_Genre', values='count').fillna(0)

# Calculate the total songs per year
genre_pivot['total_songs'] = genre_pivot.sum(axis=1)

# Calculate the percentage each genre contributes to the total songs per year
genre_percentages = genre_pivot.div(genre_pivot['total_songs'], axis=0).drop(columns=['total_songs'])

# Convert the data to "long format" for easier use in Tableau or other tools
genre_percentages_long = genre_percentages.reset_index().melt(id_vars='year', var_name='Genre', value_name='Percentage')

# Apply a rolling window to smooth the trends (e.g., 5-year window)
rolling_window = 5
genre_percentages_long['Smoothed_Percentage'] = genre_percentages_long.groupby('Genre')['Percentage'].transform(
    lambda x: x.rolling(window=rolling_window, min_periods=1).mean()
)

# Save the long-format data to a CSV file
csv_output_path = "/Users/matthewperez/Desktop/Spotify_Capstone/Genres_Over_Time_Long.csv"
genre_percentages_long.to_csv(csv_output_path, index=False)

# Plot the smoothed data as a line graph
plt.figure(figsize=(12, 8))
for genre in genre_percentages.columns:
    plt.plot(
        genre_percentages.index,
        genre_percentages[genre] * 100,  # Convert to percentages
        label=genre,
        linewidth=2
    )

# Add titles and labels
plt.title(f"Trends in Genre Percentages Over Time (Smoothed with {rolling_window}-Year Rolling Average)", fontsize=16)
plt.xlabel("Year", fontsize=14)
plt.ylabel("Percentage of Total Songs (%)", fontsize=14)
plt.legend(title="Main Genre", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(visible=True, linestyle="--", alpha=0.5)
plt.tight_layout()

# Save the chart as a PNG file
output_path = "/Users/matthewperez/Desktop/Spotify_Capstone/genre_trends_percentages_line.png"
plt.savefig(output_path)

# Show the chart
plt.show()
