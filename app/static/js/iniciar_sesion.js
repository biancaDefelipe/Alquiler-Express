// Ejecutar cuando el DOM esté listo
const popup2FA = document.getElementById("content2FA");

window.addEventListener("DOMContentLoaded", () => {
  popup2FA.style.display = "none";
  configurarLimpiezaErrores();
  configurarValidacionesPorInput();
});

  /**
   * Muestra toast durante 3 segundos.
   * @param {"success"|"error"} type
   * @param {string} message
   **/

  function showToast(type, message) {
    console.log("showToast"); 
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.textContent = message;

    container.appendChild(toast);

    // forzar layout para animar
    requestAnimationFrame(() => {
      toast.classList.add("show");
    });

    // Desaparece a los 3s y luego se quita del DOM
    setTimeout(() => {
      toast.classList.remove("show");
      toast.addEventListener(
        "transitionend",
        () => container.removeChild(toast),
        { once: true }
      );
    }, 3000);
  }

function configurarLimpiezaErrores() {
  const campos = [
    "mail", "contrasenia"
  ];
  campos.forEach(id => {
    const campo = document.getElementById(id);
    campo.addEventListener("input", () => {
      const error = document.getElementById(id + "-error");
      if (error) error.remove();
      campo.classList.remove("input-error");
    });
  });
}

function configurarValidacionesPorInput() {
  aplicarValidacionPorClase(".decimal-limit-5-2", /^\d{0,5}(\.\d{0,2})?$/, "Máximo 5 enteros y 2 decimales");
  aplicarValidacionPorClase(".decimal-limit-7-2", /^\d{0,7}(\.\d{0,2})?$/, "Máximo 7 enteros y 2 decimales");
  aplicarValidacionPorClase(".integer-limit-2", /^\d{0,2}$/, "Solo números enteros de hasta 2 dígitos");
  aplicarValidacionPorClase(".integer-limit-5", /^\d{0,5}$/, "Solo números enteros de hasta 5 dígitos");
  aplicarValidacionPorClase(".integer-limit-7", /^\d{0,7}$/, "Solo números enteros de hasta 7 dígitos");
  aplicarValidacionPorClase(".no-especiales", /^[a-zA-Z0-9\s]*$/, "No se permiten caracteres especiales")
}

function aplicarValidacionPorClase(selector, regex, mensajeError) {
  document.querySelectorAll(selector).forEach(input => {
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
  const campo = document.getElementById(idCampo);
  const errorId = "error-" + idCampo;
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
  document.querySelectorAll(".error-msg").forEach(e => e.remove());
  document.querySelectorAll(".input-error").forEach(campo => campo.classList.remove("input-error"));
}


function habilitarBotones() {
  document.getElementById("btnIngresar").disabled = false;
  document.getElementById("btnRegistrarse").disabled = false;
}


async function enviarFormulario(mail, contrasenia) {
  try {
    const url = new URL("http://localhost:4000/usuario/iniciar_sesion");
    url.searchParams.append("mail", mail);
    url.searchParams.append("contrasenia", contrasenia);

    const response = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    const resultado = await response.json();

    if (response.status === 200) {
      if (resultado['validacion']){

        if (resultado['Usuario']['rol'] == 'GERENTE') {
          verificarCodigo2fa(resultado['Usuario']['mail']);
        } else {
          //alert("Sesión iniciada con éxito.");
          document.getElementById("formIngresar").reset();
          limpiarErrores();
          rol=resultado['Usuario']['rol'].toLowerCase(); 

          window.location.href =`/`; 
        }
      }
      else{
        showToast("error", "El usuario y/o la contraseña son incorrectos.");
        document.getElementById("formIngresar").reset();
        limpiarErrores();
        habilitarBotones();
      }
    }
    else if (resultado["Code"] === "MAIL-INVALIDO"){
      showToast("error", "El mail ingresado no se encuentra registrado.");
      document.getElementById("formIngresar").reset();
      habilitarBotones();
    }
    else if (resultado["Code"] === "DATABASE-ERROR" || resultado["Code"] === "GENERIC-ERROR") {
      showToast("error", "Ocurrió un error inesperado en el sistema.");
      document.getElementById("formIngresar").reset();
      habilitarBotones();
    }
  }
  catch (error) {
    alert("Ocurrió un error, intentá nuevamente.");
    document.getElementById("formIngresar").reset();
    habilitarBotones();
  }
}

document.getElementById("formIngresar").addEventListener("submit", async function (e) {
  e.preventDefault();
  document.getElementById("btnIngresar").disabled = true;
    document.getElementById("btnRegistrarse").disabled = true;
  limpiarErrores();

  const mail = document.getElementById("mail").value.trim();
  const contrasenia = document.getElementById("contrasenia").value.trim();
  
  if (mail !== "" && contrasenia !== ""){
    enviarFormulario(mail, contrasenia);
  } else {
    habilitarBotones();
  }
});

document.getElementById("btnRegistrarse").addEventListener("click", function () {
  window.location.href = "/registro";
});





/*  ---------------------------------------------------------------------------  */
// 2FA

async function verificarCodigo2fa(mail) {

  // -------------------------------------//
  // VARIABLES
  const inputs = document.querySelectorAll("#ipt-confirmation input");
  const RESEND_SECONDS = 30;
  let codigoMail = Math.floor(Math.random() * 900000) + 100000;
  let data_2fa = { mail: mail, codigo: codigoMail };

  // ------------------------------------//
  // FUNCIONES

  function validarCodigo(code, codigoMail) {
    console.log("code:", code, "codigoMail: ", codigoMail);

    if (code == codigoMail) {
      showToast("success", "Iniciada la sesión correctamente.");
      console.log("codigo valido"); 
      window.location.href ="/"; 
    } else {
      showToast("error", "Código incorrecto.");
    }
  }

  function reenviarCodigoPorMail() {
    let codigoMail = Math.floor(Math.random() * 900000) + 100000;
    let data_2fa = { mail: mail, codigo: codigoMail };

    fetch("/usuario/enviar_correo_2fa", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data_2fa),
    })
      .then((response) => {
        if (response.ok) {
          console.log("success", "- Código enviado.");
          //agregado bian
          // Inputs para el código
            inputs.forEach((input, index) => {
            input.setAttribute("inputmode", "numeric");
            input.setAttribute("maxlength", 1);
            input.type = "text";

            input.addEventListener("input", (e) => {
              let value = e.target.value;

              // Limpia caracteres y limita a 1 solo elemento
              value = value.replace(/[^0-9]/g, "").slice(0, 1);
              e.target.value = value;

              // Mueve al siguiente input
              if (value && index < inputs.length - 1) {
                inputs[index + 1].focus();
              }

              // Cuando están todos los inputs completos
              const filled = Array.from(inputs).every((inp) => inp.value.length === 1);
              if (filled) {
                const code = Array.from(inputs)
                  .map((i) => i.value)
                  .join("");
                validarCodigo(code, codigoMail);
              }
            });

            // Forzar cursor al final
            input.addEventListener("focus", (e) => {
              const length = e.target.value.length;
              // Usamos setTimeout para asegurarnos que se aplique después del focus
              setTimeout(() => {
                e.target.setSelectionRange(length, length);
              }, 0);
            });

            input.addEventListener("keydown", (e) => {
              // Si presiona Backspace estando vacío, volver al anterior
              if (e.key === "Backspace" && input.value === "" && index > 0) {
                inputs[index - 1].focus();
              }
            });

            // Para pegar el código directamente en los inputs
            input.addEventListener("paste", (e) => {
              const pasted = (e.clipboardData || window.clipboardData).getData("text");
              const digits = pasted.replace(/[^0-9]/g, "").split("");

              e.preventDefault();

              for (let i = index; i < inputs.length && digits.length > 0; i++) {
                inputs[i].value = digits.shift();
              }

              const next = Array.from(inputs).find((inp) => inp.value === "");
              if (next) next.focus();
            });
          });
          //FIN DE AGREGADO
        } else {
          console.log("error", "- Error al enviar el código.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  // -------------------------------------------------------------------------------------------------------------------//

  popup2FA.style.display = "block";

  // Envio mail 2fa
  await fetch("/usuario/enviar_correo_2fa", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data_2fa),
  })
    .then((response) => {
      if (response.ok) {
        console.log("success", "- Código enviado.");
      } else {
        console.log("error", "- Error al enviar el código.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });

  // Inputs para el código
    inputs.forEach((input, index) => {
    input.setAttribute("inputmode", "numeric");
    input.setAttribute("maxlength", 1);
    input.type = "text";

    input.addEventListener("input", (e) => {
      let value = e.target.value;

      // Limpia caracteres y limita a 1 solo elemento
      value = value.replace(/[^0-9]/g, "").slice(0, 1);
      e.target.value = value;

      // Mueve al siguiente input
      if (value && index < inputs.length - 1) {
        inputs[index + 1].focus();
      }

      // Cuando están todos los inputs completos
      const filled = Array.from(inputs).every((inp) => inp.value.length === 1);
      if (filled) {
        const code = Array.from(inputs)
          .map((i) => i.value)
          .join("");
        validarCodigo(code, codigoMail);
      }
    });

    // Forzar cursor al final
    input.addEventListener("focus", (e) => {
      const length = e.target.value.length;
      // Usamos setTimeout para asegurarnos que se aplique después del focus
      setTimeout(() => {
        e.target.setSelectionRange(length, length);
      }, 0);
    });

    input.addEventListener("keydown", (e) => {
      // Si presiona Backspace estando vacío, volver al anterior
      if (e.key === "Backspace" && input.value === "" && index > 0) {
        inputs[index - 1].focus();
      }
    });

    // Para pegar el código directamente en los inputs
    input.addEventListener("paste", (e) => {
      const pasted = (e.clipboardData || window.clipboardData).getData("text");
      const digits = pasted.replace(/[^0-9]/g, "").split("");

      e.preventDefault();

      for (let i = index; i < inputs.length && digits.length > 0; i++) {
        inputs[i].value = digits.shift();
      }

      const next = Array.from(inputs).find((inp) => inp.value === "");
      if (next) next.focus();
    });
  });

  const btnReenviar = document.getElementById("btn-reenviar-cod");

  btnReenviar.addEventListener("click", (e) => {
    e.preventDefault();

    if (btnReenviar.disabled) {
      return;
    } else {
      btnReenviar.disabled = true;
      btnReenviar.backgroundColor = "#F4F4F4";

      reenviarCodigoPorMail();

      // Inicia contador
      let secondsLeft = RESEND_SECONDS;
      btnReenviar.textContent = `Reenviar (${secondsLeft}s)`;

      let countdownInterval;
      countdownInterval = setInterval(() => {
        secondsLeft--;
        if (secondsLeft > 0) {
          btnReenviar.textContent = `Reenviar (${secondsLeft}s)`;
        } else {
          clearInterval(countdownInterval);
          btnReenviar.disabled = false;
          btnReenviar.textContent = "Reenviar código";
        }
      }, 1000);
    }
  });

  const btnClose = document.getElementById("a-close");
  btnClose.addEventListener("click", (e) => {
    e.preventDefault();
    const popup = document.getElementById("content2FA");
    popup.style.display = "none";
  });
}
