from sqlalchemy.exc import SQLAlchemyError
from flask import request, Blueprint, render_template, jsonify, current_app, redirect, url_for
import services.propiedad_service as propiedad_service
from flask_cors import CORS
from werkzeug.utils import secure_filename
import utils.manejador_sesion as manejador_sesion
import os

# Configuración inicial para todos los endpoint de este controller.
PROPIEDAD_BP = Blueprint('Propiedad', __name__, url_prefix='/propiedad')

# Configuración inicial para todos los endpoint de este controller.
PROPIEDAD_BP = Blueprint('Propiedad', __name__, url_prefix='/propiedad')
CORS(PROPIEDAD_BP) # Aplica CORS a todas las rutas de este Blueprint

# Endpoint que da de alta una nueva propiedad.
@PROPIEDAD_BP.route("/alta", methods=["POST"])
def alta_propiedad():
    try:
        datos_propiedad = request.form.to_dict() # Obtiene el objeto en formato json que se pasa como parametro.
        print(datos_propiedad)
        imagen = request.files.get("imagen")
        print(imagen.filename)
        propiedad_service.alta_propiedad(datos_propiedad, imagen) # Le pasa la pelota a la funcion del service.
        return jsonify({'Mensaje': 'Propiedad creada con exito.'}), 201 # Mensaje final de exito. Para que el FE sepa que se completó la tarea en el BE.

    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': 'DATABASE-ERROR'}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except Exception as e:
        return jsonify({'Error': str(e), 'Code': 'GENERIC-ERROR'}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.


@PROPIEDAD_BP.route("/obtener", methods=["GET"])
def obtener_propiedad():
    try:
        id_propiedad = request.args.get("id")
        propiedad = propiedad_service.obtener_propiedad_con_id(id_propiedad)
        respuesta = {}
        if propiedad is not None:
            respuesta = propiedad.serialize() 
        return jsonify(respuesta), 200 

    except SQLAlchemyError as e:
        print (e)
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500        
    except Exception as e:
        return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500
    
"""
@PROPIEDAD_BP.route("/getPropiedades", methods=["GET"])
def obtener_propiedades():
    propiedades = propiedad_service.listar_propiedades() 
    return render_template("listado_propiedades.html", propiedades=propiedades)
"""

@PROPIEDAD_BP.route("/getPropiedades", methods=["GET"])
def obtener_propiedades():
    propiedades = propiedad_service.listar_propiedades()
    props_dicts = [p.serialize() for p in propiedades]
    print(props_dicts)
    sesion = manejador_sesion.ver_sesion_actual()
    if sesion['rol'] == 'GERENTE' or sesion['rol'] == 'EMPLEADO':
        return render_template("listado_propiedades.html", propiedades=propiedades, propiedades_json=props_dicts)
    else:
        return redirect(url_for('inicio'))

@PROPIEDAD_BP.route ("/getPropiedadesBusqueda", methods=["GET"])
def obtener_propiedades_buscadas():
    """
        Endpoint para obtener una lista de propiedades que cumplan con los criterios de búsqueda
    """
    try:
        localidad = request.args.get('localidad').upper()
        huespedes = request.args.get('huespedes')
        check_in = request.args.get('checkin')
        check_out = request.args.get('checkout')

        criterios_busqueda = {
            'localidad': localidad,
            'huespedes': int(huespedes) if huespedes else None,
            'check-in': check_in,
            'check-out': check_out
        }
        print(f"Criterios de búsqueda recibidos: {criterios_busqueda}")

        propiedades = propiedad_service.obtener_propiedades_buscadas(criterios_busqueda)
        respuesta = {}
        if propiedades is not None:
            respuesta = [prop.serialize() for prop in propiedades]
        return jsonify(respuesta), 200
    except SQLAlchemyError as e:
        print (e)
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500
        
    except Exception as e:
        return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500
  
  
@PROPIEDAD_BP.route("/registrarFinDeLimpieza/<int:id_propiedad>", methods=["POST"])
def registrar_fin_de_limpieza(id_propiedad):
    """
        Endpoint para registrar el fin de la limpieza de una propiedad
    """
    try:
        propiedad_service.registrar_fin_de_limpieza_service(id_propiedad)
        return jsonify({'Mensaje': 'Fin de limpieza registrado con exito.'}), 200
    except SQLAlchemyError as e:
        print (e)
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500
    except Exception as e:
        print (e)
        return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500


# /modificar?id=4 <- GET (PÁGINA WEB PARA MODIFICAR LA PROPIEDAD)
@PROPIEDAD_BP.route('/modificar', methods=['GET'])
def modificar():
    id_propiedad = request.args.get('id')
    sesion = manejador_sesion.ver_sesion_actual()
    if sesion['rol'] != 'VISITANTE':
        return render_template('modificar_propiedad.html', id=id_propiedad)
    else:
        return redirect(url_for('inicio'))
    
    
# /modificar/4 <- POST (modifica los datos de una propiedad)
@PROPIEDAD_BP.route("/modificar/<int:id_propiedad>", methods=["POST"])
def modificar_propiedad(id_propiedad):
    try:
        datos = request.form.to_dict()
        imagen = request.files.get("imagen")
        print(f"propiedad {id_propiedad}: {datos}")
        propiedad_service.modificar_propiedad_service(id_propiedad, datos, imagen)
        return jsonify({'Mensaje': 'Propiedad modificada con exito.'}), 200
    except SQLAlchemyError as e:
        print (e)
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500
    except Exception as e:
        print (e)
        return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500


@PROPIEDAD_BP.route("/eliminar/<int:id_propiedad>", methods=["DELETE"])
def eliminar_propiedad(id_propiedad):
    try:
        propiedad_service.eliminar_propiedad_service(id_propiedad)
        return jsonify({'Mensaje': 'Propiedad eliminada con exito.'}), 200
    except SQLAlchemyError as e:
        print (e)
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500
    except Exception as e:
        print (e)
        return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500