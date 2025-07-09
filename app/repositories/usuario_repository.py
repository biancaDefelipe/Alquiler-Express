from sqlalchemy.exc import SQLAlchemyError
from models import DATABASE
from models.usuario import Usuario
from datetime import datetime


def obtener_personal():
    try:
        return DATABASE.session.query(Usuario.nombre, Usuario.apellido, Usuario.dni, Usuario.mail, Usuario.telefono, Usuario.fecha_nacimiento, Usuario.rol).filter(Usuario.rol.in_(["EMPLEADO", "GERENTE"]), Usuario.eliminado == "NO").order_by(Usuario.id_usuario.desc()).all()
    
    except SQLAlchemyError as e :
        print (e)
        DATABASE.session.rollback() # Si salta una excepcion en el proceso, tengo que volver para atras los cambios que se hicieron, para no generar inconsistencias en la DB.
        raise # Propaga la excepcion, para que la pesque el controller correspondiente y avise al FE con un mensaje y codigo de error.
 
def obtener_inquilinos():
    try:
        return DATABASE.session.query(Usuario.id_usuario, Usuario.nombre, Usuario.apellido, Usuario.dni, Usuario.mail, Usuario.telefono, Usuario.fecha_nacimiento, Usuario.rol).filter(Usuario.rol.in_(["INQUILINO"])).all()
    
    except SQLAlchemyError as e :
        print (e)
        DATABASE.session.rollback() 
        raise 



def alta_usuario(datos_usuario, contra):
    """
        Genera una nueva instancia de la clase a guardar con los datos que se recibieron
        Raises:
            SQLAlchemyError: Si ocurre un error al acceder a la base de datos.
    """
    nuevo_usuario = Usuario(
        dni=datos_usuario['dni'],
        nombre=datos_usuario['nombre'],
        apellido=datos_usuario['apellido'],
        mail=datos_usuario['mail'],
        telefono=datos_usuario['telefono'],
        fecha_nacimiento=datos_usuario['fecha_nacimiento'],  # debe ser YYYY-MM-DD o usar datetime.date para formatear la fecha antes de esta etapa (en el service).
        #la contraseña se autogenera
        contrasenia=contra,  
        rol= datos_usuario['rol'].upper(),
        fecha_registro= datetime.strptime(datos_usuario['fecha_registro'], "%Y-%m-%d").date(),
        eliminado= datos_usuario['eliminado'].upper()
    )
    print(nuevo_usuario.__str__())
    try:
        DATABASE.session.add(nuevo_usuario) # Da de alta el nuevo registro.
        DATABASE.session.commit() # Commitea los cambios.

    except SQLAlchemyError as e :
        print (e)
        DATABASE.session.rollback() # Si salta una excepcion en el proceso, tengo que volver para atras los cambios que se hicieron, para no generar inconsistencias en la DB.
        raise # Propaga la excepcion, para que la pesque el controller correspondiente y avise al FE con un mensaje y codigo de error.
 
def reactivar_usuario(usuario_id, datos_usuario, contra):
    """
        Reactiva un usuario previamente eliminado, actualizando sus datos y contraseña.
        No actualiza mail ni DNI.
        Raises:
            SQLAlchemyError: Si ocurre un error al acceder a la base de datos.
    """
    try:
        # Trae la instancia existente
        usuario = DATABASE.session.get(Usuario, usuario_id)

        if usuario:
            # Actualiza los campos permitidos
            usuario.nombre = datos_usuario["nombre"]
            usuario.apellido = datos_usuario["apellido"]
            usuario.telefono = datos_usuario["telefono"]
            usuario.fecha_nacimiento = datos_usuario["fecha_nacimiento"]
            usuario.rol = datos_usuario["rol"].upper()
            usuario.contrasenia = contra
            usuario.fecha_registro= datetime.strptime(datos_usuario['fecha_registro'], "%Y-%m-%d").date(),
            usuario.eliminado = datos_usuario["eliminado"].upper()

            print(usuario.__str__())

            DATABASE.session.commit()  # Guarda los cambios
        
        else:
            DATABASE.session.rollback()
            raise ValueError(f"Usuario con id {usuario_id} no encontrado")

    except SQLAlchemyError as e:
        print(e)
        DATABASE.session.rollback()
        raise


def obtener_todos_los_usuarios():
    try:
        usuarios = DATABASE.session.query(Usuario).all() # Obtiene todos los usuarios.
        return usuarios

    except SQLAlchemyError as e:
        raise # Propaga la excepcion, para que la pesque el controller correspondiente y avise al FE con un mensaje y codigo de error.

def obtener_usuario_con_id(id_usuario):
    try:
        usuario = DATABASE.session.get(Usuario, id_usuario) # Obtiene un usuario con un id especifico. Como id_usuario es PK, se busca solo con el get()
        return usuario

    except SQLAlchemyError as e:
        raise # Propaga la excepcion, para que la pesque el controller correspondiente y avise al FE con un mensaje y codigo de error.

def buscar_por_dni(dni):
    try:
        return Usuario.query.filter_by(dni=dni).all()

    except SQLAlchemyError as e:
        raise

def obtener_usuario_con_mail(mail):    
    """
        Valida si existe un usuario con el mail recibido como parametro.
        Args: 
            mail (string): mail de un usuario.
        Returns: 
            Usuario: si se encuentra al usuario.
            None: si no encuentra al usuario.
        Raises:
            SQLAlchemyError: Si ocurre un error al acceder a la base de datos.
    """
    try:
        usuario = DATABASE.session.query(Usuario).filter_by(mail=mail).first() # Obtiene un usuario con un id especifico. Como mail no es PK, se tiene que buscar con el filter_by().first()
        return usuario

    except SQLAlchemyError as e:
        raise # Propaga la excepcion, para que la pesque el controller correspondiente y avise al FE con un mensaje y codigo de error.

def obtener_usuario_con_dni(dni):    
    try:
        return DATABASE.session.query(Usuario).filter_by(dni=dni).first() # Obtiene un usuario con un id especifico. Como mail no es PK, se tiene que buscar con el filter_by().first()
    except SQLAlchemyError as e:
        raise # Propaga la excepcion, para que la pesque el controller correspondiente y avise al FE con un mensaje y codigo de error.


def obtener_contrasenia_usuario(mail):
    try:
        return DATABASE.session.query(Usuario.contrasenia).filter_by(mail=mail).scalar()
    except SQLAlchemyError:
        DATABASE.session.rollback()
        raise

def obtener_contrasenia_usuario_con_id(id_usuario):
    try:
        return DATABASE.session.query(Usuario.contrasenia).filter_by(id_usuario=id_usuario).scalar()
    except SQLAlchemyError:
        DATABASE.session.rollback()
        raise

def obtener_solo_usuario_sin_contrasenia(mail):
    try:
        resultado = DATABASE.session.query(Usuario.id_usuario, Usuario.nombre, Usuario.apellido, Usuario.dni,
                                           Usuario.mail, Usuario.telefono, Usuario.fecha_nacimiento, Usuario.rol,
                                           Usuario.eliminado).filter_by(mail=mail).first()

        if resultado:
            return {
                "id_usuario": resultado[0],
                "nombre": resultado[1],
                "apellido": resultado[2],
                "dni": resultado[3],
                "mail": resultado[4],
                "telefono": resultado[5],
                "fecha_nacimiento": resultado[6],
                "rol": resultado[7],
                "eliminado": resultado[8]
            }
        else:
            return None

    except SQLAlchemyError:
        DATABASE.session.rollback()
        raise

def eliminar_logico_usuario(id_usuario):
    try:
        usuario = DATABASE.session.get(Usuario, id_usuario)
        
        if usuario:
            # Actualiza los campos permitidos
            usuario.eliminado = 'SI'
            
            DATABASE.session.commit() # Commitea los cambios

        else:
            DATABASE.session.rollback()
            raise ValueError(f"Usuario con id {id_usuario} no encontrado")

    except SQLAlchemyError:
        DATABASE.session.rollback() # Si salta una excepcion en el proceso, tengo que volver para atras los cambios que se hicieron, para no generar inconsistencias en la DB.
        raise # Propaga la excepcion, para que la pesque el controller correspondiente y avise al FE con un mensaje y codigo de error.

def modificar_usuario(usuario, datos_actualizados):
    try:
        for campo, valor in datos_actualizados.items():
            if hasattr(usuario, campo):
                setattr(usuario, campo, valor)

        DATABASE.session.commit()
    
    except SQLAlchemyError:
        DATABASE.session.rollback() # Si salta una excepcion en el proceso, tengo que volver para atras los cambios que se hicieron, para no generar inconsistencias en la DB.
        raise # Propaga la excepcion, para que la pesque el controller correspondiente y avise al FE con un mensaje y codigo de error.

def cambiar_contrasenia(usuario, nueva_contrasenia_hash):
    try:
        if hasattr(usuario, 'contrasenia'):
            setattr(usuario, 'contrasenia', nueva_contrasenia_hash)

        DATABASE.session.commit()
        
    except SQLAlchemyError:
        DATABASE.session.rollback() # Si salta una excepcion en el proceso, tengo que volver para atras los cambios que se hicieron, para no generar inconsistencias en la DB.
        raise # Propaga la excepcion, para que la pesque el controller correspondiente y avise al FE con un mensaje y codigo de error.

def modificar_email_empleado(usuario, nuevo_mail, contra_hash):
    try:
        if hasattr(usuario, 'mail'):
            setattr(usuario, 'mail', nuevo_mail)
        
        if hasattr(usuario, 'contrasenia'):
            setattr(usuario, 'contrasenia', contra_hash)

        DATABASE.session.commit()
    
    except SQLAlchemyError:
        DATABASE.session.rollback() # Si salta una excepcion en el proceso, tengo que volver para atras los cambios que se hicieron, para no generar inconsistencias en la DB.
        raise # Propaga la excepcion, para que la pesque el controller correspondiente y avise al FE con un mensaje y codigo de error.

def cambiar_rol_usuario(usuario, nuevo_rol):
    try:
        if hasattr(usuario, 'rol'):
            setattr(usuario, 'rol', nuevo_rol)

        DATABASE.session.commit()
            
    except SQLAlchemyError:
        DATABASE.session.rollback() # Si salta una excepcion en el proceso, tengo que volver para atras los cambios que se hicieron, para no generar inconsistencias en la DB.
        raise # Propaga la excepcion, para que la pesque el controller correspondiente y avise al FE con un mensaje y codigo de error.

