const digitos = document.querySelectorAll(".digito");

digitos.forEach((digito, index) => {
    digito.addEventListener("input", () => {
        if (digito.value.length === 1 && index < digitos.length - 1) {
            digitos[index + 1].focus();
        }
    });

    digito.addEventListener("keydown", (e) => {
        if (e.key === "Backspace" && index > 0 && digito.value.length === 0) {
            digitos[index - 1].focus();
        }
    });
});