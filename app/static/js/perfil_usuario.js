
const btnGuardarCambios = document.getElementById("btnGuardar");
const btnCambiarContrasenia = document.getElementById("btnCambiarContrasenia");
const btnGuardarContrasenia = document.getElementById("btnGuardarContrasenia");
const modalCambiarContrasenia = bootstrap.Modal.getInstance(document.getElementById('modalCambiarContrasenia'));
let id_usuario_actual = null;

document.addEventListener("DOMContentLoaded", async() => {
  const campos = ["dni", "fecha-nacimiento", "nombre", "apellido", "email", "telefono"];
  campos.forEach(id => {
    const campo = document.getElementById(id);
    campo.addEventListener("input", () => {
      const error = document.getElementById(id + "-error");
      if (error) error.remove();
      campo.classList.remove("input-error");
    });
  });

  const datos_sesion_actual = await ver_sesion_actual();
  id_usuario_actual = datos_sesion_actual.id_usuario;
  const datos_usuario = await obtener_un_solo_usuario_por_ID(id_usuario_actual);

  document.getElementById("dni").innerText = datos_usuario.dni || "";
  document.getElementById("fecha-nacimiento").innerText = datos_usuario.fecha_nacimiento || "";
  document.getElementById("nombre").value = datos_usuario.nombre || "";
  document.getElementById("apellido").value = datos_usuario.apellido || "";
  document.getElementById("email").innerText = datos_usuario.mail || "";
  document.getElementById("telefono").value = datos_usuario.telefono || ""; // Uso value acá porque es un input!!
});

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

/////////////////////////// funciones ///////////////////////////

function habilitarBotones() {
  btnGuardarCambios.disabled = false;
  btnCambiarContrasenia.disabled = false;
  btnGuardarContrasenia.disabled = false;
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

function fechaAString(fechaNacimiento){
  let fecha = new Date(fechaNacimiento); // fechaNacimiento es la fecha en formato Date
  let fechaString = fecha.toISOString().split('T')[0]; // esto devuelve 'YYYY-MM-DD'
  console.log(fechaString); // lo muestro para probar 
  return fechaString
}

///////////////////////////validación////////////////////////////////////
//usando async pauso la ejecución hasta que no se resulva la modificacion del usuario
async function validarFormulario() {
  limpiarErrores();
  let tieneError= false; 
  //uso trim para eliminar espacios en blanco
  const dni = document.getElementById("dni").innerText.trim();
  const fecha_nacimiento = document.getElementById("fecha-nacimiento").innerText.trim();
  const nombre = document.getElementById("nombre").value.trim();
  const apellido = document.getElementById("apellido").value.trim();
  const email = document.getElementById("email").innerText.trim();
  const telefono = document.getElementById("telefono").value.trim();

  
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
  else if (!/^\d+$/.test(telefono)) {
    mostrarError("telefono", "El teléfono no puede contener espacios ni caracteres especiales.");
    tieneError = true;
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


  if (!tieneError){
    console.log("Formulario válido. Procediendo con el registro.");
    // si está todo ok armo el json
    const datosUsuario = {
      dni: dni,
      fecha_nacimiento: fechaAString(fecha_nacimiento), // YYYY-MM-DD
      nombre: nombre,
      apellido: apellido,
      mail: email,
      telefono: telefono,
      //id_usuario: 2, dni: 98765432, nombre: Maria, apellido: Lopez, mail: maria@gmail.com, telefono: 987654321, fecha_nacimiento: 01-02-1986, rol: INQUILINO
    };
    return datosUsuario; 
  }
  return null; 
}

async function validarFormularioContrasenia() {
  limpiarErrores();
  let tieneError= false; 
  //uso trim para eliminar espacios en blanco
  const contrasenia_actual = document.getElementById("contrasenia-actual").value.trim();
  const nueva_contrasenia = document.getElementById("nueva-contrasenia").value.trim();
  const repetir_contrasenia = document.getElementById("repetir-contrasenia").value.trim();

  
  if (nueva_contrasenia.length < 7) { // validar que el nombre tenga al menos 3 caracteres
    mostrarError("nueva-contrasenia", "La nueva contraseña debe tener al menos 7 caracteres.");
    tieneError=true;
  }
  if (repetir_contrasenia.length < 7) { // validar que el apellido tenga al menos 2 caracteres
    mostrarError("repetir-contrasenia", "La nueva contraseña debe tener al menos 7 caracteres.");
    tieneError=true;
  }

  if (nueva_contrasenia != repetir_contrasenia) { // validar que ambas contrasenias coincidan.
    mostrarError("nueva-contrasenia", "Las contraseñas ingresadas no coinciden.");
    mostrarError("repetir-contrasenia", "Las contraseñas ingresadas no coinciden.");
    tieneError=true;
  }


  if (!tieneError){
    console.log("Formulario válido. Procediendo con el registro.");
    // si está todo ok armo el json
    const datosContrasenia = {
      contrasenia_actual: contrasenia_actual,
      nueva_contrasenia: nueva_contrasenia,
      repetir_contrasenia: repetir_contrasenia
    };
    return datosContrasenia; 
  }
  return null; 
}


async function enviarFormulario(datosUsuario){
  try {
    const url = `http://localhost:4000/usuario/modificar?id_usuario=${id_usuario_actual}`;

    const response = await fetch(url, { 
      //solicitur http al servidor local corriendo en el puerto 4000, a la ruta /modificar
      //await para que espere que llegue la respuesta antes de seguir
      method: "PUT",
      headers: {
        "Content-Type": "application/json" //le digo al servidor que le estoy enviando un json
      },
      body: JSON.stringify(datosUsuario) // convierto el obj Usuario a un json
    });
  
    const resultado = await response.json();
  
    if (response.status === 200) {
      alert("Los cambios se guardaron con éxito.");
      limpiarErrores();
      habilitarBotones();
//      window.location.href = urlIndex;

    }else if (resultado["Code"] == "ID-INVALIDO"){
      alert("Ocurrió un error al intentar guardar los cambios. Por favor vuelva a intentarlo.");
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

async function enviarFormularioContrasenia(datosContrasenia){
  const datos_sesion_actual = await ver_sesion_actual();
  id_usuario_actual = datos_sesion_actual.id_usuario;

  try {
    const url = `http://localhost:4000/usuario/cambiar_contrasenia?id_usuario=${id_usuario_actual}`;

    const response = await fetch(url, { 
      //solicitur http al servidor local corriendo en el puerto 4000, a la ruta /modificar
      //await para que espere que llegue la respuesta antes de seguir
      method: "PUT",
      headers: {
        "Content-Type": "application/json" //le digo al servidor que le estoy enviando un json
      },
      body: JSON.stringify(datosContrasenia) // convierto el obj Usuario a un json
    });
  
    const resultado = await response.json();
  
    if (response.status === 200) {
      alert("La contraseña se cambió con éxito.");
      limpiarErrores();
      habilitarBotones();
      
      // Cerrar el modal "Cambiar contraseña"
      const modalElement = document.getElementById('modalCambiarContrasenia');
      const modalInstance = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);
      modalInstance.hide();

      // Reiniciar solo el contenido de los inputs del modal "Cambiar contraseña"
      document.getElementById("formCambioContrasenia").reset();
      
      // Reiniciar solo los ojitos (sin tocar inputs ni errores)
      document.querySelectorAll("#formCambioContrasenia .toggle-password").forEach(button => {
        const input = document.getElementById(button.dataset.target);
        const icon = button.querySelector("i");

        // Volver a ocultar el texto (si estaba visible)
        input.type = "password";

        // Restaurar el ícono a ojo abierto
        icon.classList.remove("bi-eye-slash");
        icon.classList.add("bi-eye");
      });

    }else if (resultado["Code"] == "ID-INEXISTENTE"){
      alert("No se pudo cambiar su contraseña. Por favor, intente nuevamente.");
      habilitarBotones();
    } else if (resultado["Code"] == "CONTRASENIA-ACTUAL-INVALIDA"){
      mostrarError("contrasenia-actual", "La contraseña actual ingresada es incorrecta.");
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
  btnGuardarCambios.disabled = true;
  btnCambiarContrasenia.disabled = true;
  btnGuardarContrasenia.disabled = true;
  //btnCancelar.classList.add("disabled-link");

  limpiarErrores(); // borra errores anteriores
  const datosUsuario = await validarFormulario(); // corre validaciones
  console.log(datosUsuario);

  if (!(datosUsuario == null)) {
    
    console.log("form valido");
    enviarFormulario(datosUsuario, id_usuario_actual);
 ;
  } else {
    console.log("form con errores");
    habilitarBotones();
   
  }
     
});

document.getElementById("formCambioContrasenia").addEventListener("submit", async function (e) {
  e.preventDefault(); // previene el envío por defecto

  // deshabilitar botones
  btnGuardarCambios.disabled = true;
  btnCambiarContrasenia.disabled = true;
  btnGuardarContrasenia.disabled = true;
  //btnCancelar.classList.add("disabled-link");

  limpiarErrores(); // borra errores anteriores
  const datosContrasenia = await validarFormularioContrasenia(); // corre validaciones
  console.log(datosContrasenia);

  if (!(datosContrasenia == null)) {
    
    console.log("form valido");
    enviarFormularioContrasenia(datosContrasenia, id_usuario_actual);
 ;
  } else {
    console.log("form con errores");
    habilitarBotones();
   
  }
     
});