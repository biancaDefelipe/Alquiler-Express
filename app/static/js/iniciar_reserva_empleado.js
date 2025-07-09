document.addEventListener("DOMContentLoaded", async () => {
    const params = new URLSearchParams(window.location.search);

    const id_propiedad_param = params.get("id"); 
    const huespedes = params.get("res_hues");
    const checkin = params.get("res_in");
    const checkout = params.get("res_out");
    const id_inquilino_param = params.get("id_usuario"); 

    const mediosDePagoDiv = document.getElementById('medios_de_pago');

  
    console.log("Parámetros recibidos en JS:");
    console.log("ID Propiedad (param):", id_propiedad_param);
    console.log("Huéspedes:", huespedes);
    console.log("Check-in:", checkin);
    console.log("Check-out:", checkout);
    console.log("ID Inquilino (param):", id_inquilino_param);

    const datos_usuario = await obtener_un_solo_usuario_por_ID(id_inquilino_param); // Usar el parámetro renombrado
    const datos_propiedad = await obtener_datos_propiedad(id_propiedad_param); // Usar el parámetro renombrado

    // Calcular la diferencia de días
    const fechaIn = new Date(checkin);
    const fechaOut = new Date(checkout);
    const diferencia = Math.ceil((fechaOut.getTime() - fechaIn.getTime()) / (1000 * 60 * 60 * 24));

    // Llenar el HTML con la información
    if (datos_usuario) {
        document.getElementById("email").value = datos_usuario.mail || "";
        document.getElementById("nombre").innerText = (datos_usuario.nombre || "") + " " + (datos_usuario.apellido || "");
        document.getElementById("dni").innerText = datos_usuario.dni || "";
    } else {
        console.error("No se pudieron obtener los datos del usuario.");
    }

    if (datos_propiedad) {
        document.getElementById("precio_dia").innerText = datos_propiedad.precio_por_dia ? datos_propiedad.precio_por_dia.toFixed(2) : "";
        document.getElementById("propiedad").innerText = `#${id_propiedad_param}. ${datos_propiedad.titulo || ""}.`;
    } else {
        console.error("No se pudieron obtener los datos de la propiedad.");
    }

    document.getElementById("fecha_inicio").innerText = checkin || "";
    document.getElementById("fecha_fin").innerText = checkout || "";
    document.getElementById("dias_seleccionados").innerText = diferencia || "";
    document.getElementById("huespedes").innerText = huespedes || "";

    // Insertar los radio buttons de medios de pago
    mediosDePagoDiv.innerHTML = obtener_html_medios_de_pago();

    // Calcular y mostrar el total
    const precio_total_calculado = (datos_propiedad?.precio_por_dia || 0) * diferencia;
    document.getElementById("total").innerText = precio_total_calculado ? precio_total_calculado.toFixed(2) : "";


    const precio_total = document.getElementById("total").textContent;
    const fecha_inicio = document.getElementById("fecha_inicio").textContent;
    const fecha_fin = document.getElementById("fecha_fin").textContent;

    const btnConfirmar = document.getElementById("btn-confirmar");
    btnConfirmar.addEventListener("click", () => {
        const medioDePagoSeleccionado = obtenerMedioDePagoSeleccionado();
        console.log("Medio de pago seleccionado (al hacer click):", medioDePagoSeleccionado);

        if (medioDePagoSeleccionado) {
            // Pasar los valores correctamente al darDeAltaReserva
            darDeAltaReserva(datos_propiedad, datos_usuario, precio_total, fecha_inicio, fecha_fin, medioDePagoSeleccionado);
        } else {
            alert("Por favor, selecciona un medio de pago.");
        }
    });

    // --- FUNCIÓN PARA OBTENER EL MEDIO DE PAGO SELECCIONADO ---
  
    function obtenerMedioDePagoSeleccionado() {
        const radios = document.querySelectorAll('input[name="pago"]');
        for (const radio of radios) {
            if (radio.checked) {
                // Si agregaste el atributo 'value' a tus radio buttons en obtener_html_medios_de_pago(),
                // esta es la forma más directa y robusta de obtener el valor.
                return radio.value;
            }
        }
        return null; // Si no hay ninguno seleccionado
    }

    // --- MODIFICACIÓN DE darDeAltaReserva PARA ACEPTAR EL MEDIO DE PAGO ---
  
    async function darDeAltaReserva(datos_propiedad, datos_usuario, precio_total, fecha_inicio, fecha_fin, medio_de_pago_seleccionado) {
        const datos_reserva = {
            id_propiedad: datos_propiedad?.id_propiedad, 
            id_usuario: datos_usuario?.id_usuario,     
            fecha_inicio: fecha_inicio,
            fecha_fin: fecha_fin,
            precio_total: parseFloat(precio_total), 
            medio_de_pago: medio_de_pago_seleccionado,
        };
        console.log("Datos de reserva a enviar:", datos_reserva);

        try {
            const response = await fetch("/reserva/alta", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(datos_reserva),
            });

            if (response.ok) {
                const data = await response.json();
                console.log("Reserva creada:", data);
                const reserva_id = data.reserva_id;
                console.log("Alta hecha. ID de reserva:", reserva_id);
                // PASAR EL MEDIO DE PAGO SELECCIONADO A ENVIARMAIL
                enviarMail(datos_propiedad, datos_usuario, precio_total, fecha_inicio, fecha_fin, reserva_id, medio_de_pago_seleccionado);
                alert("La reserva ha sido confirmada.");
                window.location.href = "/";
            } else {
                console.error("Error en el alta de la reserva:", response.status);
                alert("Ocurrió un error al intentar crear la reserva. Por favor, inténtalo de nuevo.");
            }
        } catch (error) {
            console.error("Error general en el alta de la reserva:", error);
            alert("Ocurrió un error inesperado al procesar la reserva.");
        }
    }

    // --- MODIFICACIÓN DE enviarMail PARA ACEPTAR EL MEDIO DE PAGO ---
    async function enviarMail(datos_propiedad, datos_usuario, precio_total, fecha_inicio, fecha_fin, reserva_id, medio_de_pago_seleccionado) {
        console.log("reserva_id en enviar mail", reserva_id);
        const data = {
            datos_reserva: {
                id_reserva: reserva_id,
                fecha_inicio: fecha_inicio,
                fecha_fin: fecha_fin,
                medio_de_pago: medio_de_pago_seleccionado, // ¡USAR EL PARÁMETRO RECIBIDO!
                precio_total: precio_total,
            },
            datos_usuario: {
                id_usuario: datos_usuario?.id_usuario,
                nombre: datos_usuario?.nombre,
                apellido: datos_usuario?.apellido,
                dni: datos_usuario?.dni,
                mail: datos_usuario?.mail,
            },
            datos_propiedad: {
                id_propiedad: datos_propiedad?.id_propiedad, 
                localidad: datos_propiedad?.localidad,
                calle: datos_propiedad?.calle,
                numero: datos_propiedad?.numero,
                piso: datos_propiedad?.piso,
                departamento: datos_propiedad?.departamento
            },
        };

        try {
            const response = await fetch("/reserva/enviar_mail_reserva_exitosa", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                console.log("Mail enviado.");
            } else {
                console.error("Error al enviar el mail:", response.status);
                alert("Ocurrió un error al enviar el mail"); 
            }
        } catch (error) {
            console.error("Error general:", error);
        }
    }


    function cargar_null_si_es_vacio(valor) {
        return valor === "" ? null : valor;
    }

    async function obtener_un_solo_usuario_por_ID(id_usuario) {
        try {
            const url = `http://localhost:4000/usuario/getUsuarioPorID?id=${id_usuario}`;
            const response = await fetch(url, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            });
            if (!response.ok) {
                console.error(`Error al obtener usuario: ${response.status} ${response.statusText}`);
                return null;
            }
            const datos = await response.json();
            console.log("Usuario obtenido:", datos);
            return datos;
        } catch (error) {
            console.error("Error inesperado al obtener usuario:", error);
            return null;
        }
    }

async function obtener_datos_propiedad(id_prop) {
    try {
        const url = `http://localhost:4000/propiedad/obtener?id=${id_prop}`;
        const response = await fetch(url, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });
        if (!response.ok) {
            console.error(`Error al obtener propiedad: ${response.status} ${response.statusText}`);
            return null;
        }
        const datos = await response.json();


        if (datos && datos.precio_por_dia) {
            datos.precio_por_dia = parseFloat(datos.precio_por_dia);
  
            if (isNaN(datos.precio_por_dia)) {
                console.log("Precio por día no es un número válido después de la conversión:", datos.precio_por_dia);
                datos.precio_por_dia = 0; 
            }
        } else {
            datos.precio_por_dia = 0; 
        }
        //

       
        return datos;
    } catch (error) {
        console.error("Error inesperado al obtener propiedad:", error);
        
        return null;
    }
}
    // función que genera el HTML para los radio buttons de pago
    function obtener_html_medios_de_pago() {
        return `
            <strong>Medio de pago</strong>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="pago" value="tarjeta" id="pagoTarjeta" checked>
                <label class="form-check-label" for="pagoTarjeta">Pago con tarjeta</label>
            </div>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="pago" value="transferencia" id="pagoTransferencia">
                <label class="form-check-label" for="pagoTransferencia">Pago por transferencia</label>
            </div>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="pago" value="efectivo" id="pagoEfectivo">
                <label class="form-check-label" for="pagoEfectivo">Pago en efectivo</label>
            </div>
        `;
    }
}); // Fin de DOMContentLoaded