document.addEventListener("DOMContentLoaded", function () {
    const searchForm = document.getElementById("searchForm");
    const modal = new bootstrap.Modal(document.getElementById("confirmModal"));
    
    const modalMensaje = document.getElementById("modalMensaje");
    const confirmarBtn = document.getElementById("confirmarBtn");
    
    const btnPorIniciar = document.getElementById("btnPorIniciar");
    const btnPorFinalizar = document.getElementById("btnPorFinalizar");
    const btnTodas = document.getElementById("btnTodas");

    const tbody = document.querySelector("#tabla tbody"); // obtener el tbody una vez
    const mensajeNoResultados = document.createElement("tr"); // crear el elemento del mensaje
    mensajeNoResultados.id = "mensaje-no-resultados";
    mensajeNoResultados.style.display = "none"; // ocultar por defecto
    mensajeNoResultados.innerHTML = `<td colspan="10" class="text-center text-muted py-3"></td>`; // Colspan para ocupar toda la tabla

    let filtroIniciarActivo = false;
    let filtroFinalizarActivo = false;

    // función para mostrar/ocultar el mensaje de no resultados
    function mostrarMensajeNoResultados(mostrar, mensaje = "") {
        if (mostrar) {
            mensajeNoResultados.querySelector("td").textContent = mensaje;
            mensajeNoResultados.style.display = "";
            tbody.appendChild(mensajeNoResultados); 
        } else {
            mensajeNoResultados.style.display = "none";
            if (mensajeNoResultados.parentNode) {
                mensajeNoResultados.parentNode.removeChild(mensajeNoResultados);
            }
        }
    }

  /*  function ordenarReservasPorFechaInicio() {
        const filas = Array.from(tbody.rows).filter(row => row.id !== "mensaje-no-resultados"); // excluir el mensaje
        const hoy = new Date();
        hoy.setHours(0, 0, 0, 0);

        let filasPrioritarias = [];
        let filasRestantes = [];

        filas.forEach((row) => {
            const id = row.dataset.idReserva;
            const reserva = window.reservas.find(r => String(r.id_reserva) === id);
            
            if (!reserva) {
                console.warn(`Reserva con ID ${id} no encontrada en los datos de window.reservas.`);
                return;
            }

            const fechaInicio = new Date(reserva.fecha_inicio);
            fechaInicio.setHours(0, 0, 0, 0);
            const fechaFin = new Date(reserva.fecha_fin);
            fechaFin.setHours(0, 0, 0, 0);

            if (reserva.estado.toUpperCase() === "ABONADA" || reserva.estado.toUpperCase() === "EN CURSO") {
                const fechasFuturas = [fechaInicio, fechaFin].filter(f => f >= hoy);
                let fechaMasCercana;

                if (fechasFuturas.length > 0) {
                    fechasFuturas.sort((a, b) => a - b);
                    fechaMasCercana = fechasFuturas[0];
                } else {
                    const diferenciaInicio = Math.abs(hoy - fechaInicio);
                    const diferenciaFin = Math.abs(hoy - fechaFin);
                    fechaMasCercana = diferenciaInicio < diferenciaFin ? fechaInicio : fechaFin;
                }
                filasPrioritarias.push({ row, fechaMasCercana });
            } else {
                filasRestantes.push(row);
            }
        });

        filasPrioritarias.sort((a, b) => a.fechaMasCercana - b.fechaMasCercana);

        tbody.innerHTML = ""; 
        mostrarMensajeNoResultados(false); // ocultar mensaje si hay filas

        filasPrioritarias.forEach(({ row }) => {
            tbody.appendChild(row);
        });

        filasRestantes.forEach(row => {
            tbody.appendChild(row);
        });

        // verificar si después de ordenar no quedan filas visibles (solo si no hay mensaje de no resultados)
        const filasVisiblesDespuesDeOrdenar = Array.from(tbody.rows).filter(row => row.style.display !== "none" && row.id !== "mensaje-no-resultados").length;
        if (filasVisiblesDespuesDeOrdenar === 0) {
             // si todas las filas son ocultadas por otro filtro, pero no en ordenar
        }
    }*/
   function ordenarReservasPorFechaInicio() {
    const filas = Array.from(tbody.rows).filter(row => row.id !== "mensaje-no-resultados"); // excluir mensaje
    const hoy = new Date();
    hoy.setHours(0, 0, 0, 0);

    let filasPrioritarias = [];
    let filasNoPrioritarias = [];

    filas.forEach((row) => {
        const id = row.dataset.idReserva;
        const reserva = window.reservas.find(r => String(r.id_reserva) === id);

        if (!reserva) {
            console.warn(`Reserva con ID ${id} no encontrada en los datos de window.reservas.`);
            return;
        }

        const fechaInicio = new Date(reserva.fecha_inicio);
        fechaInicio.setHours(0, 0, 0, 0);
        const fechaFin = new Date(reserva.fecha_fin);
        fechaFin.setHours(0, 0, 0, 0);

        const fechasFuturas = [fechaInicio, fechaFin].filter(f => f >= hoy);
        let fechaMasCercana;

        if (fechasFuturas.length > 0) {
            fechasFuturas.sort((a, b) => a - b);
            fechaMasCercana = fechasFuturas[0];
        } else {
            const diferenciaInicio = Math.abs(hoy - fechaInicio);
            const diferenciaFin = Math.abs(hoy - fechaFin);
            fechaMasCercana = diferenciaInicio < diferenciaFin ? fechaInicio : fechaFin;
        }

        const estado = reserva.estado.toUpperCase();
        if (estado === "ABONADA" || estado === "EN CURSO") {
            filasPrioritarias.push({ row, fechaMasCercana });
        } else {
            filasNoPrioritarias.push({ row, fechaMasCercana });
        }
    });

    // Ordenar ambos grupos por la fecha más cercana
    filasPrioritarias.sort((a, b) => a.fechaMasCercana - b.fechaMasCercana);
    filasNoPrioritarias.sort((a, b) => a.fechaMasCercana - b.fechaMasCercana);

    tbody.innerHTML = "";
    mostrarMensajeNoResultados(false); // ocultar mensaje si hay filas

    filasPrioritarias.forEach(({ row }) => tbody.appendChild(row));
    filasNoPrioritarias.forEach(({ row }) => tbody.appendChild(row));

    const filasVisiblesDespuesDeOrdenar = Array.from(tbody.rows).filter(
        row => row.style.display !== "none" && row.id !== "mensaje-no-resultados"
    ).length;

    if (filasVisiblesDespuesDeOrdenar === 0) {
        mostrarMensajeNoResultados(true); 
    }
}


        btnPorIniciar.addEventListener("click", () => {
            if (btnPorIniciar.disabled) return;

            filtroIniciarActivo = true;
            filtroFinalizarActivo = false;

            btnPorIniciar.classList.remove("btn-success");
            btnPorIniciar.classList.add("btn-warning");
            btnPorIniciar.disabled = true;

            btnPorFinalizar.classList.remove("btn-warning");
            btnPorFinalizar.classList.add("btn-success");
            btnPorFinalizar.disabled = false;

            btnTodas.classList.remove("btn-warning");
            btnTodas.classList.add("btn-success");
            btnTodas.disabled = false;

            const hoy = new Date();
            hoy.setHours(0, 0, 0, 0);
            const filas = Array.from(tbody.rows).filter(row => row.id !== "mensaje-no-resultados");

            let filasFiltradas = [];

            filas.forEach((row) => {
                const id = row.dataset.idReserva;
                const reserva = window.reservas.find(r => String(r.id_reserva) === id);
                if (!reserva) return;

                const fechaInicio = new Date(reserva.fecha_inicio);
                fechaInicio.setHours(0, 0, 0, 0);

                if (reserva.estado.toUpperCase() === "ABONADA" && fechaInicio > hoy) {
                    filasFiltradas.push({ row, fechaInicio });
                } else {
                    row.style.display = "none";
                }
            });

            filasFiltradas.sort((a, b) => a.fechaInicio - b.fechaInicio);

            Array.from(tbody.rows).forEach(row => {
                if (!filasFiltradas.some(f => f.row === row)) {
                    if (row.id !== "mensaje-no-resultados") {
                        row.style.display = "none";
                    }
                }
            });

            filasFiltradas.forEach(({ row }) => {
                row.style.display = "";
                tbody.appendChild(row);
            });

            if (filasFiltradas.length === 0) {
                mostrarMensajeNoResultados(true, "No hay reservas por iniciar.");
            } else {
                mostrarMensajeNoResultados(false);
            }
        });


        btnPorFinalizar.addEventListener("click", () => {
            if (btnPorFinalizar.disabled) return;

            filtroFinalizarActivo = true;
            filtroIniciarActivo = false;

            btnPorFinalizar.classList.remove("btn-success");
            btnPorFinalizar.classList.add("btn-warning");
            btnPorFinalizar.disabled = true;

            btnPorIniciar.classList.remove("btn-warning");
            btnPorIniciar.classList.add("btn-success");
            btnPorIniciar.disabled = false;

            btnTodas.classList.remove("btn-warning");
            btnTodas.classList.add("btn-success");
            btnTodas.disabled = false;

            const filas = Array.from(tbody.rows).filter(row => row.id !== "mensaje-no-resultados");

            let filasReservas = [];

            filas.forEach((row) => {
                const id = row.dataset.idReserva;
                const reserva = window.reservas.find(r => String(r.id_reserva) === id);
                if (!reserva) return;

                const estado = reserva.estado.toUpperCase();
                const fechaFin = new Date(reserva.fecha_fin);
                fechaFin.setHours(0, 0, 0, 0);

                if (estado === "EN CURSO") {
                    filasReservas.push({ row, fechaFin });
                } else {
                    row.style.display = "none";
                }
            });

            filasReservas.sort((a, b) => a.fechaFin - b.fechaFin);

            Array.from(tbody.rows).forEach(row => {
                if (!filasReservas.some(f => f.row === row)) {
                    if (row.id !== "mensaje-no-resultados") {
                        row.style.display = "none";
                    }
                }
            });

            filasReservas.forEach(({ row }) => {
                tbody.appendChild(row);
                row.style.display = "";
            });

            if (filasReservas.length === 0) {
                mostrarMensajeNoResultados(true, "No hay reservas por finalizar.");
            } else {
                mostrarMensajeNoResultados(false);
            }
        });

    function mostrarTodasLasReservas() {
        Array.from(tbody.rows).forEach(row => {
            row.style.display = "";
        });
        mostrarMensajeNoResultados(false); // ocultar mensaje cuando se muestran todas
    }

    let reservaIdActual = null;
    let tipoAccion = null;

    if (typeof window.reservas !== 'undefined') {
        window.reservas.forEach(reserva => {
            console.log(`Reserva ID: ${reserva.id_reserva}, Estado: ${reserva.estado}`);
        });
    }

    ///// FUNCION PARA ACTUALIZAR LOS BOTONES SEGUN SU ESTADO
    function actualizarBotonesSegunEstado() {
        const tabla = document.getElementById("tabla");
        const filas = tabla.tBodies[0].rows;
        const hoy = new Date();
        hoy.setHours(0, 0, 0, 0);

        Array.from(filas).forEach(fila => {
            if (fila.id === "mensaje-no-resultados") return; // ignorar el mensaje de no resultados

            const idReservaFila = fila.dataset.idReserva;
            const reserva = window.reservas.find(r => String(r.id_reserva) === idReservaFila);

            if (!reserva) {
                console.warn(`Reserva con ID ${idReservaFila} no encontrada en el array global 'reservas'.`);
                return;
            }

            const estado = reserva.estado.toUpperCase();
            const fechaInicioReserva = new Date(reserva.fecha_inicio);
            fechaInicioReserva.setHours(0, 0, 0, 0);

            const checkInCell = fila.cells[7]; // Celda del Check-In
            const checkOutCell = fila.cells[8]; // Celda del Check-Out
            const cancelarBtn = fila.cells[9] ? fila.cells[9].querySelector("button") : null; // Botón Cancelar

            // Actualizar la celda del estado
            fila.cells[6].textContent = reserva.estado;
            fila.cells[6].className = `estado-${reserva.estado.toLowerCase().replace(" ", "-")}`;

            // logica para los botones de Check-In y Check-Out
            if (estado === "ABONADA") {
                checkInCell.innerHTML = `
                    <button class="btn btn-sm text-white btn-checkin"
                            data-id="${reserva.id_reserva}"
                            data-checkin="${reserva.fecha_check_in || ''}"
                            onclick="confirmarCheck('${reserva.id_reserva}', 'in')">
                        Check-In
                    </button>
                `;
                checkOutCell.innerHTML = `
                    <button class="btn btn-sm text-white btn-checkout"
                            data-id="${reserva.id_reserva}"
                            data-checkout="${reserva.fecha_check_out || ''}"
                            onclick="confirmarCheck('${reserva.id_reserva}', 'out')"
                            disabled style="opacity: 0.5;">
                        Check-Out
                    </button>
                `;
            } else if (estado === "EN CURSO") {
                checkInCell.innerHTML = `<span class="text-success">${formatearFechaConHora(reserva.fecha_check_in || '-')}</span>`;
                checkOutCell.innerHTML = `
                    <button class="btn btn-sm text-white btn-checkout"
                            data-id="${reserva.id_reserva}"
                            data-checkout="${reserva.fecha_check_out || ''}"
                            onclick="confirmarCheck('${reserva.id_reserva}', 'out')">
                        Check-Out
                    </button>
                `;
            } else if (estado === "FINALIZADA") {
                checkInCell.innerHTML = `<span class="text-success">${formatearFechaConHora(reserva.fecha_check_in || '-')}</span>`;
                checkOutCell.innerHTML = `<span class="text-success">${formatearFechaConHora(reserva.fecha_check_out || '-')}</span>`;
            } else if (estado === "CANCELADA") {
                checkInCell.innerHTML = `<span class="text-secondary">-</span>`;
                checkOutCell.innerHTML = `<span class="text-secondary">-</span>`;
            } else {
                checkInCell.innerHTML = `
                    <button class="btn btn-sm text-white btn-checkin"
                            data-id="${reserva.id_reserva}"
                            data-checkin="${reserva.fecha_check_in || ''}"
                            onclick="confirmarCheck('${reserva.id_reserva}', 'in')"
                            disabled style="opacity: 0.5;">
                        Check-In
                    </button>
                `;
                checkOutCell.innerHTML = `
                    <button class="btn btn-sm text-white btn-checkout"
                            data-id="${reserva.id_reserva}"
                            data-checkout="${reserva.fecha_check_out || ''}"
                            onclick="confirmarCheck('${reserva.id_reserva}', 'out')"
                            disabled style="opacity: 0.5;">
                        Check-Out
                    </button>
                `;
            }

            // logica para el botón Cancelar
            if (cancelarBtn) {
                if (estado === "ABONADA" && fechaInicioReserva > hoy) {
                    cancelarBtn.disabled = false;
                    cancelarBtn.style.opacity = 1;
                    cancelarBtn.title = '';
                } else {
                    cancelarBtn.disabled = true;
                    cancelarBtn.style.opacity = 0.5;
                    cancelarBtn.title = 'Solo se pueden cancelar reservas abonadas y con fecha de inicio futura.';
                }
            }
        });
    }

    // llamadas iniciales
    actualizarBotonesSegunEstado();
    ordenarReservasPorFechaInicio();

    searchForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const codigo = document.getElementById("codigoReserva").value.trim();
        
        if (!codigo) {
            mostrarTodasLasReservas();
            ordenarReservasPorFechaInicio();
            return;
        }

        let found = false;
        Array.from(tbody.rows).forEach(row => {
            if (row.id === "mensaje-no-resultados") { // ocultar el mensaje si está presente
                row.style.display = "none";
                return;
            }

            const celdaCodigo = row.cells[0].textContent.trim();
            if (celdaCodigo === codigo) {
                row.style.display = "";
                found = true;
            } else {
                row.style.display = "none";
            }
        });

        if (!found) {
            mostrarMensajeNoResultados(true, `No se encontró la reserva con el código "${codigo}"`);
        } else {
            mostrarMensajeNoResultados(false);
        }
    });

    window.confirmarCheck = function (idReserva, tipo) {
        reservaIdActual = idReserva;
        tipoAccion = tipo;
        modalMensaje.textContent = `¿Estás seguro que querés registrar el ${tipo === 'in' ? 'check-in' : 'check-out'} de la reserva ${idReserva}?`;
        modal.show();
    };

    window.cancelarReserva = function (idReserva) {
        reservaIdActual = idReserva;
        tipoAccion = 'cancelar';
        modalMensaje.textContent = `¿Estás seguro que querés CANCELAR la reserva ${idReserva}?`;
        modal.show();
    };

    confirmarBtn.addEventListener("click", async function () {
        if (!reservaIdActual || !tipoAccion) return;

        let url = '';
        let successMessage = '';
        let errorMessage = '';

        if (tipoAccion === 'in') {
            url = `/reserva/checkin/${reservaIdActual}`;
            successMessage = 'Se registró correctamente el check-in.';
            errorMessage = 'No se pudo registrar el check-in';
        } else if (tipoAccion === 'out') {
            url = `/reserva/checkout/${reservaIdActual}`;
            successMessage = 'Se registró correctamente el check-out.';
            errorMessage = 'No se pudo registrar el check-out';
        } else if (tipoAccion === 'cancelar') {
            url = `/reserva/cancelar/${reservaIdActual}`;
            successMessage = 'La reserva ha sido cancelada correctamente.';
            errorMessage = 'No se pudo cancelar la reserva';
        } else {
            console.error("Tipo de acción desconocido:", tipoAccion);
            modal.hide();
            return;
        }

        try {
            const response = await fetch(url, {
                method: "POST"
            });
            const data = await response.json();

            if (response.ok && data.Success) {
                alert(successMessage);

                const fila = document.querySelector(`tr[data-id-reserva="${reservaIdActual}"]`);
                const reservaIndex = window.reservas.findIndex(r => String(r.id_reserva) === reservaIdActual);

                if (reservaIndex !== -1 && fila) {
                    window.reservas[reservaIndex].estado = data.nuevo_estado;
                    if (tipoAccion === 'in') {
                        window.reservas[reservaIndex].fecha_check_in = data.fecha_check;
                    } else if (tipoAccion === 'out') {
                        window.reservas[reservaIndex].fecha_check_out = data.fecha_check;
                    }
                } else {
                    console.error("Fila o reserva no encontrada en el DOM/array:", reservaIdActual);
                }
                actualizarBotonesSegunEstado();
            } else if (response.status === 409) {
                alert(data.Error || `${errorMessage} porque la propiedad ya tiene una reserva en curso.`);
                console.error("Error de conflicto:", data);
            } else {
                alert(data.Error || `Hubo un error al intentar registrar la acción: ${errorMessage}`);
                console.error("Error en respuesta del servidor:", data);
            }
        } catch (error) {
            console.error("Error en la solicitud:", error);
            alert("Ocurrió un error, intente de nuevo.");
        } finally {
            modal.hide();
            reservaIdActual = null;
            tipoAccion = null;
        }
    });

    function formatearFechaConHora(fechaStr) {
        if (!fechaStr || typeof fechaStr !== "string") return "-";

        const fechaObj = new Date(fechaStr.replace(' ', 'T'));
        
        if (isNaN(fechaObj.getTime())) {
            const partes = fechaStr.match(/^(\d{2})\/(\d{2})\/(\d{4}) (\d{2}):(\d{2})$/);
            if (partes) {
                 const [_, dia, mes, anio, horas, minutos] = partes;
                 const fechaObjAlt = new Date(anio, mes - 1, dia, horas, minutos);
                 if (!isNaN(fechaObjAlt.getTime())) {
                    return `${fechaObjAlt.getFullYear()}/${String(fechaObjAlt.getMonth() + 1).padStart(2, '0')}/${String(fechaObjAlt.getDate()).padStart(2, '0')} ${String(fechaObjAlt.getHours()).padStart(2, '0')}:${String(fechaObjAlt.getMinutes()).padStart(2, '0')}`;
                 }
            }
            return "-";
        }

        return `${fechaObj.getFullYear()}/${String(fechaObj.getMonth() + 1).padStart(2, '0')}/${String(fechaObj.getDate()).padStart(2, '0')} ${String(fechaObj.getHours()).padStart(2, '0')}:${String(fechaObj.getMinutes()).padStart(2, '0')}`;
    }

    function filtrarPorEstado() {
        const filtro = document.getElementById("filterEstado").value.toLowerCase();
        const filas = Array.from(tbody.rows).filter(row => row.id !== "mensaje-no-resultados"); // Excluir el mensaje

        let filasVisiblesCount = 0;
        filas.forEach(fila => {
            const idReservaFila = fila.dataset.idReserva;
            const reserva = window.reservas.find(r => String(r.id_reserva) === idReservaFila);
            if (!reserva) return;

            const estado = reserva.estado.toLowerCase();

            if (filtro === "todas" || estado === filtro) {
                fila.style.display = "";
                filasVisiblesCount++;
            } else {
                fila.style.display = "none";
            }
        });

        if (filtro !== "todas" && filasVisiblesCount === 0) {
            mostrarMensajeNoResultados(true, `No hay reservas en estado "${filtro}".`);
        } else {
            mostrarMensajeNoResultados(false);
        }
    }

    document.getElementById("filterEstado").addEventListener("change", filtrarPorEstado);
    btnTodas.addEventListener("click", () => {
    mostrarTodasLasReservas();
    ordenarReservasPorFechaInicio();
    const filterEstado = document.getElementById("filterEstado");
    filterEstado.value = "todas"; // <-- esta línea resetea el dropdown
        


    // Estilos de botones
    //btnTodas.disabled = true;
    //btnTodas.classList.remove("btn-secondary");
   //btnTodas.classList.add("btn-info");
        console.log("EN EL FILTRAR POR ESTADO")
    // Reactivar los otros botones y resetear estilos
    btnPorIniciar.disabled = false;
    btnPorIniciar.classList.remove("btn-warning");
    btnPorIniciar.classList.add("btn-success");

    btnPorFinalizar.disabled = false;
    btnPorFinalizar.classList.remove("btn-warning");
    btnPorFinalizar.classList.add("btn-success");

    filtroIniciarActivo = false;
    filtroFinalizarActivo = false;

    mostrarMensajeNoResultados(false);
});


});