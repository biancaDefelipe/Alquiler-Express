from models import DATABASE
from models.respuesta import Respuesta
from sqlalchemy.exc import SQLAlchemyError

def crear_respuesta(respuesta_obj):
    
    try:
        DATABASE.session.add(respuesta_obj)
        DATABASE.session.commit()
        return respuesta_obj
    except Exception:
        DATABASE.session.rollback()
        raise
    


def obtener_por_id_pregunta(id_pregunta):
    return DATABASE.session.query(Respuesta).filter_by(id_pregunta=id_pregunta).first()

def obtener_por_id(id_respuesta):
    return DATABASE.session.query(Respuesta).get(id_respuesta)

def eliminar_respuesta(id_respuesta):
    try:
        respuesta = DATABASE.session.query(Respuesta).get(id_respuesta)
        if respuesta:
            DATABASE.session.delete(respuesta)
            DATABASE.session.commit()
            return True
        return False
    except Exception:
        DATABASE.session.rollback()
        return False
