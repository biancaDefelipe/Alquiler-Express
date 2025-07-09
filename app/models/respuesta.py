from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, CheckConstraint, DateTime
from models import DATABASE


class Respuesta(DATABASE.Model):
    __tablename__ = 'respuesta'
    id_pregunta=Column(Integer, ForeignKey('pregunta.id_pregunta'), nullable=False)
    id_respuesta = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)
    fecha= Column(Date, nullable=False)
    respuesta = Column(String(155), nullable=False)


    __table_args__ = (
        CheckConstraint('length(respuesta) <= 155'),
    )

    def __str__(self):
        return (
            f"\nid_propiedad: {self.id_respuesta}, id_usuario: {self.id_usuario}, "
            f"fecha: {self.fecha}, id_pregunta: {self.id_pregunta}"
            f"respuesta: {self.respuesta}\n"
        )

    def serialize(self):
        return {
            "id_respuesta": self.id_respuesta,
            "id_usuario": self.id_usuario, 
            "id_pregunta" : self.id_pregunta,
            "fecha": self.fecha,
            "respuesta": self.respuesta
        }