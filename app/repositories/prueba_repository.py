from sqlalchemy.exc import SQLAlchemyError
from models import DATABASE
from models.usuario import Usuario
from models.propiedad import Propiedad


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

def obtener_usuario_con_mail(mail):    
    try:
        usuario = DATABASE.session.query(Usuario).filter_by(mail=mail).first() # Obtiene un usuario con un id especifico. Como mail no es PK, se tiene que buscar con el filter_by().first()
        return usuario

    except SQLAlchemyError as e:
        raise # Propaga la excepcion, para que la pesque el controller correspondiente y avise al FE con un mensaje y codigo de error.


def alta_usuario(datos_usuario):
    # Genera una nueva instancia de la clase a guardar con los datos que se recibieron.
    nuevo_usuario = Usuario(
        dni=datos_usuario['dni'],
        nombre=datos_usuario['nombre'],
        apellido=datos_usuario['apellido'],
        mail=datos_usuario['mail'],
        telefono=datos_usuario['telefono'],
        fecha_nacimiento=datos_usuario['fecha_nacimiento'],  # debe ser YYYY-MM-DD o usar datetime.date para formatear la fecha antes de esta etapa (en el service).
        contrasenia=datos_usuario['contrasenia'],
        rol=datos_usuario.get('rol')  # rol puede ser null
    )

    try:
        DATABASE.session.add(nuevo_usuario) # Da de alta el nuevo registro.
        DATABASE.session.commit() # Commitea los cambios.

    except SQLAlchemyError:
        DATABASE.session.rollback() # Si salta una excepcion en el proceso, tengo que volver para atras los cambios que se hicieron, para no generar inconsistencias en la DB.
        raise # Propaga la excepcion, para que la pesque el controller correspondiente y avise al FE con un mensaje y codigo de error.

def eliminar_usuario(usuario):
    try:
        DATABASE.session.delete(usuario) # Elimina el usuario
        DATABASE.session.commit() # Commitea los cambios

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


def obtener_todos_las_propiedades():
    try:
        propiedades = DATABASE.session.query(Propiedad).all()
        return propiedades

    except SQLAlchemyError as e:
        raise 


def obtener_usuarios_por_rol(rol):
    try:
        usuarios = DATABASE.session.query(Usuario).filter_by(rol=rol).all()
        return usuarios
    except SQLAlchemyError:
        raise
