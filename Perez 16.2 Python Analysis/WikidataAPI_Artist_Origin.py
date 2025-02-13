# My template for utilizing the WikiData API to find the origin/birthplace of bands/arists. 
# Output is saved as 2 letter country code. I have anohter file where I parse artist/band names
# so entries like 'Coldplay X BTS' or 'Michael Jackson Featuring Paul McCartney' are recognizied as different artists

import requests
import pycountry

def get_country_code(country_name):
    """
    Converts a country name to a two-letter country code.
    """
    try:
        country = pycountry.countries.lookup(country_name)
        return country.alpha_2
    except LookupError:
        print(f"Could not find country code for '{country_name}'")
        return None

def get_origin_or_nationality(name):
    """
    Tries to find the origin for a band or nationality for an individual.
    If not found as a band, it checks for individual nationality.
    """
    # Search for the entity on Wikidata
    search_url = "https://www.wikidata.org/w/api.php"
    search_params = {
        "action": "wbsearchentities",
        "format": "json",
        "language": "en",
        "search": name
    }
    
    search_response = requests.get(search_url, params=search_params).json()
    if not search_response["search"]:
        print(f"No Wikidata entry found for '{name}'")
        return "Can't be found"
    
    # Get the Wikidata entity ID
    entity_id = search_response["search"][0]["id"]
    
    # Query the entity data
    entity_url = f"https://www.wikidata.org/wiki/Special:EntityData/{entity_id}.json"
    entity_response = requests.get(entity_url).json()
    
    try:
        claims = entity_response["entities"][entity_id]["claims"]

        # First, try to get "origin" (P495) for bands
        if "P495" in claims:
            origin_id = claims["P495"][0]["mainsnak"]["datavalue"]["value"]["id"]
        # If not found, try "country of citizenship" (P27) for individuals
        elif "P27" in claims:
            origin_id = claims["P27"][0]["mainsnak"]["datavalue"]["value"]["id"]
        else:
            print(f"No origin or nationality found for '{name}'")
            return "Can't be found"

        # Query the country label
        country_url = f"https://www.wikidata.org/wiki/Special:EntityData/{origin_id}.json"
        country_response = requests.get(country_url).json()
        country_name = country_response["entities"][origin_id]["labels"]["en"]["value"]
        return country_name
    except KeyError as e:
        print(f"Error parsing data for '{name}': {e}")
        return "Can't be found"

def process_entries(data):
    """
    Processes a list of entries (bands or individual artists), fetches their origin/nationality, and outputs 2-letter country codes.
    """
    results = []
    for entry in data:
        name = entry["name"]
        
        print(f"Processing: {name}")
        country_name = get_origin_or_nationality(name)
        if country_name != "Can't be found":
            country_code = get_country_code(country_name)
        else:
            country_code = "Can't be found"
        
        results.append({"name": name, "country_code": country_code})
    
    return results

# Example Dataset
data = [
    {"name": "Coldplay"},
    {"name": "BTS"},
    {"name": "Jason Aldean"},
    {"name": "Carrie Underwood"},
    {"name": "Lil Nas X"},
    {"name": "Ed Sheeran"},
    {"name": "Ariana Grande"},
    {"name": "Justin Bieber"}
]

# Process the dataset
results = process_entries(data)

# Output results
for result in results:
    print(f"{result['name']}: {result['country_code']}")
