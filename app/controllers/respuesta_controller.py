from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from services import respuesta_service, pregunta_service
import utils.manejador_sesion as manejador_sesion

respuesta_bp = Blueprint('respuesta_bp', __name__, url_prefix='/respuesta')


@respuesta_bp.route("/responder", methods=["POST"])
def responder_pregunta():
    try:
        datos = request.get_json()
        respuesta = respuesta_service.crear_respuesta(datos)
        return jsonify({"Mensaje": "Respuesta creada con éxito", "respuesta_id": respuesta.id_respuesta}), 201
    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500


@respuesta_bp.route('/eliminar/<int:id_respuesta>', methods=['DELETE'])
def eliminar_respuesta(id_respuesta):
    sesion = manejador_sesion.ver_sesion_actual()
    if not sesion or 'id_usuario' not in sesion:
        return jsonify({"error": "No autenticado"}), 401

    try:
        respuesta= respuesta_service.obtener_respuesta_por_id(id_respuesta)
        if (respuesta):
            
            pregunta = pregunta_service.obtener_pregunta_por_id(respuesta.id_pregunta)
            if not pregunta:
                return jsonify({"error": "No se pudo eliminar la respuesta."}), 404
            eliminado = respuesta_service.eliminar_respuesta(id_respuesta, pregunta)
            if eliminado:
                return jsonify({"mensaje": "Respuesta eliminada correctamente"}), 200
            else:
                return jsonify({"error": "No se pudo eliminar la respuesta"}), 500
        else: 
            return jsonify({"error": "No se pudo eliminar la respuesta"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500