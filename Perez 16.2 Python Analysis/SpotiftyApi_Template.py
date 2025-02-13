# My template to use the Spotify API. Used API to populate datatsets with additional data (Genre, Popularity Score, Artist id, year etc)
# Have to change the def get_song_info and the URL endpoint inside of it, to get different datasources 
# Can Load different different datasets
# also had to save requests in chunks  and throttle requests inorder to circumvent the API request limits.

# Import necessary libraries
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import time
import pandas as pd
import numpy as np
from requests.exceptions import SSLError

# Load environment variables aka keys to use API
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Load the CSV file with the spotify_ids
uni_file_path = "/Users/matthewperez/Desktop/Spotify_Capstone/universal_top_spotify_songs.csv"
uniDf = pd.read_csv(uni_file_path)

# Fix column naming issue
uniDf.rename(columns={' "spotify_id"': 'spotify_id'}, inplace=True)

# Create a DataFrame with unique Spotify IDs
unique_spotify_ids_df = uniDf.drop_duplicates(subset="spotify_id").reset_index(drop=True)

# Split the unique Spotify IDs into 10 chunks
chunks = np.array_split(unique_spotify_ids_df, 10)

# Function to get an API token
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    return json_result["access_token"]

# Function to create authentication headers
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# Function to get song information from Spotify API
def get_song_info(token, song_id):
    global request_count, start_time

    # Check for rate limits
    if request_count >= 150:
        elapsed_time = time.time() - start_time
        if elapsed_time < 60:
            time_to_wait = 60 - elapsed_time
            print(f"Rate limit reached. Pausing for {time_to_wait:.2f} seconds...")
            time.sleep(time_to_wait)
        request_count = 0
        start_time = time.time()
    
    url = f"https://api.spotify.com/v1/tracks/{song_id}?country=US"
    headers = get_auth_header(token)
    
    try:
        result = get(url, headers=headers)
    except SSLError as e:
        print(f"SSL Error for song ID {song_id}: {e}")
        return None

    request_count += 1

    if result.status_code == 429:  # Rate limit error
        retry_after = result.headers.get("Retry-After", 1)
        print(f"Rate limited. Retrying after {retry_after} seconds...")
        time.sleep(int(retry_after))
        return get_song_info(token, song_id)

    if result.status_code != 200:
        print(f"Error: API request failed with status code {result.status_code}")
        return None

    try:
        json_result = json.loads(result.content)
        album_release_date = json_result["album"]["release_date"]
        artist_id = json_result["artists"][0]["id"]
        popularity = json_result["popularity"]

        return {
            "album_release_date": album_release_date,
            "artist_id": artist_id,
            "popularity": popularity,
        }
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error decoding or parsing JSON for song ID {song_id}: {e}")
        return None

# Function to process a chunk and save results
def process_chunk(chunk, chunk_number, token):
    chunk_filename = f"/Users/matthewperez/Desktop/Spotify_Capstone/chunk_{chunk_number + 1}_data.csv"

    # Check if the chunk file already exists
    if os.path.exists(chunk_filename):
        print(f"Chunk {chunk_number + 1} already exists. Skipping...")
        return

    print(f"Processing chunk {chunk_number + 1}/{len(chunks)}...")
    new_data = []

    for song_id in chunk["spotify_id"]:
        print(f"Fetching data for Spotify ID: {song_id}")
        song_info = get_song_info(token, song_id)
        if song_info:
            new_data.append(song_info)
        else:
            # Append None values if the API call fails
            new_data.append({"album_release_date": None, "artist_id": None, "popularity": None})

    # Convert the new data into a DataFrame
    chunk_df = pd.DataFrame(new_data)
    chunk_df["spotify_id"] = chunk["spotify_id"].values

    # Save the chunk's data to a CSV file
    chunk_df.to_csv(chunk_filename, index=False)
    print(f"Chunk {chunk_number + 1} saved to '{chunk_filename}'")

# Main logic
token = get_token()
request_count = 0
start_time = time.time()

# Start processing from a specific chunk to avoid overwriting
start_chunk = 8  # Change this to the appropriate starting chunk (e.g., 0, 1, 2, etc.)

for i, chunk in enumerate(chunks[start_chunk:], start=start_chunk):
    process_chunk(chunk, i, token)
    print(f"Finished processing chunk {i + 1}/{len(chunks)}")

#  Combine all chunks into a single DataFrame
import glob

all_chunks = glob.glob("/Users/matthewperez/Desktop/Spotify_Capstone/chunk_*_data.csv")
combined_df = pd.concat([pd.read_csv(chunk) for chunk in all_chunks], ignore_index=True)
combined_df.to_csv("/Users/matthewperez/Desktop/Spotify_Capstone/combined_spotify_data.csv", index=False)
print("All chunks combined and saved to 'combined_spotify_data.csv'")
