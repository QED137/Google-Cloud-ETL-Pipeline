create DATABASE weatherDB;

use weatherDB;

CREATE TABLE if NOT EXISTS cities (
 city_id INT AUTO_INCREMENT PRIMARY KEY,
 city VARCHAR(100),
 country VARCHAR(100),
 latitude FLOAT,
 longitude FLOAT
 
);

SELECT * from cities;
ALTER TABLE cities
ADD CONSTRAINT unique_city UNIQUE (city);
SELECT * from cities;

-- DROP DATABASE weatherDB;
CREATE TABLE weather (
    weather_id INT AUTO_INCREMENT,
    city_id INT NOT NULL,
    forecast_time DATETIME,
    outlook VARCHAR(255),
    temperature FLOAT,
    rain_in_last_3h FLOAT,
    wind_speed FLOAT,
    rain_prob FLOAT,
    data_retrieved_at DATETIME,
    PRIMARY KEY (weather_id),
    FOREIGN KEY (city_id) REFERENCES cities(City_id)
);
SELECT * from weather;
CREATE TABLE airports(
    city_id INT NOT NULL,
    icao VARCHAR(10),
    municipality_name VARCHAR(255),
    PRIMARY KEY (icao),
    FOREIGN KEY (city_id) REFERENCES cities(City_id)
);
CREATE TABLE flights(
    flight_id INT AUTO_INCREMENT,
    arrival_airport_icao VARCHAR(10),
    departure_airport_icao VARCHAR(10),
    departure_airport_name VARCHAR(30),
    scheduled_arrival_time DATETIME,
    flight_number VARCHAR(30),
    data_retrieved_at DATETIME,
    PRIMARY KEY (flight_id),
    FOREIGN KEY (arrival_airport_icao) REFERENCES airports(icao)
);

SELECT * from flights;