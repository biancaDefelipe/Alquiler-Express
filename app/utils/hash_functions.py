import bcrypt
import secrets
 
def hashear_contra(contra):
    """
        Genera una contraseña aleatoria de 10 caracteres y la devuelve hasheada.
    """
    
    #hasheo la contraseña 
    contra_bytes = contra.encode('utf-8')
    salt = bcrypt.gensalt()
    contra_hash = bcrypt.hashpw(contra_bytes, salt)
    
    #decodifico a string para poder guardarla en la bd
    print (contra_hash.decode('utf-8'))
    return contra_hash.decode('utf-8') 

def generar_contra(): 
    #creo contraseña random
    return secrets.token_urlsafe(10)  #algo como 'djs82kaKla'
    
    
    
def verificar_contrasenia(contra_input, hash_guardado):
    """
        Verifica que ambas contraseñas sea idénticas.
        Args: 
            constra_input: contraseña ingresada por el usuario
            hash_guardado: contraseña hasheada guardada en la bd
        Returns: 
            True: si ambas coinciden.
            False: si no coinciden.
    """
    return bcrypt.checkpw(contra_input.encode('utf-8'), hash_guardado.encode('utf-8'))

def hashear_contrasenia(contra):
    """
        Recibe una contraseña ingresada por el usuario y la hashea.
        Args: 
            contra: cadena no hasheada
        Returns: 
            String
    """
    hash_bytes = bcrypt.hashpw(contra.encode('utf-8'), bcrypt.gensalt())
    # decodificar a string para poder almacenarla en la base de datos
    return hash_bytes.decode('utf-8')


# @Javi en el inicio de sesión hacer algo así, para verificar que las contraseñas coincidan
#if verificar_contrasenia(password_ingresada, usuario.contrasenia):
    # Login exitoso
#    return {"mensaje": "Login correcto"}, 200
#else:
    # Contraseña incorrecta
#   return {"error": "Contraseña incorrecta"}, 401