# Acá va todo lo que sea logica de negocio y validaciones
# que este relacionado a las reservas.
import repositories.reserva_repository as reserva_repository
import repositories.propiedad_repository as propiedad_repository
from utils.manejador_fechas import formatear_fecha_iso_a_custom
from datetime import datetime
from utils.mail_functions import *


def realizar_reserva(datos_reserva):
    try:
        print('-------datos reserva pre', datos_reserva)
        # supongamos que datos_reserva es el dict que viene en el POST
        fecha_inicio_str = datos_reserva["fecha_inicio"]   # e.g. "2025-05-30"
        fecha_fin_str    = datos_reserva["fecha_fin"]      # e.g. "2025-05-21"

        # convertimos a date
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
        fecha_fin    = datetime.strptime(fecha_fin_str,    "%Y-%m-%d").date()
        
        datos_reserva["fecha_inicio"] = fecha_inicio
        datos_reserva["fecha_fin"]    = fecha_fin
        
        if datos_reserva.get("fecha_check_in"):
            datos_reserva["fecha_check_in"]  = datetime.strptime(datos_reserva["fecha_check_in"],  "%Y-%m-%d").date()
        else:
            datos_reserva["fecha_check_in"]  = None
            
        if datos_reserva.get("fecha_check_out"):
            datos_reserva["fecha_check_out"] = datetime.strptime(datos_reserva["fecha_check_out"], "%Y-%m-%d").date()
        else:
            datos_reserva["fecha_check_out"] = None
        
        reserva = reserva_repository.realizar_reserva(datos_reserva)
        print('reserva creada en service: ', reserva)
        return reserva
    except Exception as e:
        print(e)
        raise
    
    
def obtener_reservas():
    try:
        return reserva_repository.obtener_reservas()
    except Exception as e:
        print(e)
        raise
    
    
def obtener_reserva(id):
    try:
        return reserva_repository.obtener_reserva(id)
    except Exception as e:
        print(e)
        raise
    
def enviar_mail_reserva_exitosa_service(data):
    print('**** inicio enviar_mail_reserva_exitosa_service ****')
    mailDestinatario = data["datos_usuario"]["mail"]
    mail_enviar_reserva_alquiler(mailDestinatario, mail_msj_reserva_alquiler(data["datos_reserva"], data["datos_usuario"], data["datos_propiedad"]))
    
def listar_reservas_con_dni():
    try: 
        reservas = reserva_repository.obtener_reservas_con_dni()
        resultado = []

        for reserva, dni in reservas:
            r = reserva.serialize()
            r["dni_inquilino"] = dni
            del r["id_usuario"]

            r["fecha_check_in"] = formatear_fecha_iso_a_custom(r.get("fecha_check_in"))
            r["fecha_check_out"] = formatear_fecha_iso_a_custom(r.get("fecha_check_out"))

            resultado.append(r)

        return resultado
    except Exception as e: 
        print(e)
        raise


def listar_reservas_con_id(id):
    try: 
        reservas = reserva_repository.obtener_reservas_con_id(id)
        resultado = []

        for reserva in reservas:
            r = reserva.serialize()
            del r["id_usuario"]

            r["fecha_check_in"] = formatear_fecha_iso_a_custom(r.get("fecha_check_in"))
            r["fecha_check_out"] = formatear_fecha_iso_a_custom(r.get("fecha_check_out"))

            resultado.append(r)

        return resultado
    
    except Exception as e: 
        print(e)
        raise

    
def registrar_checkin(id_reserva):
    try:
        fecha_actual = datetime.now()  # datetime object, no string
        reserva=reserva_repository.registrar_checkin(id_reserva, fecha_actual)
        propiedad_repository.cambiar_estado_propiedad(reserva.id_propiedad, "OCUPADA")
        return fecha_actual
    except Exception as e: 
        print (e)
        raise 

def registrar_checkout(id_reserva):
    try:
        fecha_actual = datetime.now()  # datetime object, no string
        reserva=reserva_repository.registrar_checkout(id_reserva, fecha_actual)
        propiedad_repository.cambiar_estado_propiedad(reserva.id_propiedad, "EN LIMPIEZA")
        return fecha_actual
    except Exception as e: 
        print (e)
        raise
    
    
def cancelar_reserva(id_reserva, cancel_type): 
    try: 
        data=reserva_repository.cancelar_reserva(id_reserva)
        print (data)
        if (data): 
            try:
                enviar_mail_cancelacion_exitosa_service(data, cancel_type)
                return data
            except Exception as e: 
                print ('error en enviar_mail_cancelacion_exitosa_service de service', e)
                raise 
    except Exception as e: 
        print ('error en cancelar_reserva de service', e)
        raise 
    
    
def enviar_mail_cancelacion_exitosa_service(data, cancel_type):
    print('**** inicio enviar_mail_reserva_cancelada_service ****')
    mailDestinatario = data["mail_usuario"]
    mail_enviar_cancelacion_alquiler(mailDestinatario, data, cancel_type)
    

def obtener_reservas_del_usuario(id_usuario):
    try:
        return reserva_repository.obtener_reservas_del_usuario(id_usuario)
    except Exception as e:
        print(e)
        raise

# Lista las reservas de una propiedad dado un ID
def listar_por_propiedad(id_propiedad):
    try:
        return reserva_repository.listar_por_propiedad(id_propiedad)
    except Exception as e:
        print(e)
        raise
    
    
def calificar_reserva(id_reserva, calificacion):
    try:
        return reserva_repository.calificar_reserva(id_reserva, calificacion)
    except Exception as e:
        print(e)
        raise