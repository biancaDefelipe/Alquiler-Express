window.addEventListener('DOMContentLoaded', () => {
  const hoy = new Date().toISOString().split('T')[0]; // formato 'YYYY-MM-DD'
  document.getElementById("fechaNacimiento").setAttribute("max", hoy);
});
document.addEventListener("DOMContentLoaded", () => {
  const campos = ["nombre", "apellido", "email", "telefono", "dni", "fechaNacimiento"];
  campos.forEach(id => {
    const campo = document.getElementById(id);
    campo.addEventListener("input", () => {
      const error = document.getElementById(id + "-error");
      if (error) error.remove();
      campo.classList.remove("input-error");
    });
  });
});
const btnRegistrar = document.getElementById("btnRegistrar");
const btnCancelar = document.getElementById("btnCancelar");

/////////////////////////// funciones ///////////////////////////

function habilitarBotones() {
  btnRegistrar.disabled = false;
  btnCancelar.classList.remove("disabled-link");
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

// calcular la edad a partir de la fecha de nacimiento
function calcularEdad(fechaNacimiento) {
  const fechaHoy = new Date();
  const nacimiento = new Date(fechaNacimiento);
  let edad = fechaHoy.getFullYear() - nacimiento.getFullYear();
  const mes = fechaHoy.getMonth();
  const dia = fechaHoy.getDate();

  if (mes < nacimiento.getMonth() || (mes === nacimiento.getMonth() && dia < nacimiento.getDate())) {
    edad--; // si no paso el cumpleaños este año, resto un año
  }
  return edad;
}

//convertir fecha de nacimiento a string para poder guardarla en la bd
function fechaAString(fechaNacimiento){
  let fecha = new Date(fechaNacimiento); // fechaNacimiento es la fecha en formato Date
  let fechaString = fecha.toISOString().split('T')[0]; // esto devuelve 'YYYY-MM-DD'
  console.log(fechaString); // lo muestro para probar 
  return fechaString
}

///////////////////////////validación////////////////////////////////////
//usando async pauso la ejecución hasta que no se resulva el alta del usuario
async function validarFormulario() {
  limpiarErrores();
  let tieneError= false; 
  //uso trim para eliminar espacios en blanco
  const nombre = document.getElementById("nombre").value.trim();
  const apellido = document.getElementById("apellido").value.trim();
  const email = document.getElementById("email").value.trim();
  const telefono = document.getElementById("telefono").value.trim();
  const dni = document.getElementById("dni").value.trim();
  const fechaNacimiento = document.getElementById("fechaNacimiento").value;

  const edad = calcularEdad(fechaNacimiento); // validar que la edad sea mayor o igual a 18 años
  if (edad < 18) {
    mostrarError("fechaNacimiento", "Debe tener al menos 18 años para registrarse.");
    tieneError=true;
  }
   
  if (/\d/.test(nombre)) { // validar que el nombre no tenga numeros
    mostrarError("nombre", "El nombre no puede contener números.");
    tieneError=true;
  }

  if (/\d/.test(apellido)) {   //validar que el apellido no contenga números
    mostrarError("apellido", "El apellido no puede contener números.");
    tieneError=true;
  }

  // validar que el teléfono no contenga letras
  if (/[a-zA-Z]/.test(telefono)) { //.test()  para comprobar si una expresión regular (el patrón que está entre las barras /.../) encuentra alguna coincidencia dentro de una cadena de texto
    mostrarError("telefono", "El teléfono no puede contener letras.");
    tieneError=true;
  }

  
  if (nombre.length < 3) { // validar que el nombre tenga al menos 3 caracteres
    mostrarError("nombre", "El nombre debe tener al menos 3 caracteres.");
    tieneError=true;
  }
  if (apellido.length < 2) { // validar que el apellido tenga al menos 2 caracteres
    mostrarError("apellido", "El apellido debe tener al menos 2 caracteres.");
    tieneError=true;
  }

  
  if (telefono.length < 7) { // validar que el número de teléfono tenga al menos 7 dígitos
    mostrarError("telefono", "El número de teléfono debe tener al menos 7 dígitos.");
    tieneError=true;
  }

  
  if (dni.length < 8) { // validar que el DNI tenga al menos 8 dígitos
    mostrarError("dni", "El DNI debe tener al menos 8 dígitos.");
    tieneError=true;
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    mostrarError("email", "Ingrese un correo válido.");
    tieneError = true;
  }

  if (!tieneError){
    console.log("Formulario válido. Procediendo con el registro.");
    
        
    // si está todo ok armo el json
    const hoy = new Date();
    const fecha_hoy = hoy.toISOString().slice(0, 10); // "YYYY-MM-DD"

    const datosUsuario = {
      dni: dni,
      nombre: nombre,
      apellido: apellido,
      mail: email,
      telefono: telefono,
      fecha_nacimiento: fechaAString(fechaNacimiento), // YYYY-MM-DD
      contrasenia: null, 
      rol: "EMPLEADO",
      fecha_registro: fecha_hoy,
      eliminado: "NO"      
    };
    return datosUsuario; 
  }
  return null; 
}
async function enviarFormulario(datosUsuario){
  try {
    const response = await fetch("http://localhost:4000/usuario/alta", { 
      //solicitur http al servidor local corriendo en el puerto 4000, a la ruta /alta
      //await para que espere que llegue la respuesta antes de seguir
      method: "POST",
      headers: {
        "Content-Type": "application/json" //le digo al servidor que le estoy enviando un json
      },
      body: JSON.stringify(datosUsuario) // convierto el obj Usuario a un json
    });
  
    const resultado = await response.json();
  
    if (response.status === 201) {
      alert("Usuario registrado con éxito.");
      document.getElementById("formRegistro").reset();
      limpiarErrores();
      habilitarBotones();
//      window.location.href = urlIndex;

    } else if (resultado["Code"] == "MAIL-INVALIDO"){
      mostrarError("email", "El email ingresado ya está registrado.");
      habilitarBotones();
    }else if (resultado["Code"] == "DNI-INVALIDO"){
      mostrarError("dni", "El dni ingresado ya está registrado.");
      habilitarBotones();
    }else if (resultado["Code"] == "MAIL-ELIMINADO-ERROR"){
      mostrarError("email", "El email ingresado no se encuentra disponible.");
      habilitarBotones();
    }else if (resultado["Code"] == "DNI-ELIMINADO-ERROR"){
      mostrarError("dni", "El DNI ingresado no se encuentra disponible.");
      habilitarBotones();
    } else if (resultado ["Code"]== "DATABASE-ERROR") {
      alert("Ocurrió un error inesperado en el sistema.");//     + (resultado.DatabaseError || resultado.Error));
      habilitarBotones();
    } else if (resultado ["Code"]== "GENERIC-ERROR"){
      alert("Ocurrió un error inesperado.");
      habilitarBotones();
    }
  } catch (error) {
    alert("Ocurrió un error, intenté nuevamente");
    habilitarBotones();
  }
}

document.getElementById("formRegistro").addEventListener("submit", async function (e) {
  e.preventDefault(); // previene el envío por defecto

  // deshabilitar botones
  btnRegistrar.disabled = true;
  btnCancelar.classList.add("disabled-link");

  limpiarErrores(); // borra errores anteriores
  const datosUsuario = await validarFormulario(); // corre validaciones
  console.log(datosUsuario);

  if (!(datosUsuario == null)) {
    
    console.log("form valido");
    enviarFormulario(datosUsuario); 
 ;
  } else {
    console.log("form con errores");
    habilitarBotones();
   
  }
     
});