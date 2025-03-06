from ETL.Extract import extract_data
from ETL.Load import load_data_to_db
from ETL.Transform import passenger_cleaned, data_cleaned, airportS_cleaned, arrivalA_cleaned, pilot_cleaned, flightS_cleaned, flight_cleaned


def run_etl(input_path, connection):
    df = extract_data(input_path)
    if df is not None:
        passenger_transformed = passenger_cleaned(df)
        data_tranformed = data_cleaned(df)
        airportS_tranformed = airportS_cleaned(df)
        arrivalA_tranformed = arrivalA_cleaned(df)
        pilot_tranformed = pilot_cleaned(df)
        flightS_tranformed = flightS_cleaned(df)
        flight_transformed = flight_cleaned(df)
        if connection:
            load_data_to_db(passenger_transformed, data_tranformed, airportS_tranformed, arrivalA_tranformed, pilot_tranformed, flightS_tranformed, flight_transformed, connection)
