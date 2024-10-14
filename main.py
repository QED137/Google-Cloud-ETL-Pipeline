# main.py
from data.cities import cities_data
from db.push_to_database import push_to_database
from db.retrieve_from_db import retrieve_from_db
from db.database import load_config, connect_database, connectiontwo
from data.weather import get_weather_data
from data.flight import icao_airport_codes, get_flight_data



def main():
    # 1. Load the config from the database.py module
    config = load_config()

    # 2. Set up the database connection using the config
    #engine = connect_database(config) #engine for local database
    engineTwo=connectiontwo() #engine for cloud
    API_key = config['API']['api_key']

    if engineTwo:
        # 3. Define the list of cities to fetch data for
        #city_list = ['Berlin', 'Hamburg', 'Munich']

        # 4. Fetch city data from Wikipedia using cities_data
        #city_df = cities_data(city_list)
        #print(f"City data: \n{city_df}")

        # # 5. Push city data into the database
        # #push_to_database(city_df, 'cities', engine)

        # # 6. Retrieve city data from the database
        #cities_from_db = retrieve_from_db('cities', engine)
        #print(f"Cities from DB: \n{cities_from_db}")

        # # 7. Fetch weather data using the retrieved city data from the DB
        # api_key = config['API']['api_key']
        #weather_df = get_weather_data(API_key,cities_from_db)
        #print(f"Weather data: \n{weather_df}")
        #air_df =icao_airport_codes()
        #print(air_df)
        
        #push_to_database(air_df, 'airports', engine)
        #air_from_DB=retrieve_from_db('airports', engine)
        #print(air_from_DB)
        # icao_list = ["EDDB", "EDDH"] #  one can also fetch the data for icao code form database
        # flights_to_db = get_flight_data(icao_list)
        
        # #write flight information to the database 
        # push_to_database(flights_to_db, 'flights', engine)
        
        '''
        This section pushes the weather data to a new database hosted on the cloud.
        We will use the `push_to_database` function, passing the new connection details (password and IP) 
        for the cloud database.

        The following line establishes a connection to the second MySQL Workbench database on the cloud:
        '''
         # This is the second function for connecting to the cloud-based MySQL database.
        
        # find the city data form web scrapping 
        city_list = ['Berlin', 'Hamburg', 'Munich']
        
        #city_df = cities_data(city_list)
        
        # now push city data to cloud database 
        #push_to_database(city_df, 'cities', engineTwo)
        
        #retrieve city data from city database 
        cities_from_db = retrieve_from_db('cities', engineTwo)
        
        #call icao function for fetching icao data from api 
        air_df =icao_airport_codes(engineTwo)
        
        #print(cities_from_db)
        
        #print(air_df)
        
         
        # The following function call pushes the weather data to the new database created on the cloud:
        
        #push_to_database(air_df, 'airports', engineTwo)
        #to check the push function is working good
        db_from_cloud=retrieve_from_db('airports', engineTwo)
        
        #get flisght information 
        flights_to_db = get_flight_data(db_from_cloud['icao'])
        #pushing flight information to db
        push_to_database(flights_to_db,'flights', engineTwo)
        retrieve_flight_from_db=retrieve_from_db('flights', engineTwo)
        
        print(retrieve_flight_from_db)
        
        

        
        
        
        
    else:
        print("Could not connect to the database.")
    #-------------------------------------------------------------
    

if __name__ == "__main__":
    main()
