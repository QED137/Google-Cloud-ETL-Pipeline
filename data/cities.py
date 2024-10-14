import requests
import pandas as pd
from bs4 import BeautifulSoup
from lat_lon_parser import parse  # latitude/longitude parser

def cities_data(cities):
    """
    Fetches city information (latitude, longitude, and country) from Wikipedia.
    
    Args:
        cities (list): A list of city names.
    
    Returns:
        pd.DataFrame: A DataFrame containing city information.
    """
    city_data = []
    
    for city in cities:
        url = f"https://www.wikipedia.org/wiki/{city}"
        response = requests.get(url)
        city_soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the relevant information
        try:
            city_latitude = city_soup.find(class_="latitude").get_text()
            city_longitude = city_soup.find(class_="longitude").get_text()
            country = city_soup.find(class_="infobox-data").get_text()
            city_data.append({
                "City": city,
                "Country": country,
                "Latitude": parse(city_latitude),  # Latitude in decimal format
                "Longitude": parse(city_longitude)  # Longitude in decimal format
            })
        except AttributeError:
            print(f"Could not find data for {city}")
            continue

    return pd.DataFrame(city_data)
