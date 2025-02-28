import pandas as pd
import pyodbc

# === EXTRACCIÓN DE DATOS ===
def extract_data(file_path):
    try:
        # Leer el archivo CSV
        df = pd.read_csv(file_path)
        print("Datos extraídos con éxito.")
        return df
    except Exception as e:
        print(f"Error al extraer los datos: {e}")
        return None

# === TRANSFORMACIÓN DE DATOS ===
def transform_data(df):
    try:
        df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()
        df = df.dropna()
        df = df.drop_duplicates()

        df['age'] = pd.to_numeric(df['age'], errors='coerce')
        df['departure_date'] = pd.to_datetime(df['departure_date'], errors='coerce')

        df = df.dropna(subset=['age', 'departure_date'])
        return df
    except Exception as e:
        print(f"Error al transformar los datos: {e}")
        return None

# === CONEXION DB ===
def connect_to_db():
    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost\\SQLEXPRESS;'
            'DATABASE=Aeropuerto;'
            'UID=root;'
            'PWD=root'
        )
        print("Conexión a la base de datos establecida.")
        return connection
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# === CARGA DE DATOS ===
def load_data_to_db(df, connection):
    try:
        cursor = connection.cursor()

        # Verificar si la tabla existe antes de crearla
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'Continentes') AND type in (N'U'))
            BEGIN
                CREATE TABLE Continentes (
                    idContinente INT IDENTITY(1,1) PRIMARY KEY,
                    Nombre VARCHAR(45) NOT NULL UNIQUE
                )
            END
        ''')
        connection.commit()

        # Insertar los datos de Continentes, evitando duplicados
        for continente in df['continents'].unique():
            cursor.execute('''
                IF NOT EXISTS (SELECT 1 FROM Continentes WHERE Nombre = ?)
                BEGIN
                    INSERT INTO Continentes (Nombre) VALUES (?)
                END
            ''', (continente, continente))
            connection.commit()
        print("Datos de los continentes cargados con éxito.")

        # Verificar si la tabla Vuelos existe antes de crearla
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'Vuelos') AND type in (N'U'))
            BEGIN
                CREATE TABLE Vuelos (
                    idVuelo INT IDENTITY(1,1) PRIMARY KEY,
                    Piloto VARCHAR(45) NOT NULL,
                    Estado VARCHAR(45) NOT NULL,
                    FechaSalida DATE NOT NULL
                )
            END
        ''')
        connection.commit()

        # Insertar los datos de los vuelos
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT INTO Vuelos (Piloto, Estado, FechaSalida) 
                VALUES (?, ?, ?)
            ''', (row['pilot_name'], row['flight_status'], row['departure_date']))
            connection.commit()

        print("Datos de los vuelos cargados con éxito.")

        # Verificar si la tabla Paises existe antes de crearla
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'Paises') AND type in (N'U'))
            BEGIN
                CREATE TABLE Paises (
                    idPais INT IDENTITY(1,1) PRIMARY KEY,
                    Nombre VARCHAR(45) NOT NULL,
                    Codigo VARCHAR(45) NOT NULL,
                    Continentes_idContinente INT NOT NULL,
                    CONSTRAINT fk_Paises_Continentes FOREIGN KEY (Continentes_idContinente)
                        REFERENCES Continentes(idContinente)
                        ON DELETE NO ACTION
                        ON UPDATE NO ACTION
                )
            END
        ''')
        connection.commit()

        # Insertar los datos de los países, asegurando la relación con Continentes
        for _, row in df[['country_name', 'airport_country_code', 'continents']].drop_duplicates().iterrows():
            # Obtener el id del continente correspondiente
            cursor.execute('SELECT idContinente FROM Continentes WHERE Nombre = ?', (row['continents'],))
            continente_id = cursor.fetchone()

            if continente_id:
                continente_id = continente_id[0]

                # Verificar si el país ya existe
                cursor.execute('SELECT 1 FROM Paises WHERE Nombre = ? AND Codigo = ?', (row['country_name'], row['airport_country_code']))
                exists = cursor.fetchone()

                if not exists:
                    # Insertar país en la tabla Paises
                    cursor.execute('''
                        INSERT INTO Paises (Nombre, Codigo, Continentes_idContinente) 
                        VALUES (?, ?, ?)
                    ''', (row['country_name'], row['airport_country_code'], continente_id))
                    connection.commit()

        print("Datos de los países cargados con éxito.")

        # Verificar si la tabla Pasajeros existe antes de crearla
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'Pasajeros') AND type in (N'U'))
            BEGIN
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
                    CONSTRAINT fk_Pasajeros_Paises FOREIGN KEY (Paises_idPais)
                        REFERENCES Paises(idPais)
                        ON DELETE NO ACTION
                        ON UPDATE NO ACTION
                )
            END
        ''')
        connection.commit()

        # Insertar los pasajeros en la base de datos
        for _, row in df.iterrows():
            # Obtener el idPais correspondiente al país del pasajero
            cursor.execute('SELECT idPais FROM Paises WHERE Nombre = ?', (row['country_name'],))
            pais_id = cursor.fetchone()

            # Obtener el idVuelo correspondiente al vuelo del pasajero
            cursor.execute('SELECT idVuelo FROM Vuelos WHERE Piloto = ? AND Estado = ? AND FechaSalida = ?',
                            (row['pilot_name'], row['flight_status'], row['departure_date']))
            vuelo_id = cursor.fetchone()

            if pais_id and vuelo_id:
                pais_id = pais_id[0]
                vuelo_id = vuelo_id[0]

                # Verificar si el pasajero ya existe
                cursor.execute('SELECT 1 FROM Pasajeros WHERE idPasajero = ?', (row['passenger_id'],))
                exists = cursor.fetchone()

                if not exists:
                    # Insertar pasajero en la tabla Pasajeros
                    cursor.execute('''
                        INSERT INTO Pasajeros (idPasajero, Nombre, Apellido, Sexo, Edad, Vuelo_idVuelo, Paises_idPais) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (row['passenger_id'], row['first_name'], row['last_name'], row['gender'], row['age'], vuelo_id, pais_id))
                    connection.commit()

        print("Datos de los pasajeros cargados con éxito.")

        # Verificar si la tabla Aeropuertos existe antes de crearla
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'Aeropuertos') AND type in (N'U'))
            BEGIN
                CREATE TABLE Aeropuertos (
                    idAeropuerto INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
                    Nombre VARCHAR(100) NOT NULL,
                    Paises_idPais INT NOT NULL,
                    CONSTRAINT fk_Aeropuertos_Paises FOREIGN KEY (Paises_idPais)
                        REFERENCES Paises(idPais)
                        ON DELETE NO ACTION
                        ON UPDATE NO ACTION
                )
            END
        ''')
        connection.commit()

        # Insertar los aeropuertos en la base de datos
        for _, row in df.iterrows():
            # Obtener el idPais correspondiente al país del aeropuerto
            cursor.execute('SELECT idPais FROM Paises WHERE Codigo = ?', (row['airport_country_code'],))
            pais_id = cursor.fetchone()

            if pais_id:
                pais_id = pais_id[0]

                # Verificar si el aeropuerto ya existe
                cursor.execute('SELECT 1 FROM Aeropuertos WHERE Nombre = ?', (row['airport_name'],))
                exists = cursor.fetchone()

                if not exists:
                    # Insertar aeropuerto en la tabla Aeropuertos
                    cursor.execute('''
                        INSERT INTO Aeropuertos (Nombre, Paises_idPais) 
                        VALUES (?, ?)
                    ''', (row['airport_name'], pais_id))
                    connection.commit()

        print("Datos de los aeropuertos cargados con éxito.")

    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        connection.rollback()

def run_etl(input_path):
    # Extracción de datos
    df = extract_data(input_path)
    if df is not None:
        # Transformación de datos
        df_transformed = transform_data(df)
        if df_transformed is not None:
            # Conectar a la base de datos
            connection = connect_to_db()
            if connection:
                # Cargar los datos en la base de datos
                load_data_to_db(df_transformed, connection)

if __name__ == "__main__":
    input_file_path = "./Data/VuelosDataSet.csv"
    run_etl(input_file_path)
