# Perfect Parse 2
# parsing artist names to take into account featured artists and collaborations


import re

# Function to parse artist names based on the specified delimiters
def parse_artist_names(artist_string):
    # Handle "Lil Nas X" as a special case (do not split)
    artist_string = artist_string.replace("Lil Nas X", "Lil Nas_X")
    
    # Remove parentheses and their contents (e.g., "Artist (feat. someone)" -> "Artist")
    artist_string = re.sub(r'\(.*?\)', '', artist_string)
    
    # Split the string using the updated delimiters
    # This splits on commas, 'x', 'featuring', 'Featuring', '&', 'and', 'with', and 'X' (case-insensitive for 'X')
    artist_list = re.split(r'\s*(?:,|\s*x\s*|\s*featuring\s*|\s*Featuring\s*|\s*&\s*|\s*and\s*|\s*with\s*|\s*X\s*)\s*', artist_string, flags=re.IGNORECASE)
    
    # Replace the temporary "Lil Nas_X" back to "Lil Nas X"
    artist_list = [artist.replace("Lil Nas_X", "Lil Nas X") for artist in artist_list]
    
    # Strip each artist name of any leading/trailing whitespace
    return [artist.strip() for artist in artist_list if artist.strip()]

# Example song data (use actual data instead)
songs = [
    {"title": "Song 1", "artists": "Coldplay x BTS"},
    {"title": "Song 2", "artists": "Jason Aldean & Carrie Underwood"},
    {"title": "Song 3", "artists": "Lil Nas X, Ed Sheeran"},
    {"title": "Song 4", "artists": "Ariana Grande and Justin Bieber"},
    {"title": "Song 5", "artists": "Foo Fighters (live)"},
    {"title": "Song 6", "artists": "Post Malone with Swae Lee"},
    {"title": "Song 7", "artists": "BLACKPINK X Selena Gomez"}
]

# Function to collect all unique artists from songs
def collect_artists(songs):
    all_artists = []
    for song in songs:
        artists = parse_artist_names(song['artists'])  # Parse artist names for each song
        all_artists.extend(artists)  # Add to the all_artists list
    return list(set(all_artists))  # Return a list of unique artists

# Collect artists from all songs
all_artists = collect_artists(songs)

# Print the parsed list of artists
print("Parsed Artists List:")
print(all_artists)
