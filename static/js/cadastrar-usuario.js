console.log("JavaScript carregado com sucesso!");


// Certifique-se de que a função está definida de forma global
function formatPhone() {
    var telInput = document.getElementById('tel');
    var value = telInput.value.replace(/\D/g, ''); // Remove caracteres não numéricos

    if (value.length > 11) value = value.slice(0, 11); // Limita a 11 dígitos

    if (value.length > 10) {
        value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3'); // Formato celular
    } else if (value.length > 6) {
        value = value.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3'); // Formato fixo
    } else if (value.length > 2) {
        value = value.replace(/(\d{2})(\d{1,5})/, '($1) $2'); // Formato DDD
    }
    telInput.value = value;
}

// Adicionando o evento de submit após garantir que o DOM está carregado
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('form-cadastro').addEventListener('submit', function (e) {
        e.preventDefault();
        var telInput = document.getElementById('tel');
        var telValue = telInput.value.trim();

        if (telValue) {
            telValue = '+55' + telValue.replace(/\D/g, ''); // Remove qualquer caractere não numérico
            telInput.value = telValue;
        }

        this.submit();
    });
});
