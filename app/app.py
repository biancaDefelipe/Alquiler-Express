from flask import Flask, request, jsonify, render_template, request, redirect, url_for
import os
import instance.inicializador_db as ini_db
import utils.manejador_sesion as manejador_sesion
import utils.manejador_pago as manejador_pago
from models import DATABASE
from controllers.usuario_controller import USUARIO_BP
from services.usuario_service import obtener_un_solo_usuario_por_ID
from controllers.propiedad_controller import PROPIEDAD_BP
from controllers.reserva_controller import RESERVA_BP
from controllers.pregunta_controller import PREGUNTA_BP
from controllers.estadisticas_controller import ESTADISTICAS_BP
from services import usuario_service
from flask_cors import CORS
import mercadopago
from flask_mail import Mail, Message
from datetime import datetime
from controllers.comentario_controller import comentario_bp
from controllers.respuesta_controller import respuesta_bp
from services import propiedad_service


#--------------------------------------------------------<--------------------------------------------#

def crear_app():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    DB_PATH = os.path.join(BASE_DIR, "instance", "database.db")

    # Inicializar appTTT
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # Configuracion de rutas para la DB
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializar DB con la app
    DATABASE.init_app(app)

    # Crear tablas dentro del contexto de la app
    with app.app_context():
        DATABASE.create_all()

    # CORS (permitir conexiones desde múltiples orígenes, como React o distintos puertos)
    CORS(app, resources={r"/*": {
        "origins": [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:4000",
            "http://127.0.0.1:4000"
        ],
        "supports_credentials": True  # si uso cookies o autenticación con sesiones
    }})

    # Registrar blueprints para dar acceso a los controllers y sus endpoints
    app.register_blueprint(USUARIO_BP)
    app.register_blueprint(PROPIEDAD_BP)
    app.register_blueprint(RESERVA_BP)
    app.register_blueprint(PREGUNTA_BP)
    app.register_blueprint(respuesta_bp)
    app.register_blueprint(comentario_bp)
    app.register_blueprint(ESTADISTICAS_BP)

    # ------------------------------------------------------------------------------------------------------------- #
    # Rutas y lógica

    @app.route('/')
    def inicio():
        sesion = manejador_sesion.ver_sesion_actual()
        if sesion['rol'] == 'VISITANTE':
            return render_template("base.html")
        else:
            return render_template(f"base_{sesion['rol'].lower()}.html")
    
# ------------------------------------------------------------------------------------------------------------- #
    # Pantalla de registro de empleado

    @app.route('/altaEmpleado')
    def altaEmpleado():
        return render_template('registrar_empleado.html')

    @app.route('/registro')
    def registro():
        return render_template('registro_inquilino.html')

    @app.route('/iniciar_sesion')
    def iniciar_sesion():
        manejador_pago.limpiar_pago()
        return render_template('iniciar_sesion.html')

    @app.route('/perfil_usuario')
    def perfil_usuario():
        return render_template('perfil_usuario.html')
    
# ------------------------------------------------------------------------------------------------------------- #
    # Propiedad

    @app.route('/registro/propiedad')
    def registro_propiedad():
        return render_template('registrar_propiedad.html')
    
    @app.route("/ver_propiedad")
    def ver_detalle_propiedad():
        sesion = manejador_sesion.ver_sesion_actual()
        if sesion['rol'] == 'VISITANTE':
            return render_template("detalle_propiedad.html")
        else:
            return render_template(f"detalle_propiedad_{sesion['rol'].lower()}.html")
        
    @app.route("/ver_propiedad_id")
    def ver_detalle_propiedad_id():
        sesion = manejador_sesion.ver_sesion_actual()
        id_propiedad = request.args.get("id")  # obtiene el ID desde la URL

        propiedad = propiedad_service.obtener_propiedad_con_id(id_propiedad) # trae el objeto python en vez del json

        if sesion['rol'] == 'VISITANTE':
            return render_template("detalle_propiedad.html", propiedad=propiedad)
        else:
            return render_template(f"detalle_propiedad_{sesion['rol'].lower()}.html", propiedad=propiedad)


    @app.route('/iniciar_reserva')
    def iniciar_reserva():
        res_id = request.args.get('id')
        res_hues = request.args.get('res_hues')
        res_in = request.args.get('res_in')
        res_out = request.args.get('res_out')

        # res_usu = request.args.get('usuario')
        sesion = manejador_sesion.ver_sesion_actual()
        usuario = sesion['id_usuario']

        # usuario= obtener_un_solo_usuario_por_ID (sesion['id_usuario'])  #con esto llamo a la funcion de service y respository para traer la info del usuario: funciona bien!!!
        return render_template(
            'iniciar_reserva.html',
            id=res_id,
            res_hues=res_hues,
            res_in=res_in,
            res_out=res_out,
            usuario=usuario
        )

    # SDK Mercado Pago

    @app.route("/pagar_reserva/mercado_pago/")
    def pagar_reserva_mercado_pago():
        titulo = request.args.get("titulo", type=str)
        precio_total = request.args.get("precio_total", type=int)
        return render_template("pagar_reserva.html", titulo=titulo, precio_total=precio_total)

    sdk = mercadopago.SDK("APP_USR-7661064361183067-051021-c78af2e10040a9045a740b25d6af250e-2435216924")

    @app.route("/pagar_reserva/mercado_pago/pagar", methods=["POST"])
    def pagar_reserva():
        data = request.get_json()

        preference_data = {
            "items": [
                {
                    "title": data.get("descripcion"),
                    "quantity": 1,
                    "currency_id": "ARS",
                    "unit_price": float(data.get("precio", 0))
                }
            ]
        }

        try:
            preference_response = sdk.preference().create(preference_data)
            print("Respuesta de Mercado Pago:", preference_response)
            preference_id = preference_response["response"]["id"]
            url = preference_response["response"]["init_point"]
            print("ID de preferencia:", preference_id)
            print("URL de pago:", url)
            return jsonify({"id": preference_id, "url": url})
        except Exception as e:
            print("Error creando preferencia:", e)
            return jsonify({"error": "Error creando la preferencia"}), 500

    @app.route("/mp_webhook", methods=["POST"])
    def mp_webhook():
        data = request.get_json(force=True)
        manejador_pago.realizar_pago(data.get("id"))
        print("Pago recibido MP:", data)
        return jsonify({"received": True}), 200

    @app.route("/iframe")
    def iframe():
        return render_template("prueba_iframe.html")

    @app.route('/pago.json')
    def pago_json():
        pago = manejador_pago.ver_pago()
        if not (pago['id_pago'] is None):
            manejador_pago.limpiar_pago()
        return pago
    
    @app.route('/alquilar_propiedad')
    def alquilar_propiedad():
        return render_template('alquilar_propiedad.html')

    @app.route('/alquilar_propiedad/pago')
    def alquilar_propiedad_comprobante():
        return render_template('alquilar_propiedad_comprobante.html')
    
    @app.route('/generar_estadisticas')
    def generar_estadisticas():
        return render_template('generar_estadisticas.html')

# ------------------------------------------------------------------------------------------------------------- #
    # Iniciar proceso de reserva desde empleado
    
    @app.route('/iniciar_reserva_emp')
    def reservar_desde_empleado():
        id_usuario = request.args.get('id_usuario')
        id_prop = request.args.get("id")
        res_hues = request.args.get("res_hues")
        res_in = request.args.get("res_in")
        res_out = request.args.get("res_out")
        print(f"DEBUG: id_usuario recibido: {id_usuario}")
        print(f"DEBUG: id_propiedad recibido: {id_prop}")
        print(f"DEBUG: res_hues recibido: {res_hues}")
        print(f"DEBUG: res_in recibido: {res_in}")
        print(f"DEBUG: res_out recibido: {res_out}")

        return render_template("iniciar_reserva_empleado.html", id_usuario=id_usuario, id_propiedad=id_prop, res_hues=res_hues, res_in=res_in, res_out=res_out)

    return app


if __name__ == "__main__":
    ini_db.inicializar_db()
    manejador_sesion.limpiar_sesion()
    app = crear_app()
    app.run(debug=True, port=4000)
