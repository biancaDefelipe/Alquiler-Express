import datetime
import repositories.estadisticas_repository as estadisticas_repository
from exceptions.validacion_error import validacion_error

# Chart.js debe recibir un dict que tenga las siguientes claves:
        # - "labels": Categorías, nombres o ids que van en el eje X.
        # - "values": Cantidades o importes que van en el eje Y.
        # - "titulo": Texto que va arriba del gráfico.


def generar_estadistica(datos_estadistica):
    match datos_estadistica["estadistica"]:
        case "cantidad-usuarios":
            # Obtener tuplas (fecha_registro, cantidad)
            lista_tuplas = estadisticas_repository.obtener_cantidad_inquilinos_por_fecha_registro(datos_estadistica)

            # Parsear fechas límite
            fecha_desde = datetime.date.fromisoformat(datos_estadistica["fecha_desde"])
            fecha_hasta = datetime.date.fromisoformat(datos_estadistica["fecha_hasta"])

            # Mapear conteos existentes en un dict
            conteos = {f: c for (f, c) in lista_tuplas}

            # Construir conjunto de fechas garantizando los extremos
            fechas_set = set(conteos.keys())
            fechas_set.add(fecha_desde)
            fechas_set.add(fecha_hasta)

            # Ordenar las fechas
            fechas_ordenadas = sorted(fechas_set)

            # Generar labels y values solo con extremos y días con datos
            labels = [f.isoformat() for f in fechas_ordenadas]
            values = [conteos.get(f, 0) for f in fechas_ordenadas]

            return {
                "labels": labels,
                "values": values,
                "titulo": "Cantidad de usuarios inquilinos registrados por día"
            }
        case "ingresos-totales":
            match datos_estadistica["filtro"]:
                case "por-cada-propiedad":
                    # Tuplas (id_propiedad, titulo, total_ingresos)
                    resultados = estadisticas_repository.obtener_ingresos_por_cada_propiedad(datos_estadistica)
                    
                    if not resultados:
                        return {"labels": [],
                                "values": [], 
                                "titulo": "No se encontraron datos para el rango de fechas seleccionado."}
                    # Solo para cada propiedad: id - primeros 100 chars del titulo
                    
                    labels = [f"ID {fila[0]} - {fila[1]}" for fila in resultados]
                    values = [float(fila[2]) for fila in resultados]
                    
                    return {"labels": labels,
                            "values": values,
                            "titulo": "Total de ingresos por propiedad"}

                case "por-tipo-propiedad":
                    resultados = estadisticas_repository.obtener_ingresos_por_tipo_propiedad(datos_estadistica)

                    if not resultados:
                        return {
                            "labels": [],
                            "values": [],
                            "titulo": "No se encontraron datos para el rango de fechas seleccionado."
                        }
                    else:
                        labels = [fila[0] for fila in resultados]
                        values = [float(fila[1]) for fila in resultados]

                        return {
                            "labels": labels,
                            "values": values,
                            "titulo": "Total de ingresos por tipo de propiedad"
                        }
                case _:  # case default
                    raise validacion_error("No se reconocio el filtro para las estadisticas que desea generar.")
       
        case "cantidad-reservas":
            match datos_estadistica["filtro"]:
                case "por-cada-propiedad":
                    # Tuplas (id_propiedad, titulo, cant_reservas)
                    resultados = estadisticas_repository.obtener_reservas_por_cada_propiedad(datos_estadistica)
                    
                    if not resultados:
                        return {"labels": [],
                                "values": [],
                                "titulo": "No se encontraron datos para el rango de fechas seleccionado."}
                    
                    labels = [f"{fila[0]} - {fila[1][:100]}" for fila in resultados]
                    values = [int(fila[2]) for fila in resultados]
                    
                    return {"labels": labels,
                            "values": values,
                            "titulo": "Cantidad de reservas por propiedad"}

                case "por-tipo-propiedad":
                    resultados = estadisticas_repository.obtener_reservas_por_tipo_propiedad(datos_estadistica)

                    if not resultados:
                        return {
                            "labels": [],
                            "values": [],
                            "titulo": "No se encontraron datos para el rango de fechas seleccionado."
                        }
                    else:
                        labels = [fila[0] for fila in resultados]
                        values = [int(fila[1]) for fila in resultados]

                        return {
                            "labels": labels,
                            "values": values,
                            "titulo": "Cantidad de reservas por tipo de propiedad"
                        }
                case _:  # case default
                    raise validacion_error("No se reconocio el filtro para las estadisticas que desea generar.")
        case _:  # case default
            raise validacion_error("No se reconocio el tipo de estadisticas que desea generar.")