document.addEventListener("DOMContentLoaded", async () => {

  const modalConfirmacionEl = document.getElementById("confirmModal");
  const modalConfirmacion = new bootstrap.Modal(modalConfirmacionEl);
  const modalMensaje = document.getElementById("modalMensaje");
  const confirmarBtn = document.getElementById("confirmarBtn");

  const comentarioModalEl = document.getElementById("comentarioModal");
  const comentarioModal = new bootstrap.Modal(comentarioModalEl);
  const formComentario = document.getElementById("formComentario");
  const inputIdReserva = document.getElementById("inputIdReserva");
  const inputComentario = document.getElementById("inputComentario");

  let reservaIdActual = null;

  // Función para consultar si ya existe comentario para una reserva
  async function existeComentario(id_reserva) {
    try {
      const res = await fetch(`/comentarios/existe?id_reserva=${encodeURIComponent(id_reserva)}`, {
        method: "GET",
        credentials: "include",
        headers: { "Content-Type": "application/json" }
      });
      if (!res.ok) throw new Error("Error en consulta existencia comentario");
      const data = await res.json();
      return data.existe;
    } catch (error) {
      console.error("Error consultando comentario existente:", error);
      return false; 
    }
  }

  // Actualizar botones comentar deshabilitando si ya existe comentario
  const botonesComentar = document.querySelectorAll(".btn-comentar");
  for (const boton of botonesComentar) {
    if (!boton.disabled) {
      const idReserva = boton.dataset.idReserva;
      const yaComento = await existeComentario(idReserva);
      if (yaComento) {
        boton.disabled = true;
        boton.classList.remove("btn-info");
        boton.classList.add("btn-secondary");
        boton.textContent = "Comentado";
        boton.title = "Ya comentaste esta reserva.";
      }
    }
  }

  // Evento click para botón comentar
  botonesComentar.forEach(boton => {
    boton.addEventListener("click", async () => {
      const idReserva = boton.dataset.idReserva;
      try {
        const yaComento = await existeComentario(idReserva);
        if (yaComento) {
          alert("Ya realizaste un comentario para esta reserva.");
          boton.disabled = true;
          boton.classList.remove("btn-info");
          boton.classList.add("btn-secondary");
          boton.textContent = "Comentado";
          boton.title = "Ya comentaste esta reserva.";
          return;
        }
        // Abrir modal para nuevo comentario
        inputIdReserva.value = idReserva;
        inputComentario.value = "";
        comentarioModal.show();
      
      } catch (error) {
        alert("Error al validar el comentario.");
        console.error(error);
      }
    });
  });

  // Envío del formulario de comentario
  formComentario.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
      id_reserva: inputIdReserva.value,
      texto: inputComentario.value.trim(),
    };

    if (!data.texto) {
      alert("El comentario no puede estar vacío.");
      return;
    }

    try {
      const response = await fetch(`http://localhost:4000/comentarios/alta`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });

      const result = await response.json();

      if (response.ok) {
        alert("Comentario publicado con éxito.");
        comentarioModal.hide();

        const botonComentar = document.querySelector(`.btn-comentar[data-id-reserva='${data.id_reserva}']`);
        if (botonComentar) {
          botonComentar.disabled = true;
          botonComentar.classList.remove("btn-info");
          botonComentar.classList.add("btn-secondary");
          botonComentar.textContent = "Comentado";
          botonComentar.title = "Ya comentaste esta reserva.";
        }

        if (window.reservas) {
          const reserva = reservas.find(r => String(r.id_reserva) === data.id_reserva);
          if (reserva) reserva.ya_comento = true;
        }
      } else {
        alert("Error al enviar comentario: " + (result.Error || ""));
      }
    } catch (error) {
      alert("Error de red al enviar comentario.");
      console.error(error);
    }
  });

  // Función para actualizar botones cancelar según estado
  function actualizarBotonesSegunEstado() {
    const filas = document.querySelectorAll("#tabla tbody tr");

    filas.forEach(fila => {
      const idReserva = fila.dataset.idReserva;
      const reserva = window.reservas ? reservas.find(r => String(r.id_reserva) === idReserva) : null;

      if (!reserva) return;

      const estado = reserva.estado.toUpperCase();
      const cancelarBtn = fila.querySelector(".btn-cancelar");

      if (cancelarBtn) {
        if (estado === "ABONADA") {
          cancelarBtn.disabled = false;
          cancelarBtn.style.opacity = 1;
        } else {
          cancelarBtn.disabled = true;
          cancelarBtn.style.opacity = 0.5;
        }
      }
    });
  }

  actualizarBotonesSegunEstado();

  // Modal confirmación para cancelar reserva
  window.confirmarCancelacion = function (idReserva) {
    reservaIdActual = idReserva;
    modalMensaje.textContent = `¿Estás seguro que querés cancelar la reserva ${idReserva}?`;
    modalConfirmacion.show();
  };

  confirmarBtn.addEventListener("click", function () {
    if (!reservaIdActual) return;

    fetch(`/reserva/cancelar/${reservaIdActual}`, {
      method: "POST"
    })
      .then(response => response.json().then(data => ({ status: response.status, body: data })))
      .then(({ status, body }) => {
        if (status === 201 && body.Success) {
          alert(`Se registró correctamente la cancelación de la reserva ${body.Reserva}`);

          const estadoCelda = document.getElementById(`estado-${body.Reserva}`);
          if (estadoCelda) {
            estadoCelda.textContent = body.nuevo_estado;
            estadoCelda.className = `estado-${body.nuevo_estado.toLowerCase().replace(" ", "-")}`;
          }
          const btnCancelar = document.getElementById(`btn-cancelar-${body.Reserva}`);
          if (btnCancelar) {
            btnCancelar.disabled = true;
            btnCancelar.style.opacity = 0.5;
          }

          if (window.reservas) {
            const reserva = reservas.find(r => String(r.id_reserva) === String(body.Reserva));
            if (reserva) reserva.estado = body.nuevo_estado;
          }

          actualizarBotonesSegunEstado();

          botonesComentar.forEach(async (boton) => {
            if (!boton.disabled) {
              const idReserva = boton.dataset.idReserva;
              const yaComento = await existeComentario(idReserva);
              if (yaComento) {
                boton.disabled = true;
                boton.classList.remove("btn-info");
                boton.classList.add("btn-secondary");
                boton.textContent = "Comentado";
                boton.title = "Ya comentaste esta reserva.";
              }
            }
          });

        } else {
          alert("Hubo un error al intentar registrar la acción.");
          console.error("Error en respuesta del servidor:", body);
        }
      })
      .catch(error => {
        console.error("Error:", error);
        alert("Ocurrió un error en la solicitud.");
      });

    modalConfirmacion.hide();
  });


  document.querySelectorAll('.btn-verPropiedad').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const idPropiedad = e.currentTarget.getAttribute('data-id-propiedad');
      if (idPropiedad) {
        window.location.href = `/ver_propiedad?id=${idPropiedad}&res_hues=None&res_in=None&res_out=None`;
      }
    });
  });

});

const calificarModal = new bootstrap.Modal(document.getElementById('calificarModal'));

function calificarReserva(idReserva) {
  document.getElementById('reservaIdInput').value = idReserva;
  calificarModal.show();
}

async function enviarCalificacion() {
  const id_reserva = document.getElementById('reservaIdInput').value;
  const calificacion = document.querySelector('select#rating').value;

  try {

    if (calificacion != '' && calificacion != null && calificacion != undefined){
      const res = await fetch(`/reserva/calificar/${id_reserva}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "calificacion": calificacion })
      });

      calificarModal.hide();
      alert("Calificación enviada con éxito");
      
    } else {
      console.log('calificacion vacia!', calificacion)
    }

    window.location.reload();

  } catch (e) {
    calificarModal.hide();
    console.error(e);
    alert('No se pudo enviar la calificación');
  }
}