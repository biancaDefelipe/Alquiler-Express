import sqlite3 as sql
import os

ROOT_PATH = os.path.dirname(__file__)

SCHEMA_PATH = os.path.join(ROOT_PATH, 'schema.sql')
DB_PATH = os.path.join(ROOT_PATH, 'database.db')


def crear_db():
    try:
        with open(SCHEMA_PATH, 'r', encoding= 'utf-8') as archivo:
            schema = archivo.read()
    except FileNotFoundError:
        print(f"El archivo {SCHEMA_PATH} no fue encontrado.")
    except IOError:
        print(f"Error al leer el archivo '{SCHEMA_PATH}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

    try:
        conexion = sql.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.executescript(schema)
        conexion.commit()
    except sql.DatabaseError as e:
        print(f"Ocurrio un error al inicializar la base de datos: {e}")
    finally:
        conexion.close()
        

def inicializar_db():
    if not os.path.exists(DB_PATH):
        crear_db()
    else:
        print(f"Se encontró un archivo para la base de datos en la ruta: {DB_PATH}")