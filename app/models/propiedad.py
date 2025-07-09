from sqlalchemy import Column, Integer, String, Numeric, CheckConstraint
from models import DATABASE


class Propiedad(DATABASE.Model):
    __tablename__ = 'propiedad'

    id_propiedad = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False)
    tipo = Column(String(24), nullable=False)
    localidad = Column(String(50), nullable=False)
    descripcion = Column(String(255), nullable=True)
    cantidad_banios = Column(Integer, nullable=False)
    cantidad_habitaciones = Column(Integer, nullable=False)
    cantidad_huespedes = Column(Integer, nullable=False)
    politica_cancelacion = Column(String(100), nullable=False)
    metros_cuadrados = Column(Numeric(9, 2), nullable=False)
    minimo_dias = Column(Integer, nullable=False)
    precio_por_dia = Column(Numeric(9, 2), nullable=False)
    calle = Column(String(42), nullable=False)
    numero = Column(String(12), nullable=False)
    piso = Column(String(3), nullable=True)
    departamento = Column(String(4), nullable=True)
    esta_habilitada = Column(String(2), nullable=False)
    estado = Column(String(50), nullable=False)
    calificacion = Column(Numeric(9, 2), nullable=True, default=0.0)
    total_calificaciones = Column(Integer, nullable=True, default=0)
    suma_calificaciones = Column(Integer, nullable=True, default=0)

    __table_args__ = (
        CheckConstraint('length(titulo) <= 100'),
        CheckConstraint('length(tipo) <= 24'),
        CheckConstraint('length(localidad) <= 50'),
        CheckConstraint('length(descripcion) <= 255'),
        CheckConstraint('cantidad_banios BETWEEN 1 AND 99'),
        CheckConstraint('cantidad_habitaciones BETWEEN 1 AND 99'),
        CheckConstraint('cantidad_huespedes BETWEEN 1 AND 99'),
        CheckConstraint('length(politica_cancelacion) <= 100'),
        CheckConstraint('metros_cuadrados > 0'),
        CheckConstraint('minimo_dias BETWEEN 1 AND 99'),
        CheckConstraint('precio_por_dia > 0'),
        CheckConstraint('length(calle) <= 42'),
        CheckConstraint('length(numero) <= 12'),
        CheckConstraint('length(piso) <= 3'),
        CheckConstraint('length(departamento) <= 4'),
        CheckConstraint('length(esta_habilitada) <= 2'),
        CheckConstraint('length(estado) <= 50'),
    )

    def __str__(self):
        return (
            f"\nid_propiedad: {self.id_propiedad}, titulo: {self.titulo}, tipo: {self.tipo}, "
            f"localidad: {self.localidad}, descripcion: {self.descripcion}, cantidad_banios: {self.cantidad_banios}, "
            f"cantidad_habitaciones: {self.cantidad_habitaciones}, cantidad_huespedes: {self.cantidad_huespedes}, politica_cancelacion: {self.politica_cancelacion}, "
            f"metros_cuadrados: {self.metros_cuadrados}, minimo_dias: {self.minimo_dias}, precio_por_dia: {self.precio_por_dia}, "
            f"calle: {self.calle}, numero: {self.numero}, piso: {self.piso}, "
            f"departamento: {self.departamento}, esta_habilitada: {self.esta_habilitada}, estado: {self.estado}\n"
        )

    def serialize(self):
        return {
            "id_propiedad": self.id_propiedad,
            "titulo": self.titulo,
            "tipo": self.tipo,
            "localidad": self.localidad,
            "descripcion": self.descripcion,
            "cantidad_banios": self.cantidad_banios,
            "cantidad_habitaciones": self.cantidad_habitaciones,
            "cantidad_huespedes": self.cantidad_huespedes,
            "politica_cancelacion": self.politica_cancelacion,
            "metros_cuadrados": self.metros_cuadrados,
            "minimo_dias": self.minimo_dias,
            "precio_por_dia": self.precio_por_dia,
            "calle": self.calle,
            "numero": self.numero,
            "piso": self.piso,
            "departamento": self.departamento,
            "esta_habilitada": self.esta_habilitada,
            "estado": self.estado,
            "calificacion": self.calificacion,
            "total_calificaciones": self.total_calificaciones,
            "suma_calificaciones": self.suma_calificaciones
        }