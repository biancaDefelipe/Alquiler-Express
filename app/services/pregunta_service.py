# Lógica de negocio para preguntas y respuestas

import repositories.pregunta_repository as pregunta_repository
from datetime import datetime
from datetime import date
from repositories import pregunta_repository, respuesta_repository
from models.pregunta import Pregunta
def crear_pregunta(data):
    try:
        data["fecha_creacion"] = datetime.now()
        return pregunta_repository.crear_pregunta(data)
    except Exception as e:
        print(e)
        raise
    

def alta_pregunta(datos):
    try:
        nueva_pregunta = Pregunta(
            pregunta=datos["pregunta"],
            id_propiedad=datos["id_propiedad"],
            id_usuario=datos["id_usuario"],
            fecha=datetime.now().date(), 
            esta_respondida="NO"
            
        )
        return pregunta_repository.alta_pregunta(nueva_pregunta)
    except Exception as e:
        print(f"Error al crear pregunta: {e}")
        raise

def obtener_todas_preguntas(id_propiedad):
    try:
        return pregunta_repository.obtener_todas_preguntas(id_propiedad)
    except Exception as e:
        print(e)
        raise


def obtener_pregunta_por_id(id_pregunta):
    return pregunta_repository.obtener_por_id(id_pregunta)

def eliminar_pregunta_y_respuesta_si_corresponde(id_pregunta):
    pregunta = pregunta_repository.obtener_por_id(id_pregunta)

    if not pregunta:
        return False

    if pregunta.esta_respondida.upper() == "SI":
        # Buscar y eliminar la respuesta vinculada
        respuesta = respuesta_repository.obtener_por_id_pregunta(id_pregunta)
        if respuesta:
            respuesta_repository.eliminar_respuesta(respuesta.id_respuesta)

    return pregunta_repository.eliminar_pregunta(id_pregunta)


