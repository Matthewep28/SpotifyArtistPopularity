# Linear Regression of the amount of weeks an artist has been on the billboard 100 to the artist's popularity score

import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

# Load the xmas_3.csv file
file_path = "/Users/matthewperez/Desktop/Spotify_Capstone/xmas_3.csv"  # Replace with the path to xmas_3.csv
xmas_3_df = pd.read_csv(file_path)

# Ensure 'date' is in datetime format and filter for dates 2010 and after
xmas_3_df["date"] = pd.to_datetime(xmas_3_df["date"])
filtered_df = xmas_3_df[xmas_3_df["date"].dt.year >= 2010]

# Count the number of times each unique artist_id appeared on a unique date
artist_date_counts = filtered_df.groupby(["artist_id", "date"]).size().reset_index(name="appearance_count")

# Merge with the popularity scores
artist_popularity = filtered_df[["artist_id", "popularity"]].drop_duplicates()
merged_data = pd.merge(artist_date_counts, artist_popularity, on="artist_id", how="inner")

# Drop rows where 'popularity' or 'appearance_count' is NaN
merged_data.dropna(subset=["appearance_count", "popularity"], inplace=True)

# Save the merged data to a CSV file
csv_output_path = "/Users/matthewperez/Desktop/Spotify_Capstone/WeeksOnCharts_to_Pop.csv"
merged_data.to_csv(csv_output_path, index=False)

# Prepare data for linear regression
X = merged_data["appearance_count"].values.reshape(-1, 1)  # Feature: Count of appearances
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
plt.xlabel("Appearance Count (Times per Unique Date)")
plt.ylabel("Popularity Score")
plt.title("Linear Regression: Appearance Count vs. Popularity")
plt.legend()
plt.ylim(0, 100)
plt.show()
