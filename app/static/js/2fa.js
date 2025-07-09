// -------------------------------------------------------------------------------------------------------------------//
// SETEO DE VARIABLES

  const mail = "tinchodimaria@gmail.com";
  const inputs = document.querySelectorAll("#ipt-confirmation input");
  const RESEND_SECONDS = 30;
  let codigoMail = Math.floor(Math.random() * 900000) + 100000;
  let data_2fa = {mail: mail, codigo: codigoMail};

// -------------------------------------------------------------------------------------------------------------------//
// FUNCIONES

  function validarCodigo(code, codigoMail) {
    console.log('code:', code, 'codigoMail: ', codigoMail);

    if (code == codigoMail) {
      showToast("success", "Iniciada la sesión correctamente.");
    } else {
      showToast("error", "Código incorrecto.");
    }
  }

  function reenviarCodigoPorMail() {

    let codigoMail = Math.floor(Math.random() * 900000) + 100000;
    let data_2fa = {mail: mail, codigo: codigoMail};

    fetch("/usuario/enviar_correo_2fa", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data_2fa)
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
  }

  /**
   * Muestra toast durante 3 segundos.
   * @param {"success"|"error"} type
   * @param {string} message
   **/

  function showToast(type, message) {
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

// -------------------------------------------------------------------------------------------------------------------//

document.addEventListener("DOMContentLoaded", () => {

  // Envio mail 2fa
  fetch("/usuario/enviar_correo_2fa", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data_2fa)
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
    const popup = document.getElementById("pup2FA");
    popup.style.display = "none";
  });

});