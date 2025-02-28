USE Aeropuerto;

-- Tabla de Continentes
CREATE TABLE Continent (
    ContinentID INT PRIMARY KEY IDENTITY,
    ContinentName VARCHAR(100)
);

-- Tabla de Aeropuertos
CREATE TABLE Airport (
    AirportID INT PRIMARY KEY IDENTITY,
    AirportName VARCHAR(100),
    CountryCode VARCHAR(5),
    CountryName VARCHAR(100),
    ContinentID INT,
    FOREIGN KEY (ContinentID) REFERENCES Continent(ContinentID)
);

-- Tabla de Pasajeros
CREATE TABLE Passenger (
    PassengerID VARCHAR(50) PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Gender VARCHAR(10),
    Age INT,
    Nationality VARCHAR(50)
);

-- Tabla de Vuelos
CREATE TABLE Flight (
    FlightID INT PRIMARY KEY IDENTITY,
    DepartureDate DATE,
    ArrivalAirport VARCHAR(100),
    PilotName VARCHAR(100),
    FlightStatus VARCHAR(20),
    PassengerID VARCHAR(50),
    AirportID INT,
    FOREIGN KEY (PassengerID) REFERENCES Passenger(PassengerID),
    FOREIGN KEY (AirportID) REFERENCES Airport(AirportID)
);
