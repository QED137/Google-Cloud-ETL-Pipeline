# data/weather.py
import requests
import pandas as pd
from pytz import timezone
from datetime import datetime
from db.database import connect_database, load_config
load_config()

def get_weather_data(api_key, cities_df):
    berlin_timezone = timezone('Europe/Berlin')

    weather_items = []
    for _, city in cities_df.iterrows():
        latitude = city["latitude"]
        longitude = city["longitude"]
        city_id = city["city_id"]

        url = (f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}&units=metric")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve data for city {city['city']}: {e}")
            continue

        weather_data = response.json() 
        retrieval_time = datetime.now(berlin_timezone).strftime("%Y-%m-%d %H:%M:%S")

        for item in weather_data["list"]:
            weather_item = {
                "city_id": city_id,
                "forecast_time": item.get("dt_txt", None),
                "outlook": item["weather"][0].get("description", None),
                "temperature": item["main"].get("temp", None),
                "rain_in_last_3h": item.get("rain", {}).get("3h", 0),
                "wind_speed": item["wind"].get("speed", None),
                "rain_prob": item.get("pop", None),
                "data_retrieved_at": retrieval_time
            }
            weather_items.append(weather_item)

    weather_df = pd.DataFrame(weather_items)
    weather_df["forecast_time"] = pd.to_datetime(weather_df["forecast_time"])
    weather_df["data_retrieved_at"] = pd.to_datetime(weather_df["data_retrieved_at"])

    return weather_df
