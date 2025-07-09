////////////////////////////FUNCIONES/////////////////////////////////
async function borrarPregunta(idPregunta) {
  if (!confirm("¿Seguro que querés eliminar esta pregunta? Si tiene respuesta también será eliminada.")) return;

  try {
    const response = await fetch(`http://localhost:4000/pregunta/eliminar/${idPregunta}`, {
      method: "DELETE", 
      headers: { "Content-Type": "application/json" },
    });

    if (response.status === 200) {
      alert("Pregunta eliminada correctamente.");
      const idPropiedad = document.getElementById("id-propiedad").getAttribute("data-id");
      cargarPreguntasYRespuestas(idPropiedad);
    } else {
      const error = await response.json();
      alert(error.error || "Error al eliminar la pregunta.");
    }
  } catch (error) {
    console.error("Error al eliminar pregunta:", error);
    alert("Ocurrió un error inesperado.");
  }
}
async function borrarRespuesta(idRespuesta) {
  if (!confirm("¿Seguro que querés eliminar esta respuesta?")) return;

  try {
    const response = await fetch(`http://localhost:4000/respuesta/eliminar/${idRespuesta}`, {
      method: "DELETE", 
      headers: {
    'Content-Type': 'application/json'
  }

    });

    if (response.status === 200) {
      alert("Respuesta eliminada correctamente.");
      const idPropiedad = document.getElementById("id-propiedad").getAttribute("data-id");
      cargarPreguntasYRespuestas(idPropiedad);
    } else {
      const error = await response.json();
      alert(error.error || "Error al eliminar la respuesta.");
    }
  } catch (error) {
    console.error("Error al eliminar respuesta:", error);
    alert("Ocurrió un error inesperado.");
  }
}



async function cerrarSesion() {    
  try {
    const url = `http://localhost:4000/usuario/cerrar_sesion`;
    const response = await fetch(url, { method: "GET", headers: { "Content-Type": "application/json" } });
    const resultado = await response.json();
    if (response.status === 200) window.location.href = "/";
    else alert("Ocurrió un error al intentar cerrar sesion.");
  } catch (error) {
    alert("Ocurrió un error al intentar cerrar sesion.");
  }
}

async function obtener_datos_propiedad(id) {
  try {
    const url = `http://localhost:4000/propiedad/obtener?id=${id}`;
    const response = await fetch(url, { method: "GET", headers: { "Content-Type": "application/json" } });
    const resultado = await response.json();
    if (response.status === 200) return resultado;
    else alert("Ocurrió un error al obtener los datos de la propiedad.");
  } catch (error) {
    alert("Ocurrió un error inesperado en la aplicación.");
  }
}

function cargar_pantalla(propiedad) {
  const idElemento = document.getElementById("id-propiedad");
  idElemento.textContent = `ID #${propiedad.id_propiedad}`;
  idElemento.setAttribute("data-id", propiedad.id_propiedad);

  const puntuacion_placeholder = Number(propiedad.calificacion).toFixed(1);
  const piso = propiedad.piso ?? "-";
  const dpto = propiedad.departamento ?? "-";
  const ubicacion = `${propiedad.localidad}, ${propiedad.calle} ${propiedad.numero}, Piso ${piso} Dpto ${dpto}`;
  const descripcion = propiedad.descripcion ?? "-";
  const ruta_imagen = `static/img/img-propiedades/${propiedad.id_propiedad}/1.jpg`;

  document.getElementById("titulo-propiedad").textContent = propiedad.titulo;
  document.getElementById('imagen-propiedad').src = ruta_imagen;
  document.getElementById("puntuacion").textContent = puntuacion_placeholder;
  document.getElementById("ubicacion").textContent = ubicacion;
  document.getElementById("dimensiones").textContent = `${propiedad.metros_cuadrados} m²`;
  document.getElementById("cantidad-huespedes").textContent = `${propiedad.cantidad_huespedes} adulto/s`;
  document.getElementById("cantidad-habitaciones").textContent = `${propiedad.cantidad_habitaciones} habitación/es`;
  document.getElementById("cantidad-banios").textContent = `${propiedad.cantidad_banios} baño/s`;
  document.getElementById("politica-cancelacion").textContent = propiedad.politica_cancelacion;
  document.getElementById("duracion-minima").textContent = `${propiedad.minimo_dias} día/s`;
  document.getElementById("precio-por-dia").textContent = `AR$ ${propiedad.precio_por_dia}`;
  document.getElementById("descripcion-propiedad").textContent = descripcion;
  console.log('TOTAL CALIFIACIONEs:',propiedad.total_calificaciones)
  document.getElementById("total-calificaciones").textContent = `${propiedad.total_calificaciones} calificaciones`;
}

// devuelve { id_usuario, rol } o null si no está logueado
async function obtenerUsuarioActual() {
  try {
    const resp = await fetch("http://localhost:4000/usuario/ver_sesion_actual");
    const data = await resp.json();

    if (data && data.id_usuario) {
      return { id_usuario: data.id_usuario, rol: data.rol };
    } else {
      return null; // usuario no logueado
    }
  } catch (error) {
    console.error("Error al obtener el usuario actual:", error);
    return null;
  }
}

async function cargarPreguntasYRespuestas(id_propiedad) {
  const contenedor = document.getElementById("contenedor-preguntas");
  contenedor.innerHTML = "";

  try {
    const usuarioActual = await obtenerUsuarioActual();

    const resp = await fetch(`http://localhost:4000/pregunta/preguntas_respuestas/${id_propiedad}`);
    const data = await resp.json();

    if (data.length === 0) {
      contenedor.innerHTML = '<p class="text-muted comentarios-vacio">Aún no hay preguntas.</p>';
      return;
    }
        
    // Ordenar preguntas más nuevas arriba
    data.sort((a, b) => {
      const dateA = new Date(a.fecha);
      const dateB = new Date(b.fecha);
      if (dateA.getTime() === dateB.getTime()) return b.id_pregunta - a.id_pregunta;
      return dateB - dateA;
    });

    const puedeBorrar = (idPropietario) => {
      if (!usuarioActual) return false; // visitante no puede borrar
      if (usuarioActual.rol === "EMPLEADO" || usuarioActual.rol === "GERENTE") return true;
      if (usuarioActual.rol === "INQUILINO") return usuarioActual.id_usuario === idPropietario;
      return false;
    };

    data.forEach(p => {
      const item = document.createElement("div");
      item.classList.add("pregunta-item");

      const botonBorrarPregunta = puedeBorrar(p.id_usuario)
        ? `<button class="btn btn-danger btn-sm eliminar-comentario" onclick="borrarPregunta(${p.id_pregunta})">Eliminar</button>`
        : "";

      // Botón responder solo si no tiene respuesta y el usuario es empleado o gerente
      let botonResponderHTML = "";
      if (!p.respuesta && (usuarioActual?.rol === "EMPLEADO" || usuarioActual?.rol === "GERENTE")) {
        botonResponderHTML = `
          <button class="btn btn-secondary btn-sm eliminar-comentario" onclick="mostrarModalResponder(${p.id_pregunta})">
            Responder
          </button>
        `;
      }

      const preguntaHTML = `
        <div class="pregunta-texto">
          ${p.pregunta}
          ${botonBorrarPregunta}
          ${botonResponderHTML}
        </div>
      `;

      let respuestaHTML = "";

      if (p.respuesta?.respuesta) {
        const fechaObj = new Date(p.respuesta.fecha);
        const fechaFormateada = fechaObj.toLocaleDateString("es-AR");

        const botonBorrarRespuesta = puedeBorrar(p.respuesta.id_usuario)
          ? `<button class="btn btn-danger btn-sm eliminar-comentario" onclick="borrarRespuesta(${p.respuesta.id_respuesta})">Eliminar</button>`
          : "";

        respuestaHTML = `
          <div class="respuesta-texto">
            ↳ ${p.respuesta.respuesta}
            ${botonBorrarRespuesta}
            <div class="respuesta-fecha text-muted" style="font-size: 0.9em;">
              Respondido el ${fechaFormateada}
            </div>
          </div>
        `;
      }

      item.innerHTML = preguntaHTML + respuestaHTML;
      contenedor.appendChild(item);
    });
  } catch (error) {
    console.error("Error al cargar preguntas:", error);
    contenedor.innerHTML = '<p class="text-danger">Error al cargar preguntas.</p>';
  }
}

async function ver_sesion_actual() {
  try {
    const res = await fetch(`http://localhost:4000/usuario/ver_sesion_actual`);
    const data = await res.json();
    return res.status === 200 ? data : null;
  } catch (error) {
    alert("Error al verificar sesión.");
  }
}

async function cargarComentarios(idPropiedad) {
  try {
    console.log("ID PROPIEDAD: ", idPropiedad); 
    const [comentariosRes, sesionRes] = await Promise.all([
      fetch(`http://localhost:4000/comentarios?id_propiedad=${idPropiedad}`),
      fetch(`http://localhost:4000/usuario/ver_sesion_actual`)
    ]);
    if (!comentariosRes.ok || !sesionRes.ok) {
      alert("Error al obtener comentarios o sesión.");
      return;

    }

    const comentarios = await comentariosRes.json();
    const sesion = await sesionRes.json();
    const usuario_id = sesion.id_usuario;
    console.log("COMENTARIOS: ", comentarios); 
    const contenedor = document.querySelector('.comentarios');
    contenedor.innerHTML = '<h3>Comentarios de otros usuarios</h3>';

    if (comentarios.length === 0) {
      contenedor.innerHTML += '<label class="comentarios-vacio">Aún no hay comentarios.</label>';
      return;
    }
      // Ordenar los comentarios de más nuevos a más viejos
      comentarios.sort((a, b) => {
        const dateA = new Date(a.fecha);
        const dateB = new Date(b.fecha);
        if (dateA.getTime() === dateB.getTime()) return b.id_comentario - a.id_comentario;
        return dateB - dateA;
      });
    comentarios.forEach(c => {
      const div = document.createElement('div');
      div.className = 'comentario';

      const fechaFormateada = c.fecha.split("-").reverse().join("/");
      div.innerHTML = `
        <p><strong>${c.nombre_usuario} ${c.apellido_usuario}</strong> <span>${fechaFormateada}</span></p>
        <p>${c.texto}</p>
      `;

  if (sesion.rol === "EMPLEADO" || sesion.rol === "GERENTE" || c.id_usuario === usuario_id) {
    const btn = document.createElement("button");
    btn.textContent = "Eliminar";
    btn.className = "btn btn-danger btn-sm eliminar-comentario";
    btn.dataset.id = c.id_comentario;

    btn.addEventListener("click", async () => {
      if (confirm("¿Estás seguro de que querés eliminar este comentario?")) {
        const res = await fetch(`/comentarios/${c.id_comentario}/eliminar`, { method: "DELETE" });
        if (res.ok) {
          div.remove();
          alert ("El comentario fue eliminado exitosamente.")
        } else {
          alert("Error al eliminar comentario.");
        }
      }
    });

    div.appendChild(btn);
  }


      contenedor.appendChild(div);
    });
  } catch (error) {
    console.error(error);
    alert("Error inesperado al cargar comentarios.");
  }
}

/////////////////////// GESTIÓN DEL MODAL RESPONDER ///////////////////////

let preguntaSeleccionada = null;

function mostrarModalResponder(id_pregunta) {
 
  preguntaSeleccionada = id_pregunta;
  document.getElementById("inputRespuesta").value = "";
  document.getElementById("errorRespuesta").style.display = "none";
  const modal = new bootstrap.Modal(document.getElementById("modalResponder"));
  modal.show();
}

document.addEventListener("DOMContentLoaded", async () => {
  const btnCerrarSesion = document.getElementById('btn-cerrar-sesion');
  const btnConfirmacionCerrarSesion = document.getElementById('btn-confirmacion-cerrar-sesion');
  const btnReservar = document.getElementById("btn-reservar");
  const btnRegistrarInquilino = document.getElementById("btn-registrar-inquilino");
  const btnBuscarDni = document.getElementById("btn-buscarDNI");
  const btnResponder = document.getElementById("btnResponder");

  const params = new URLSearchParams(window.location.search);
  const id_propiedad = params.get("id");

  if (!id_propiedad) return alert("ID de propiedad no especificado.");

  const propiedad = await obtener_datos_propiedad(id_propiedad);
  cargar_pantalla(propiedad);
  await cargarComentarios(id_propiedad);
  await cargarPreguntasYRespuestas(propiedad.id_propiedad);

  if (btnCerrarSesion) {
    btnCerrarSesion.addEventListener('click', (e) => {
      e.preventDefault();
      const modal = new bootstrap.Modal(document.getElementById('cerrarSesionModal'));
      modal.show();
    });

    btnConfirmacionCerrarSesion.addEventListener('click', (e) => {
      e.preventDefault();
      cerrarSesion();
    });
  }

  if (btnReservar) {
    btnReservar.addEventListener("click", async () => {
      const sesion = await ver_sesion_actual();
      if (!sesion || sesion.rol === "VISITANTE") {
        alert("Debe estar autenticado para reservar.");
        window.location.href = "/iniciar_sesion";
      } else {
        const res_hues = params.get("res_hues");
        const res_in = params.get("res_in");
        const res_out = params.get("res_out");
        window.location.href = `/iniciar_reserva?id=${id_propiedad}&res_hues=${res_hues}&res_in=${res_in}&res_out=${res_out}`;
      }
    });
  }

  if (btnBuscarDni) {
    btnBuscarDni.addEventListener("click", (e) => {
      e.preventDefault();
      const nuevaURL = "/usuario/get_lista_inquilinos?" + params.toString();
      window.location.href = nuevaURL;
    });
  }

  if (btnRegistrarInquilino) {
    btnRegistrarInquilino.addEventListener('click', () => {
      window.location.href = "/iniciar_sesion";
    });
  }

  // GESTIÓN PREGUNTAS
  const modalPreguntaEl = document.getElementById("modalPregunta");
  if (modalPreguntaEl) {
    modalPreguntaEl.addEventListener('hidden.bs.modal', () => {
      inputPregunta.value = "";
      btnPublicar.disabled = true;  
    });
  }
  const inputPregunta = document.getElementById("inputPregunta");
  const btnPublicar = document.getElementById("btnPublicarPregunta");
 


  inputPregunta?.addEventListener("input", function () {
    btnPublicar.disabled = inputPregunta.value.trim().length === 0;

  });

  btnPublicar?.addEventListener("click", async function () {
    const pregunta = inputPregunta.value.trim();
    if (pregunta.length === 0) return;

    try {
      const response = await fetch(`http://localhost:4000/pregunta/alta/${id_propiedad}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pregunta }),
      });

      if (response.ok) {
        await cargarPreguntasYRespuestas(id_propiedad);
        inputPregunta.value = "";
        btnPublicar.disabled = true;
        const modal = bootstrap.Modal.getInstance(document.getElementById("modalPregunta"));
        modal.hide();
        alert("Pregunta publicada con éxito");
      } else {
        alert("Error al publicar la pregunta");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Ocurrió un error al enviar la pregunta");
    }
  });

  // GESTIÓN MODAL RESPONDER
  if (btnResponder) {
    btnResponder.addEventListener("click", async () => {
      const respuestaTexto = document.getElementById("inputRespuesta").value.trim();
      const errorDiv = document.getElementById("errorRespuesta");

      if (respuestaTexto.length === 0) {
        errorDiv.style.display = "block";
        return;
      }

      try {
        const sesion = await ver_sesion_actual();
        if (!sesion) {
          alert("Debe iniciar sesión para responder.");
          return;
        }

        const body = {
          id_pregunta: preguntaSeleccionada,
          id_usuario: sesion.id_usuario,
          respuesta: respuestaTexto
        };

        const response = await fetch("http://localhost:4000/respuesta/responder", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body)
        });

        if (response.ok) {
          const modal = bootstrap.Modal.getInstance(document.getElementById("modalResponder"));
          modal.hide();
          await cargarPreguntasYRespuestas(id_propiedad);
        } else {
          alert("Error al responder la pregunta");
        }
      } catch (e) {
        console.error("Error al responder:", e);
        alert("Error inesperado");
      }
    });
  }
});
