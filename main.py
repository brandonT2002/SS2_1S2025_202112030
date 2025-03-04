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
        df = df.dropna(subset=['passenger_id', 'first_name', 'last_name', 'gender', 'age', 'departure_date', 'country_name'])

        df['age'] = pd.to_numeric(df['age'], errors='coerce')
        df['departure_date'] = pd.to_datetime(df['departure_date'], errors='coerce')

        df = df.dropna(subset=['age', 'departure_date'])
        df = df.drop_duplicates()

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
        cursor.fast_executemany = True  # Habilitar fast_executemany para inserciones masivas

        # === CONTINENTES ===
        continentes_unicos = df['continents'].unique()
        valores = [(continente,) for continente in continentes_unicos]

        cursor.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'Continentes') AND type in (N'U'))
                            BEGIN CREATE TABLE Continentes (
                                idContinente INT IDENTITY(1,1) PRIMARY KEY,
                                Nombre VARCHAR(45) NOT NULL UNIQUE
                            ) END''')
        connection.commit()

        cursor.executemany('''INSERT INTO Continentes (Nombre) VALUES (?)''', valores)
        connection.commit()
        print("Datos de los continentes cargados con éxito.")

        # === VUELOS ===
        datos_vuelos = [(row['pilot_name'], row['flight_status'], row['departure_date']) for _, row in df.iterrows()]

        cursor.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'Vuelos') AND type in (N'U'))
                            BEGIN CREATE TABLE Vuelos (
                                idVuelo INT IDENTITY(1,1) PRIMARY KEY,
                                Piloto VARCHAR(45) NOT NULL,
                                Estado VARCHAR(45) NOT NULL,
                                FechaSalida DATE NOT NULL
                            ) END''')
        connection.commit()

        cursor.executemany('''INSERT INTO Vuelos (Piloto, Estado, FechaSalida) VALUES (?, ?, ?)''', datos_vuelos)
        connection.commit()
        print("Datos de los vuelos cargados con éxito.")

        # === PAISES ===
        datos_paises = df[['country_name', 'airport_country_code', 'continents']].drop_duplicates()

        # Obtener id de continentes solo una vez
        cursor.execute('SELECT idContinente, Nombre FROM Continentes')
        continentes_dict = {row[1]: row[0] for row in cursor.fetchall()}

        datos_paises = [
            (row['country_name'], row['airport_country_code'], continentes_dict.get(row['continents'], None))
            for _, row in datos_paises.iterrows() if row['continents'] in continentes_dict
        ]

        cursor.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'Paises') AND type in (N'U'))
                            BEGIN CREATE TABLE Paises (
                                idPais INT IDENTITY(1,1) PRIMARY KEY,
                                Nombre VARCHAR(45) NOT NULL,
                                Codigo VARCHAR(45) NOT NULL,
                                Continentes_idContinente INT NOT NULL,
                                CONSTRAINT fk_Paises_Continentes FOREIGN KEY (Continentes_idContinente)
                                    REFERENCES Continentes(idContinente)
                                    ON DELETE NO ACTION
                                    ON UPDATE NO ACTION
                            ) END''')
        connection.commit()

        cursor.executemany('''INSERT INTO Paises (Nombre, Codigo, Continentes_idContinente) VALUES (?, ?, ?)''', datos_paises)
        connection.commit()
        print("Datos de los países cargados con éxito.")

        # === PASAJEROS ===
        data_to_insert = []

        for _, row in df.iterrows():
            # Buscar id del país
            cursor.execute('SELECT idPais FROM Paises WHERE TRIM(Nombre) = TRIM(?)', (row['country_name'],))
            pais_id = cursor.fetchone()

            # Buscar id del vuelo
            cursor.execute('''SELECT idVuelo FROM Vuelos 
                            WHERE TRIM(Piloto) = TRIM(?) 
                            AND Estado = ? 
                            AND FechaSalida = ?''',
                        (row['pilot_name'], row['flight_status'], row['departure_date']))
            vuelo_id = cursor.fetchone()

            if pais_id and vuelo_id:
                data_to_insert.append((
                    row['passenger_id'], row['first_name'], row['last_name'], 
                    row['gender'], row['age'], vuelo_id[0], pais_id[0]
                ))
            else:
                print(f"⚠️ No se encontró país o vuelo para: {row['country_name']} - {row['pilot_name']} ({row['departure_date']})")

        # Insertar en la base de datos si hay datos válidos
        if data_to_insert:
            print(f"Insertando {len(data_to_insert)} registros...")
            cursor.executemany('''INSERT INTO Pasajeros 
                                (idPasajero, Nombre, Apellido, Sexo, Edad, Vuelo_idVuelo, Paises_idPais)
                                VALUES (?, ?, ?, ?, ?, ?, ?)''', data_to_insert)
            connection.commit()
            print("✅ Datos insertados correctamente.")
        else:
            print("❌ No hay datos válidos para insertar.")

        # === AEROPUERTOS ===
        cursor.execute('SELECT idPais, Codigo FROM Paises')
        paises_dict = {row[1]: row[0] for row in cursor.fetchall()}

        data_to_insert = []
        for _, row in df.iterrows():
            pais_id = paises_dict.get(row['airport_country_code'])
            if pais_id:
                data_to_insert.append((row['airport_name'], pais_id))

        if data_to_insert:
            cursor.executemany('''INSERT INTO Aeropuertos (Nombre, Paises_idPais) VALUES (?, ?)''', data_to_insert)
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