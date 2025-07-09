from models.comentario import Comentario
from repositories import comentario_repository
from datetime import date
from models import DATABASE

def puede_comentar(id_usuario, id_reserva):
    if not comentario_repository.reserva_finalizada(id_reserva, id_usuario):
        return False
    comentario_existente = comentario_repository.get_comentario_por_usuario_y_reserva(id_usuario, id_reserva)
    return comentario_existente is None

def crear_comentario(id_usuario, id_reserva, texto):
    if not puede_comentar(id_usuario, id_reserva):
        return None 

    nuevo_comentario = Comentario(
        id_usuario=id_usuario,
        id_reserva=id_reserva,
        texto=texto,
        fecha=date.today()
    )
    comentario_repository.guardar_comentario(nuevo_comentario)
    return nuevo_comentario

def obtener_comentarios_de_propiedad(id_propiedad):
    return comentario_repository.obtener_comentarios_con_usuario_por_propiedad(id_propiedad)


def obtener_comentario_por_id(id_comentario):
    return comentario_repository.get_comentario_por_id(id_comentario)

def eliminar_comentario(id_comentario):
    return comentario_repository.eliminar_comentario_por_id(id_comentario)

def existe_comentario(id_usuario, id_reserva):
    comentario = DATABASE.session.query(Comentario).filter_by(
        id_usuario=id_usuario,
        id_reserva=id_reserva
    ).first()
    return comentario is not None
