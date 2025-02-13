#linear regression model of number of top 10 hits an artist has to popularity score
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Load the xmas_3.csv file
file_path = "/Users/matthewperez/Desktop/Spotify_Capstone/xmas_3.csv"  # Replace with the path to xmas_3.csv
xmas_3_df = pd.read_csv(file_path)

# Ensure 'date' is in datetime format and filter for dates 2010 and after
xmas_3_df["date"] = pd.to_datetime(xmas_3_df["date"])
filtered_df = xmas_3_df[xmas_3_df["date"].dt.year >= 2010]

# Filter the dataframe to only include ranks between 1 and 10
filtered_df_top_10 = filtered_df[(filtered_df["rank"] >= 1) & (filtered_df["rank"] <= 10)]

# Count unique artist-song combinations that had any rank between 1-10
artist_song_top_10 = filtered_df_top_10.groupby(["artist_id", "song"])["rank"].max().reset_index()

# Count how many unique artist-song combinations there are for each artist_id
artist_song_counts = artist_song_top_10.groupby("artist_id")["song"].nunique().reset_index()
artist_song_counts.rename(columns={"song": "top_10_hit_count"}, inplace=True)

# Merge with the popularity scores
artist_popularity = filtered_df[["artist_id", "popularity"]].drop_duplicates()
merged_data = pd.merge(artist_song_counts, artist_popularity, on="artist_id", how="inner")

# Drop rows where 'popularity' or 'top_10_hit_count' is NaN
merged_data.dropna(subset=["top_10_hit_count", "popularity"], inplace=True)

# Save the final data to a CSV
csv_output_path = '/Users/matthewperez/Desktop/Spotify_Capstone/#ofTop10Hits_to_popScore.csv'
merged_data.to_csv(csv_output_path, index=False)

# Prepare data for linear regression
X = merged_data["top_10_hit_count"].values.reshape(-1, 1)  # Feature: Count of unique songs in top 10 ranks
y = merged_data["popularity"].values  # Target: Popularity score

# Perform linear regression
model = LinearRegression()
model.fit(X, y)

# Display regression results
print(f"Coefficient: {model.coef_[0]}")
print(f"Intercept: {model.intercept_}")
print(f"R^2 Score: {model.score(X, y)}")

# Plot the regression
plt.scatter(X, y, color="blue", label="Data Points")
plt.plot(X, model.predict(X), color="red", label="Regression Line")
plt.xlabel("Top 10 Hits Count")
plt.ylabel("Popularity Score")
plt.title("Linear Regression: Top 10 Hits Count vs. Popularity")
plt.legend()

# Set the y-axis limit to 100 (adjust if necessary)
plt.ylim(0, 100)

plt.show()

# Get the top 20 artists based on their top 10 hit counts
top_artists = artist_song_counts.sort_values(by="top_10_hit_count", ascending=False).head(20)

# Print the top 20 artists and their top 10 hit counts
print("Top 20 Artists with Most Top 10 Hits:")
print(top_artists)
