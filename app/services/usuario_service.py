import repositories.prueba_repository as prueba_repository
import repositories.usuario_repository as usuario_repository
from exceptions.mail_invalido import mail_invalido
from exceptions.mail_eliminado import mail_eliminado
from exceptions.dni_eliminado import dni_eliminado
from exceptions.dni_invalido import dni_invalido
from exceptions.contrasenia_actual_incorrecta import contrasenia_actual_incorrecta
from exceptions.envio_mail_error import envio_mail_error
from exceptions.validacion_error import validacion_error
from utils.hash_functions import hashear_contra, generar_contra, verificar_contrasenia
from utils.mail_functions import *

def alta_usuario(datos_usuario):
    usuario_mail = usuario_repository.obtener_usuario_con_mail(datos_usuario["mail"])
    usuario_dni= usuario_repository.obtener_usuario_con_dni(datos_usuario["dni"])
    
    if (usuario_dni):
        if (usuario_dni.eliminado == "NO"):
            raise dni_invalido(usuario_dni.dni)
        
        elif (usuario_dni.eliminado == "SI"):
            raise dni_eliminado(usuario_dni.dni)
    
    if (usuario_mail):
        if (usuario_mail.eliminado == "NO"):
            raise mail_invalido(usuario_mail.mail)
        
        elif (usuario_mail.eliminado == "SI"):
            raise mail_eliminado(usuario_mail.mail)
        
    try: 
        contra_sin_hash= generar_contra()
        contra_hash=hashear_contra(contra_sin_hash)
        msj =msj_registro(datos_usuario['nombre'], contra_sin_hash)
        enviar_mail_registro(datos_usuario, msj)
        usuario_repository.alta_usuario(datos_usuario, contra_hash) # Da de alta al usuario con los datos recibidos.

    except Exception as e: 
        print (e)
        raise envio_mail_error(datos_usuario["mail"])
        
            
        
def obtener_usuarios():
    return usuario_repository.obtener_todos_los_usuarios() # Le pasa la pelota al metodo del repository.

def obtener_un_solo_usuario(mail):
    """
        Llama a la función del repository que busca a un usuario por mail. 
        Arg: 
            mail(String): mail del usuario buscado.
        Returns: 
            Usuario: si se encuentra al usuario.
            None: si no encuentra al usuario
    """
    return usuario_repository.obtener_usuario_con_mail(mail) # Le pasa la pelota al metodo del repository.

def iniciar_sesion(mail, contrasenia):
    """
        Valida que exista un usuario con el mail ingresado, y que su contrasenia sea coincida con la ingresada.
        
        Params: 
            mail(String): mail del usuario buscado.
            contrasenia(String): contrasenia que se va a validar.
        Returns: 
            Usuario: si lo encuentra y la contrasenia coincide con la ingresada.
            None: si no encuentra al usuario
        Exception:
            ValueError: si el mail no está registrado en el sistema.
    """
    usuario = usuario_repository.obtener_solo_usuario_sin_contrasenia(mail)
    if (not usuario) or (usuario["eliminado"] == 'SI'):
        raise mail_invalido(mail)
    else:
        hash_guardado = usuario_repository.obtener_contrasenia_usuario(mail)
        if verificar_contrasenia(contrasenia, hash_guardado):
            rol_usuario = usuario["rol"]
            
            if rol_usuario == "INQUILINO" or rol_usuario == "EMPLEADO":
                return usuario
            elif rol_usuario == "GERENTE":
                # Acá mando el mail para  validar factor autenticación???
                return usuario
        else:
            return None


def eliminar_usuario(mail):
    # Valida que exista o lanza un error.
    usuario = usuario_repository.obtener_usuario_con_mail(mail)
    if not usuario:
        raise ValueError(f"Usuario con mail {mail} no encontrado")
    else:
        usuario_repository.eliminar_logico_usuario(usuario.id_usuario) # Elimina al usuario que encontro.

def modificar_usuario(id_usuario, datos_actualizados):
    # Valida que exista o lanza un error.
    usuario = usuario_repository.obtener_usuario_con_id(id_usuario)
    if not usuario:
        raise ValueError(f"Usuario con id {id_usuario} no encontrado")
    else:
       usuario_repository.modificar_usuario(usuario, datos_actualizados) # Modifica al usuario autenticado


def cambiar_contrasenia(id_usuario, datos_actualizados):
    # Valida que exista o lanza un error.
    usuario = usuario_repository.obtener_usuario_con_id(id_usuario)
    if not usuario:
        raise ValueError(f"Usuario con id {id_usuario} no encontrado")
    else:
        contrasenia_actual_payload = datos_actualizados["contrasenia_actual"]
        nueva_contrasenia_payload = datos_actualizados["nueva_contrasenia"]
        repetir_contrasenia_payload = datos_actualizados["repetir_contrasenia"]
        
        contrasenia_actual_db = usuario_repository.obtener_contrasenia_usuario_con_id(id_usuario)        
        
        if verificar_contrasenia(contrasenia_actual_payload, contrasenia_actual_db) and (nueva_contrasenia_payload == repetir_contrasenia_payload):
            nueva_contrasenia_hash = hashear_contra(nueva_contrasenia_payload)
            usuario_repository.cambiar_contrasenia(usuario, nueva_contrasenia_hash) # Modifica al usuario autenticado
        else:
            raise contrasenia_actual_incorrecta(f"La contrasenia {contrasenia_actual_payload} es incorrecta.")


def modificar_mail_empleado(mail_actual, nuevo_mail):
    # Valida que exista o lanza un error.
    usuario = usuario_repository.obtener_usuario_con_mail(mail_actual)
    if not usuario:
        raise mail_invalido(mail_actual)
    else:
        usuario_mail = usuario_repository.obtener_usuario_con_mail(nuevo_mail)
        if not usuario_mail:
            try: 
                contra_sin_hash= generar_contra()
                contra_con_hash = hashear_contra(contra_sin_hash)
                msj = msj_modificar_mail(usuario.nombre, contra_sin_hash)
                enviar_mail_modificacion({'mail': nuevo_mail}, msj)
                
            except Exception as e: 
                print (e)
                raise envio_mail_error(usuario_mail.mail)
            
            usuario_repository.modificar_email_empleado(usuario, nuevo_mail, contra_con_hash)
        else:
            raise ValueError(f"Ya existe un usuario con el mail {nuevo_mail} en el sistema.")


def enviar_mail_2fa(mail, codigo):
    print(codigo)
    mail_enviar_2fa(mail, mail_msj_2fa(codigo))

def listar_personal():
    return usuario_repository.obtener_personal()

def listar_inquilinos():
    return usuario_repository.obtener_inquilinos()


def cambiar_rol_usuario(usuario_mail):
    usuario = usuario_repository.obtener_usuario_con_mail(usuario_mail)
    if not usuario:
        raise mail_invalido()
    else:
        if usuario.rol == "EMPLEADO":
            usuario_repository.cambiar_rol_usuario(usuario, "GERENTE")

        elif usuario.rol == "GERENTE":
            usuario_repository.cambiar_rol_usuario(usuario, "EMPLEADO")

            
def obtener_un_solo_usuario_por_ID(id):
    return usuario_repository.obtener_usuario_con_id(id) 

def buscar_inquilinos_por_dni(dni):
    return usuario_repository.buscar_por_dni(dni)