from models.comentario import Comentario
from models.reserva import Reserva
from models import DATABASE

from datetime import date
from models.usuario import Usuario

def get_comentario_por_usuario_y_reserva(id_usuario, id_reserva):
    return Comentario.query.filter_by(id_usuario=id_usuario, id_reserva=id_reserva).first()

def guardar_comentario(comentario):
    from app import DATABASE
    DATABASE.session.add(comentario)
    DATABASE.session.commit()

def reserva_finalizada(id_reserva, id_usuario):
    reserva = Reserva.query.get(id_reserva)
    print("DEBUG reserva:", reserva)
    if not reserva:
        return False
    return reserva.id_usuario == id_usuario

def obtener_comentarios_con_usuario_por_propiedad(id_propiedad):

    return (
        Comentario.query
        .join(Reserva, Comentario.id_reserva == Reserva.id_reserva)
        .join(Usuario, Comentario.id_usuario == Usuario.id_usuario)
        .filter(Reserva.id_propiedad == id_propiedad)
        .all()
    )

def get_comentario_por_id(id_comentario):
    return Comentario.query.filter_by(id_comentario=id_comentario).first()

def eliminar_comentario_por_id(id_comentario):
    comentario = get_comentario_por_id(id_comentario)
    if comentario:
        try:
            DATABASE.session.delete(comentario)
            DATABASE.session.commit()
            return True
        except Exception as e:
            DATABASE.session.rollback()
            print(f"Error al eliminar comentario: {e}")
            return False
    return False