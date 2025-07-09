import repositories.propiedad_repository as propiedad_repository
import utils.registrar_imagen as registrar_imagen

def alta_propiedad(datos_propiedad, imagen):
    id_propiedad = propiedad_repository.alta_propiedad(datos_propiedad)
    print(id_propiedad)
    registrar_imagen.registrar_imagen(imagen, id_propiedad, "1.jpg")

def listar_propiedades():
    return propiedad_repository.obtener_propiedades()


def obtener_propiedad_con_id(id_propiedad):
    return propiedad_repository.obtener_propiedad_con_id(id_propiedad)


def obtener_propiedades_buscadas(criterios_busqueda): 
    """
        Llama a la función del repository que devuelve una lista de propiedades que cumplan con los criterios de búsqueda
        Arg: 
            criterios_busqueda(Diccionario): criterios de busqueda ingresados por el usuario (localidad, cantidad de huespedes, check-in y check-out)
        Returns: 
            propiedades_disponibles: si hay al menos una propiedad que cumpla con los criterios de búsqueda 
            None: ni no hay propiedades que cumplan con los criterios. 
    """
    return propiedad_repository.obtener_propiedades_buscadas(criterios_busqueda)

def registrar_fin_de_limpieza_service(id_propiedad_in):
    return propiedad_repository.registrar_fin_de_limpieza(id_propiedad_in)

def modificar_propiedad_service(id_propiedad, datos, imagen):
    registrar_imagen.modificar_imagen(imagen, id_propiedad, "1.jpg")
    return propiedad_repository.modificar_propiedad_repository(id_propiedad, datos)

def eliminar_propiedad_service(id_propiedad):
    return propiedad_repository.eliminar_propiedad_repository(id_propiedad)