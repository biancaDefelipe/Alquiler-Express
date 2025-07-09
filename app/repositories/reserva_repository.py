from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, CheckConstraint
from models import DATABASE
from models.usuario import Usuario
from models.reserva import Reserva
from models.propiedad import Propiedad
import math

def realizar_reserva(datos_reserva):
    """
        Genera un nuevo registro en tabla "Reserva" con los datos recibidos
    """
    nueva_reserva = Reserva(
        id_usuario = datos_reserva['id_usuario'],
        id_propiedad = datos_reserva['id_propiedad'],
        fecha_inicio = datos_reserva['fecha_inicio'],
        fecha_fin = datos_reserva['fecha_fin'],
        precio_total = datos_reserva['precio_total'],
        medio_de_pago = datos_reserva['medio_de_pago'],
        estado = 'ABONADA',
        fecha_check_in = None,
        fecha_check_out = None,
        calificacion = 0
    )
    print(nueva_reserva.__str__())
    
    try:
        DATABASE.session.add(nueva_reserva)
        DATABASE.session.commit()
        print('reserva creada en repository: ', nueva_reserva)
        return nueva_reserva
    except SQLAlchemyError as e :
        print (e)
        DATABASE.session.rollback() 
        raise
    
    
def obtener_reservas():
    try:
        reservas = DATABASE.session.query(Reserva).all() 
        return reservas
    except SQLAlchemyError as e:
        raise
    
    
def obtener_reserva(id):
    try:
        reserva = DATABASE.session.get(Reserva, id) 
        return reserva
    except SQLAlchemyError as e:
        raise

def obtener_reservas_con_dni():

    try: 
        return DATABASE.session.query(Reserva, Usuario.dni).join(Usuario, Reserva.id_usuario == Usuario.id_usuario).all()
    except SQLAlchemyError as e: 
        raise


def obtener_reservas_con_id(id_usuario):
    try:
        return DATABASE.session.query(Reserva).filter(Reserva.id_usuario == id_usuario).all()
    except SQLAlchemyError as e:
        raise


def registrar_checkin(id_reserva, fecha_checkin):
    '''
    Registra el check-in para una reserva, si no hay otra reserva en curso para la misma propiedad
    '''
    try:
        reserva = DATABASE.session.query(Reserva).filter_by(id_reserva=id_reserva).first()
        if not reserva:
            raise ValueError(f"No se encontró la reserva con ID {id_reserva}")

        # Verificar que no haya otra reserva en curso con check-in registrado
        reserva_conflictiva = DATABASE.session.query(Reserva).filter(
            Reserva.id_propiedad == reserva.id_propiedad,
            Reserva.id_reserva != reserva.id_reserva,
            Reserva.fecha_check_in != None,
            Reserva.estado == "EN CURSO"
        ).first()

        if reserva_conflictiva:
            raise ValueError(
                f"La propiedad ya tiene un check-in registrado en otra reserva (ID: {reserva_conflictiva.id_reserva})."
            )

        # Registrar check-in
        reserva.fecha_check_in = fecha_checkin
        reserva.estado = "EN CURSO"
        DATABASE.session.commit()
        return reserva

    except SQLAlchemyError as e:
        print(e)
        DATABASE.session.rollback()
        raise

    
def cancelar_reserva(id_reserva): 
    ''' 
    Cancela una reserva que se encuentra en estado "ABONADA" aplicando la política de cancelación correspondiente.
    '''
    session = DATABASE.session
    try:
        result = (
            session.query(
                Reserva,
                Usuario.nombre.label('nombre_usuario'),
                Usuario.apellido.label('apellido_usuario'),
                Usuario.mail.label('mail_usuario'),
                Usuario.dni.label('dni_usuario'),
                Propiedad.id_propiedad.label('id_propiedad'),
                Propiedad.politica_cancelacion.label('politica_cancelacion')
            )
            .join(Usuario, Reserva.id_usuario == Usuario.id_usuario)
            .join(Propiedad, Reserva.id_propiedad == Propiedad.id_propiedad)
            .filter(Reserva.id_reserva == id_reserva)
            .first()
        )

        if not result:
            raise ValueError(f"No se encontró la reserva con ID {id_reserva}")
        
        reserva = result.Reserva  # instancia real de Reserva

        # Cambiar estado y guardar
        reserva.estado = "CANCELADA"
        session.commit()

        # Retornar diccionario sin incluir 'estado'
        return {
            "id_reserva": reserva.id_reserva,
            "nombre_usuario": result.nombre_usuario,
            "apellido_usuario": result.apellido_usuario,
            "mail_usuario": result.mail_usuario,
            "dni_usuario":result.dni_usuario,
            "id_propiedad": result.id_propiedad,
            "politica_cancelacion": result.politica_cancelacion,
            "fecha_inicio_reserva": reserva.fecha_inicio.isoformat() if reserva.fecha_inicio else None,
            "fecha_fin_reserva": reserva.fecha_fin.isoformat() if reserva.fecha_fin else None,
            "medio_de_pago": reserva.medio_de_pago,
            "precio_total_reserva": float(reserva.precio_total)
        }

    except Exception as e:
        print('Error en cancelar_reserva de repository', e)
        session.rollback()
        raise e
    

def registrar_checkout(id_reserva, fecha_checkout):
    '''
    registra el check-out, con la fecha recibida como parametro para la reserva con id_reserva
    '''
    try: 
        reserva = DATABASE.session.query(Reserva).filter_by(id_reserva=id_reserva).first()
        if not reserva:
            raise ValueError(f"No se encontró la reserva con ID {id_reserva}")
        
        reserva.fecha_check_out = fecha_checkout
        reserva.estado= "FINALIZADA"
        DATABASE.session.commit()
        return reserva
    except SQLAlchemyError as e: 
        print (e)
        DATABASE.session.rollback() 
        raise
    

def obtener_reservas_del_usuario(id_usuario):
    return DATABASE.session.query(Reserva).filter_by(id_usuario=id_usuario).all()

# Lista las reservas de una propiedad dado un ID
def listar_por_propiedad(id_propiedad):
    """
    Lista todas las reservas asociadas a una propiedad específica.
    """
    try:
        return DATABASE.session.query(Reserva).filter_by(id_propiedad=id_propiedad).all()
    except SQLAlchemyError as e:
        print(e)
        raise
    
def calificar_reserva(id_reserva, calificacion):
    try:
        reserva = DATABASE.session.query(Reserva).filter_by(id_reserva=id_reserva).first()
        print("------------------> reserva", reserva)
        
        reserva.calificacion = calificacion

        if not reserva:
            raise ValueError(f"No se encontró la reserva con ID {id_reserva}")

        propiedad = DATABASE.session.query(Propiedad).filter_by(id_propiedad=reserva.id_propiedad).first()

        print("------------------> propiedad", propiedad)
        if not propiedad:
            raise ValueError(f"No se encontró la propiedad con ID {propiedad.id_propiedad}")

        propiedad.total_calificaciones += 1
        propiedad.suma_calificaciones = propiedad.suma_calificaciones + calificacion
        propiedad.calificacion = propiedad.suma_calificaciones / propiedad.total_calificaciones
        
        DATABASE.session.commit()
        return propiedad
    
    except Exception as e:
        print(e)
        DATABASE.session.rollback()
        raise