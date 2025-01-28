document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.ver-mais').forEach((botao) => botao.classList.add('active'));
});

function mostrarMais(idTabela, dadosExtras) {
    const tabela = document.getElementById(idTabela);
    dadosExtras.forEach((dado, index) => {
        const novaLinha = document.createElement("tr");
        novaLinha.classList.add("linha-extra");
        novaLinha.innerHTML = `
            <td>${index + 4}</td>
            <td>${dado.produto || dado.categoria}</td>
            <td>${dado.quantidade}</td>
        `;
        tabela.appendChild(novaLinha);
    });

    alternarBotoes(idTabela, 'ver-mais', 'ver-menos');
}

function mostrarMenos(idTabela) {
    const tabela = document.getElementById(idTabela);
    const linhasExtras = tabela.querySelectorAll(".linha-extra");
    linhasExtras.forEach((linha) => linha.remove());

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

// Inicia o "Ver Mais" como visível
document.querySelectorAll('.ver-mais').forEach((botao) => botao.classList.add('active'));