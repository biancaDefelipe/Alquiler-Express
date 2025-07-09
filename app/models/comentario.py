from sqlalchemy import Column, Integer, Text, Date, ForeignKey, UniqueConstraint
from datetime import date
from models import DATABASE
from sqlalchemy.orm import relationship

class Comentario(DATABASE.Model):
    __tablename__ = 'comentario'

    id_comentario = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)
    id_reserva = Column(Integer, ForeignKey('reserva.id_reserva'), nullable=False)
    texto = Column(Text, nullable=False)
    fecha = Column(Date, nullable=False, default=date.today)
    usuario = relationship("Usuario", backref="comentarios")
    reserva = relationship("Reserva", backref="comentarios")

    __table_args__ = (
        UniqueConstraint('id_usuario', 'id_reserva', name='u_usuario_reserva'),
    )

    def __str__(self):
        return (
            f"\nid_comentario: {self.id_comentario}, id_usuario: {self.id_usuario}, "
            f"id_reserva: {self.id_reserva}, texto: {self.texto}, fecha: {self.fecha}\n"
        )

    def serialize(self):
        return {
            "id_comentario": self.id_comentario,
            "id_usuario": self.id_usuario,
            "id_reserva": self.id_reserva,
            "texto": self.texto,
            "fecha": str(self.fecha)
        }

    def serialize_con_usuario(self):
        return {
            "id_comentario": self.id_comentario,
            "id_usuario": self.id_usuario,
            "nombre_usuario": self.usuario.nombre,
            "apellido_usuario": self.usuario.apellido,
            "fecha": self.fecha.strftime('%d-%m-%Y'),
            "texto": self.texto
        }
