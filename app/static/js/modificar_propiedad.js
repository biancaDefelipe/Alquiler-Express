// Ejecutar cuando el DOM esté listo
window.addEventListener("DOMContentLoaded", () => {
  configurarLimpiezaErrores();
  configurarValidacionesPorInput();
  cargarValoresPropiedad();
  modificarImagen();
});

function configurarLimpiezaErrores() {
  const campos = [
    "tipo",
    "localidad",
    "metros_cuadrados",
    "calle",
    "numero",
    "piso",
    "departamento",
    "cantidad_banios",
    "cantidad_habitaciones",
    "cantidad_huespedes",
    "minimo_dias",
    "precio_por_dia",
    "titulo",
    "descripcion",
    "cargar-imagen",
  ];
  campos.forEach((id) => {
    const campo = document.getElementById(id);
    campo.addEventListener("input", () => {
      const error = document.getElementById("error-" + id);
      if (error) error.remove();
      campo.classList.remove("input-error");
    });
  });
}

function quitarAcentos(str) {
  return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

function configurarValidacionesPorInput() {
  aplicarValidacionPorClase(".decimal-limit-5-2", /^\d{0,5}(\.\d{0,2})?$/, "Máximo 5 enteros y 2 decimales");
  aplicarValidacionPorClase(".decimal-limit-7-2", /^\d{0,7}(\.\d{0,2})?$/, "Máximo 7 enteros y 2 decimales");
  aplicarValidacionPorClase(".integer-limit-2", /^\d{0,2}$/, "Solo números enteros de hasta 2 dígitos");
  aplicarValidacionPorClase(".integer-limit-5", /^\d{0,5}$/, "Solo números enteros de hasta 5 dígitos");
  aplicarValidacionPorClase(".integer-limit-7", /^\d{0,7}$/, "Solo números enteros de hasta 7 dígitos");
  aplicarValidacionPorClase(".no-especiales", /^[a-zA-Z0-9\s]*$/, "No se permiten caracteres especiales");
}

function aplicarValidacionPorClase(selector, regex, mensajeError) {
  document.querySelectorAll(selector).forEach((input) => {
    input.addEventListener("input", function (e) {
      const valor = e.target.value;
      const errorSpan = document.getElementById("error-" + e.target.id);

      if (!regex.test(valor)) {
        e.target.classList.add("input-error");
        if (errorSpan) errorSpan.textContent = mensajeError;
      } else {
        e.target.classList.remove("input-error");
        if (errorSpan) errorSpan.textContent = "";
      }
    });
  });
}

function mostrarError(idCampo, mensaje) {
  let campo = document.getElementById(idCampo);
  let errorId = "error-" + idCampo;
  let errorElemento = document.getElementById(errorId);

  if (!errorElemento) {
    errorElemento = document.createElement("span");
    errorElemento.id = errorId;
    errorElemento.classList.add("error-msg");
    campo.insertAdjacentElement("afterend", errorElemento);
  }

  errorElemento.innerText = mensaje;
  errorElemento.style.display = "block";
  campo.classList.add("input-error");
}

function limpiarErrores() {
  document.querySelectorAll(".error-msg").forEach((e) => e.remove());
  document
    .querySelectorAll(".input-error")
    .forEach((campo) => campo.classList.remove("input-error"));
}

function cargar_null_si_es_vacio(valor) {
  return valor === "" ? null : valor;
}

function habilitarBotones() {
  document.getElementById("btnModificar").disabled = false;
}

async function validarFormulario() {
  limpiarErrores();
  let tieneError = false;

  const camposObligatorios = [
    "tipo",
    "localidad",
    "metros_cuadrados",
    "calle",
    "numero",
    "cantidad_banios",
    "cantidad_habitaciones",
    "cantidad_huespedes",
    "minimo_dias",
    "precio_por_dia",
    "titulo"
  ];

  camposObligatorios.forEach((id) => {
    const valor = document.getElementById(id).value.trim();
    if (valor === "") {
      mostrarError(id, "Debe completar este campo.");
      tieneError = true;
    }
  });

  const tipo = document.getElementById("tipo").value.trim();
  const localidad = document.getElementById("localidad").value.trim();

  if (/\d/.test(tipo)) {
    mostrarError("tipo", "El tipo no puede contener números.");
    tieneError = true;
  }

  if (/\d/.test(localidad)) {
    mostrarError("localidad", "La localidad no puede contener números.");
    tieneError = true;
  }

  if (!tieneError) {
    //const nombreImagen = Array.from(archivo).map((file) => file);

    const datos_propiedad = {
      tipo: document.getElementById("tipo").value.trim(),
      localidad: document.getElementById("localidad").value.trim(),
      calle: document.getElementById("calle").value.trim(),
      numero: document.getElementById("numero").value,
      cantidad_banios: document.getElementById("cantidad_banios").value,
      cantidad_habitaciones: document.getElementById("cantidad_habitaciones").value,
      cantidad_huespedes: document.getElementById("cantidad_huespedes").value,
      /* politica_cancelacion: quitarAcentos(
        document.getElementById("politica_cancelacion").value.trim()
      ),
      */
      minimo_dias: document.getElementById("minimo_dias").value,
      precio_por_dia: document.getElementById("precio_por_dia").value,
      titulo: document.getElementById("titulo").value.trim(),
      metros_cuadrados: document.getElementById("metros_cuadrados").value,
      piso: cargar_null_si_es_vacio(
        document.getElementById("piso").value.trim()
      ),
      departamento: cargar_null_si_es_vacio(
        document.getElementById("departamento").value.trim()
      ),
      descripcion: cargar_null_si_es_vacio(
        document.getElementById("descripcion").value.trim()
      ),
      esta_habilitada: "SI",
      estado: "LIBRE",
      //imagen: archivo,
    };

    console.log(datos_propiedad);
    return datos_propiedad;
  }

  return null;
}

async function enviarFormulario(datos_propiedad) {
  try {
    const urlParams = new URLSearchParams(window.location.search);
    const idPropiedad = urlParams.get("id");
    const formData = new FormData();

    for (const clave in datos_propiedad) {
      const valor = datos_propiedad[clave];
      if (valor !== null && valor !== undefined && valor !== "") {
        formData.append(clave, valor);
      }
    }

    const archivo = document.getElementById("cargar-imagen").files;
    if (archivo.length > 0) {
      formData.append("imagen", archivo[0]);
    }

    url = `/propiedad/modificar/${idPropiedad}`;

    const response = await fetch(url, {
      method: "POST",
      body: formData,
    });

    const resultado = await response.json();

    if (response.status == 200) {

      alert(`Propiedad modificada con éxito.`);
      limpiarErrores();
      habilitarBotones();
      
    } else if (resultado["Code"] === "DATABASE-ERROR" || resultado["Code"] === "GENERIC-ERROR") {

      console.error("Error en el servidor:", resultado, "status:", response.status, "code:", resultado["Code"]);
      alert("Ocurrió un error inesperado en el sistema.");
      habilitarBotones();

    }

  } catch (error) {
    console.error("Error al enviar el formulario:", error);
    alert("Ocurrió un error, intentá nuevamente.");
    habilitarBotones();
  }
}

document.getElementById("formRegistro").addEventListener("submit", async function (e) {
  e.preventDefault();
  document.getElementById("btnModificar").disabled = true;
  limpiarErrores(); 
  const datos_propiedad = await validarFormulario();
  if (datos_propiedad !== null) {
    enviarFormulario(datos_propiedad);
  } else {
    habilitarBotones();
  }
});

function cargarValoresPropiedad() {
  const urlParams = new URLSearchParams(window.location.search);
  const idPropiedad = urlParams.get("id");
  console.log("id propiedad:", idPropiedad);

  if (idPropiedad) {
    fetch(`/propiedad/obtener?id=${idPropiedad}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Error al cargar la propiedad");
        }
        return response.json();
      })
      .then((data) => {
        document.getElementById("tipo").value = data.tipo;
        document.getElementById("localidad").value = data.localidad;
        document.getElementById("calle").value = data.calle;
        document.getElementById("numero").value = data.numero;
        document.getElementById("piso").value = data.piso || "";
        document.getElementById("departamento").value = data.departamento || "";
        document.getElementById("cantidad_banios").value = data.cantidad_banios;
        document.getElementById("cantidad_habitaciones").value = data.cantidad_habitaciones;
        document.getElementById("cantidad_huespedes").value = data.cantidad_huespedes;
        document.getElementById("politica_cancelacion").value = data.politica_cancelacion;
        document.getElementById("minimo_dias").value = data.minimo_dias;
        document.getElementById("precio_por_dia").value = data.precio_por_dia;
        document.getElementById("titulo").value = data.titulo;
        document.getElementById("metros_cuadrados").value = data.metros_cuadrados;
        document.getElementById("descripcion").value = data.descripcion || "";
      })
      .catch((err) =>
        console.error(`No se pudo cargar propiedad con id ${idPropiedad}:`, err)
      );
  }

  const ruta_imagen = `/static/img/img-propiedades/${idPropiedad}/1.jpg`;
  document.getElementById("previewImagen").src = ruta_imagen;
}

function modificarImagen() {
  const inputFile = document.getElementById("cargar-imagen");
  const btnCambiarImagen = document.getElementById("btnCambiarImagen");
  const previewImg = document.getElementById("previewImagen");

  btnCambiarImagen.addEventListener("click", () => {
    inputFile.click();
  });

  inputFile.addEventListener("change", () => {
    const file = inputFile.files[0];
    if (!file) return;
    const url = URL.createObjectURL(file);
    previewImg.src = url;
    previewImg.onload = () => URL.revokeObjectURL(url);
  });
}