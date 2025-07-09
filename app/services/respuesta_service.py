from models.respuesta import Respuesta
from repositories import respuesta_repository, pregunta_repository
from datetime import datetime
from models import DATABASE

def crear_respuesta(data):
    try:
        nueva_respuesta = Respuesta(
            id_pregunta=data["id_pregunta"],
            id_usuario=data["id_usuario"],
            fecha=datetime.now().date(),
            respuesta=data["respuesta"]
        )
        pregunta= pregunta_repository.obtener_por_id(nueva_respuesta.id_pregunta)
        pregunta_repository.setear_respondida(pregunta)
        return respuesta_repository.crear_respuesta(nueva_respuesta)
    except Exception as e:
        print(e)
        raise
     
        
def eliminar_respuesta(id_respuesta, pregunta):
    respuesta = respuesta_repository.obtener_por_id(id_respuesta)
    if not respuesta:
        return None
    else:
        pregunta_repository.eliminar_respuesta(pregunta)
        return respuesta_repository.eliminar_respuesta(id_respuesta)

def obtener_respuesta_por_id(id_respuesta): 
    return respuesta_repository.obtener_por_id(id_respuesta)