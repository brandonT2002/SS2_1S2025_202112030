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

def count_tables(connection):
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM Continentes")
    count_continentes = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Vuelos")
    count_vuelos = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Paises")
    count_paises = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Pasajeros")
    count_pasajeros = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Aeropuertos")
    count_aeropuertos = cursor.fetchone()[0]

    print(f"Continentes: {count_continentes}")
    print(f"Vuelos: {count_vuelos}")
    print(f"Paises: {count_paises}")
    print(f"Pasajeros: {count_pasajeros}")
    print(f"Aeropuertos: {count_aeropuertos}")

