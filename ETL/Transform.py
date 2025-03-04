import pandas as pd

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