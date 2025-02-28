USE Aeropuerto;

-- Eliminar las tablas si existen
DROP TABLE Aeropuertos;
DROP TABLE Pasajeros;
DROP TABLE Paises;
DROP TABLE Vuelos;
DROP TABLE Continentes;

-- Crear la tabla Continentes
CREATE TABLE Continentes (
    idContinente INT NOT NULL PRIMARY KEY,
    Nombre VARCHAR(45) NOT NULL
);

-- Crear la tabla Vuelos
CREATE TABLE Vuelos (
    idVuelo INT NOT NULL PRIMARY KEY,
    Piloto VARCHAR(45) NOT NULL,
    Estado VARCHAR(45) NOT NULL,
    FechaSalida DATE NOT NULL
);

-- Crear la tabla Paises
CREATE TABLE Paises (
    idPais INT NOT NULL PRIMARY KEY,
    Nombre VARCHAR(45) NOT NULL,
    Codigo VARCHAR(45) NOT NULL,
    Continentes_idContinente INT NOT NULL,
    CONSTRAINT fk_Paises_Continentes1 FOREIGN KEY (Continentes_idContinente)
        REFERENCES Continentes(idContinente)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);

-- Crear la tabla Pasajeros
CREATE TABLE Pasajeros (
    idPasajero VARCHAR(10) NOT NULL PRIMARY KEY,
    Nombre VARCHAR(45) NOT NULL,
    Apellido VARCHAR(45) NOT NULL,
    Sexo VARCHAR(45) NOT NULL,
    Edad INT NOT NULL,
    Vuelo_idVuelo INT NOT NULL,
    Paises_idPais INT NOT NULL,
    CONSTRAINT fk_Pasajero_Vuelo FOREIGN KEY (Vuelo_idVuelo)
        REFERENCES Vuelos(idVuelo)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT fk_Pasajeros_Paises1 FOREIGN KEY (Paises_idPais)
        REFERENCES Paises(idPais)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);

-- Crear la tabla Aeropuertos
CREATE TABLE Aeropuertos (
    idAeropuerto INT NOT NULL PRIMARY KEY,
    Nombre VARCHAR(45) NOT NULL,
    Paises_idPais INT NOT NULL,
    CONSTRAINT fk_Aeropuertos_Paises1 FOREIGN KEY (Paises_idPais)
        REFERENCES Paises(idPais)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);
