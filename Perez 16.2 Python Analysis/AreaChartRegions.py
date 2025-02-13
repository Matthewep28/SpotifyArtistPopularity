# shows the longterm make up of Regions on the Billboard 100 as a line graph

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = "/Users/matthewperez/Desktop/Spotify_Capstone/charts_with_main_genre.csv"
df = pd.read_csv(file_path)

# Step 1: Filter the data
def filter_data(df):
    # Convert  to datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Exclude 'Unknown' and 'Other' groups
    df = df[(df['group'] != 'Unknown') & (df['group'] != 'Other')]
    return df

filtered_df = filter_data(df)

# Step 2: Count song occurrences per year and region (group)
def count_songs_per_year(df):
    # Extract year from the 'date' column
    df['year'] = df['date'].dt.year

    # Group by year and group, and count unique songs
    song_counts = df.groupby(['year', 'group'])['song'].count().reset_index()
    song_counts.rename(columns={'song': 'song_count'}, inplace=True)

    # Calculate the total number of songs per year
    total_songs_per_year = song_counts.groupby('year')['song_count'].sum().reset_index()
    total_songs_per_year.rename(columns={'song_count': 'total_songs'}, inplace=True)

    # Merge total songs per year into the song counts
    song_counts = song_counts.merge(total_songs_per_year, on='year')

    # Calculate percentage makeup of each group per year
    song_counts['percentage_makeup'] = (song_counts['song_count'] / song_counts['total_songs']) * 100

    return song_counts

song_counts = count_songs_per_year(filtered_df)

# Save the dataset to a CSV file
csv_output_path = "/Users/matthewperez/Desktop/Spotify_Capstone/AreaChartRegions.csv"
song_counts.to_csv(csv_output_path, index=False)

# Step 3: Create the area chart
def plot_area_chart(df):
    # Pivot data for plotting
    pivot_df = df.pivot(index='year', columns='group', values='percentage_makeup').fillna(0)

    # Plot the area chart
    plt.figure(figsize=(12, 8))
    plt.stackplot(
        pivot_df.index, 
        pivot_df.T, 
        labels=pivot_df.columns, 
        alpha=0.8
    )

    # Add plot details
    plt.title("Year-by-Year Group Makeup of Total Songs", fontsize=14)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Percentage Makeup (%)", fontsize=12)
    plt.legend(title="Group", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Show the plot
    plt.show()

# Plot the area chart
plot_area_chart(song_counts)

