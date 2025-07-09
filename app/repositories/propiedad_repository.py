from sqlalchemy.exc import SQLAlchemyError
from models import DATABASE
from models.propiedad import Propiedad
from models.reserva import Reserva
from sqlalchemy import join, and_, not_, exists

from datetime import date


def alta_propiedad(datos_propiedad):
    nueva_propiedad = Propiedad(
        titulo = datos_propiedad['titulo'],
        tipo = datos_propiedad['tipo'],
        localidad = datos_propiedad['localidad'].upper(),
        descripcion = None if datos_propiedad.get('descripcion') == 'null' else datos_propiedad.get('descripcion'),
        cantidad_banios = datos_propiedad['cantidad_banios'],
        cantidad_habitaciones = datos_propiedad['cantidad_habitaciones'],
        cantidad_huespedes = datos_propiedad['cantidad_huespedes'],
        politica_cancelacion = datos_propiedad['politica_cancelacion'],
        metros_cuadrados = None if datos_propiedad.get('metros_cuadrados') == 'null' else datos_propiedad.get('metros_cuadrados'),
        # metros_cuadrados = datos_propiedad.get('metros_cuadrados'),
        minimo_dias = datos_propiedad['minimo_dias'],
        precio_por_dia = datos_propiedad['precio_por_dia'],
        calle = datos_propiedad['calle'],
        numero = datos_propiedad['numero'],
        piso = None if datos_propiedad.get('piso') == 'null' else datos_propiedad.get('piso'),
        departamento = None if datos_propiedad.get('departamento') == 'null' else datos_propiedad.get('departamento'),
        esta_habilitada = datos_propiedad['esta_habilitada'],
        estado = datos_propiedad['estado'],
        calificacion = 0.0,  # Valor por defecto
        total_calificaciones = 0,  # Valor por defecto
        suma_calificaciones = 0 # Valor por defecto 
    )

    try:
        DATABASE.session.add(nueva_propiedad) # Da de alta el nuevo registro.
        DATABASE.session.commit() # Commitea los cambios.
        return nueva_propiedad.id_propiedad

    except SQLAlchemyError as e:
        print(e)
        DATABASE.session.rollback() # Si salta una excepcion en el proceso, tengo que volver para atras los cambios que se hicieron, para no generar inconsistencias en la DB.
        raise # Propaga la excepcion, para que la pesque el controller correspondiente y avise al FE con un mensaje y codigo de error.


def obtener_propiedad_con_id(id_propiedad):
    try:
        propiedad = DATABASE.session.get(Propiedad, id_propiedad) # Obtiene una propiedad con un id especifico. Como id_propiedad es PK, se busca solo con el get()
        return propiedad

    except SQLAlchemyError as e:
        raise # Propaga la excepcion, para que la pesque el controller correspondiente y avise al FE con un mensaje y codigo de error.


def obtener_propiedades():
    return DATABASE.session.query(Propiedad).order_by(Propiedad.id_propiedad.desc()).all()



def obtener_propiedades_buscadas(criterios_busqueda):
    """
        Obtiene una lista de propiedades que cumplan con los criterios de búsqueda recibidos
        Args: 
            criterios_busqueda(Diccionario):criterios de busqueda ingresados por el usuario (localidad, cantidad de huespedes, check-in y check-out)
        Returns: 
            propiedades_disponibles: si hay al menos una propiedad que cumpla con los criterios de búsqueda 
            None: ni no hay propiedades que cumplan con los criterios.
        Raises:
            SQLAlchemyError: Si ocurre un error al acceder a la base de datos.
    """
    check_in_str = criterios_busqueda['check-in']
    check_out_str = criterios_busqueda['check-out']
    huespedes = criterios_busqueda['huespedes']
    localidad = criterios_busqueda['localidad'].upper()

    print (type(huespedes))
    print(type(check_in_str))
    try:
        check_in_date = date.fromisoformat(check_in_str)
        check_out_date = date.fromisoformat(check_out_str)
        print(f"Check-in Date: {check_in_date}, Type: {type(check_in_date)}")
        print(f"Check-out Date: {check_out_date}, Type: {type(check_out_date)}")
        duracion_estancia = (check_out_date - check_in_date).days
        print (duracion_estancia)
        propiedades_disponibles = DATABASE.session.query(Propiedad).filter(
            and_(
                Propiedad.cantidad_huespedes >= huespedes,
                Propiedad.localidad == localidad,
                Propiedad.minimo_dias <= duracion_estancia,
                Propiedad.esta_habilitada== "SI",
                not_(
                    exists().where(
                        and_(
                            Reserva.id_propiedad == Propiedad.id_propiedad,
                            Reserva.fecha_inicio < check_out_date,
                            Reserva.fecha_fin > check_in_date, 
                            Reserva.estado.in_(["ABONADA", "EN CURSO"])
                        )
                    )
                )
            )
        ).all()
        print(propiedades_disponibles)
        return propiedades_disponibles
    except SQLAlchemyError as e :
        print (e)
        DATABASE.session.rollback()
        raise
    except ValueError as ve:
        print(f"Error de formato de fecha: {ve}")
        DATABASE.session.rollback()
        raise
    
def registrar_fin_de_limpieza(id_propiedad_in):
    """
        Cambia el estado de la propiedad a "LIBRE" cuando se registra el fin de la limpieza.
    """
    try:
        propiedad = DATABASE.session.query(Propiedad).filter_by(id_propiedad=id_propiedad_in).first()
        if propiedad:
            propiedad.estado = "LIBRE"
            DATABASE.session.commit()
            print("Estado actualizado a LIBRE.")
        else:
            print("Propiedad no encontrada.")
            
    except SQLAlchemyError as e:
        print(e)
        DATABASE.session.rollback()
        raise
    
def cambiar_estado_propiedad(id_propiedad, estado):
    """
        Cambia el estado de la propiedad a el estado recibido por parámetro cuando se registra un check-in/check-out
    """
    try:
        propiedad = DATABASE.session.query(Propiedad).filter_by(id_propiedad=id_propiedad).first()
        if propiedad:
            propiedad.estado = estado
            DATABASE.session.commit()
            print("Estado actualizado.")
        else:
            print("Propiedad no encontrada.")
            
    except SQLAlchemyError as e:
        print(e)
        DATABASE.session.rollback()
        raise

def modificar_propiedad_repository(id_propiedad, data):
    try:
        propiedad = DATABASE.session.get(Propiedad, id_propiedad)
        if propiedad:
            for campo, valor in data.items():
                if hasattr(propiedad, campo):
                    setattr(propiedad, campo, valor)
            DATABASE.session.commit()
            return propiedad
        return None
    
    except SQLAlchemyError as e:
        print(e)
        DATABASE.session.rollback()
        raise

def eliminar_propiedad_repository(id_propiedad):
    try:
        propiedad = DATABASE.session.get(Propiedad, id_propiedad)
        if propiedad:
            DATABASE.session.delete(propiedad)
            DATABASE.session.commit()
            print("Propiedad eliminada con exito.")
        else:
            print("Propiedad no encontrada.")

    except SQLAlchemyError as e:
        print(e)
        DATABASE.session.rollback()
        raise