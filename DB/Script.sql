CREATE DATABASE Aeropuerto;

USE Aeropuerto;

CREATE TABLE Passengers (
    passenger_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    gender VARCHAR(10),
    age INT,
    nationality VARCHAR(50)
);

CREATE TABLE Airports (
    airport_id VARCHAR(50) PRIMARY KEY,
    airport_name VARCHAR(100),
    country_code CHAR(2),
    country_name VARCHAR(100),
    continent VARCHAR(50)
);

CREATE TABLE Flights (
    flight_id VARCHAR(50) PRIMARY KEY,
    departure_date DATETIME,
    arrival_airport VARCHAR(50),
    pilot_name VARCHAR(100),
    flight_status VARCHAR(20),
    FOREIGN KEY (arrival_airport) REFERENCES Airports(airport_id)
);

CREATE TABLE Passenger_Flights (
    passenger_id VARCHAR(50),
    flight_id VARCHAR(50),
    PRIMARY KEY (passenger_id, flight_id),
    FOREIGN KEY (passenger_id) REFERENCES Passengers(passenger_id),
    FOREIGN KEY (flight_id) REFERENCES Flights(flight_id)
);
