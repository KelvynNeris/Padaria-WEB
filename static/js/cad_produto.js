// Lógica para exibir campos de preço por unidade
document.getElementById('precoPorUnidade').addEventListener('change', function () {
    var campoPreco = document.getElementById('campoPreco');
    var campoUnidades = document.getElementById('campoUnidades');
    var campoPrecoInput = document.getElementById('preco');
    var campoUnidadesInput = document.getElementById('unidades_estocadas');

    if (this.checked) {
        campoPreco.style.display = 'block';
        campoUnidades.style.display = 'block';
        campoPrecoInput.setAttribute('required', 'true');
        campoUnidadesInput.setAttribute('required', 'true');

        document.getElementById('campoKilos').style.display = 'none';
        document.getElementById('campoPrecoKilo').style.display = 'none';
        document.getElementById('precoPorKilo').checked = false;
        document.getElementById('kilos_estocados').removeAttribute('required');
        document.getElementById('preco_kilo').removeAttribute('required');
        document.getElementById('vendido_por_kilo').value = 'false';
    } else {
        campoPreco.style.display = 'none';
        campoUnidades.style.display = 'none';
        campoPrecoInput.removeAttribute('required');
        campoUnidadesInput.removeAttribute('required');
    }
});

// Lógica para exibir campos de preço por kilo
document.getElementById('precoPorKilo').addEventListener('change', function () {
    var campoKilos = document.getElementById('campoKilos');
    var campoPrecoKilo = document.getElementById('campoPrecoKilo');
    var campoKilosInput = document.getElementById('kilos_estocados');
    var campoPrecoKiloInput = document.getElementById('preco_kilo');

    if (this.checked) {
        campoKilos.style.display = 'block';
        campoPrecoKilo.style.display = 'block';
        campoKilosInput.setAttribute('required', 'true');
        campoPrecoKiloInput.setAttribute('required', 'true');

        document.getElementById('campoPreco').style.display = 'none';
        document.getElementById('campoUnidades').style.display = 'none';
        document.getElementById('precoPorUnidade').checked = false;
        document.getElementById('preco').removeAttribute('required');
        document.getElementById('unidades_estocadas').removeAttribute('required');
        document.getElementById('vendido_por_kilo').value = 'true';
    } else {
        campoKilos.style.display = 'none';
        campoPrecoKilo.style.display = 'none';
        campoKilosInput.removeAttribute('required');
        campoPrecoKiloInput.removeAttribute('required');
    }
});