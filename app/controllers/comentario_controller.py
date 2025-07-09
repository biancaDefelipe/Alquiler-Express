from flask import Blueprint, request, jsonify
from services import comentario_service
import utils.manejador_sesion as manejador_sesion

comentario_bp = Blueprint('comentario_bp', __name__, url_prefix='/comentarios')

@comentario_bp.route('/alta', methods=['POST'])
def crear_comentario_api():
    sesion = manejador_sesion.ver_sesion_actual()
    if not sesion or 'id_usuario' not in sesion:
        return jsonify({"error": "No autenticado"}), 401

    data = request.get_json()
    id_usuario = sesion['id_usuario']
    id_reserva = data.get('id_reserva')
    texto = data.get('texto')

    print(f"DEBUG POST /comentarios/alta — id_usuario={id_usuario}, id_reserva={id_reserva}, texto={texto}")

    if not texto or not id_reserva:
        return jsonify({"error": "Faltan datos"}), 400

    try:
        comentario = comentario_service.crear_comentario(int(id_usuario), int(id_reserva), texto)
        if comentario:
            return jsonify(comentario.serialize()), 201
        else:
            return jsonify({"error": "No podés comentar esta reserva"}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@comentario_bp.route('', methods=['GET'])
def ver_comentarios_por_propiedad():
    id_propiedad = request.args.get('id_propiedad', type=int)
    if not id_propiedad:
        return jsonify({"error": "ID de propiedad requerido"}), 400
    try:
        comentarios = comentario_service.obtener_comentarios_de_propiedad(id_propiedad)
        return jsonify([c.serialize_con_usuario() for c in comentarios])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@comentario_bp.route('/<int:id_comentario>/eliminar', methods=['DELETE'])
def eliminar_comentario(id_comentario):
    sesion = manejador_sesion.ver_sesion_actual()
    if not sesion or 'id_usuario' not in sesion:
        return jsonify({"error": "No autenticado"}), 401

    id_usuario = sesion['id_usuario']
    rol_usuario = sesion['rol']


    try:
        comentario = comentario_service.obtener_comentario_por_id(id_comentario)
        if comentario is None:
            return jsonify({"error": "Comentario no encontrado"}), 404

        # Permitir si es el autor, o si es EMPLEADO o GERENTE
        if comentario.id_usuario != id_usuario and rol_usuario not in ["EMPLEADO", "GERENTE"]:
            return jsonify({"error": "No autorizado para eliminar este comentario"}), 403


        eliminado = comentario_service.eliminar_comentario(id_comentario)
        if eliminado:
            return jsonify({"mensaje": "Comentario eliminado correctamente"}), 200
        else:
            return jsonify({"error": "No se pudo eliminar el comentario"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@comentario_bp.route("/existe", methods=["GET"])
def existe_comentario_endpoint():
    id_usuario = manejador_sesion.ver_sesion_actual()["id_usuario"]
    id_reserva = request.args.get("id_reserva")
    existe = comentario_service.existe_comentario(id_usuario, id_reserva)
    return jsonify({"existe": existe}), 200