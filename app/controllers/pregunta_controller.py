from sqlalchemy.exc import SQLAlchemyError
from flask import request, Blueprint, jsonify
import services.pregunta_service as pregunta_service
from flask_cors import CORS
from utils import manejador_sesion

PREGUNTA_BP = Blueprint('Pregunta', __name__, url_prefix='/pregunta')
CORS(PREGUNTA_BP)

@PREGUNTA_BP.route('/alta/<int:id_propiedad>', methods=["POST"])
def alta_pregunta(id_propiedad):
    try:
        datos_json = request.get_json()
        sesion = manejador_sesion.ver_sesion_actual()

        datos = {
            "pregunta": datos_json["pregunta"],
            "id_usuario": sesion["id_usuario"],
            "id_propiedad": id_propiedad
        }

        pregunta = pregunta_service.alta_pregunta(datos)
        return jsonify({
            "Mensaje": "Pregunta creada con éxito",
            "pregunta_id": pregunta.id_pregunta
        }), 201

    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500
    except Exception as e:
        return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500


@PREGUNTA_BP.route('/preguntas_respuestas/<int:id_propiedad>',  methods=["GET"])
def obtener_preguntas_y_respuestas(id_propiedad):
    try:
        preguntas = pregunta_service.obtener_todas_preguntas(id_propiedad)
        respuesta = []
        print("Contenido de preguntas:", preguntas)
        print("Tipo:", type(preguntas))

        for pregunta, respuesta_obj in preguntas:
            item = pregunta.serialize()  # ESTA LÍNEA ES FUNDAMENTAL
            if respuesta_obj is not None:
                item['respuesta'] = respuesta_obj.serialize()
            else:
                item['respuesta'] = None
            respuesta.append(item)

        return jsonify(respuesta), 200

    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500
    except Exception as e:
        return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500


@PREGUNTA_BP.route('/eliminar/<int:id_pregunta>', methods=['DELETE'])
def eliminar_pregunta(id_pregunta):
    sesion = manejador_sesion.ver_sesion_actual()
    if not sesion or 'id_usuario' not in sesion:
        return jsonify({"error": "No autenticado"}), 401

    id_usuario = sesion['id_usuario']

    try:
        pregunta = pregunta_service.obtener_pregunta_por_id(id_pregunta)
        if not pregunta:
            return jsonify({"error": "Pregunta no encontrada"}), 404

        #if pregunta.id_usuario != id_usuario:
        #    return jsonify({"error": "No autorizado para eliminar esta pregunta"}), 403

        eliminado = pregunta_service.eliminar_pregunta_y_respuesta_si_corresponde(id_pregunta)
        if eliminado:
            return jsonify({"mensaje": "Pregunta (y respuesta, si existía) eliminada correctamente"}), 200
        else:
            return jsonify({"error": "No se pudo eliminar la pregunta"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
