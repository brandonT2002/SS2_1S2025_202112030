def delete_model(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS Vuelo;")
        cursor.execute("DROP TABLE IF EXISTS EstadoVuelo;")
        cursor.execute("DROP TABLE IF EXISTS Piloto;")
        cursor.execute("DROP TABLE IF EXISTS AeropuertoLlegada;")
        cursor.execute("DROP TABLE IF EXISTS AeropuertoSalida;")
        cursor.execute("DROP TABLE IF EXISTS FechaSalida;")
        cursor.execute("DROP TABLE IF EXISTS Pasajero;")

        connection.commit()
        cursor.close()
        print("✅ Modelo eliminado.")
    
    except Exception as e:
        print(f"❌ Error al eliminar el modelo: {e}")

def create_model(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("USE Aeropuerto")

        cursor.execute("DROP TABLE IF EXISTS Vuelo;")
        cursor.execute("DROP TABLE IF EXISTS EstadoVuelo;")
        cursor.execute("DROP TABLE IF EXISTS Piloto;")
        cursor.execute("DROP TABLE IF EXISTS AeropuertoLlegada;")
        cursor.execute("DROP TABLE IF EXISTS AeropuertoSalida;")
        cursor.execute("DROP TABLE IF EXISTS FechaSalida;")
        cursor.execute("DROP TABLE IF EXISTS Pasajero;")

        cursor.execute("""
            CREATE TABLE Pasajero (
                IdPasajero VARCHAR(50) PRIMARY KEY,
                Nombre NVARCHAR(50),
                Apellido NVARCHAR(50),
                Genero NVARCHAR(10),
                Edad INT,
                Nacionalidad NVARCHAR(50)
            );
        """)

        cursor.execute("""
            CREATE TABLE FechaSalida (
                IdFechaSalida INT IDENTITY(1,1) PRIMARY KEY,
                Fecha DATE,
                Anio INT,
                Mes INT,
                Dia INT
            );
        """)

        cursor.execute("""
            CREATE TABLE AeropuertoSalida (
                IdAeropuertoSalida INT IDENTITY(1,1) PRIMARY KEY,
                NombreAeropuerto NVARCHAR(100),
                CodigoPais NVARCHAR(10),
                NombrePais NVARCHAR(50),
                ContinenteAeropuerto NVARCHAR(50),
                Continente NVARCHAR(50)
            );
        """)

        cursor.execute("""
            CREATE TABLE AeropuertoLlegada (
                IdAeropuertoLlegada INT IDENTITY(1,1) PRIMARY KEY,
                NombreAeropuerto NVARCHAR(100)
            );
        """)

        cursor.execute("""
            CREATE TABLE Piloto (
                IdPiloto INT IDENTITY(1,1) PRIMARY KEY,
                NombrePiloto NVARCHAR(100)
            );
        """)

        cursor.execute("""
            CREATE TABLE EstadoVuelo (
                IdEstadoVuelo INT IDENTITY(1,1) PRIMARY KEY,
                Estado NVARCHAR(50)
            );
        """)

        cursor.execute("""
            CREATE TABLE Vuelo (
                IdVuelo INT IDENTITY(1,1) PRIMARY KEY,
                IdPasajero VARCHAR(50),
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
        """)

        # Confirmar la transacción
        connection.commit()

        # Cerrar cursor
        cursor.close()
        
        print("✅ Modelo creado.")
    
    except Exception as e:
        print(f"❌ Error al crear el modelo: {e}")

def queries(connection):
    cursor = connection.cursor()

    # Consultas iniciales
    cursor.execute("SELECT COUNT(*) FROM Pasajero;")
    pasajeros = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM FechaSalida;")
    fechas = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM AeropuertoSalida;")
    aeropuertoS = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM AeropuertoLlegada;")
    aeropuertoL = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Piloto;")
    pilotos = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM EstadoVuelo;")
    estados = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Vuelo;")
    vuelos = cursor.fetchone()[0]

    # Consulta para obtener los pasajeros por género
    cursor.execute("""
        SELECT 
            Genero,
            COUNT(*) AS TotalPasajeros
        FROM Pasajero
        WHERE Genero IN ('Male', 'Female')
        GROUP BY Genero;
    """)
    results = cursor.fetchall()

    print(f"Pasajeros: {pasajeros}")
    print(f"Fechas de Salida: {fechas}")
    print(f"Aeropuertos Salida: {aeropuertoS}")
    print(f"Aeropuertos Llegada: {aeropuertoL}")
    print(f"Pilotos: {pilotos}")
    print(f"Estados: {estados}")
    print(f"Vuelos: {vuelos}")
    
    for result in results:
        genero = result[0]
        usuarios = result[1]
        porcentaje = (usuarios / pasajeros) * 100
        print(f"{genero}: {porcentaje:.2f}%")

    # Consulta: Nacionalidades con su mes/año de mayor fecha de salida
    cursor.execute("""
        SELECT 
            P.Nacionalidad, 
            YEAR(FS.Fecha) AS Anio, 
            MONTH(FS.Fecha) AS Mes,
            COUNT(*) AS Vuelos
        FROM Vuelo V
        JOIN Pasajero P ON V.IdPasajero = P.IdPasajero
        JOIN FechaSalida FS ON V.IdFechaSalida = FS.IdFechaSalida
        GROUP BY P.Nacionalidad, YEAR(FS.Fecha), MONTH(FS.Fecha)
        ORDER BY P.Nacionalidad, Anio, Mes;
    """)
    nacionalidades = cursor.fetchall()
    print("\nNacionalidades con su mes/año de mayor fecha de salida:")
    for row in nacionalidades:
        print(f"Nacionalidad: {row[0]}, Año: {row[1]}, Mes: {row[2]}, Vuelos: {row[3]}")

    # Consulta: COUNT de vuelos por país
    cursor.execute("""
        SELECT 
            A.NombrePais, 
            COUNT(*) AS Vuelos
        FROM Vuelo V
        JOIN AeropuertoSalida A ON V.IdAeropuertoSalida = A.IdAeropuertoSalida
        GROUP BY A.NombrePais;
    """)
    vuelos_por_pais = cursor.fetchall()
    print("\nVuelos por país:")
    for row in vuelos_por_pais:
        print(f"País: {row[0]}, Vuelos: {row[1]}")

    # Consulta: Top 5 aeropuertos con mayor número de pasajeros
    cursor.execute("""
        SELECT TOP 5 
            A.NombreAeropuerto, 
            COUNT(DISTINCT V.IdPasajero) AS Pasajeros
        FROM Vuelo V
        JOIN AeropuertoSalida A ON V.IdAeropuertoSalida = A.IdAeropuertoSalida
        GROUP BY A.NombreAeropuerto
        ORDER BY Pasajeros DESC;
    """)
    aeropuertos_top5 = cursor.fetchall()
    print("\nTop 5 aeropuertos con mayor número de pasajeros:")
    for row in aeropuertos_top5:
        print(f"Aeropuerto: {row[0]}, Pasajeros: {row[1]}")

    # Consulta: COUNT de vuelos dividido por estado de vuelo
    cursor.execute("""
        SELECT 
            EV.Estado, 
            COUNT(*) AS Vuelos
        FROM Vuelo V
        JOIN EstadoVuelo EV ON V.IdEstadoVuelo = EV.IdEstadoVuelo
        GROUP BY EV.Estado;
    """)
    vuelos_por_estado = cursor.fetchall()
    print("\nVuelos por estado de vuelo:")
    for row in vuelos_por_estado:
        print(f"Estado: {row[0]}, Vuelos: {row[1]}")

    # Consulta: Top 5 de los países más visitados
    cursor.execute("""
        SELECT TOP 5
            A.NombrePais,
            COUNT(DISTINCT V.IdPasajero) AS Pasajeros
        FROM Vuelo V
        JOIN AeropuertoLlegada AL ON V.IdAeropuertoLlegada = AL.IdAeropuertoLlegada
        JOIN AeropuertoSalida A ON V.IdAeropuertoSalida = A.IdAeropuertoSalida
        GROUP BY A.NombrePais
        ORDER BY Pasajeros DESC;
    """)
    paises_top5 = cursor.fetchall()
    print("\nTop 5 de los países más visitados:")
    for row in paises_top5:
        print(f"País: {row[0]}, Pasajeros: {row[1]}")

    # Consulta: Top 5 de los continentes más visitados
    cursor.execute("""
        SELECT TOP 5
            A.Continente, 
            COUNT(DISTINCT V.IdPasajero) AS Pasajeros
        FROM Vuelo V
        JOIN AeropuertoLlegada AL ON V.IdAeropuertoLlegada = AL.IdAeropuertoLlegada
        JOIN AeropuertoSalida A ON V.IdAeropuertoSalida = A.IdAeropuertoSalida
        GROUP BY A.Continente
        ORDER BY Pasajeros DESC;
    """)
    continentes_top5 = cursor.fetchall()
    print("\nTop 5 de los continentes más visitados:")
    for row in continentes_top5:
        print(f"Continente: {row[0]}, Pasajeros: {row[1]}")

    # Consulta: Top 5 de edades dividido por género que más viajan
    cursor.execute("""
        SELECT TOP 5
            P.Genero,
            P.Edad,
            COUNT(*) AS Vuelos
        FROM Vuelo V
        JOIN Pasajero P ON V.IdPasajero = P.IdPasajero
        GROUP BY P.Genero, P.Edad
        ORDER BY Vuelos DESC;
    """)
    edades_top5 = cursor.fetchall()
    print("\nTop 5 de edades dividido por género que más viajan:")
    for row in edades_top5:
        print(f"Género: {row[0]}, Edad: {row[1]}, Vuelos: {row[2]}")

    # Consulta: COUNT de vuelos por MM-YYYY
    cursor.execute("""
        SELECT 
            FORMAT(FS.Fecha, 'MM-yyyy') AS MesAnio,
            COUNT(*) AS Vuelos
        FROM Vuelo V
        JOIN FechaSalida FS ON V.IdFechaSalida = FS.IdFechaSalida
        GROUP BY FORMAT(FS.Fecha, 'MM-yyyy')
        ORDER BY MesAnio;
    """)
    vuelos_por_mesanio = cursor.fetchall()
    print("\nVuelos por Mes/Año:")
    for row in vuelos_por_mesanio:
        print(f"Mes/Año: {row[0]}, Vuelos: {row[1]}")
