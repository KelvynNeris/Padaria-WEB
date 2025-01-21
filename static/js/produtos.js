function atualizarQuantidade(idProduto, acao) {
    const input = document.getElementById(`input-${idProduto}`);
    const quantidadeSpan = document.getElementById(`quantidade-${idProduto}`);
    const quantidade = parseInt(input.value);

    if (isNaN(quantidade) || quantidade <= 0) {
        alert("Por favor, insira uma quantidade válida.");
        return;
    }

    // Requisição AJAX para atualizar a quantidade
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
                // Atualiza a interface com a nova quantidade
                quantidadeSpan.textContent = data.nova_quantidade;
                input.value = '';
            } else {
                alert(data.error || 'Erro ao atualizar a quantidade.');
            }
        })
        .catch(error => {
            console.error('Erro na requisição:', error);
        });
}
