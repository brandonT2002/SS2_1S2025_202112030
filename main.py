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

        # === CONTINENTES ===
        continentes_unicos = df['continents'].unique()
        valores = ",".join([f"('{continente}')" for continente in continentes_unicos])

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

        cursor.execute(f'''
            INSERT INTO Continentes (Nombre)
            SELECT DISTINCT temp.continente
            FROM (VALUES {valores}) AS temp(continente)
            WHERE NOT EXISTS (SELECT 1 FROM Continentes WHERE Nombre = temp.continente)
        ''')
        connection.commit()
        print("Datos de los continentes cargados con éxito.")

        # === VUELOS ===
        datos_vuelos = [(row['pilot_name'], row['flight_status'], row['departure_date']) for _, row in df.iterrows()]
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

        cursor.executemany('''
            INSERT INTO Vuelos (Piloto, Estado, FechaSalida)
            VALUES (?, ?, ?)
        ''', datos_vuelos)

        connection.commit()
        print("Datos de los vuelos cargados con éxito.")

        # === PAISES ===
        datos_paises = df[['country_name', 'airport_country_code', 'continents']].drop_duplicates()

        cursor.execute('SELECT idContinente, Nombre FROM Continentes')
        continentes_dict = {row[1]: row[0] for row in cursor.fetchall()}

        datos_paises = [
            (row['country_name'], row['airport_country_code'], continentes_dict.get(row['continents'], None))
            for _, row in datos_paises.iterrows() if row['continents'] in continentes_dict
        ]

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

        cursor.executemany('''
            INSERT INTO Paises (Nombre, Codigo, Continentes_idContinente)
            SELECT ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM Paises WHERE Nombre = ? AND Codigo = ?
            )
        ''', [(pais[0], pais[1], pais[2], pais[0], pais[1]) for pais in datos_paises])

        connection.commit()
        print("Datos de los países cargados con éxito.")

        # === PASAJEROS ===
        cursor.execute('''
            IF OBJECT_ID('tempdb..#TempPasajeros') IS NOT NULL DROP TABLE #TempPasajeros;
            CREATE TABLE #TempPasajeros (
                idPasajero VARCHAR(10),
                Nombre VARCHAR(45),
                Apellido VARCHAR(45),
                Sexo VARCHAR(45),
                Edad INT,
                Vuelo_idVuelo INT,
                Paises_idPais INT
            )
        ''')
        connection.commit()

        data_to_insert = []
        for _, row in df.iterrows():
            cursor.execute('SELECT idPais FROM Paises WHERE Nombre = ?', (row['country_name'],))
            pais_id = cursor.fetchone()

            cursor.execute('SELECT idVuelo FROM Vuelos WHERE Piloto = ? AND Estado = ? AND FechaSalida = ?',
                            (row['pilot_name'], row['flight_status'], row['departure_date']))
            vuelo_id = cursor.fetchone()

            if pais_id and vuelo_id:
                pais_id = pais_id[0]
                vuelo_id = vuelo_id[0]
                data_to_insert.append((row['passenger_id'], row['first_name'], row['last_name'], row['gender'], row['age'], vuelo_id, pais_id))

        if data_to_insert:
            cursor.executemany('INSERT INTO #TempPasajeros (idPasajero, Nombre, Apellido, Sexo, Edad, Vuelo_idVuelo, Paises_idPais) VALUES (?, ?, ?, ?, ?, ?, ?)', data_to_insert)
            connection.commit()

        cursor.execute('''
            MERGE INTO Pasajeros AS target
            USING #TempPasajeros AS source
            ON target.idPasajero = source.idPasajero
            WHEN NOT MATCHED THEN
                INSERT (idPasajero, Nombre, Apellido, Sexo, Edad, Vuelo_idVuelo, Paises_idPais)
                VALUES (source.idPasajero, source.Nombre, source.Apellido, source.Sexo, source.Edad, source.Vuelo_idVuelo, source.Paises_idPais);
        ''')
        connection.commit()

        cursor.execute('DROP TABLE #TempPasajeros')
        connection.commit()

        print("Datos de los pasajeros cargados con éxito.")

        # === AEROPUERTOS ===
        cursor.execute('''
            IF OBJECT_ID('tempdb..#TempAeropuertos') IS NOT NULL DROP TABLE #TempAeropuertos;
            CREATE TABLE #TempAeropuertos (
                Nombre VARCHAR(100),
                Paises_idPais INT
            )
        ''')
        connection.commit()

        data_to_insert = []
        for _, row in df.iterrows():
            cursor.execute('SELECT idPais FROM Paises WHERE Codigo = ?', (row['airport_country_code'],))
            pais_id = cursor.fetchone()

            if pais_id:
                pais_id = pais_id[0]
                data_to_insert.append((row['airport_name'], pais_id))

        if data_to_insert:
            cursor.executemany('INSERT INTO #TempAeropuertos (Nombre, Paises_idPais) VALUES (?, ?)', data_to_insert)
            connection.commit()

        cursor.execute('''
            MERGE INTO Aeropuertos AS target
            USING #TempAeropuertos AS source
            ON target.Nombre = source.Nombre
            WHEN NOT MATCHED THEN
                INSERT (Nombre, Paises_idPais)
                VALUES (source.Nombre, source.Paises_idPais);
        ''')
        connection.commit()

        # Limpiar la tabla temporal
        cursor.execute('DROP TABLE #TempAeropuertos')
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