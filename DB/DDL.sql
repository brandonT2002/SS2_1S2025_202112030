USE Aeropuerto;

-- Eliminar las tablas si existen
DROP TABLE Vuelo;
DROP TABLE EstadoVuelo;
DROP TABLE Piloto;
DROP TABLE AeropuertoLlegada;
DROP TABLE AeropuertoSalida;
DROP TABLE FechaSalida;
DROP TABLE Pasajero;

CREATE TABLE Pasajero (
    IdPasajero INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(50),
    Apellido NVARCHAR(50),
    Genero NVARCHAR(10),
    Edad INT,
    Nacionalidad NVARCHAR(50)
);
GO

CREATE TABLE FechaSalida (
    IdFechaSalida INT IDENTITY(1,1) PRIMARY KEY,
    Fecha DATE,
    Anio INT,
    Mes INT,
    Dia INT
);
GO

CREATE TABLE AeropuertoSalida (
    IdAeropuertoSalida INT IDENTITY(1,1) PRIMARY KEY,
    NombreAeropuerto NVARCHAR(100),
    CodigoPais NVARCHAR(10),
    NombrePais NVARCHAR(50),
    ContinenteAeropuerto NVARCHAR(50),
    Continente NVARCHAR(50)
);
GO

CREATE TABLE AeropuertoLlegada (
    IdAeropuertoLlegada INT IDENTITY(1,1) PRIMARY KEY,
    NombreAeropuerto NVARCHAR(100)
);
GO

CREATE TABLE Piloto (
    IdPiloto INT IDENTITY(1,1) PRIMARY KEY,
    NombrePiloto NVARCHAR(100)
);
GO

CREATE TABLE EstadoVuelo (
    IdEstadoVuelo INT IDENTITY(1,1) PRIMARY KEY,
    Estado NVARCHAR(50)
);
GO

CREATE TABLE Vuelo (
    IdVuelo INT IDENTITY(1,1) PRIMARY KEY,
    IdPasajero INT,
    IdFechaSalida INT,
    IdAeropuertoSalida INT,
    IdAeropuertoLlegada INT,
    IdPiloto INT,
    IdEstadoVuelo INT,
    CONSTRAINT FK_Vuelo_Pasajero FOREIGN KEY (IdPasajero) 
        REFERENCES Pasajero(IdPasajero),
    CONSTRAINT FK_Vuelo_FechaSalida FOREIGN KEY (IdFechaSalida) 
        REFERENCES FechaSalida(IdFechaSalida),
    CONSTRAINT FK_Vuelo_AeropuertoSalida FOREIGN KEY (IdAeropuertoSalida) 
        REFERENCES AeropuertoSalida(IdAeropuertoSalida),
    CONSTRAINT FK_Vuelo_AeropuertoLlegada FOREIGN KEY (IdAeropuertoLlegada) 
        REFERENCES AeropuertoLlegada(IdAeropuertoLlegada),
    CONSTRAINT FK_Vuelo_Piloto FOREIGN KEY (IdPiloto) 
        REFERENCES Piloto(IdPiloto),
    CONSTRAINT FK_Vuelo_EstadoVuelo FOREIGN KEY (IdEstadoVuelo) 
        REFERENCES EstadoVuelo(IdEstadoVuelo)
);
GO