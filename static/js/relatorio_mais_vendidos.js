document.addEventListener('DOMContentLoaded', function () {
    // Inicialmente, o botão "Ver Mais" deve estar ativo
    document.querySelectorAll('.ver-mais').forEach((botao) => {
        botao.classList.add('active');
    });
});

function mostrarMais(idTabela) {
    const tabela = document.getElementById(idTabela);
    const tbody = tabela.querySelector('tbody');
    const linhasExtras = tabela.querySelectorAll('.linha-extra');

    // Exibe o tbody e as linhas extras ocultas
    if (tbody) {
        tbody.style.display = 'table-row-group';  // Exibe o tbody
    }
    linhasExtras.forEach((linha) => {
        linha.style.display = 'table-row';  // Exibe as linhas extras
    });

    alternarBotoes(idTabela, 'ver-mais', 'ver-menos');
}

function mostrarMenos(idTabela) {
    const tabela = document.getElementById(idTabela);
    const tbody = tabela.querySelector('tbody');
    const linhasExtras = tabela.querySelectorAll('.linha-extra');

    // Oculta as linhas extras e o tbody
    if (tbody) {
        tbody.style.display = 'none';  // Esconde o tbody
    }
    linhasExtras.forEach((linha) => {
        linha.style.display = 'none';  // Esconde as linhas extras
    });

    alternarBotoes(idTabela, 'ver-menos', 'ver-mais');
}

function alternarBotoes(idTabela, esconderClasse, mostrarClasse) {
    const tabela = document.getElementById(idTabela);
    const acoesDiv = tabela.closest('.relatorio-section').querySelector('.botoes-acoes');

    if (acoesDiv) {
        const esconderBtn = acoesDiv.querySelector(`.${esconderClasse}`);
        const mostrarBtn = acoesDiv.querySelector(`.${mostrarClasse}`);

        if (esconderBtn && mostrarBtn) {
            esconderBtn.classList.remove('active');
            mostrarBtn.classList.add('active');
        }
    } else {
        console.error('Elemento não encontrado');
    }
}

function atualizarFiltros() {
    const filtro = document.getElementById('filtro-quantidade').value;
    const dataInicial = document.getElementById('data-inicial').value;
    const dataFinal = document.getElementById('data-final').value;

    const form = document.getElementById('form-filtros');
    document.getElementById('input-filtro').value = filtro;

    // Atualiza o formulário com os valores atuais
    form.submit();
}