import pandas as pd

# === TRANSFORMACIÓN DE DATOS ===
def passenger_cleaned(df):
    try:
        passenger_cleaned = df.drop_duplicates(subset=['Passenger ID'])  # Eliminar duplicados por 'Passenger ID'
        passenger_cleaned = passenger_cleaned.dropna(subset=['Passenger ID', 'First Name', 'Last Name', 'Gender', 'Age', 'Nationality'])  # Eliminar filas con valores nulos

        # Estandarización de nombres de columnas para coincidir con la base de datos
        passenger_cleaned = passenger_cleaned.rename(columns={
            'Passenger ID': 'IdPasajero',
            'First Name': 'Nombre',
            'Last Name': 'Apellido',
            'Gender': 'Genero',
            'Age': 'Edad',
            'Nationality': 'Nacionalidad'
        })
        return passenger_cleaned
    except Exception as e:
        print(f"Error al transformar los datos: {e}")
        return None

def data_cleaned(df):
    try:
        df_cleaned = df.drop_duplicates(subset=['Departure Date'])  # Eliminar duplicados por 'Departure Date'
        df_cleaned = df_cleaned.dropna(subset=['Departure Date'])  # Eliminar filas con valores nulos en 'Departure Date'

        # Asegurar que la columna 'Departure Date' esté en formato de fecha
        df_cleaned['Departure Date'] = pd.to_datetime(df_cleaned['Departure Date'], errors='coerce')

        # Eliminar las filas donde 'Departure Date' no se pudo convertir correctamente
        df_cleaned = df_cleaned.dropna(subset=['Departure Date'])

        # Extraer Año, Mes y Día de la 'Departure Date'
        df_cleaned['Anio'] = df_cleaned['Departure Date'].dt.year
        df_cleaned['Mes'] = df_cleaned['Departure Date'].dt.month
        df_cleaned['Dia'] = df_cleaned['Departure Date'].dt.day
        return df_cleaned
    except Exception as e:
        print(f"Error al transformar los datos: {e}")
        return None

def airportS_cleaned(df):
    try:
        # Limpiar los datos: eliminar duplicados y valores nulos en las columnas necesarias
        df_cleaned = df.drop_duplicates(subset=['Airport Name'])  # Eliminar duplicados por 'Airport Name'
        df_cleaned = df_cleaned.dropna(subset=['Airport Name', 'Airport Country Code', 'Country Name', 'Airport Continent', 'Continents'])  # Eliminar filas con valores nulos

        # Asegurarnos de que los datos sean consistentes, estandarizar nombres y valores
        columns_to_strip = ['Airport Name', 'Airport Country Code', 'Country Name', 'Airport Continent', 'Continents']
        df_cleaned[columns_to_strip] = df_cleaned[columns_to_strip].apply(lambda x: x.str.strip())
        return df_cleaned
    except Exception as e:
        print(f"Error al transformar los datos: {e}")
        return None

def arrivalA_cleaned(df):
    try:
        # Limpiar los datos: eliminar duplicados y valores nulos en 'Arrival Airport'
        df_cleaned = df.drop_duplicates(subset=['Arrival Airport']).dropna(subset=['Arrival Airport'])

        # Asegurarnos de que los datos sean consistentes (eliminar espacios en blanco)
        df_cleaned['Arrival Airport'] = df_cleaned['Arrival Airport'].str.strip()
        return df_cleaned
    except Exception as e:
        print(f"Error al transformar los datos: {e}")
        return None

def pilot_cleaned(df):
    try:
        # Limpiar datos: eliminar duplicados y valores nulos
        df_cleaned = df.drop_duplicates(subset=['Pilot Name']).dropna(subset=['Pilot Name'])
        df_cleaned['Pilot Name'] = df_cleaned['Pilot Name'].str.strip()
        return df_cleaned
    except Exception as e:
        print(f"Error al transformar los datos: {e}")
        return None

def flightS_cleaned(df):
    try:
        # Limpiar los datos: eliminar duplicados y valores nulos en 'Flight Status'
        df_cleaned = df.drop_duplicates(subset=['Flight Status']).dropna(subset=['Flight Status'])

        # Asegurar consistencia en los datos (eliminar espacios en blanco)
        df_cleaned['Flight Status'] = df_cleaned['Flight Status'].str.strip()

        return df_cleaned
    except Exception as e:
        print(f"Error al transformar los datos: {e}")
        return None

def flight_cleaned(df):
    try:
        # **1. Limpiar los datos**
        df_cleaned = df.drop_duplicates(subset=['Passenger ID', 'Departure Date', 'Airport Name', 'Arrival Airport', 'Pilot Name', 'Flight Status'])
        df_cleaned = df_cleaned.dropna(subset=['Passenger ID', 'Departure Date', 'Airport Name', 'Arrival Airport', 'Pilot Name', 'Flight Status'])

        # Convertir fechas a formato correcto
        df_cleaned['Departure Date'] = pd.to_datetime(df_cleaned['Departure Date'], errors='coerce').dt.date

        return df_cleaned
    except Exception as e:
        print(f"Error al transformar los datos: {e}")
        return None