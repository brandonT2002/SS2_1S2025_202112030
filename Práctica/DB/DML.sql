USE Aeropuerto;

-- Insertar pasajeros
INSERT INTO Pasajero (Nombre, Apellido, Genero, Edad, Nacionalidad) 
VALUES 
('Carlos', 'Ramírez', 'Masculino', 35, 'Guatemala'),
('María', 'Gómez', 'Femenino', 28, 'México'),
('Luis', 'Fernández', 'Masculino', 42, 'España');

-- Insertar fechas de salida
INSERT INTO FechaSalida (Fecha, Anio, Mes, Dia) 
VALUES 
('2025-03-10', 2025, 3, 10),
('2025-04-15', 2025, 4, 15),
('2025-05-20', 2025, 5, 20);

-- Insertar aeropuertos de salida
INSERT INTO AeropuertoSalida (NombreAeropuerto, CodigoPais, NombrePais, ContinenteAeropuerto, Continente) 
VALUES 
('Aeropuerto Internacional La Aurora', 'GT', 'Guatemala', 'América Central', 'América'),
('Aeropuerto Internacional Benito Juárez', 'MX', 'México', 'América del Norte', 'América'),
('Aeropuerto Internacional de Barajas', 'ES', 'España', 'Europa Occidental', 'Europa');

-- Insertar aeropuertos de llegada
INSERT INTO AeropuertoLlegada (NombreAeropuerto) 
VALUES 
('Aeropuerto Internacional John F. Kennedy'),
('Aeropuerto Internacional El Dorado'),
('Aeropuerto Internacional de Miami');

-- Insertar pilotos
INSERT INTO Piloto (NombrePiloto) 
VALUES 
('Juan Pérez'),
('Ana López'),
('Miguel Torres');

-- Insertar estados de vuelo
INSERT INTO EstadoVuelo (Estado) 
VALUES 
('En horario'),
('Retrasado'),
('Cancelado');

-- Insertar vuelos
INSERT INTO Vuelo (IdPasajero, IdFechaSalida, IdAeropuertoSalida, IdAeropuertoLlegada, IdPiloto, IdEstadoVuelo) 
VALUES 
(1, 1, 1, 1, 1, 1), 
(2, 2, 2, 2, 2, 2), 
(3, 3, 3, 3, 3, 3);
