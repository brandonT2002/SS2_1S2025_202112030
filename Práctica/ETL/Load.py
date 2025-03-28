# === CARGA DE DATOS ===
def load_data_to_db(df_cleaned, data_tranformed, airportS_tranformed, arrivalA_tranformed, pilot_tranformed, flightS_tranformed, flight_transformed, connection):
    try:
        cursor = connection.cursor()
        cursor.fast_executemany = True

        merge_query = """
            MERGE INTO Pasajero AS target
            USING (VALUES (?, ?, ?, ?, ?, ?)) AS source (IdPasajero, Nombre, Apellido, Genero, Edad, Nacionalidad)
            ON target.IdPasajero = source.IdPasajero
            WHEN NOT MATCHED BY TARGET THEN
                INSERT (IdPasajero, Nombre, Apellido, Genero, Edad, Nacionalidad)
                VALUES (source.IdPasajero, source.Nombre, source.Apellido, source.Genero, source.Edad, source.Nacionalidad);
        """

        # preparar insert masivo
        data_to_insert = []
        for index, row in df_cleaned.iterrows():
            data_to_insert.append((row['IdPasajero'], row['Nombre'], row['Apellido'], row['Genero'], row['Edad'], row['Nacionalidad']))

        cursor.fast_executemany = True  # a echar punta
        cursor.executemany(merge_query, data_to_insert)
        connection.commit()
        print("✅ Pasajeros insertados correctamente.")

        # ===============================

        # Preparar la consulta SQL para realizar un MERGE
        merge_query = """
            MERGE INTO FechaSalida AS target
            USING (VALUES (?, ?, ?, ?)) AS source (Fecha, Anio, Mes, Dia)
            ON target.Fecha = source.Fecha
            WHEN NOT MATCHED BY TARGET THEN
                INSERT (Fecha, Anio, Mes, Dia)
                VALUES (source.Fecha, source.Anio, source.Mes, source.Dia);
        """

        # preparar insert masivo
        data_to_insert = []
        for index, row in data_tranformed.iterrows():
            data_to_insert.append((row['Departure Date'].date(), row['Anio'], row['Mes'], row['Dia']))

        cursor.fast_executemany = True  # a echar punta
        cursor.executemany(merge_query, data_to_insert)
        connection.commit()

        print("✅ Fechas de salida insertadas correctamente.")

        # ===============================

        # Consulta SQL optimizada con MERGE para evitar duplicados
        merge_query = """
            MERGE INTO AeropuertoSalida AS target
            USING (VALUES (?, ?, ?, ?, ?)) AS source (NombreAeropuerto, CodigoPais, NombrePais, ContinenteAeropuerto, Continente)
            ON target.NombreAeropuerto = source.NombreAeropuerto AND target.CodigoPais = source.CodigoPais
            WHEN NOT MATCHED THEN
                INSERT (NombreAeropuerto, CodigoPais, NombrePais, ContinenteAeropuerto, Continente)
                VALUES (source.NombreAeropuerto, source.CodigoPais, source.NombrePais, source.ContinenteAeropuerto, source.Continente);
        """

        # Preparar los datos para inserción masiva
        data_to_insert = list(airportS_tranformed[['Airport Name', 'Airport Country Code', 'Country Name', 'Airport Continent', 'Continents']].itertuples(index=False, name=None))

        # preparar insert masivo
        cursor.fast_executemany = True  # a echar punta
        cursor.executemany(merge_query, data_to_insert)
        connection.commit()

        print("✅ Aeropuertos de salida insertados correctamente.")

        # ===============================

        # Consulta SQL optimizada con MERGE para evitar duplicados
        merge_query = """
            MERGE INTO AeropuertoLlegada AS target
            USING (VALUES (?)) AS source (NombreAeropuerto)
            ON target.NombreAeropuerto = source.NombreAeropuerto
            WHEN NOT MATCHED THEN
                INSERT (NombreAeropuerto)
                VALUES (source.NombreAeropuerto);
        """

        # Preparar los datos para inserción masiva
        data_to_insert = list(arrivalA_tranformed[['Arrival Airport']].itertuples(index=False, name=None))

        # preparar insert masivo
        cursor.fast_executemany = True  # a echar punta
        cursor.executemany(merge_query, data_to_insert)
        connection.commit()

        print("✅ Aeropuertos de llegada insertados correctamente.")

        # ===============================
        # Crear una tabla temporal para la inserción masiva
        cursor.execute("CREATE TABLE #PilotosTemp (NombrePiloto NVARCHAR(100));")

        # Insertar los datos en la tabla temporal
        insert_query = "INSERT INTO #PilotosTemp (NombrePiloto) VALUES (?);"
        cursor.fast_executemany = True  # Activar inserción rápida
        cursor.executemany(insert_query, list(pilot_tranformed[['Pilot Name']].itertuples(index=False, name=None)))

        # Ejecutar MERGE con la tabla temporal
        merge_query = """
            MERGE INTO Piloto AS target
            USING #PilotosTemp AS source
            ON target.NombrePiloto = source.NombrePiloto
            WHEN NOT MATCHED THEN
                INSERT (NombrePiloto) VALUES (source.NombrePiloto);
        """
        cursor.execute(merge_query)
        connection.commit()

        print("✅ Pilotos insertados correctamente.")

        # ===============================
        # Consulta SQL optimizada con MERGE para evitar duplicados
        merge_query = """
            MERGE INTO EstadoVuelo AS target
            USING (VALUES (?)) AS source (Estado)
            ON target.Estado = source.Estado
            WHEN NOT MATCHED THEN
                INSERT (Estado)
                VALUES (source.Estado);
        """

        # Preparar los datos para inserción masiva
        data_to_insert = list(flightS_tranformed[['Flight Status']].itertuples(index=False, name=None))

        # Insertar los datos en la base de datos de manera eficiente
        cursor.fast_executemany = True  # a echar punta
        cursor.executemany(merge_query, data_to_insert)
        connection.commit()

        print("✅ Estados de vuelo insertados correctamente.")

        # ===============================

        # Obtener los valores únicos de cada columna relevante
        passenger_values = flight_transformed['Passenger ID'].dropna().unique().tolist()
        date_values = flight_transformed['Departure Date'].dropna().unique().tolist()
        airport_values = flight_transformed['Airport Name'].dropna().unique().tolist()
        arrival_values = flight_transformed['Arrival Airport'].dropna().unique().tolist()
        pilot_values = flight_transformed['Pilot Name'].dropna().unique().tolist()
        flight_status_values = flight_transformed['Flight Status'].dropna().unique().tolist()

        # Consultar todos los IDs en lotes para evitar sobrecarga en SQL Server
        passenger_ids = fetch_ids(cursor, "Pasajero", "IdPasajero", passenger_values)
        date_ids = fetch_ids(cursor, "FechaSalida", "Fecha", date_values)
        airport_ids = fetch_ids(cursor, "AeropuertoSalida", "NombreAeropuerto", airport_values)
        arrival_airport_ids = fetch_ids(cursor, "AeropuertoLlegada", "NombreAeropuerto", arrival_values)
        pilot_ids = fetch_ids(cursor, "Piloto", "NombrePiloto", pilot_values)
        flight_status_ids = fetch_ids(cursor, "EstadoVuelo", "Estado", flight_status_values)

        # **3. Preparar datos para inserción masiva**
        insert_data = []
        for _, row in flight_transformed.iterrows():
            IdPasajero = passenger_ids.get(row['Passenger ID'])
            IdFechaSalida = date_ids.get(row['Departure Date'])
            IdAeropuertoSalida = airport_ids.get(row['Airport Name'])
            IdAeropuertoLlegada = arrival_airport_ids.get(row['Arrival Airport'])
            IdPiloto = pilot_ids.get(row['Pilot Name'])
            IdEstadoVuelo = flight_status_ids.get(row['Flight Status'])

            if None in (IdPasajero, IdFechaSalida, IdAeropuertoSalida, IdAeropuertoLlegada, IdPiloto, IdEstadoVuelo):
                continue

            insert_data.append((IdPasajero, IdFechaSalida, IdAeropuertoSalida, IdAeropuertoLlegada, IdPiloto, IdEstadoVuelo))

        # **4. Inserción masiva**
        insert_query = """
            INSERT INTO Vuelo (IdPasajero, IdFechaSalida, IdAeropuertoSalida, IdAeropuertoLlegada, IdPiloto, IdEstadoVuelo)
            VALUES (?, ?, ?, ?, ?, ?)
        """

        cursor.fast_executemany = True  # Acelerar la ejecución masiva
        cursor.executemany(insert_query, insert_data)
        connection.commit()

        print(f"✅ Vuelos insertados correctamente.")

        # Cerrar la conexión a la base de datos
        connection.close()
    except Exception as e:
        print(f"❌ Error al cargar los datos: {e}")
        connection.rollback()

def fetch_ids(cursor, table, column_name, values, batch_size=1000):
    """ Obtiene los IDs correspondientes a una lista de valores en lotes pequeños """
    id_map = {}
    for i in range(0, len(values), batch_size):
        batch = values[i:i + batch_size]
        placeholders = ', '.join(['?'] * len(batch))
        query = f"SELECT {column_name}, Id{table} FROM {table} WHERE {column_name} IN ({placeholders})"
        cursor.execute(query, *batch)
        id_map.update({row[0]: row[1] for row in cursor.fetchall()})
    return id_map