from sqlalchemy.exc import SQLAlchemyError
from flask import request, Blueprint, jsonify
import services.prueba_service as prueba_service


# Configuración inicial para todos los endpoint de este controller.
USUARIO_BP = Blueprint('Usuario', __name__, url_prefix='/usuario')
PROPIEDAD_BP = Blueprint('Propiedad', __name__, url_prefix='/propiedad')

# Endpoints de ejemplo. El FE llamará a estas funciones según corresponda.

# Endpoint que obtiene todos los usuarios.
@USUARIO_BP.route("/getall", methods=["GET"])
def obtener_usuarios():
    try:
        usuarios = prueba_service.obtener_usuarios() # Le pasa la pelota a la funcion del service.
        respuesta = {}
        if usuarios is not None:
            respuesta = [usuario.serialize() for usuario in usuarios] # Le da formato json a la respuesta que se obtuvo.
        return jsonify(respuesta), 200 # Mensaje final de exito. Para que el FE sepa que se completó la tarea en el BE.
    
    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e)}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except Exception as e:
        return jsonify({'ErrorInesperado': str(e)}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.

# Endpoint que obtiene un usuario con mail especifico.
@USUARIO_BP.route("/get", methods=["GET"])
def obtener_un_solo_usuario():
    try:
        mail = request.args.get('mail') # Obtiene el dato que se pasa como parametro.
        usuario = prueba_service.obtener_un_solo_usuario(mail) # Le pasa la pelota a la funcion del service.
        respuesta = {}
        if usuario is not None:
            respuesta = usuario.serialize() # Le da formato json a la respuesta que se obtuvo.
        return jsonify(respuesta), 200 # Mensaje final de exito. Para que el FE sepa que se completó la tarea en el BE.

    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e)}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except Exception as e:
        return jsonify({'ErrorInesperado': str(e)}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.

# Endpoint que da de alta un nuevo usuario.
@USUARIO_BP.route("/alta", methods=["POST"])
def alta_usuario():
    try:
        datos_usuario = request.get_json() # Obtiene el objeto en formato json que se pasa como parametro.
        prueba_service.alta_usuario(datos_usuario) # Le pasa la pelota a la funcion del service.
        return jsonify({'Mensaje': 'Usuario creado con exito.'}), 201 # Mensaje final de exito. Para que el FE sepa que se completó la tarea en el BE.

    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e)}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except ValueError as e:
        return jsonify({'ValueError': str(e)}), 400 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except Exception as e:
        return jsonify({'Error': str(e)}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.

# Endpoint que elimina un usuario con mail especifico.
@USUARIO_BP.route("/eliminar", methods=["DELETE"])
def eliminar_usuario():
    try:
        mail = request.args.get('mail') # Obtiene el dato que se pasa como parametro.
        prueba_service.eliminar_usuario(mail) # Le pasa la pelota a la funcion del service.
        return jsonify({'Mensaje': 'Usuario eliminado con exito.'}), 201 # Mensaje final de exito. Para que el FE sepa que se completó la tarea en el BE.
    
    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e)}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.    
    except ValueError as e:
        return jsonify({'ValueError': str(e)}), 400 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except Exception as e:
        return jsonify({'Error': str(e)}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.


@USUARIO_BP.route("/modificar", methods=["PUT"])
def modificar_usuario():
    try:
        mail = request.args.get('mail') # Obtiene el dato que se pasa como parametro.
        datos_actualizados = request.get_json() # Obtiene el objeto en formato json que se pasa como parametro.
        prueba_service.modificar_usuario(mail, datos_actualizados) # Le pasa la pelota a la funcion del service.
        return jsonify({'Mensaje': 'Usuario modificado con exito.'}), 201 # Mensaje final de exito. Para que el FE sepa que se completó la tarea en el BE.

    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e)}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except ValueError as e:
        return jsonify({'ValueError': str(e)}), 400 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except Exception as e:
        return jsonify({'Error': str(e)}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.


#  Faltan testear !!!
# Endpoint que obtiene todos las propiedades
@PROPIEDAD_BP.route("/getallPropiedades", methods=["GET"])
def obtener_propiedades():
    try:
        propiedades = prueba_service.obtener_propiedades()
        respuesta = {}
        if propiedades is not None:
            respuesta = [prop.serialize() for prop in propiedades] 
        return jsonify(respuesta), 200 
    
    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e)}), 500 
    except Exception as e:
        return jsonify({'ErrorInesperado': str(e)}), 500
    
