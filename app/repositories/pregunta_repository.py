
from models import DATABASE
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import aliased
from sqlalchemy import outerjoin
from models.pregunta import  Pregunta
from models.respuesta import Respuesta


def obtener_todas_preguntas(id_propiedad):
    
    '''Devuelve una lista de tuplas del tipo (Pregunta, Respuesta) para la propiedad con id reciido'''
    try: 
        # alias para poder hacer join correctamente
        R = aliased(Respuesta)

        resultados = (
            DATABASE.session.query(Pregunta, R)
            .outerjoin(R, Pregunta.id_pregunta == R.id_pregunta)
            .filter(Pregunta.id_propiedad == id_propiedad)
            .all()
        )
        return resultados
    except SQLAlchemyError: 
        raise

def alta_pregunta(pregunta_obj):
    try:
        DATABASE.session.add(pregunta_obj)
        DATABASE.session.commit()
        return pregunta_obj
    except SQLAlchemyError:
        raise
    except Exception:
        DATABASE.session.rollback()
        raise


def obtener_por_id(id_pregunta):
    return DATABASE.session.query(Pregunta).get(id_pregunta)

def eliminar_pregunta(id_pregunta):
    try:
        pregunta = obtener_por_id(id_pregunta)
        if pregunta:
            DATABASE.session.delete(pregunta)
            DATABASE.session.commit()
            return True
        return False
    except Exception:
        DATABASE.session.rollback()
        return False

def eliminar_respuesta(pregunta): 
    try:
            if hasattr(pregunta, 'esta_respondida'):
                setattr(pregunta, 'esta_respondida', 'NO')

            DATABASE.session.commit()
            
    except SQLAlchemyError:
            DATABASE.session.rollback()
            raise
        
          
def setear_respondida(pregunta): 
    try:
            if hasattr(pregunta, 'esta_respondida'):
                setattr(pregunta, 'esta_respondida', 'SI')
            DATABASE.session.commit()
    except SQLAlchemyError:
            DATABASE.session.rollback()
            raise