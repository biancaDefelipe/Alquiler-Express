# Acá va todo lo que sea endpoints que
# este relacionado a las reservas.

from sqlalchemy.exc import SQLAlchemyError
from flask import request, Blueprint, jsonify
import services.reserva_service as reserva_service
from flask_cors import CORS
from flask import request, Blueprint, jsonify, render_template
import services.reserva_service as reserva_service
from exceptions.envio_mail_error import envio_mail_error
import utils.manejador_sesion as manejador_sesion
from services import comentario_service

RESERVA_BP = Blueprint('Reserva', __name__, url_prefix='/reserva')
CORS(RESERVA_BP) # Aplica CORS a todas las rutas de este Blueprint


@RESERVA_BP.route("/alta", methods=["POST"])
def alta_reserva():
    try:
        datos_reserva = request.get_json() 
        reserva = reserva_service.realizar_reserva(datos_reserva)
        print('reserva creada en controller: ', reserva)
        return jsonify({'Mensaje': 'Reserva creada con exito.', 'reserva_id': reserva.id_reserva}), 201
    
    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500
    
    
@RESERVA_BP.route("/getall", methods=["GET"])
def obtener_reservas():
    try:
        reservas = reserva_service.obtener_reservas() 
        respuesta = {}
        if reservas is not None:
            respuesta = [reserva.serialize() for reserva in reservas] 
        return jsonify(respuesta), 200 
    
    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500
    
    
@RESERVA_BP.route("/get", methods=["GET"])
def obtener_reserva():
    try:
        id = request.args.get('id') 
        reserva = reserva_service.obtener_reserva(id) 
        respuesta = {}
        if reserva is not None:
            respuesta = reserva.serialize() 
        return jsonify(respuesta), 200 
    
    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500
    
# Endpoint para enviar correo de reserva exitosa
@RESERVA_BP.route("/enviar_mail_reserva_exitosa", methods=["POST"])
def enviar_mail_reserva_exitosa():
    try:
        print('**** inicio enviar_mail_reserva_exitosa ****')
        data = request.get_json()
        print('-------------------------------------- data:', data)
        reserva_service.enviar_mail_reserva_exitosa_service(data)
        return jsonify({'Mensaje': 'Mensaje enviado.'}), 201
    
    except SQLAlchemyError as e:
        print("Error en el sql: ", e)
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500
    except Exception as e:
        print("Error general: ", e)
        return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500
    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500


#agregado bian
@RESERVA_BP.route("/getReservas", methods=["GET"])
def obtener_reservas_con_dni():
    try: 
        reservas = reserva_service.listar_reservas_con_dni()
        return render_template("listado_reservas.html", reservas=reservas)
    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500


# Agregado por Javi para HU/ver_alquileres.
@RESERVA_BP.route("/reservas_usuario", methods=["GET"])
def obtener_reservas_usuario():
    try:
        sesion = manejador_sesion.ver_sesion_actual()
        reservas = reserva_service.listar_reservas_con_id(sesion["id_usuario"])
        return render_template("ver_alquileres_inquilino.html", reservas=reservas)
    
    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500
    except Exception as e:
        return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500


@RESERVA_BP.route('/checkin/<int:id_reserva>', methods=['POST'])
def registrar_checkin(id_reserva):
    try:
        fecha = reserva_service.registrar_checkin(id_reserva)
        if fecha:
            return jsonify({"Success": True, "fecha_check": fecha.strftime("%d/%m/%Y %H:%M"), "nuevo_estado": "EN CURSO"}), 200
        return jsonify({'GenericError': "Date error", 'Code': "GENERIC-ERROR"}), 400 
    except SQLAlchemyError as e: 
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500 
    except ValueError as e: 
        return jsonify({'ValueError': str(e), 'Code': "VALUE-ERROR"}), 409
  
  
@RESERVA_BP.route('/checkout/<int:id_reserva>', methods=['POST'])
def registrar_checkout(id_reserva):
    try:
        fecha = reserva_service.registrar_checkout(id_reserva)
        if fecha:
            return jsonify({"Success": True, "fecha_check": fecha.strftime("%d/%m/%Y %H:%M"), "nuevo_estado": "FINALIZADA"}), 200
        return jsonify({'GenericError': "Date error", 'Code': "GENERIC-ERROR"}), 400 
    except SQLAlchemyError as e: 
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500
    
    
# Cancelar reserva con ID
@RESERVA_BP.route('/cancelar/<int:id_reserva>', methods=['POST'])
def cancelar_reserva(id_reserva):
    try:
        payload = request.get_json(silent=True) or {}
        cancel_type = payload.get('cancel_type', 'CANCELACION_USUARIO')  # Default 'CANCELACION_USUARIO' si no viene el cancel_type
        data = reserva_service.cancelar_reserva(id_reserva, cancel_type) 
        if (data):
            return jsonify({"Success": True, "Reserva":data["id_reserva"],"nuevo_estado": "CANCELADA"}), 201
        else:
            return jsonify({'Mensaje': 'Ocurrio un problem al cancelar la reserva'}), 500

    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500
    
    
# Lista las reservas de una propiedad dado un ID
@RESERVA_BP.route('/reservas/propiedad/<int:id_propiedad>', methods=['GET'])
def reservas_por_propiedad(id_propiedad):
    try:
        lista_reservas = reserva_service.listar_por_propiedad(id_propiedad)
        data = [r.serialize() for r in lista_reservas]
        return jsonify(reservas=data), 200
    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500
    

@RESERVA_BP.route('/calificar/<int:id_reserva>', methods=['POST'])
def calificar_reserva(id_reserva):
    try:
        payload = request.get_json(silent=True) or {}
        calificacion = payload.get('calificacion', None)
        calificacion = int(calificacion)
        
        if calificacion is None:
            return jsonify({'Error': 'Calificación no proporcionada'}), 400
        
        reserva_service.calificar_reserva(id_reserva, calificacion)
        
        return jsonify({"Success": True, "Mensaje": "Reserva calificada exitosamente"}), 200
    
    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500
    except Exception as e:
        return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500