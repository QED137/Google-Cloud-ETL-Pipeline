import pandas as pd
from datetime import datetime, timedelta
import requests
from pytz import timezone
from db.database import load_config, connect_database
config = load_config()

AeroDatabox = config['API']['Air_API'] #api key for flight data from rapitd api

def icao_airport_codes(engine):
    engine=connect_database(config)

    cities_df = pd.read_sql("cities", con=engine)

    list_for_df = []
    
    for _, city in cities_df.iterrows():
        latitude = city["latitude"]
        longitude = city["longitude"]
        city_id = city["city_id"]
    
        url = "https://aerodatabox.p.rapidapi.com/airports/search/location"
    
        querystring = {"lat":latitude,"lon":longitude,"radiusKm":"50","limit":"5","withFlightInfoOnly":"true"}
        headers = {
          "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com",
          "X-RapidAPI-Key": AeroDatabox #USE THE PROVIDED KEY
        }

        response = requests.get(url, headers=headers, params=querystring)
        
        for item in response.json()['items']:
            airports_data = {
            "city_id": city_id,
            "icao": item.get("icao", None),
            "municipality_name": item.get("municipalityName", None)
        }
            

        list_for_df.append(airports_data)
        
    airports_df = pd.DataFrame(list_for_df)

    return airports_df


def get_flight_data(icao_list):
    
    
    api_key = AeroDatabox

    berlin_timezone = timezone('Europe/Berlin')
    today = datetime.now(berlin_timezone).date()
    tomorrow = (today + timedelta(days=1))

    flight_items = []

    for icao in icao_list:
        # the api can only make 12 hour calls, therefore, 2 12 hour calls make a full day
        # using the nested lists below we can make a morning call and extract the data
        # then make an afternoon call and extract the data
        times = [["00:00","11:59"],
                 ["12:00","23:59"]]

        for time in times:
            
            url = f"https://aerodatabox.p.rapidapi.com/flights/airports/icao/{icao}/{tomorrow}T{time[0]}/{tomorrow}T{time[1]}"

            querystring = {"withLeg":"true",
                        "direction":"Arrival",
                        "withCancelled":"false",
                        "withCodeshared":"true",
                        "withCargo":"false",
                        "withPrivate":"false"}

            headers = {
              'x-rapidapi-host': "aerodatabox.p.rapidapi.com",
              'x-rapidapi-key': api_key
              }

            response = requests.get(url, headers=headers, params=querystring)

            flights_json = response.json()

            retrieval_time = datetime.now(berlin_timezone).strftime("%Y-%m-%d %H:%M:%S")

            for item in flights_json["arrivals"]:
                flight_item = {
                    "arrival_airport_icao": icao,
                    "departure_airport_icao": item["departure"]["airport"].get("icao", None),
                    "departure_airport_name": item["departure"]["airport"].get("name", None),
                    "scheduled_arrival_time": item["arrival"]["scheduledTime"].get("local", None),
                    "flight_number": item.get("number", None),
                    "data_retrieved_at": retrieval_time
                }

                flight_items.append(flight_item)

    flights_df = pd.DataFrame(flight_items)
    flights_df["scheduled_arrival_time"] = flights_df["scheduled_arrival_time"].str[:-6]
    flights_df["scheduled_arrival_time"] = pd.to_datetime(flights_df["scheduled_arrival_time"])
    flights_df["data_retrieved_at"] = pd.to_datetime(flights_df["data_retrieved_at"])

    return flights_df