from Utils.ConnectionDB import connect_to_db
from ETL.ETL import run_etl
from Queries.Queries import delete_model
from Queries.Queries import create_model
from Queries.Queries import count_tables
import easygui

def show_menu():
    print()
    print("╔══════════════════════════════════════╗")
    print("║          PRACTICA 1 - SEMI2          ║")
    print("╠══════════════════════════════════════╣")
    print("║ 1. Eliminar Modelo                   ║")
    print("║ 2. Crear Nuevo Modelo                ║")
    print("║ 3. ETL                               ║")
    print("║ 4. Consultas                         ║")
    print("║ 5. Exit                              ║")
    print("╚══════════════════════════════════════╝")
    option = int(input("Opcion: "))
    print()
    return option

def menu(connect):
    while True:
        option = show_menu()
        if option == 1:
            delete_model(connect)
        elif option == 2:
            create_model(connect)
        elif option == 3:
            file_path = easygui.fileopenbox()
            with open(file_path, "r", encoding="utf-8"):
                run_etl(file_path, connect)
        elif option == 4:
            count_tables(connect)
        elif option == 5:
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    connect = connect_to_db()
    menu(connect)
