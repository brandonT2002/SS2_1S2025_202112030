from Utils.ConnectionDB import connect_to_db
from ETL.Extract import extract_data
from ETL.Load import load_data_to_db
from ETL.Transform import transform_data


def run_etl(input_path):
    df = extract_data(input_path)
    if df is not None:
        df_transformed = transform_data(df)
        if df_transformed is not None:
            connection = connect_to_db()
            if connection:
                load_data_to_db(df_transformed, connection)
