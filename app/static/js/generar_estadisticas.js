const btnGenerarEstadistica = document.getElementById("btn-generar-estadistica");
const titulo = document.getElementById("titulo-estadistica");
const totalElm = document.getElementById("total-estadistica");
let grafico_estadistica = null;

document.addEventListener("DOMContentLoaded", async() => {
  const campos = ["estadistica", "filtro", "fecha-desde", "fecha-hasta"];
  campos.forEach(id => {
    const campo = document.getElementById(id);
    campo.addEventListener("input", () => {
      const error = document.getElementById(id + "-error");
      if (error) error.remove();
      campo.classList.remove("input-error");
    });
  });

  const estadisticaSelect = document.getElementById("estadistica");
  const filtroContainer = document.getElementById("filtro-container");

  estadisticaSelect.addEventListener("change", () => {
    if (!estadisticaSelect.value || estadisticaSelect.value === "cantidad-usuarios") {
      // Ocultar el filtro
      filtroContainer.style.display = "none";
      // Limpiar el filtro para evitar valores colgados
      document.getElementById("filtro").value = "";
    } else {
      // Mostrar el filtro
      filtroContainer.style.display = "";
    }
  });

  // Forzar evaluación inicial.
  // si el <select> tenía un valor guardado (o por defecto),
  // se aplica la lógica de mostrar/ocultar filtro inmediatamente.
  estadisticaSelect.dispatchEvent(new Event('change'));
});


/////////////////////////// funciones ///////////////////////////

function habilitarBotones() {
  btnGenerarEstadistica.disabled = false;
}

function mostrarError(idCampo, mensaje) {
  const campo = document.getElementById(idCampo);
  const errorId = idCampo + "-error";
  
  // evito duplicar mensajes de error
  if (!document.getElementById(errorId)) {
    const error = document.createElement("p");
    error.id = errorId;
    error.className = "error-msg";
    error.innerText = mensaje;
    error.style.display= "block"; 
    campo.classList.add("input-error");
    campo.parentNode.appendChild(error);
  }
}

function limpiarErrores() {
  const errores = document.querySelectorAll(".error-msg");
  errores.forEach(e => e.remove());

  const camposConError = document.querySelectorAll(".input-error");
  camposConError.forEach(campo => campo.classList.remove("input-error"));
}

function fechaAString(fechaRecibida){
  let fecha = new Date(fechaRecibida); // fechaRecibida es la fecha en formato Date
  let fechaString = fecha.toISOString().split('T')[0]; // esto devuelve 'YYYY-MM-DD'
  console.log(fechaString); // lo muestro para probar 
  return fechaString
}

///////////////////////////validación////////////////////////////////////
//usando async pauso la ejecución hasta que no se resulva la modificacion del usuario
async function validarFormulario() {
  limpiarErrores();
  let tieneError= false; 

  const filtroContainer = document.getElementById("filtro-container");

  //uso trim para eliminar espacios en blanco
  const estadistica = document.getElementById("estadistica").value.trim();
  const filtro = document.getElementById("filtro").value.trim();
  const fecha_desde = document.getElementById("fecha-desde").value.trim();
  const fecha_hasta = document.getElementById("fecha-hasta").value.trim();

  console.log("Estadistica: " + estadistica);
  console.log("Filtro: " + filtro);
  console.log("Fecha desde: " + fecha_desde);
  console.log("Fecha hasta: " + fecha_hasta);

  const fecha_min = "1950-01-01";
  const fecha_max = "2099-12-31";

  if (!estadistica) {
    mostrarError("estadistica", "Debe seleccionar una estadistica.");
    tieneError=true; 
  }
  if (!filtro && filtroContainer.style.display !== "none") {
    mostrarError("filtro", "Debe seleccionar un filtro.");
    tieneError=true; 
  }
  if (!fecha_desde) {
    mostrarError("fecha-desde", "Debe seleccionar una fecha.");
    tieneError=true; 
  }
  if (!fecha_hasta) {
    mostrarError("fecha-hasta", "Debe seleccionar una fecha.");
    tieneError=true; 
  }
  

  // Validar que la fecha_desde sea menor que la fecha_hasta:
  if (fecha_desde >= fecha_hasta){
    mostrarError("fecha-desde", "La Fecha de inicio del período debe ser anterior a la Fecha de fin del período.");
    mostrarError("fecha-hasta", "La Fecha de fin del período debe ser posterior a la Fecha de inicio del período.");
    tieneError=true;
  }


  if (!tieneError){
    console.log("Formulario válido. Procediendo con el registro.");
    // si está todo ok armo el json
    const datosEstadistica = {
      estadistica: estadistica,
      filtro: filtro,
      fecha_desde: fechaAString(fecha_desde), // YYYY-MM-DD
      fecha_hasta: fechaAString(fecha_hasta), // YYYY-MM-DD
      //id_usuario: 2, dni: 98765432, nombre: Maria, apellido: Lopez, mail: maria@gmail.com, telefono: 987654321, fecha_nacimiento: 01-02-1986, rol: INQUILINO
    };
    return datosEstadistica; 
  }
  return null; 
}

function limpiarEstadisticaAnterior(){

  // Destruir el gráfico anterior
  if (grafico_estadistica) {
    grafico_estadistica.destroy();
    console.log("destruyo");
    totalElm.textContent = "";
  }
}

function mostrar_estadistica(datos_estadistica, tipo = "bar", dataset_label = "Cantidad", textoTotal, opcionesExtras = {}) {
  // Destruir gráfico previo
  if (grafico_estadistica) {
    grafico_estadistica.destroy();
  }

  const ctx = document.getElementById("grafico-estadistica").getContext("2d");
  const config = {
    type: tipo,
    data: {
      labels: datos_estadistica.labels,
      datasets: [{
        label: dataset_label,
        data: datos_estadistica.values,
        backgroundColor: tipo === "line" ? "rgba(54, 162, 235, 0.2)" : "rgba(54, 162, 235, 0.6)",
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 2,
        fill: tipo !== "line"
      }]
    },
    options: {
      responsive: true,
      indexAxis: opcionesExtras.indexAxis || 'x',  // recuerda que para barras horizontales ya configuras indexAxis:'y'
      scales: {
        x: {
          beginAtZero: true,
          ticks: { precision: 0 }
        },
        y: {
          // Aquí truncamos los labels largos
          ticks: {
            callback: function(value) {
              const label = this.getLabelForValue(value);
              return label.length > 20
                ? label.substring(0, 17) + '...'
                : label;
            },
            precision: 0,
            stepSize: 1
          }
        }
      },
      ...opcionesExtras
    }
  };

  grafico_estadistica = new Chart(ctx, config);

  // Mostrar total debajo del gráfico
  const total = datos_estadistica.values.reduce((a, b) => a + b, 0);
  if (totalElm) {
    totalElm.textContent = `${textoTotal} ${total}`;
  }
}


async function enviarFormulario(datosEstadistica){
  try {
    const url = `http://localhost:4000/estadisticas/generar`;

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(datosEstadistica)
    });
  
    const resultado = await response.json();
    console.log("Respuesta del servidor:", resultado);

    
  
    if (response.status === 200) {
      titulo.textContent = resultado.titulo || "";
      let textoTotal = "";

      switch (datosEstadistica["estadistica"]) {
        case "cantidad-usuarios":
          textoTotal = "Total de usuarios inquilinos registrados: ";
          mostrar_estadistica(resultado, "line", "Cantidad de usuarios inquilinos", textoTotal);
          break;

        case "ingresos-totales":
          if (datosEstadistica["filtro"] == "por-cada-propiedad"){
            textoTotal = "Total de ingresos entre todas las propiedades: $";
          }
          else if (datosEstadistica["filtro"] == "por-tipo-propiedad"){
            textoTotal = "Total de ingresos entre todos los tipos de propiedad: $";
          }
          mostrar_estadistica(resultado, "bar", "Total de ingresos", textoTotal, { indexAxis: "y" });
          break

        case "cantidad-reservas":
          if (datosEstadistica["filtro"] == "por-cada-propiedad"){
            textoTotal = "Total de reservas entre todas las propiedades: ";
          }
          else if (datosEstadistica["filtro"] == "por-tipo-propiedad"){
            textoTotal = "Total de reservas entre todos los tipos de propiedad: ";
          }
          mostrar_estadistica(resultado, "bar", "Cantidad de reservas", textoTotal, { indexAxis: "y" });
          break

        default:
          break
      }
      
      limpiarErrores();
      habilitarBotones();

    } else if (resultado ["Code"]== "DATABASE-ERROR") {
      alert("Ocurrió un error inesperado en el sistema.");//     + (resultado.DatabaseError || resultado.Error));
      habilitarBotones();
      titulo.textContent = "";
      totalElm.textContent = "";
    } else if (resultado ["Code"]== "GENERIC-ERROR"){
      alert("Ocurrió un error inesperado.");
      habilitarBotones();
      titulo.textContent = "";
      totalElm.textContent = "";
    }
  } catch (error) {
    console.log(error);
    alert("Ocurrió un error, intenté nuevamente");
    habilitarBotones();
    titulo.textContent = "";
    totalElm.textContent = "";
  }
}


document.getElementById("formEstadisticas").addEventListener("submit", async function (e) {
  e.preventDefault(); // previene el envío por defecto

  // deshabilitar botones
  btnGenerarEstadistica.disabled = true;

  // borra errores anteriores
  limpiarErrores();

  limpiarEstadisticaAnterior();

  // corre validaciones
  const datosEstadistica = await validarFormulario();
  console.log(datosEstadistica);

  if (!(datosEstadistica == null)) {    
    console.log("form valido");
    enviarFormulario(datosEstadistica);  
  }
  else {
    console.log("form con errores");
    habilitarBotones();
    // Mostrar un mensaje de error en lugar del titulo.
    titulo.textContent = "";
    totalElm.textContent = "";
  }
     
});
