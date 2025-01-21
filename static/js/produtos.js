function atualizarQuantidade(idProduto, acao) {
    const input = document.getElementById(`input-${idProduto}`);
    const quantidadeSpan = document.getElementById(`quantidade-${idProduto}`);
    const quantidade = parseInt(input.value);

    if (isNaN(quantidade) || quantidade <= 0) {
        exibirMensagemErro("Por favor, insira uma quantidade válida.");
        return;
    }

    fetch('/atualizar_quantidade', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id_produto: idProduto,
            quantidade: quantidade,
            acao: acao,
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                quantidadeSpan.textContent = data.nova_quantidade;
                input.value = '';
                exibirMensagemSucesso("Quantidade atualizada com sucesso!");
            } else {
                exibirMensagemErro(data.error || 'Erro ao atualizar a quantidade.');
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
