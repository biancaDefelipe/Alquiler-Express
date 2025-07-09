from sqlalchemy import Column, Integer, String, Date, CheckConstraint
from models import DATABASE


class Usuario(DATABASE.Model):
    __tablename__ = 'usuario'

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    dni = Column(String(24), nullable=False, unique=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    mail = Column(String(50), nullable=False, unique=True)
    telefono = Column(String(24), nullable=False)
    fecha_nacimiento = Column(String(10), nullable=False)
    contrasenia = Column(String, nullable=False)
    rol = Column(String(24), nullable=False)
    fecha_registro = Column(Date, nullable=False)
    eliminado = Column(String(2), nullable=False)

    __table_args__ = (
        CheckConstraint('length(dni) <= 24'),
        CheckConstraint('length(nombre) <= 50'),
        CheckConstraint('length(apellido) <= 50'),
        CheckConstraint('length(mail) <= 50'),
        CheckConstraint('length(telefono) <= 24'),
        CheckConstraint('length(fecha_nacimiento) = 10'),
        CheckConstraint('length(rol) <= 24'),
        CheckConstraint('length(eliminado) <= 2')
    )

    def __str__(self):
        return (
            f"\nid_usuario: {self.id_usuario}, dni: {self.dni}, nombre: {self.nombre}, "
            f"apellido: {self.apellido}, mail: {self.mail}, telefono: {self.telefono}, "
            f"fecha_nacimiento: {self.fecha_nacimiento}, rol: {self.rol}, "
            f"fecha_registro: {self.fecha_registro}, eliminado: {self.eliminado}\n"
        )

    def serialize(self):
        return {
            "id_usuario": self.id_usuario,
            "dni": self.dni,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "mail": self.mail,
            "telefono": self.telefono,
            "fecha_nacimiento": self.fecha_nacimiento,
            "rol": self.rol,
            "fecha_registro": self.fecha_registro,
            "eliminado": self.eliminado
        }