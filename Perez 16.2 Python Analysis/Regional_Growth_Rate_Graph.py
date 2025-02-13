# Yearly Growth Rate of Global Regions Market Share of Billboard 100 Artists' Origin since 2005 as Linear Graph

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "/Users/matthewperez/Desktop/Spotify_Capstone/charts_with_main_genre.csv"
df = pd.read_csv(file_path)

# Step 1: Filter the data
def filter_data(df):
    # Convert 'date' to datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Filter for dates since 2005
    #df = df[df['date'].dt.year >= 2005]

    # Exclude 'Unknown' group
    df = df[df['group'] != 'Unknown']
    return df

filtered_df = filter_data(df)

# Step 2: Count song occurrences per year and region (group)
def count_songs_per_year(df):
    # Extract year from the 'date' column
    df['year'] = df['date'].dt.year

    # Group by year and group, and count unique songs
    song_counts = df.groupby(['year', 'group'])['song'].count().reset_index()
    song_counts.rename(columns={'song': 'song_count'}, inplace=True)
    
    # Filter for regions with at least 3 songs per year
    song_counts = song_counts[song_counts['song_count'] >= 3]
    return song_counts

song_counts = count_songs_per_year(filtered_df)

# Step 3: Calculate year-to-year percentage growth for each region
def calculate_growth(df):
    # Sort by group and year
    df = df.sort_values(by=['group', 'year'])

    # Calculate percentage growth
    df['growth_rate'] = df.groupby('group')['song_count'].pct_change() * 100

    # Replace NaN and infinite growth rates
    df['growth_rate'] = df['growth_rate'].fillna(0)
    return df

growth_df = calculate_growth(song_counts)

# Step 4: Identify the top 10 regions with the highest cumulative growth
def get_top_regions(df):
    # Sum growth rates per group
    cumulative_growth = df.groupby('group')['growth_rate'].sum().reset_index()
    cumulative_growth = cumulative_growth.sort_values(by='growth_rate', ascending=False)
    
    # Get the top 10 regions
    top_regions = cumulative_growth.head(10)['group'].tolist()
    return top_regions

top_regions = get_top_regions(growth_df)

# Filter the data for only the top regions
filtered_growth_df = growth_df[growth_df['group'].isin(top_regions)]

# Step 5: Smooth the growth rates using a 5-year rolling average
def apply_rolling_average(df):
    df['smoothed_growth'] = df.groupby('group')['growth_rate'].rolling(window=5, min_periods=1).mean().reset_index(level=0, drop=True)
    return df

smoothed_df = apply_rolling_average(filtered_growth_df)

csv_output_path = "/Users/matthewperez/Desktop/Spotify_Capstone/Region_Growth_Line.csv"
smoothed_df.to_csv(csv_output_path, index=False)

# Step 6: Plot the growth rates as a line graph
def plot_growth_rates(df, top_regions):
    plt.figure(figsize=(12, 8))
    sns.set(style="whitegrid")
    
    # Create a line plot for each region
    for region in top_regions:
        region_data = df[df['group'] == region]
        plt.plot(region_data['year'], region_data['smoothed_growth'], label=region, linewidth=2)
    
    # Add plot details
    plt.title("Top 10 Regions with Year-to-Year Song Growth (2005+)", fontsize=14)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Smoothed Growth Rate (%)", fontsize=12)
    plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Show the plot
    plt.show()

# Plot the results
plot_growth_rates(smoothed_df, top_regions)
