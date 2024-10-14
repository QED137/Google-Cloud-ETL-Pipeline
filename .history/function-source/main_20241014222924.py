import functions_framework
import pandas as pd
import sqlalchemy
from keys import cloud_db_pass, Api_key, HO  # private module
from pytz import timezone
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine.base import Engine
import requests

def connection():
    schema = "google_cloud_DB"
    host = "34.76.110.104"
    user = "root"
    password = cloud_db_pass
    port = 3306
    connect_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{schema}"
    try:
        engine = create_engine(connect_string)
        print("Database connection successful.")
    except SQLAlchemyError as e:
        raise ValueError(f"Database connection failed: {e}")

    return engine

def retrieve_from_db(table: str, engine) -> pd.DataFrame:
    """
    Retrieve data from the database.
    
    Args:
        table (str): The name of the table to retrieve data from.
        engine (Engine): The SQLAlchemy engine to use for the database connection.
    
    Returns:
        pd.DataFrame: The data retrieved from the database.
    """
    try:
        with engine.begin() as conn:
            df = pd.read_sql(f"SELECT * FROM {table}", con=conn)
        return df
    except SQLAlchemyError as e:
        print(f"Error while retrieving data from {table}: {e}")
    return pd.DataFrame()

def push_to_database(df: pd.DataFrame, table: str, engine):
    """
    Push DataFrame to the database table.
    
    Args:
        df (DataFrame): The DataFrame to push to the database.
        table (str): The table name in the database.
        engine (Engine): The SQLAlchemy engine to use for the database connection.
    
    Returns:
        None
    """
    try:
        with engine.begin() as conn:
            df.to_sql(table, con=conn, if_exists='append', index=False)
        print(f"Data successfully pushed to {table} table.")
    except SQLAlchemyError as e:
        print(f"Error while pushing data to the database: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

@functions_framework.http
def get_weather(request):
    """HTTP Cloud Function.
    
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    engine = connection()
    #retrieving data from the database 
    cities_df = retrieve_from_db('cities', engine)
    berlin_timezone = timezone('Europe/Berlin')
    api_key = Api_key

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

    push_to_database(weather_df, 'weather', engine)

    return "Data has been written into cloud database"
