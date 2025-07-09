from sqlalchemy.exc import SQLAlchemyError
from flask import request, Blueprint, jsonify, render_template
import services.usuario_service as usuario_service
from exceptions.mail_invalido import mail_invalido
from exceptions.mail_eliminado import mail_eliminado
from exceptions.dni_eliminado import dni_eliminado
from exceptions.dni_invalido import dni_invalido
from exceptions.contrasenia_actual_incorrecta import contrasenia_actual_incorrecta
from exceptions.envio_mail_error import envio_mail_error
from exceptions.validacion_error import validacion_error
import utils.manejador_sesion as manejador_sesion

USUARIO_BP = Blueprint('Usuario', __name__, url_prefix='/usuario')

# Endpoint para dar de alta a un usuario
@USUARIO_BP.route("/alta", methods=["POST"])
def alta_usuario():
    try:
        datos_usuario = request.get_json()
        usuario_service.alta_usuario(datos_usuario)
        
        return jsonify({'Mensaje': 'Usuario creado con exito.'}), 201 
    
    except mail_invalido as e:
        return jsonify({'Mail-Invalido': str(e), 'Code': "MAIL-INVALIDO"}), 400 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except dni_invalido as e:
        return jsonify({'Dni-Invalido': str(e), 'Code': "DNI-INVALIDO"}), 400 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except envio_mail_error as e: 
        return jsonify({'Envio-Mail-Error': str(e), 'Code': "ENVIO-MAIL-ERROR"}), 502 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except mail_eliminado as e: 
        return jsonify({'Mail-Eliminado-Error': str(e), 'Code': "MAIL-ELIMINADO-ERROR"}), 501 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except dni_eliminado as e: 
        return jsonify({'Mail-Eliminado-Error': str(e), 'Code': "DNI-ELIMINADO-ERROR"}), 501 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except Exception as e:
        return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    


@USUARIO_BP.route("/getall", methods=["GET"])
def obtener_usuarios():
    """
        Endpoint para obtener todos los usuario de la BD
    """
    try:
        usuarios = usuario_service.obtener_usuarios() # Le pasa la pelota a la funcion del service.
        respuesta = {}
        if usuarios is not None:
            respuesta = [usuario.serialize() for usuario in usuarios] # Le da formato json a la respuesta que se obtuvo.
        return jsonify(respuesta), 200 # Mensaje final de exito. Para que el FE sepa que se completó la tarea en el BE.
    
    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except Exception as e:
        return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.


@USUARIO_BP.route("/get", methods=["GET"])
def obtener_un_solo_usuario():
    """
        Endpoint para obtener un usuario específico
    """
    try:
        mail = request.args.get('mail') 
        usuario = usuario_service.obtener_un_solo_usuario(mail) 
        respuesta = {}
        if usuario is not None:
            respuesta = usuario.serialize() 
        return jsonify(respuesta), 200 

    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500  
    except Exception as e:
       return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500 
   
   
# Endpoint para enviar correo 2fa
@USUARIO_BP.route("/enviar_correo_2fa", methods=["POST"])
def enviar_correo_2fa():
    try:
        data_2fa = request.get_json()
        print('-------------------------------------- data_2fa:', data_2fa)
        usuario_service.enviar_mail_2fa(data_2fa["mail"], data_2fa["codigo"])
        return jsonify({'Mensaje': 'Mensaje enviado.'}), 201
    except mail_invalido as e:
        print("Error en el mail 2fa: ", e)
        return jsonify({'Mail-Invalido': str(e), 'Code': "MAIL-INVALIDO"}), 400
    except SQLAlchemyError as e:
        print("Error en el sql 2fa: ", e)
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500
    except Exception as e:
        print("Error general 2fa: ", e)
        return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500


@USUARIO_BP.route("/iniciar_sesion", methods=["GET"])
def iniciar_sesion():
    """
        Endpoint para manejar el inicio de sesion de un usuario
    """
    try:
        mail = request.args.get('mail')
        contrasenia = request.args.get('contrasenia')
        usuario = usuario_service.iniciar_sesion(mail, contrasenia)
        if usuario:
            manejador_sesion.iniciar_sesion(usuario['id_usuario'], usuario['rol'])
            return jsonify({'Usuario': usuario, 'validacion': True}), 200
        else:
            return jsonify({'Usuario': None, 'validacion': False}), 200
        
    except mail_invalido as e:
        return jsonify({'ValueError': str(e), 'Code': "MAIL-INVALIDO"}), 400  
    except validacion_error as e:
        return jsonify({'ValueError': str(e), 'Code': "VALIDACION-ERROR"}), 400  
    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500  
    except Exception as e:
       return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500
    

@USUARIO_BP.route("/cerrar_sesion", methods=["GET"])
def cerrar_sesion():
    """
        Endpoint para manejar el cierre de sesion de un usuario
    """
    try:
        manejador_sesion.limpiar_sesion()
        return jsonify({}), 200 
    except Exception as e:
       return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500 


@USUARIO_BP.route("/cambiar_rol", methods=["POST"])
def cambiar_rol():
    """
        Endpoint para cambiar el rol de un usuario empleado o gerente.
    """
    try:
        usuario_mail = request.args.get('mail')
        usuario_service.cambiar_rol_usuario(usuario_mail)
        return jsonify({}), 200
    
    except mail_invalido as e:
        return jsonify({'ValueError': str(e), 'Code': "MAIL-INVALIDO"}), 400  
    except Exception as e:
       return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500 

    
# Endpoint que obtiene todos los empleados y los gerentes: Listar Personal
@USUARIO_BP.route("/getEmpleadosGerentes", methods=["GET"]) 
def obtener_usuarios_empleados_y_gerentes():
    empleados = usuario_service.listar_personal()

    sesion_actual = manejador_sesion.ver_sesion_actual()
    usuario_actual = usuario_service.obtener_un_solo_usuario_por_ID(sesion_actual["id_usuario"])
    print(usuario_actual)
    mail_usuario_actual = usuario_actual.mail

    return render_template("listado_empleados.html",empleados = empleados, mail_usuario_actual = mail_usuario_actual)

@USUARIO_BP.route('/tabla_empleados')
def tabla_empleados():
    empleados = usuario_service.listar_personal()  # tu lógica para obtener los empleados

    sesion_actual = manejador_sesion.ver_sesion_actual()
    usuario_actual = usuario_service.obtener_un_solo_usuario_por_ID(sesion_actual["id_usuario"])
    print(usuario_actual)
    mail_usuario_actual = usuario_actual.mail

    return render_template('tabla_empleados.html', empleados = empleados, mail_usuario_actual = mail_usuario_actual)

@USUARIO_BP.route('/get_lista_inquilinos')
def tabla_inquilinos():
    # inquilinos = usuario_service.listar_inquilinos() 
    dni = request.args.get('dni')
    if dni:
        inquilinos = usuario_service.buscar_inquilinos_por_dni(dni)
    else:
        inquilinos = usuario_service.listar_inquilinos() 
    return render_template('listado_inquilinos.html', inquilinos=inquilinos)

# Endpoint que elimina logicamente un usuario con mail especifico.
@USUARIO_BP.route("/eliminar", methods=["DELETE"])
def eliminar_usuario():
    try:
        mail = request.args.get('mail') # Obtiene el dato que se pasa como parametro.
        usuario_service.eliminar_usuario(mail) # Le pasa la pelota a la funcion del service.
        return jsonify({'Mensaje': 'Usuario eliminado con exito.'}), 200 # Mensaje final de exito. Para que el FE sepa que se completó la tarea en el BE.
    
    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e)}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.    
    except ValueError as e:
        return jsonify({'ValueError': str(e)}), 400 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except Exception as e:
        return jsonify({'Error': str(e)}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.


@USUARIO_BP.route("/modificar", methods=["PUT"])
def modificar_usuario():
    try:
        id_usuario = request.args.get('id_usuario') # Obtiene el dato que se pasa como parametro.
        datos_actualizados = request.get_json() # Obtiene el objeto en formato json que se pasa como parametro.
        usuario_service.modificar_usuario(id_usuario, datos_actualizados) # Le pasa la pelota a la funcion del service.
        return jsonify({'Mensaje': 'Usuario modificado con exito.'}), 200 # Mensaje final de exito. Para que el FE sepa que se completó la tarea en el BE.

    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except ValueError as e:
        return jsonify({'ValueError': str(e), 'Code': "ID-INEXISTENTE"}), 400 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except Exception as e:
        return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    

@USUARIO_BP.route("/modificar_mail_empleado", methods=["PUT"])
def modificar_mail_empleado():
    try:
        mail_actual = request.args.get('mail_actual') # Obtiene el dato que se pasa como parametro.
        nuevo_mail = request.args.get('nuevo_mail') # Obtiene el dato que se pasa como parametro.
        usuario_service.modificar_mail_empleado(mail_actual, nuevo_mail) # Le pasa la pelota a la funcion del service.
        return jsonify({'Mensaje': 'Usuario modificado con exito.'}), 200 # Mensaje final de exito. Para que el FE sepa que se completó la tarea en el BE.

    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except mail_invalido as e:
        return jsonify({'Mail-Invalido': str(e), 'Code': "MAIL-INVALIDO"}), 400 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except ValueError as e:
        return jsonify({'ValueError': str(e), 'Code': "MAIL-EXISTENTE"}), 400 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except Exception as e:
        return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.



@USUARIO_BP.route("/cambiar_contrasenia", methods=["PUT"])
def cambiar_contrasenia():
    try:
        id_usuario = request.args.get('id_usuario') # Obtiene el dato que se pasa como parametro.
        datos_form_contrasenia = request.get_json() # Obtiene el objeto en formato json que se pasa como parametro.
        usuario_service.cambiar_contrasenia(id_usuario, datos_form_contrasenia) # Le pasa la pelota a la funcion del service.
        return jsonify({'Mensaje': 'Contrasenia modificada con exito.'}), 200 # Mensaje final de exito. Para que el FE sepa que se completó la tarea en el BE.

    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except contrasenia_actual_incorrecta as e:
        return jsonify({'ValueError': str(e), 'Code': "CONTRASENIA-ACTUAL-INVALIDA"}), 400 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except ValueError as e:
        return jsonify({'ValueError': str(e), 'Code': "ID-INEXISTENTE"}), 400 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.
    except Exception as e:
        return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500 # Mensaje final de error. Para que el FE sepa que hubo un error en el BE.


@USUARIO_BP.route("/getUsuarioPorID", methods=["GET"]) 
def obtener_un_solo_usuario_por_ID():
    try:
        id = request.args.get('id')
        usuario = usuario_service.obtener_un_solo_usuario_por_ID(id) 
        respuesta = {}
        if usuario is not None:
            respuesta = usuario.serialize() 
            print(usuario)
        return jsonify(respuesta), 200 

    except SQLAlchemyError as e:
        return jsonify({'DatabaseError': str(e), 'Code': "DATABASE-ERROR"}), 500  
    except Exception as e:
       return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500 
    

@USUARIO_BP.route("/ver_sesion_actual", methods= ["GET"])
def ver_sesion_actual():
    try:
        # id = request.args.get('id_usuario')
        sesion_actual = manejador_sesion.ver_sesion_actual()

        return jsonify(sesion_actual), 200 

    except Exception as e:
       return jsonify({'Error': str(e), 'Code': "GENERIC-ERROR"}), 500 
   