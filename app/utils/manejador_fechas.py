from datetime import datetime

def formatear_fecha_iso_a_custom(fecha_str):
    if not fecha_str:
        return "-"
    try:
        # Parseamos string ISO (sin zona horaria)
        fecha_obj = datetime.fromisoformat(fecha_str)
        return fecha_obj.strftime("%d/%m/%Y %H:%M")
    except Exception as e:
        print("Error formateando fecha:", e)
        return fecha_str  # Si falla, devolvemos el string original
