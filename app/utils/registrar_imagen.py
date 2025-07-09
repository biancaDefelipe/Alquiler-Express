import os

RUTA_BASE_IMAGENES = os.path.join("app", "static", "img", "img-propiedades")

def registrar_imagen(imagen, id_propiedad, nombre_imagen):
    if imagen:
         # Ruta completa para la propiedad
        ruta_propiedad = os.path.join(RUTA_BASE_IMAGENES, str(id_propiedad))

        # Asegurarse de que la carpeta con id de la propiedad exista
        if not os.path.exists(ruta_propiedad):
            os.makedirs(ruta_propiedad)

        # Guardar la imagen usando el nombre recibido
        ruta_destino = os.path.join(ruta_propiedad, nombre_imagen)
        imagen.save(ruta_destino)
        
        
def modificar_imagen(imagen, id_propiedad, nombre_imagen):
    if imagen:

        carpeta_prop = os.path.join(RUTA_BASE_IMAGENES, str(id_propiedad))
        
        if not os.path.exists(carpeta_prop):
            os.makedirs(carpeta_prop, exist_ok=True)

        ruta_archivo = os.path.join(carpeta_prop, nombre_imagen)

        if os.path.isfile(ruta_archivo):
            os.remove(ruta_archivo)
            
        imagen.save(ruta_archivo)