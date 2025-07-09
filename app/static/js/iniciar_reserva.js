  document.addEventListener("DOMContentLoaded", async() => {
    const params = new URLSearchParams(window.location.search);

    
    const id_prop = params.get("id");
    const huespedes = params.get("res_hues");
    const checkin = params.get("res_in");
    const checkout = params.get("res_out");

    const mediosDePagoDiv = document.getElementById('medios_de_pago');

    // if (checkin && checkout) {
      const fechaIn = new Date(checkin);
      const fechaOut = new Date(checkout);
      const diferencia = Math.ceil((fechaOut - fechaIn) / (1000 * 60 * 60 * 24));
      document.getElementById("dias_seleccionados").innerText = diferencia || "";
    // }

    document.getElementById("fecha_inicio").innerText = checkin || "";
    document.getElementById("fecha_fin").innerText = checkout || "";
    document.getElementById("huespedes").innerText = huespedes || "";

    const datos_sesion_actual = await ver_sesion_actual();
    const datos_usuario = await obtener_un_solo_usuario_por_ID(datos_sesion_actual.id_usuario);
    
    document.getElementById("email").value = datos_usuario.mail || ""; // Uso value acá porque es un input!!
    document.getElementById("nombre").innerText = datos_usuario.nombre + " " || "";
    document.getElementById("apellido").innerText = datos_usuario.apellido || "";
    document.getElementById("dni").innerText = datos_usuario.dni || "";

    const datos_propiedad = await obtener_datos_propiedad(id_prop);
    document.getElementById("precio_dia").innerText = datos_propiedad.precio_por_dia || "";
    document.getElementById("propiedad").innerText = "#" + id_prop + ". " + datos_propiedad.titulo + "." || "";

    mediosDePagoDiv.innerHTML = obtener_html_medios_de_pago(datos_sesion_actual.rol);
    //  if (id_prop) {
      const total = datos_propiedad.precio_por_dia*diferencia;
      document.getElementById("total").innerText = total ? total.toFixed(2) : "";
    // }

    /* ---------------------------------------------------------------- */
    // Pago con mercado pago (iframe)

      const btnCloseMP = document.getElementById("btn-close-mp");
      const btnIframe = document.getElementById("btn-confirmar");

      btnIframe.addEventListener("click", () => {
        
        const precio_total = document.getElementById("total").textContent;
        const fecha_inicio = document.getElementById("fecha_inicio").textContent;
        const fecha_fin = document.getElementById("fecha_fin").textContent;
        
        const iframe = document.getElementById("iframePago");
        iframe.src = `http://127.0.0.1:4000/pagar_reserva/mercado_pago/?titulo=${encodeURIComponent(datos_propiedad.titulo)}&precio_total=${encodeURIComponent(precio_total)}`;

        console.log('------------- PROPIEDAD',datos_propiedad);
        console.log('------------- USUARIO',datos_usuario);

        const contentIframe = document.querySelector(".contentIframeAll");
        contentIframe.style.display = "flex";
        const maxEjecuciones = 10;
        let cantejecuciones = 0;

        const intervalo = setInterval(() => {

          if (cantejecuciones == maxEjecuciones) {

            clearInterval(intervalo);
            alert("El pago no pudo ser realizado");
            window.location.href = "/";
            return;

          } else {

            cantejecuciones++;

            fetch("/pago.json", { cache: "no-store" })
              .then((res) => {
                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                return res.json();
              })
              .then((data) => {
                console.log("------- Leyendo pago.json id_pago:", data.id_pago, "cantejecuciones:", cantejecuciones);
                if (data.id_pago !== null) {
                  clearInterval(intervalo);
                  darDeAltaReserva(datos_propiedad, datos_usuario, precio_total, fecha_inicio, fecha_fin);
                  console.log("Reserva ID en fetch pago.json:", reserva_id);
                }
              })
              .catch((err) => {
                console.error("Error leyendo pago.json:", err);
              });
              
          }
        }, 3000);
      });

      btnCloseMP.addEventListener("click", () => {
        const contentIframe = document.querySelector(".contentIframeAll");
        contentIframe.style.display = "none";
      });

      async function darDeAltaReserva(datos_propiedad, datos_usuario, precio_total, fecha_inicio, fecha_fin) {

        const datos_reserva = {
          id_propiedad: datos_propiedad.id_propiedad,
          id_usuario: datos_usuario.id_usuario,
          fecha_inicio: fecha_inicio,
          fecha_fin: fecha_fin,
          precio_total: precio_total,
          medio_de_pago: 'mercado_pago',
        };
        console.log (datos_reserva); 
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
            reserva_id = data.reserva_id;
            console.log("alta hecha.", reserva_id);
            enviarMail(datos_propiedad, datos_usuario, precio_total, fecha_inicio, fecha_fin, reserva_id);
            alert("Pago realizado con éxito, en breve te llegará un mail con la información de tu reserva");
            window.location.href = "/";
          } else {
            console.error("Error en el alta de la reserva:", response.status);
          }
        } catch (error) {
          console.error("Error general en el alta de la reserva:", error);
        }
      };

      async function enviarMail(datos_propiedad, datos_usuario, precio_total, fecha_inicio, fecha_fin, reserva_id) {
        console.log("reserva_id en enviar mail", reserva_id);
        const data = {
          datos_reserva: {
            id_reserva: reserva_id,
            fecha_inicio: fecha_inicio,
            fecha_fin: fecha_fin,
            medio_de_pago: 'mercado pago',
            precio_total: precio_total,
          },
          datos_usuario: {
            id_usuario: datos_usuario.id_usuario,
            nombre: datos_usuario.nombre,
            apellido: datos_usuario.apellido,
            dni: datos_usuario.dni,
            mail: datos_usuario.mail,
          },
          datos_propiedad: {
            id_propiedad: datos_propiedad.id_propiedad,
            localidad: datos_propiedad.localidad,
            calle: datos_propiedad.calle,
            numero: datos_propiedad.numero,
            piso:datos_propiedad.piso,
            departamento: datos_propiedad.departamento
          },
        };
        //PISO Y DEPTO TODO TRUCHO HAY QUE VALIDAR SI ES DEPTO/PH O SI ES CASA Y DEPENDIENDO DE ESO VEMOS QUE LE MANDAMOS

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
          }
        } catch (error) {
          console.error("Error general:", error);
        }
      }
    /* ---------------------------------------------------------------- */


  })

    // const datos_usuario = {
    //   nombre: "{{usuario.nombre}}",
    //   apellido: "{{usuario.apellido}}",
    //   mail: "{{usuario.mail}}",
    //   dni: "{{usuario.dni}}"
    // };
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
    datos_usuario = await response.json();

    if (response.status === 200) {
      console.log("Se obtuvo todo bien!")
      return datos_usuario;
    }
    else {
      alert("Ocurrió un error al obtener los datos del usuario.");
    }
  }
  catch (error) {
    alert("Ocurrió un error inesperado en la aplicación.");
  }
}

async function ver_sesion_actual() {
    try {
      const url = `http://localhost:4000/usuario/ver_sesion_actual`;

      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
      }
    });

    datos_sesion_actual = await response.json();

    if (response.status === 200) {
      console.log("Se obtuvo todo bien!")
      return datos_sesion_actual;
    }
    else {
      alert("Ocurrió un error al obtener la información de la sesión actual.");
    }
  }
  catch (error) {
    alert("Ocurrió un error inesperado en la aplicación.");
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

    resultado = await response.json();
    console.log(resultado)

    if (response.status === 200) {
      console.log("Se obtuvo todo bien!")
      return resultado;
    }
    else {
      alert("Ocurrió un error al obtener los datos de la propiedad.");
    }
  }
  catch (error) {
    alert("Ocurrió un error inesperado en la aplicación.");
  }
}


function obtener_html_medios_de_pago(rol_usuario_actual){
  const mediosPagoEmpleados = `
        <strong>Medio de pago</strong>
        <div class="form-check">
            <input class="form-check-input" type="radio" name="pago" checked>
            <label class="form-check-label">Pago con tarjeta</label>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="radio" name="pago">
            <label class="form-check-label">Pago por transferencia</label>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="radio" name="pago">
            <label class="form-check-label">Pago en efectivo</label>
        </div>
    `;

    const mediosPagoInquilino = `
        <strong>Medio de pago</strong>
        <p></p>
        <label class="form-check-label">A través de Mercado Pago con Transferencia o Tarjeta de Crédito/Débito</label>
        <p></p>
    `;

    if(rol_usuario_actual === 'INQUILINO'){
      return mediosPagoInquilino;
    }
    else{
      return mediosPagoEmpleados;
    }
}