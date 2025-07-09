/////////////////////////////////////////////////////
let resultado = []; //VARIABLE QUE ALMACENA EL RESULTADO DE UNA BUSQUEDA
/////////////FUNCIONES A IMPORTAR/////////////////////
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
/**
 * Renderiza las propiedades recibidas, como resultado de una búsqueda
 *
 * @param {List} propiedades Lista de propiedades a renderizar
 */
function renderizarPropiedades(propiedades) {
  const contenedor = document.getElementById('propiedades');
  const titulo = document.getElementById('titulo');
  titulo.innerHTML = "";
  contenedor.innerHTML = '';

    if (!Array.isArray(propiedades) || propiedades.length === 0) {
    titulo.innerHTML = "No se encontraron resultados para la búsqueda realizada ";
    return;
  }

  propiedades.forEach(prop => {
    const card = document.createElement('div');
    card.classList.add('col-md-3', 'mb-4', 'card-container');
    
    // Agregar atributos data- con la información para filtrar
    card.dataset.precio = prop.precio_por_dia;
    card.dataset.tipo = prop.tipo; 
    card.dataset.habitaciones = prop.cantidad_habitaciones;
    card.dataset.metros = prop.metros_cuadrados;
    
    const imagenUrl = `static/img/img-propiedades/${prop.id_propiedad}/1.jpg`;
    card.innerHTML = `
      <div class="card h-100">
        <img src="${imagenUrl}" class="card-img-top" alt="Propiedad${prop.id_propiedad}" width="250" height="250"/>
        <div class="card-body">
          <h5 class="card-title">${prop.localidad}</h5>
          <p class="card-text"> Dirección: ${prop.calle} ${prop.numero}</p>
          <p class="card-text"> Tipo: ${prop.tipo}</p>
          <p class="card-text"> Habitaciones: ${prop.cantidad_habitaciones}</p>
          <p class="card-text"> Huéspedes: ${prop.cantidad_huespedes}</p>
          <p class="card-text">Precio por día: ${prop.precio_por_dia}</p>

        </div>
      </div>
    `;

    contenedor.appendChild(card);
    const cardContainer = contenedor.lastElementChild;
    cardContainer.addEventListener('click', () => {
        const huespedes = document.getElementById("huespedes").value
        const checkin = document.getElementById("checkin").value;
        const checkout = document.getElementById("checkout").value;
      window.location.href = `/ver_propiedad?id=${prop.id_propiedad}&res_hues=${huespedes}&res_in=${checkin}&res_out=${checkout}`; 
    });
  });
}


/**
 * Muestra un modal con informacion de la propiedad recibida como parámetro
 *
 * @param {Json} prop Propiedad a mostrar en el modal
 */
function mostrarModalPropiedad(prop) {
  const modalBodyContent = document.getElementById('modal-body-content');
  const propiedadModalLabel = document.getElementById('propiedadModalLabel');
  propiedadModalLabel.textContent = `Propiedad ${prop.calle} ${prop.numero}`;

  const imagenUrl = `static/img/img-propiedades/${prop.id_propiedad}/1.jpg`;//Aca si vamos a mostrar muchas imagenes hay que cambiar esto!
  modalBodyContent.innerHTML = `
    <div class="row">
      <div class="col-md-6">
        <img src="${imagenUrl}" class="img-fluid rounded" alt="Propiedad ${prop.id_propiedad}">
      </div>
      <div class="col-md-6">
        <h4>Detalles de la Propiedad</h4>
        <p><strong>Calle:</strong> ${prop.calle} ${prop.numero}</p>
        <p><strong>Localidad:</strong> ${prop.localidad}</p>
        <p><strong>Tipo:</strong> ${prop.tipo}</p>
        <p><strong>Habitaciones:</strong> ${prop.cantidad_habitaciones}</p>
        <p><strong>Baños:</strong> ${prop.cantidad_banios}</p>
        <p><strong>Huéspedes:</strong> ${prop.cantidad_huespedes}</p>
        <p><strong>Precio por día:</strong> $${prop.precio_por_dia}</p>
        <p><strong>Descripción:</strong> ${prop.descripcion || 'No disponible'}</p>
      </div>
    </div>
  `;

  const propiedadModal = new bootstrap.Modal(document.getElementById('propiedadModal'));
  propiedadModal.show();
}



///////////////////////////////////////////////////SIDEBAR Y FILTROS/////////////////////////////////////
function acomodarSideBar(estado, clase){

  const sidebar = document.getElementById('sidebar');
  console.log(estado, " - ", clase)
  if (sidebar.classList.contains(estado)) {

    sidebar.classList.add(clase);
}
}
const sidebar = document.getElementById('sidebar');
const btnToggleSidebar = document.getElementById('btnToggleSidebar');

btnToggleSidebar.addEventListener('click', () => {
  sidebar.classList.toggle('collapsed');
 // const icon = btnToggleSidebar.querySelector(".icon-sidebar");
  const label = btnToggleSidebar.querySelector('.label');
  if (sidebar.classList.contains('collapsed')) {
   // icon.textContent = '>>';
      if(label){
          label.style.display = 'none';
      }
    } else {
   //icon.textContent = '<<';
      if(label){
      label.style.display = 'inline';
      console.log("cierro")
      }
    }
});
  // cerrar sidebar al hacer clic fuera
  document.addEventListener('click', function (e) {
    if (!sidebar.contains(e.target) && !btnToggleSidebar.contains(e.target)) {
      sidebar.classList.add('collapsed');
      btnToggleSidebar.textContent = '»';
    }
  });



// Función para aplicar los filtros del sidebar
document.getElementById('aplicarFiltros').addEventListener('click', function() {
  let tipoVivienda = document.getElementById('tipoVivienda').value;
  let precioMaximo = parseInt(document.getElementById('precioRange').value);
  console.log("precio seleccionado de corte",precioMaximo)
  let habitaciones = document.getElementById('cantidadHabitaciones').value;
  console.log(habitaciones); 
  let propiedadesContainer = document.getElementById('propiedades');
  let cards = propiedadesContainer.querySelectorAll('.card-container');
  
  let hayResultados = false;

  cards.forEach(card => {
    let precio = parseInt(card.dataset.precio) || 0;
  
    console.log("precio card", precio)
    let tipo = card.dataset.tipo || '';
    let habs = card.dataset.habitaciones || '';

  
    // Verificar cada filtro
    // let cumplePrecio = precio <= precioMaximo;
    let cumplePrecio=false;
    console.log("precioMaximo", precioMaximo, " precio ", precio); 
    if (precioMaximo > precio){
      console.log("preio max del if", precioMaximo)
      cumplePrecio=true;
    }
    console.log("cumple precio card", cumplePrecio)
    let cumpleTipo = !tipoVivienda || tipo.toLowerCase() === tipoVivienda.toLowerCase();
    let cumpleHabitaciones = !habitaciones || habs.toString() === habitaciones.toString();
    
    if (cumplePrecio && cumpleTipo && cumpleHabitaciones) {
      card.style.display = 'block';
      hayResultados = true;
    } else {
      card.style.display = 'none';
    }
  });

  if (hayResultados) {
    titulo.innerHTML = "";
  } else {
    titulo.innerHTML = "No se encontraron propiedades con los filtros aplicados";
    // Vaciar el contenedor si no hay resultados visibles
    propiedadesContainer.innerHTML = '';
  }

});
// Función para quitar todos los filtros

document.getElementById('quitarFiltros').addEventListener('click', function() {
  // Resetear los controles del sidebar
  document.getElementById('precioRange').value = 150000;
  document.getElementById('precioLabel').textContent = 'Hasta $300000';
  document.getElementById('tipoVivienda').value = '';
  document.getElementById('cantidadHabitaciones').value = '';
 // document.getElementById('metrosCuadrados').value = '';

  // Mostrar todas las propiedades nuevamente
  //const propiedadesContainer = document.getElementById('propiedades');
  //const cards = propiedadesContainer.querySelectorAll('.card-container');
  //cards.forEach(card => {
  // card.style.display = 'block';
  //});

  document.getElementById('titulo').innerHTML = "Propiedades";
  console.log(resultado); 
  renderizarPropiedades(resultado);
});

// Actualizar el label del rango de precio
const precioRangeInput = document.getElementById('precioRange');
const precioLabel = document.getElementById('precioLabel');
if (precioRangeInput && precioLabel) {
  precioRangeInput.addEventListener('input', function() {
    precioLabel.textContent = `Hasta $${this.value}`;
  });
}




////////////////////////////////////////ERRORES Y VALIDACIONES///////////////////
document.addEventListener("DOMContentLoaded", async() => {
  const campos = ["localidad", "huespedes", "checkin", "checkout"];
  campos.forEach(id => {
    const campo = document.getElementById(id);
    campo.addEventListener("input", () => {
      const error = document.getElementById(id + "-error");
      if (error) error.remove();
      campo.classList.remove("input-error");
    });
  });

  // SETEAR TIPO Y NOMBRE COMPLETO DE USUARIO
  const datos_sesion_actual = await ver_sesion_actual();
  const datos_usuario = await obtener_un_solo_usuario_por_ID(datos_sesion_actual.id_usuario);

  if(datos_sesion_actual.rol == "EMPLEADO" || datos_sesion_actual.rol == "GERENTE"){
    document.getElementById("tipo-usuario").innerText = "AUTENTICADO/A COMO: " + datos_sesion_actual.rol;
  }

  document.getElementById("nombre-apellido-usuario").innerText = "BIENVENIDO/A " + (datos_usuario.nombre + " " + datos_usuario.apellido).toUpperCase() + " " || "";

});

const btnBuscar = document.getElementById("btnBuscar");
const btnCancelar = document.getElementById("btnCancelar");
const today = new Date();
const oneYearFromToday = new Date();
oneYearFromToday.setFullYear(today.getFullYear() + 1);

const pickerCheckin = new Litepicker({
  element: document.getElementById('checkin'),
  format: 'YYYY-MM-DD',
  lang: 'es-ES',
  minDate: new Date(),
  maxDate: oneYearFromToday.toISOString().split('T')[0],
  setup: (picker) => {
    picker.on('selected', (date) => {
      const checkinDate = date.dateInstance;

      // establezco la fecha mínima del checkout al día siguiente del checkin
      const nextDay = new Date(checkinDate);
      nextDay.setDate(checkinDate.getDate() + 1);
      pickerCheckout.setOptions({ minDate: nextDay })

      if (pickerCheckout.getDate() && pickerCheckout.getDate() < nextDay) {
        pickerCheckout.clear();
      }
    });
  }
});

const pickerCheckout = new Litepicker({
  element: document.getElementById('checkout'),
  format: 'YYYY-MM-DD',
  lang: 'es-ES',
  minDate: new Date(),
  maxDate: oneYearFromToday.toISOString().split('T')[0],
  setup: (picker) => {
    picker.on('selected', (date) => {
      const checkoutDate = date.dateInstance;

      // establezco la fecha máxima del checkin al día anterior del checkout
      const prevDay = new Date(checkoutDate);
      prevDay.setDate(checkoutDate.getDate() - 1);
      pickerCheckin.setOptions({ maxDate: prevDay })


      if (pickerCheckin.getDate() && pickerCheckin.getDate() > prevDay) {
        pickerCheckin.clear();
      }
    });
  }
});

async function validarBusqueda(){
  const localidad = document.getElementById("localidad").value.trim();
  console.log(localidad); 
  console.log(localidad.length); 
  const huespedes = document.getElementById("huespedes").value
  const checkin = document.getElementById("checkin").value;
  const checkout = document.getElementById("checkout").value;
  limpiarErrores();
  let tieneError= false; 

 if (localidad.length < 3) { 
    console.log("la localidad tiene menos caracteres de los requeridos")
    mostrarError("localidad", "La localidad debe tener al menos 3 caracteres.");
    tieneError=true;
  }

  if (!checkin) {
    mostrarError("checkin", "Por favor, ingrese una fecha de check-in");
    tieneError=true; 
  }
  if (!checkout) {
    mostrarError("checkout", "Por favor, ingrese una fecha de check-out");
    tieneError=true;
  }

   if (!tieneError){
    console.log("Criterios de busqueda validos");
    const criteriosBusqueda = {
      localidad: localidad,
      huespedes: huespedes, 
      checkin: checkin,
      checkout: checkout
    };
  
    console.log(criteriosBusqueda); 
    return criteriosBusqueda;
  }
  return null; 

}

//////////////////////////////////ENVIO DE JSON COMUNICACIÓN CON EL BACK
async function enviarBusqueda(criteriosBusqueda) {
  if (!(criteriosBusqueda == null)) {
    console.log("form valido");
    
    try {
      const params = new URLSearchParams();
      for (const key in criteriosBusqueda) {
        params.append(key, criteriosBusqueda[key]);
      }

      const url = `http://localhost:4000/propiedad/getPropiedadesBusqueda?${params.toString()}`;

      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
      });
      //reinicializo la variable resultado
      resultado=[]; 
      resultado = await response.json();
    
      if (response.status === 200) {
        // Muestra el sidebar solo cuando hay resultados
        const sidebar = document.getElementById("sidebar");
        
        sidebar.classList.add("visible");
        acomodarSideBar('visible','sidebar-estilo-verde' )
        console.log("volvi");
        
        if(Array.isArray(resultado) && resultado.length > 0){
          renderizarPropiedades(resultado);
        } else {
          const titulo = document.getElementById('titulo');
          console.log("array vacio")
          titulo.innerHTML = "Lo sentimos, actualmente no contamos con propiedades que coincidan con los criterios ingresados";
          renderizarPropiedades([]); 
        }
      } else if (resultado["Code"] == "DATABASE-ERROR") {
        console.log(resultado["DatabaseError"]); 
        alert("Ocurrió un error inesperado en el sistema.");
      } else if (resultado["Code"] == "GENERIC-ERROR") {
        alert("Ocurrió un error inesperado.");
      }
      
    } catch (error) {
      alert("Ocurrió un error");
    }
    
    btnBuscar.disabled = false;
  } else {
    console.log("form con errores");
    btnBuscar.disabled = false;
  }
}


document.getElementById("searchForm").addEventListener("submit", async function (e) {
  e.preventDefault(); // previene el envío por defecto

  btnBuscar.disabled = true;
  ///btnCancelar.classList.add("disabled-link");

  limpiarErrores(); // borra errores anteriores
  const criteriosBusqueda = await validarBusqueda(); // corre validaciones

  
  console.log(criteriosBusqueda);

  if (!(criteriosBusqueda == null)) {
    
    console.log("form valido");
    enviarBusqueda(criteriosBusqueda); 
    btnBuscar.disabled = false;
 ;
  } else {
    console.log("form con errores");
    btnBuscar.disabled = false;
   
  }});

async function cerrarSesion() {    
  try {
    const url = `http://localhost:4000/usuario/cerrar_sesion`;

    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    });

    resultado = await response.json();

    if(response.status === 200){
      window.location.href = "/";
    }
    else{
      alert("Ocurrió un error al intentar cerrar sesion.");
    }
    acomodarSideBar()

  }
  catch (error) {
    alert("Ocurrió un error al intentar cerrar sesion.");
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



  ///////////////////////////////////////////////Modal bootstrap para medios de pago y contacto 
const btnMedios = document.getElementById('btn-medios');
const btnContacto = document.getElementById('btn-contacto');
const btnCerrarSesion = document.getElementById('btn-cerrar-sesion');
const btnConfirmacionCerrarSesion = document.getElementById('btn-confirmacion-cerrar-sesion');

document.getElementById("btn-ver-perfil").addEventListener("click", function() {
    window.location.href = "/perfil_usuario";
});


if (btnMedios){
  btnMedios.addEventListener('click', (e) => {
    e.preventDefault();
    const mediosPagoModal = new bootstrap.Modal(document.getElementById('mediosPagoModal'));

    mediosPagoModal.show();
  });
}

if (btnContacto){
  btnContacto.addEventListener('click', (e) => {
    e.preventDefault();
    const contactoModal = new bootstrap.Modal(document.getElementById('contactoModal'));

    contactoModal.show();
  });
}

if(btnCerrarSesion){
  btnCerrarSesion.addEventListener('click', (e) => {
    e.preventDefault();
    const cerrarSesionModal = new bootstrap.Modal(document.getElementById('cerrarSesionModal'));

    cerrarSesionModal.show();
  });

  btnConfirmacionCerrarSesion.addEventListener('click', (e) => {
    e.preventDefault();
    cerrarSesion();
  });
}
