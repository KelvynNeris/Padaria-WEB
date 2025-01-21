function formatPhone() {
    var telInput = document.getElementById('telefone');
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

document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('form-cadastro');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            var telInput = document.getElementById('telefone');
            var telValue = telInput.value.trim();

            if (telValue) {
                telValue = '+55' + telValue.replace(/\D/g, ''); // Adiciona o código do país
                telInput.value = telValue;
            }

            this.submit();
        });
    }
});
