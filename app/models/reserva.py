from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, CheckConstraint, DateTime
from models import DATABASE

class Reserva(DATABASE.Model):
    __tablename__ = 'reserva'

    id_reserva = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)
    id_propiedad = Column(Integer, ForeignKey('propiedad.id_propiedad'), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    precio_total = Column(Numeric(9, 2), nullable=False)
    medio_de_pago = Column(String(100), nullable=False)
    estado = Column(String(100), nullable=False)
    # Cambiado a DateTime para incluir la hora
    fecha_check_in = Column(DateTime, nullable=True) 
    fecha_check_out = Column(DateTime, nullable=True)
    calificacion =  Column(Integer, nullable=True)

    __table_args__ = (
        CheckConstraint('precio_total > 0'),
        CheckConstraint('length(medio_de_pago) <= 100'),
        CheckConstraint('length(estado) <= 100'),
    )

    def __str__(self):
        return (
            f"\nid_reserva: {self.id_reserva}, id_usuario: {self.id_usuario}, id_propiedad: {self.id_propiedad}, "
            f"fecha_inicio: {self.fecha_inicio}, fecha_fin: {self.fecha_fin}, precio_total: {self.precio_total}, "
            f"medio_de_pago: {self.medio_de_pago}, estado: {self.estado}, "
            f"fecha_check_in: {self.fecha_check_in}, fecha_check_out: {self.fecha_check_out}\n"
        )

    def serialize(self):
        return {
            "id_reserva": self.id_reserva,
            "id_usuario": self.id_usuario,
            "id_propiedad": self.id_propiedad,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin, 
            "precio_total": self.precio_total,
            "medio_de_pago": self.medio_de_pago,
            "estado": self.estado,
            #"fecha_check_in": self.fecha_check_in,
            #"fecha_check_out": self.fecha_check_out
            'fecha_check_in': self.fecha_check_in.isoformat() if self.fecha_check_in else None,
            'fecha_check_out': self.fecha_check_out.isoformat() if self.fecha_check_out else None,
            "ya_comento": getattr(self, "ya_comento", False),
            "calificacion": self.calificacion
        }
        
        
