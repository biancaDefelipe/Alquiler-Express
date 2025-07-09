from sqlalchemy.exc import SQLAlchemyError
from flask import request, Blueprint, jsonify, render_template
import services.estadisticas_service as estadisticas_service
from exceptions.validacion_error import validacion_error

ESTADISTICAS_BP = Blueprint('Estadisticas', __name__, url_prefix='/estadisticas')


@ESTADISTICAS_BP.route("/generar", methods=["POST"])
def generar_estadistica():
    try:
        datos_estadistica = request.get_json()
        estadisticas_service.generar_estadistica(datos_estadistica)
        
        resultado = estadisticas_service.generar_estadistica(datos_estadistica)
        return jsonify(resultado), 200
    
    except validacion_error as e:
        return jsonify({'ValueError': str(e), 'Code': "VALIDACION-ERROR"}), 400
    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500
    except Exception as e:
        return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500
