import pandas as pd

# === CARGA DE DATOS ===
def load_data_to_db(df, connection):
    try:
        cursor = connection.cursor()
        cursor.fast_executemany = True

        # === CONTINENTES ===
        df = df.dropna(subset=['continents'])  # Filtrar nulos en columna clave
        continentes_unicos = df['continents'].unique()
        valores = [(continente,) for continente in continentes_unicos]

        cursor.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'Continentes') AND type in (N'U'))
                            BEGIN CREATE TABLE Continentes (
                                idContinente INT IDENTITY(1,1) PRIMARY KEY,
                                Nombre VARCHAR(45) NOT NULL UNIQUE
                            ) END''')
        connection.commit()

        if valores:
            cursor.executemany('''INSERT INTO Continentes (Nombre) VALUES (?)''', valores)
            connection.commit()
            print("✅ Datos de los continentes cargados con éxito.")

        # === VUELOS ===
        df_vuelos = df.dropna(subset=['pilot_name', 'flight_status', 'departure_date'])
        datos_vuelos = [(row['pilot_name'], row['flight_status'], row['departure_date']) 
                        for _, row in df_vuelos.iterrows()]

        cursor.execute('''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'Vuelos') AND type in (N'U'))
                            BEGIN CREATE TABLE Vuelos (
                                idVuelo INT IDENTITY(1,1) PRIMARY KEY,
                                Piloto VARCHAR(45) NOT NULL,
                                Estado VARCHAR(45) NOT NULL,
                                FechaSalida DATE NOT NULL
                            ) END''')
        connection.commit()

        if datos_vuelos:
            cursor.executemany('''INSERT INTO Vuelos (Piloto, Estado, FechaSalida) VALUES (?, ?, ?)''', datos_vuelos)
            connection.commit()
            print("✅ Datos de los vuelos cargados con éxito.")

        # === PAISES ===
        df_paises = df.dropna(subset=['country_name', 'airport_country_code', 'continents']).drop_duplicates()
        
        cursor.execute('SELECT idContinente, Nombre FROM Continentes')
        continentes_dict = {row[1]: row[0] for row in cursor.fetchall()}

        datos_paises = [
            (row['country_name'], row['airport_country_code'], continentes_dict.get(row['continents']))
            for _, row in df_paises.iterrows() if row['continents'] in continentes_dict
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

        if datos_paises:
            cursor.executemany('''INSERT INTO Paises (Nombre, Codigo, Continentes_idContinente) VALUES (?, ?, ?)''', datos_paises)
            connection.commit()
            print("✅ Datos de los países cargados con éxito.")

        # === PASAJEROS ===
        data_to_insert = []

        for _, row in df.iterrows():
            if pd.isnull(row[['passenger_id', 'first_name', 'last_name', 'gender', 'age', 'country_name', 'pilot_name', 'flight_status', 'departure_date']]).any():
                continue  # Saltar filas con valores nulos en campos clave

            cursor.execute('SELECT idPais FROM Paises WHERE TRIM(Nombre) = TRIM(?)', (row['country_name'],))
            pais_id = cursor.fetchone()

            cursor.execute('''SELECT idVuelo FROM Vuelos 
                            WHERE TRIM(Piloto) = TRIM(?) 
                            AND Estado = ? 
                            AND FechaSalida = ?''',
                        (row['pilot_name'], row['flight_status'], row['departure_date']))
            vuelo_id = cursor.fetchone()

            if pais_id and vuelo_id:
                data_to_insert.append((row['passenger_id'], row['first_name'], row['last_name'], 
                                        row['gender'], row['age'], vuelo_id[0], pais_id[0]))
            else:
                print(f"❌ No se encontró país o vuelo para: {row['country_name']} - {row['pilot_name']} ({row['departure_date']})")

        if data_to_insert:
            cursor.executemany('''INSERT INTO Pasajeros 
                                (idPasajero, Nombre, Apellido, Sexo, Edad, Vuelo_idVuelo, Paises_idPais)
                                VALUES (?, ?, ?, ?, ?, ?, ?)''', data_to_insert)
            connection.commit()
            print("✅ Datos de los pasajeros insertados correctamente.")
        else:
            print("❌ No hay datos válidos para insertar.")

        # === AEROPUERTOS ===
        cursor.execute('SELECT idPais, Codigo FROM Paises')
        paises_dict = {row[1]: row[0] for row in cursor.fetchall()}

        data_to_insert = []
        for _, row in df.iterrows():
            if pd.isnull(row['airport_name']) or pd.isnull(row['airport_country_code']):
                continue  # Evitar inserción de datos nulos

            pais_id = paises_dict.get(row['airport_country_code'])
            if pais_id:
                data_to_insert.append((row['airport_name'], pais_id))

        if data_to_insert:
            cursor.executemany('''INSERT INTO Aeropuertos (Nombre, Paises_idPais) VALUES (?, ?)''', data_to_insert)
            connection.commit()
            print("✅ Datos de los aeropuertos cargados con éxito.")
        else:
            print("❌ No se encontraron aeropuertos para insertar.")

    except Exception as e:
        print(f"❌ Error al cargar los datos: {e}")
        connection.rollback()
