-- Insertar Continentes
INSERT INTO Continentes (idContinente, Nombre) VALUES
(1, 'Asia'),
(2, 'Europa'),
(3, 'América'),
(4, 'África'),
(5, 'Oceanía'),
(6, 'Antártida');

-- Insertar Paises
INSERT INTO Paises (idPais, Nombre, Codigo, Continentes_idContinente) VALUES
(1, 'India', 'IN', 1),
(2, 'España', 'ES', 2),
(3, 'Estados Unidos', 'US', 3),
(4, 'Nigeria', 'NG', 4),
(5, 'Australia', 'AU', 5),
(6, 'Argentina', 'AR', 3),
(7, 'Francia', 'FR', 2);

-- Insertar Vuelos
INSERT INTO Vuelos (idVuelo, Piloto, Estado, FechaSalida) VALUES
(1, 'Carlos Rodríguez', 'En curso', '2025-03-10'),
(2, 'Ana Pérez', 'Completado', '2025-02-28'),
(3, 'Miguel Sánchez', 'Cancelado', '2025-03-05'),
(4, 'Laura Gómez', 'En espera', '2025-03-15');

-- Insertar Pasajeros
INSERT INTO Pasajeros (idPasajero, Nombre, Apellido, Sexo, Edad, Vuelo_idVuelo, Paises_idPais) VALUES
('A001', 'Juan', 'Gómez', 'Masculino', 30, 1, 1),
('A002', 'María', 'Martínez', 'Femenino', 25, 2, 2),
('A003', 'Pedro', 'Lopez', 'Masculino', 35, 3, 3),
('A004', 'Sofía', 'Fernández', 'Femenino', 28, 4, 4),
('A005', 'Lucas', 'Rodríguez', 'Masculino', 40, 1, 5);

-- Insertar Aeropuertos
INSERT INTO Aeropuertos (idAeropuerto, Nombre, Paises_idPais) VALUES
(1, 'Aeropuerto Internacional Indira Gandhi', 1),
(2, 'Aeropuerto Adolfo Suárez Madrid-Barajas', 2),
(3, 'Aeropuerto Internacional de Los Ángeles', 3),
(4, 'Aeropuerto Internacional de Nnamdi Azikiwe', 4),
(5, 'Aeropuerto Internacional de Sydney', 5);
