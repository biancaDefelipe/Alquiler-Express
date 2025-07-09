import os
import json

RUTA_BASE_SESION = os.path.join("app")
RUTA_ARCHIVO = os.path.join(RUTA_BASE_SESION, "sesion.json")


# Registra en el json el id y rol del usuario que se autenticó.
def iniciar_sesion(id_usuario, rol):
    try:
        #os.makedirs(os.path.dirname(RUTA_ARCHIVO), exist_ok=True)
        with open(RUTA_ARCHIVO, 'w', encoding='utf-8') as archivo:
            sesion = {"id_usuario": id_usuario, "rol": rol}
            json.dump(sesion, archivo, ensure_ascii=False, indent=2)

    except FileNotFoundError:
        print(f"El archivo '{RUTA_ARCHIVO}' no fue encontrado.")
        raise
    except IOError:
        print(f"Error al escribir el archivo '{RUTA_ARCHIVO}")
        raise
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        raise


# Obtiene del json el id y rol del usuario que se autenticó.
def ver_sesion_actual():
    try:
        #os.makedirs(os.path.dirname(RUTA_ARCHIVO), exist_ok=True)
        with open(RUTA_ARCHIVO, 'r', encoding='utf-8') as archivo:
            sesion = json.load(archivo)

        return sesion

    except FileNotFoundError:
        print(f"El archivo '{RUTA_ARCHIVO}' no fue encontrado.")
        raise
    except IOError:
        print(f"Error al escribir el archivo '{RUTA_ARCHIVO}")
        raise
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        raise


# Registra en el json el rol como visitante.
def limpiar_sesion():
    try:
        #os.makedirs(os.path.dirname(RUTA_ARCHIVO), exist_ok=True)
        with open(RUTA_ARCHIVO, 'w', encoding='utf-8') as archivo:
            sesion = {"id_usuario": None, "rol": "VISITANTE"}
            json.dump(sesion, archivo, ensure_ascii=False, indent=2)

    except FileNotFoundError:
        print(f"El archivo '{RUTA_ARCHIVO}' no fue encontrado.")
        raise
    except IOError:
        print(f"Error al escribir el archivo '{RUTA_ARCHIVO}")
        raise
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        raise