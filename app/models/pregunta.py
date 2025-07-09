from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, CheckConstraint, DateTime
from models import DATABASE


class Pregunta(DATABASE.Model):
    __tablename__ = 'pregunta'
    id_pregunta = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)
    id_propiedad= Column(Integer, ForeignKey ('propiedad.id_propiedad'), nullable=False)
    fecha= Column(Date, nullable=False)
    esta_respondida = Column(String(2), nullable=False)
    pregunta = Column(String(155), nullable=False)


    __table_args__ = (
        CheckConstraint('length(pregunta) <= 155'),
        CheckConstraint('length(esta_respondida) <= 2')
    )

    def __str__(self):
        return (
            f"\nid_propiedad: {self.id_pregunta}, id_usuario: {self.id_usuario}, "
            f"id_propiedad: {self.id_propiedad}, fecha: {self.fecha}, esta_respondida: {self.esta_respondida}, "
            f"pregunta: {self.pregunta}\n"
        )

    def serialize(self):
        return {
            "id_pregunta": self.id_pregunta,
            "id_usuario": self.id_usuario,
            "id_propiedad": self.id_propiedad,
            "fecha": self.fecha,
            "esta_respondida": self.esta_respondida,
            "pregunta": self.pregunta
        }