import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from dotenv import load_dotenv
import os
import time 
from utils.manejador_pago import calcular_reembolso

# cargar las variables del archivo .env
load_dotenv()

# obtener las credenciales de las variables de entorno
remitente = os.getenv("REMITENTE")
clave_remitente = os.getenv("CLAVE_REMITENTE")
print(remitente)
print(clave_remitente)

# ---------------------------------------------------------------------------------------------------------- #

def msj_registro(nombre,contra): #sirve tanto para inquilinos como para empleados
    """
        Crea el mensaje que se recibe un usuario al registrarse. 
        Args: 
            nombre (String): nombre del usuario. 
            contra (String): contraseña del usuario.
        Returns: 
            msj: mensaje a enviar. 
    """
    
    msj= f"""
    <html>
    <body style="background-color: #f4f4f4;">
        <div style="background-color: #ffffff; padding: 20px; border-radius: 8px;">
            <p style="color: blue;">Hola <strong>{nombre}</strong>,</p>
            <p>Gracias por registrarte en nuestra plataforma</p>
            <p>Tu clave generada es: <strong>{contra}</strong></p>
            <br>
            <p>Saludos cordiales,</p>
            <p><strong>Equipo de <i>AlquilerExpress</i> </strong></p>
            <br>
            
        </div>
    </body>
    </html>
    """
    return msj

def msj_modificar_mail(nombre, contra): #sirve tanto para inquilinos como para empleados
    """
        Crea el mensaje que se recibe un usuario al registrarse. 
        Args: 
            nombre (String): nombre del usuario. 
            contra (String): contraseña del usuario.
        Returns: 
            msj: mensaje a enviar. 
    """
    
    msj= f"""
    <html>
    <body style="background-color: #f4f4f4;">
        <div style="background-color: #ffffff; padding: 20px; border-radius: 8px;">
            <p style="color: blue;">Hola <strong>{nombre}</strong>,</p>
            <p>Se ha modificado la direccion de email de su cuenta de usuario.</p>
            <p>A partir de ahora debera utilizar esta direccion de email para acceder a su cuenta de usuario.</p>
            <p>Su nueva clave generada es: <strong>{contra}</strong></p>
            <br>
            <p>Saludos cordiales,</p>
            <p><strong>Equipo de <i>AlquilerExpress</i> </strong></p>
            <br>
            
        </div>
    </body>
    </html>
    """
    return msj

#recibe obligatoriamente los dos parametros especificados mas n paramtros (*args)
#(*args significa que los recibe en forma de TUPLA)
def enviar_mail_registro(usuario, contenidomsj, *args): 
    """
        Envia un mail a usuario recibido como parametro
        Args: 
            usuario(Diccionario): diccionario con los datos del usuario
            contenidomsj: contenido del mensaje
            *args: Puede recibir mas parametros como urls, texto, 
        Returns: 
            True: si ambas coinciden.
            False: si no coinciden.
        Raises: 
            Exception
    """
    # creacion del mensaje
    mensaje = MIMEMultipart("alternative") # permite contener tanto texto plano como html
    mensaje["Subject"] = "Bienvenido/a - Registro exitoso"
    mensaje["From"] = remitente
    mensaje["To"] = usuario['mail']


    # contenido del mensaje (HTML)
    html = contenidomsj                     
    mensaje.attach(MIMEText(html, "html"))

    # envio del mail
    max_reintentos = 10  # numero máximo de intentos para enviar el mail, por si el primero falla
    intentos = 0
    while intentos < max_reintentos:
        try:
            servidor = smtplib.SMTP("smtp.gmail.com", 587)
            servidor.starttls()
            servidor.login(remitente, clave_remitente)
            servidor.sendmail(remitente, usuario['mail'], mensaje.as_string())
            servidor.quit()
            print(f"Correo enviado correctamente a {usuario['mail']}")
            return True
        except Exception as e:
            intentos += 1
            print(f"Error al enviar el correo: {e}")
            time.sleep(2)  


def enviar_mail_modificacion(usuario, contenidomsj, *args): 
    """
        Envia un mail a usuario recibido como parametro
        Args: 
            usuario(Diccionario): diccionario con los datos del usuario
            contenidomsj: contenido del mensaje
            *args: Puede recibir mas parametros como urls, texto, 
        Returns: 
            True: si ambas coinciden.
            False: si no coinciden.
        Raises: 
            Exception
    """
    # creacion del mensaje
    mensaje = MIMEMultipart("alternative") # permite contener tanto texto plano como html
    mensaje["Subject"] = "Se ha modificado su direccion de email"
    mensaje["From"] = remitente
    mensaje["To"] = usuario['mail']


    # contenido del mensaje (HTML)
    html = contenidomsj                     
    mensaje.attach(MIMEText(html, "html"))

    # envio del mail
    max_reintentos = 10  # numero máximo de intentos para enviar el mail, por si el primero falla
    intentos = 0
    while intentos < max_reintentos:
        try:
            servidor = smtplib.SMTP("smtp.gmail.com", 587)
            servidor.starttls()
            servidor.login(remitente, clave_remitente)
            servidor.sendmail(remitente, usuario['mail'], mensaje.as_string())
            servidor.quit()
            print(f"Correo enviado correctamente a {usuario['mail']}")
            return True
        except Exception as e:
            intentos += 1
            print(f"Error al enviar el correo: {e}")
            time.sleep(2)  

# ---------------------------------------------------------------------------------------------------------- #
# 2FA

def mail_msj_2fa(codigo):
    return f"""
    <html>
    <body style="background-color: #f4f4f4;">
        <div style="background-color: #ffffff; padding: 20px; border-radius: 8px;">
        
            <p style="color: blue;">2FA</strong></p>
            <p>Tu clave de un solo uso generada es: <strong>{codigo}</strong></p>
            <p>Recuerda no compartir esta clave con nadie.</p>
            <br>
            <p>Saludos cordiales,</p>
            <p><strong>Equipo de <i>AlquilerExpress</i> </strong></p>
            <br>
            
        </div>
    </body>
    </html>
    """

def mail_enviar_2fa(mailDestinatario, html): 
    print("********** HTML: ", html)
    # creacion del mensaje
    mensaje = MIMEMultipart("alternative") # permite contener tanto texto plano como html
    mensaje["Subject"] = "Código 2FA"
    mensaje["From"] = remitente
    mensaje["To"] = mailDestinatario
    
    mensaje.attach(MIMEText(html, "html"))

    # envio del mail
    max_reintentos = 2  # número de intentos para enviar mail
    intentos = 0
    while intentos < max_reintentos:
        try:
            servidor = smtplib.SMTP("smtp.gmail.com", 587)
            servidor.starttls()
            servidor.login(remitente, clave_remitente)
            servidor.sendmail(remitente, mailDestinatario, mensaje.as_string())
            servidor.quit()
            print(f"Correo enviado correctamente a {mailDestinatario}")
            return True
        except Exception as e:
            intentos += 1
            print(f"Error al enviar el correo: {e}")
            time.sleep(2)  

# ---------------------------------------------------------------------------------------------------------- #
# Reservar alquiler

def mail_msj_reserva_alquiler(datos_reserva, datos_usuario, datos_propiedad):
    print('**** inicio mail_msj_reserva_alquiler ****')
    piso = f"Piso {datos_propiedad["piso"]}" if datos_propiedad["piso"] is not None else ""
    departamento = f"Dpto {datos_propiedad["departamento"]}" if datos_propiedad["departamento"] is not None else ""
    return f"""
        <!DOCTYPE html>
        <html lang="es">
        <body style="margin:0;padding:0;background:#f0f2f5;">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:none;border-spacing:0;">
            <tr>
            <td align="center" style="padding:20px;">
                <table role="presentation" width="600" cellpadding="0" cellspacing="0"
                    style="background:#ffffff;border-radius:12px;
                            box-shadow:0 4px 20px rgba(0,0,0,0.1);
                            font-family:'Segoe UI',Tahoma,Verdana,sans-serif;
                            color:#333;">
                <tr>
                    <td style="padding:2rem;text-align:center;">
                    <h1 style="margin:0;font-size:1.75rem;color:#1e3a8a;">
                        Tu reserva ha sido generada
                    </h1>
                    <p style="margin:0.5rem 0 1.5rem;font-size:1.25rem;color:#5b21b6;">
                        Detalles de la reserva:
                    </p>
                    </td>
                </tr>
                
                <tr>
                    <td style="padding:0 2rem 2rem;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
                            style="border:none;border-spacing:0;">
                        <tr>
                        <td style="padding:0.5rem 0;font-weight:600;color:#555;width:180px;">
                            Identificador de reserva:
                        </td>
                        <td style="padding:0.5rem 0;color:#1f2937;">{datos_reserva["id_reserva"]}</td>
                        </tr>
                        <tr>
                        <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                            Fecha de inicio:
                        </td>
                        <td style="padding:0.5rem 0;color:#1f2937;">{datos_reserva["fecha_inicio"]}</td>
                        </tr>
                        <tr>
                        <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                            Fecha de fin:
                        </td>
                        <td style="padding:0.5rem 0;color:#1f2937;">{datos_reserva["fecha_fin"]}</td>
                        </tr>
                        <tr>
                        <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                            ID de propiedad:
                        </td>
                        <td style="padding:0.5rem 0;color:#1f2937;">{datos_propiedad["id_propiedad"]}</td>
                        </tr>
                        <tr>
                        <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                            Localidad:
                        </td>
                        <td style="padding:0.5rem 0;color:#1f2937;">{datos_propiedad["localidad"]}</td>
                        </tr>
                        <tr>
                        <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                            Direccion:
                        </td>
                        <td style="padding:0.5rem 0;color:#1f2937;">{datos_propiedad["calle"]} Nro {datos_propiedad["numero"]}  {piso} {departamento}</td>
                        </tr>
                        <tr>
                        <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                            DNI del inquilino:
                        </td>
                        <td style="padding:0.5rem 0;color:#1f2937;">{datos_usuario["dni"]}</td>
                        </tr>
                        <tr>
                        <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                            Nombre inquilino:
                        </td>
                        <td style="padding:0.5rem 0;color:#1f2937;">{datos_usuario["nombre"]} {datos_usuario["apellido"]}</td>
                        </tr>
                        <tr>
                        <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                            Medio de pago:
                        </td>
                        <td style="padding:0.5rem 0;color:#1f2937;">{datos_reserva["medio_de_pago"]}</td>
                        </tr>
                        <tr>
                        <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                            Precio total:
                        </td>
                        <td style="padding:0.5rem 0;color:#1f2937;">${datos_reserva["precio_total"]}</td>
                        </tr>
                    </table>
                    </td>
                </tr>
                </table>
            </td>
            </tr>
        </table>
        
        <div style="width=100%; padding: 20px;">
        
            <div style="background-color: #f0f2f5; padding: 20px; border-radius: 8px;">
                <br>
                <p style="font-size: 1rem">Saludos cordiales,</p>
                <p style="font-size: 1.2rem"><strong>Equipo de <i>AlquilerExpress</i> </strong></p>
                <br>
            </div>
            
        </div>
        
        </body>
        </html>
    """

def mail_enviar_reserva_alquiler(mailDestinatario, html): 
    print('**** inicio mail_enviar_reserva_alquiler ****')
    # creacion del mensaje
    mensaje = MIMEMultipart("alternative") # permite contener tanto texto plano como html
    mensaje["Subject"] = "Reserva generada con éxito"
    mensaje["From"] = remitente
    mensaje["To"] = mailDestinatario
    
    mensaje.attach(MIMEText(html, "html"))

    # envio del mail
    max_reintentos = 5  # número de intentos para enviar mail
    intentos = 0
    while intentos < max_reintentos:
        try:
            servidor = smtplib.SMTP("smtp.gmail.com", 587)
            servidor.starttls()
            servidor.login(remitente, clave_remitente)
            servidor.sendmail(remitente, mailDestinatario, mensaje.as_string())
            servidor.quit()
            print(f"Correo enviado correctamente a {mailDestinatario}")
            return True
        except Exception as e:
            intentos += 1
            print(f"Error al enviar el correo: {e}")
            time.sleep(2)          
        
# ---------------------------------------------------------------------------------------------------------- #
# Cancelación de Alquiler

def mail_msj_cancelacion_alquiler(data, type):
    print('**** inicio mail_msj_reserva_alquiler ****')
    
    if type == "ELIMINAR_PROPIEDAD":
        data["politica_cancelacion"] = "Cancelacion total reembolso";
        reembolso = calcular_reembolso(data["politica_cancelacion"], data["precio_total_reserva"])
        return f"""
            <!DOCTYPE html>
            <html lang="es">
            <body style="margin:0;padding:0;background:#f0f2f5;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:none;border-spacing:0;">
                <tr>
                    <td align="center" style="padding:20px;">
                        <table role="presentation" width="600" cellpadding="0" cellspacing="0"
                            style="background:#ffffff; border-radius:12px; box-shadow:0 4px 20px rgba(0,0,0,0.1); font-family:'Segoe UI',Tahoma,Verdana,sans-serif; color:#333;">
                            <tr>
                                <td style="padding:2rem; text-align:center;">
                                    <h1 style="margin:0;font-size:1.75rem;color:#1e3a8a;">
                                        Tu reserva ha sido cancelada
                                    </h1>
                                    <p style="margin:0.5rem 0 1.5rem;font-size:1.25rem;color:#5b21b6;">
                                        La reserva ha sido cancelada debido a que la propiedad ha sido dada de baja.
                                    </p>
                                </td>
                            </tr>
                        
                            <tr>
                                <td style="padding:0 2rem 2rem;">
                                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:none; border-spacing:0;">
                                        <tr>
                                            <td style="padding:0.5rem 0;font-weight:600;color:#555;width:180px;">
                                                Identificador de reserva:
                                            </td>
                                            <td style="padding:0.5rem 0;color:#1f2937;">{data["id_reserva"]}</td>
                                        </tr>
                                        <tr>
                                            <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                                                Fecha de inicio:
                                            </td>
                                            <td style="padding:0.5rem 0;color:#1f2937;">{data["fecha_inicio_reserva"]}</td>
                                        </tr>
                                        <tr>
                                            <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                                                Fecha de fin:
                                            </td>
                                            <td style="padding:0.5rem 0;color:#1f2937;">{data["fecha_fin_reserva"]}</td>
                                        </tr>
                                        <tr>
                                            <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                                                ID de propiedad:
                                            </td>
                                            <td style="padding:0.5rem 0;color:#1f2937;">{data["id_propiedad"]}</td>
                                        </tr>
                                        <tr>
                                            <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                                            Politica de cancelacion:
                                            </td>
                                            <td style="padding:0.5rem 0;color:#1f2937;">{data["politica_cancelacion"]}</td>
                                        </tr>
                                        <tr>
                                            <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                                                Precio abonado de la reserva:
                                            </td>
                                            <td style="padding:0.5rem 0;color:#1f2937;">{data["precio_total_reserva"]}</td>
                                        </tr>
                                        <tr>
                                            <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                                                DNI del inquilino:
                                            </td>
                                            <td style="padding:0.5rem 0;color:#1f2937;">{data["dni_usuario"]}</td>
                                        </tr>
                                        <tr>
                                            <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                                                Nombre inquilino:
                                            </td>
                                            <td style="padding:0.5rem 0;color:#1f2937;">{data["nombre_usuario"]} {data["apellido_usuario"]}</td>
                                        </tr>
                                        <tr>
                                            <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                                                Medio de pago:
                                            </td>
                                            <td style="padding:0.5rem 0;color:#1f2937;">{data["medio_de_pago"]}</td>
                                        </tr>
                                        <tr>
                                            <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                                                Monto total reembolsable:
                                            </td>
                                            <td style="padding:0.5rem 0;color:#1f2937;">${reembolso}</td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
            
            <div style="width=100%; padding: 20px;">
            
                <div style="background-color: #f0f2f5; padding: 20px; border-radius: 8px;">
                    <br>
                    <p style="font-size: 1rem">Saludos cordiales,</p>
                    <p style="font-size: 1.2rem"><strong>Equipo de <i>AlquilerExpress</i> </strong></p>
                    <br>
                </div>
                
            </div>
            
            </body>
            </html>
        """
    else:
        reembolso=calcular_reembolso(data["politica_cancelacion"], data["precio_total_reserva"])
        return f"""
            <!DOCTYPE html>
            <html lang="es">
            <body style="margin:0;padding:0;background:#f0f2f5;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:none;border-spacing:0;">
                <tr>
                <td align="center" style="padding:20px;">
                    <table role="presentation" width="600" cellpadding="0" cellspacing="0"
                        style="background:#ffffff;border-radius:12px;
                                box-shadow:0 4px 20px rgba(0,0,0,0.1);
                                font-family:'Segoe UI',Tahoma,Verdana,sans-serif;
                                color:#333;">
                    <tr>
                        <td style="padding:2rem;text-align:center;">
                        <h1 style="margin:0;font-size:1.75rem;color:#1e3a8a;">
                            Tu reserva ha sido cancelada
                        </h1>
                        <p style="margin:0.5rem 0 1.5rem;font-size:1.25rem;color:#5b21b6;">
                            Detalles de la cancelacion:
                        </p>
                        </td>
                    </tr>
                    
                    <tr>
                        <td style="padding:0 2rem 2rem;">
                        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:none; border-spacing:0;">
                            <tr>
                                <td style="padding:0.5rem 0;font-weight:600;color:#555;width:180px;">
                                    Identificador de reserva:
                                </td>
                                <td style="padding:0.5rem 0;color:#1f2937;">{data["id_reserva"]}</td>
                            </tr>
                            <tr>
                                <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                                    Fecha de inicio:
                                </td>
                                <td style="padding:0.5rem 0;color:#1f2937;">{data["fecha_inicio_reserva"]}</td>
                            </tr>
                            <tr>
                                <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                                    Fecha de fin:
                                </td>
                                <td style="padding:0.5rem 0;color:#1f2937;">{data["fecha_fin_reserva"]}</td>
                            </tr>
                            <tr>
                                <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                                    ID de propiedad:
                                </td>
                                <td style="padding:0.5rem 0;color:#1f2937;">{data["id_propiedad"]}</td>
                            </tr>
                            <tr>
                                <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                                Politica de cancelacion:
                                </td>
                                <td style="padding:0.5rem 0;color:#1f2937;">{data["politica_cancelacion"]}</td>
                            </tr>
                            <tr>
                                <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                                    Precio abonado de la reserva:
                                </td>
                                <td style="padding:0.5rem 0;color:#1f2937;">{data["precio_total_reserva"]}</td>
                            </tr>
                            <tr>
                                <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                                    DNI del inquilino:
                                </td>
                                <td style="padding:0.5rem 0;color:#1f2937;">{data["dni_usuario"]}</td>
                            </tr>
                            <tr>
                                <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                                    Nombre inquilino:
                                </td>
                                <td style="padding:0.5rem 0;color:#1f2937;">{data["nombre_usuario"]} {data["apellido_usuario"]}</td>
                            </tr>
                            <tr>
                                <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                                    Medio de pago:
                                </td>
                                <td style="padding:0.5rem 0;color:#1f2937;">{data["medio_de_pago"]}</td>
                            </tr>
                            <tr>
                                <td style="padding:0.5rem 0;font-weight:600;color:#555;">
                                    Monto total reembolsable:
                                </td>
                                <td style="padding:0.5rem 0;color:#1f2937;">${reembolso}</td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                </td>
                </tr>
            </table>
            
            <div style="width=100%; padding: 20px;">
            
                <div style="background-color: #f0f2f5; padding: 20px; border-radius: 8px;">
                    <br>
                    <p style="font-size: 1rem">Saludos cordiales,</p>
                    <p style="font-size: 1.2rem"><strong>Equipo de <i>AlquilerExpress</i> </strong></p>
                    <br>
                </div>
                
            </div>
            
            </body>
            </html>
        """

def mail_enviar_cancelacion_alquiler(mail, data, type): 
    print('**** inicio mail_enviar_cancelacion_alquiler ****')
    html=mail_msj_cancelacion_alquiler(data, type)
    # creacion del mensaje
    
    mensaje = MIMEMultipart("alternative") # permite contener tanto texto plano como html
    #mensaje["Subject"] = "Reserva cancelda con exito"
    
    from email.header import Header
    if type == "ELIMINAR_PROPIEDAD":
        mensaje["Subject"] = Header("Se canceló tu reserva", "utf-8")
    else:
        mensaje["Subject"] = Header("Reserva cancelada con éxito", "utf-8")
        
    mensaje["From"] = remitente
    mensaje["To"] = mail
    mensaje.attach(MIMEText(html, "html", "utf-8"))
    
    # envio del mail
    max_reintentos = 5  # número de intentos para enviar mail
    intentos = 0
    while intentos < max_reintentos:
        try:
            servidor = smtplib.SMTP("smtp.gmail.com", 587)
            servidor.starttls()
            servidor.login(remitente, clave_remitente)
            servidor.sendmail(remitente, mail, mensaje.as_string())
            servidor.quit()
            print(f"Correo enviado correctamente a {mail}")
            return True
        except Exception as e:
            intentos += 1
            print(f"Error al enviar el correo: {e}")
            time.sleep(2)          
        