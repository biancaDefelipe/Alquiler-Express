import os
import json

RUTA_BASE_SESION = os.path.join("app")
RUTA_ARCHIVO = os.path.join(RUTA_BASE_SESION, "pago.json")


def limpiar_pago():
    try:
        with open(RUTA_ARCHIVO, 'w', encoding='utf-8') as archivo:
            pago = {"id_pago": None}
            json.dump(pago, archivo, ensure_ascii=False, indent=2)
    except FileNotFoundError:
        print(f"El archivo '{RUTA_ARCHIVO}' no fue encontrado.")
        raise
    except IOError:
        print(f"Error al escribir el archivo '{RUTA_ARCHIVO}")
        raise
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        raise
    
def realizar_pago(id_pago):
    try:
        with open(RUTA_ARCHIVO, 'w', encoding='utf-8') as archivo:
            pago = {"id_pago": id_pago}
            json.dump(pago, archivo, ensure_ascii=False, indent=2)
    except FileNotFoundError:
        print(f"El archivo '{RUTA_ARCHIVO}' no fue encontrado.")
        raise
    except IOError:
        print(f"Error al escribir el archivo '{RUTA_ARCHIVO}")
        raise
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        raise
    
def ver_pago():
    try:
        with open(RUTA_ARCHIVO, 'r', encoding='utf-8') as archivo:
            pago = json.load(archivo)
        return pago
    except FileNotFoundError:
        print(f"El archivo '{RUTA_ARCHIVO}' no fue encontrado.")
        raise
    except IOError:
        print(f"Error al escribir el archivo '{RUTA_ARCHIVO}")
        raise
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        raise

import unicodedata

def normalizar(texto):
    return unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode("utf-8")

def calcular_reembolso(politica, total):
    politica = normalizar(politica.strip())
    reembolso = 0
    match politica:
        case "Cancelacion 20% reembolso":
            reembolso = total * 0.2
        case "Cancelacion total reembolso":
            reembolso = total
        case "Cancelacion no reembolsable":
            pass
        case _:
            raise ValueError(f"Politica desconocida: {politica}")
    return reembolso