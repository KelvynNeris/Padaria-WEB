function atualizarQuantidade(idProduto, acao) {
    const inputElement = document.getElementById(`input-${idProduto}`);
    const quantidadeElement = document.getElementById(`quantidade-${idProduto}`);
    const novaQuantidade = parseFloat(inputElement.value);

    if (isNaN(novaQuantidade) || novaQuantidade <= 0) {
        exibirMensagemErro("Por favor, insira uma quantidade válida.");
        return;
    }

    const atualQuantidade = parseFloat(quantidadeElement.textContent);
    const quantidadeAtualizada = acao === "colocar"
        ? atualQuantidade + novaQuantidade
        : atualQuantidade - novaQuantidade;

    // Verificar se a nova quantidade não é negativa
    if (quantidadeAtualizada < 0) {
        exibirMensagemErro("Quantidade não pode ser negativa.");
        return;
    }

    // Atualiza a quantidade na interface
    quantidadeElement.textContent = quantidadeAtualizada.toFixed(2); // Exibe com 2 casas decimais, no caso de Kilos

    // Enviar a requisição para o backend para atualizar no banco de dados
    fetch('/atualizar_quantidade', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id_produto: idProduto,
            quantidade: novaQuantidade,
            acao: acao,
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                exibirMensagemErro(data.error || 'Erro ao atualizar a quantidade.');
            } else {
                inputElement.value = ''; // Limpa o campo de input após sucesso
                exibirMensagemSucesso("Quantidade atualizada com sucesso!");
            }
        })
        .catch(error => {
            console.error('Erro na requisição:', error);
            exibirMensagemErro('Erro inesperado. Tente novamente mais tarde.');
        });
}

function abrirModalConfirmacao(idProduto) {
    const modal = document.getElementById("modal-confirmacao");
    const confirmarBtn = document.getElementById("confirmar-remocao");
    modal.style.display = "flex";

    confirmarBtn.onclick = () => {
        fetch(`/remover_produto/${idProduto}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    exibirMensagemSucesso("Produto removido com sucesso!");
                    location.reload();
                } else {
                    exibirMensagemErro(data.error || 'Erro ao remover o produto.');
                }
            })
            .catch(error => {
                console.error('Erro na requisição:', error);
                exibirMensagemErro('Erro inesperado. Tente novamente mais tarde.');
            });

        modal.style.display = "none";
    };
}

function fecharModal() {
    const modal = document.getElementById("modal-confirmacao");
    modal.style.display = "none";
}

function exibirMensagemSucesso(mensagem) {
    const alerta = document.createElement("div");
    alerta.className = "alerta alerta-sucesso";
    alerta.textContent = mensagem;
    document.body.appendChild(alerta);
    setTimeout(() => alerta.remove(), 3000);
}

function exibirMensagemErro(mensagem) {
    const alerta = document.createElement("div");
    alerta.className = "alerta alerta-erro";
    alerta.textContent = mensagem;
    document.body.appendChild(alerta);
    setTimeout(() => alerta.remove(), 3000);
}