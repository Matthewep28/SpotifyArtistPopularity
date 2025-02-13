#linear regression of amount of unique songs an artist has in the billboard 100 to their popularity score
#linear Regression redone in Tableau in final For Ease

import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

# Load  file
file_path = "/Users/matthewperez/Desktop/Spotify_Capstone/xmas_3.csv"  # Replace with the path to xmas_3.csv
xmas_3_df = pd.read_csv(file_path)


# Ensure datetime format and filter for dates 2010 and after
xmas_3_df["date"] = pd.to_datetime(xmas_3_df["date"])
filtered_df = xmas_3_df[xmas_3_df["date"].dt.year >= 2010]

# Count unique songs per artist_id
song_counts = filtered_df.groupby("artist_id")["song"].nunique().reset_index()
song_counts.rename(columns={"song": "unique_songs_count"}, inplace=True)

# Merge with the popularity scores
artist_popularity = filtered_df[["artist_id", "popularity"]].drop_duplicates()
merged_data = pd.merge(song_counts, artist_popularity, on="artist_id", how="inner")

# Drop rows where 'popularity' or 'unique_songs_count' is NaN
merged_data.dropna(subset=["unique_songs_count", "popularity"], inplace=True)

csv_output_path = "/Users/matthewperez/Desktop/Spotify_Capstone/#ofSongs_to_popScore.csv"
merged_data.to_csv(csv_output_path, index=False)

# Prepare data for linear regression
X = merged_data["unique_songs_count"].values.reshape(-1, 1)  # Feature: Count of unique songs
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
plt.xlabel("Unique Songs Count")
plt.ylabel("Popularity Score")
plt.title("Linear Regression: Unique Songs vs. Popularity")
plt.ylim(0, 100)
plt.legend()
plt.show()

#  top 20 artists based on unique song counts
top_artists = song_counts.sort_values(by="unique_songs_count", ascending=False).head(20)


print("Top 20 Artists with Most Unique Songs:")
for index, row in top_artists.iterrows():
    print(f"Artist ID: {row['artist_id']}, Unique Songs: {row['unique_songs_count']}")
