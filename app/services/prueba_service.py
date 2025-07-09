import repositories.prueba_repository as prueba_repository


def obtener_usuarios():
    return prueba_repository.obtener_todos_los_usuarios() # Le pasa la pelota al metodo del repository.

def obtener_un_solo_usuario(mail):
    return prueba_repository.obtener_usuario_con_mail(mail) # Le pasa la pelota al metodo del repository.

def alta_usuario(datos_usuario):
    # Valida que no exista o lanza un error.
    usuario = prueba_repository.obtener_usuario_con_mail(datos_usuario["mail"])
    if usuario:
        raise ValueError(f"Ya existe un usuario con mail {usuario.mail}")
    else:
        prueba_repository.alta_usuario(datos_usuario) # Da de alta al usuario con los datos recibidos.

def eliminar_usuario(mail):
    # Valida que exista o lanza un error.
    usuario = prueba_repository.obtener_usuario_con_mail(mail)
    if not usuario:
        raise ValueError(f"Usuario con mail {mail} no encontrado")
    else:
        prueba_repository.eliminar_usuario(usuario) # Elimina al usuario que encontro.

def modificar_usuario(mail, datos_actualizados):
    # Valida que exista o lanza un error.
    usuario = prueba_repository.obtener_usuario_con_mail(mail)
    if not usuario:
        raise ValueError(f"Usuario con mail {mail} no encontrado")
    else:
        prueba_repository.modificar_usuario(usuario, datos_actualizados) # Modifica al usuario que encontro

