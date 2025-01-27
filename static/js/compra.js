$(document).ready(() => {
    // Inicializar Select2 nos campos
    $('#produto, #cliente').select2({
        placeholder: "Pesquise ou selecione",
        allowClear: true,
        width: '100%'
    });

    const tabelaProdutos = $("#tabela-produtos tbody");
    const totalCompraEl = $("#total-compra");
    let totalCompra = 0;

    const atualizarTotalCompra = () => {
        totalCompraEl.text(totalCompra.toFixed(2));
    };

    // Atualizar o campo de quantidade baseado no tipo de produto
    const atualizarCamposQuantidade = () => {
        const produtoSelect = $("#produto");
        const vendidoKilo = produtoSelect.find(":selected").data("vendido-kilo");

        const quantidadeContainer = $("#quantidade-container");
        quantidadeContainer.empty(); // Limpar campos de quantidade anteriores

        if (vendidoKilo == 1) {
            // Se for vendido por quilo, adicionar campos para gramas e quilos
            quantidadeContainer.append(`
                <label for="quantidade-quilos">Quantidade (Kg):</label>
                <input type="number" id="quantidade-quilos" name="quantidade-quilos" min="0.01" step="0.01" placeholder="Kg">
                <label for="quantidade-gramas">Quantidade (g):</label>
                <input type="number" id="quantidade-gramas" name="quantidade-gramas" min="1" placeholder="g">
            `);
        } else {
            // Caso contrário, manter o input atual de quantidade por unidade
            quantidadeContainer.append(`
                <input type="number" id="quantidade" name="quantidade" min="1" placeholder="0">
            `);
        }
    };

    // Alterar a quantidade de campos ao escolher o produto
    $("#produto").on("change", atualizarCamposQuantidade);

    // Função para adicionar o produto na tabela
    $("#adicionar-produto").on("click", () => {
        const produtoSelect = $("#produto");
        const quantidadeInput = $("#quantidade");
        const quantidadeQuilosInput = $("#quantidade-quilos");
        const quantidadeGramasInput = $("#quantidade-gramas");

        const produtoId = produtoSelect.val();
        const produtoNome = produtoSelect.find(":selected").text();
        const precoUnitario = parseFloat(produtoSelect.find(":selected").data("vendido-kilo") == 1 ?
            produtoSelect.find(":selected").data("preco-kilo") :
            produtoSelect.find(":selected").data("preco"));

        let quantidade = 0;

        // Se for vendido por quilo, somar as quantidades de gramas e quilos
        if (produtoSelect.find(":selected").data("vendido-kilo") == 1) {
            const quantidadeQuilos = parseFloat(quantidadeQuilosInput.val()) || 0;
            const quantidadeGramas = parseInt(quantidadeGramasInput.val()) || 0;
            quantidade = quantidadeQuilos + (quantidadeGramas / 1000); // Convertendo gramas para quilos
        } else {
            quantidade = parseInt(quantidadeInput.val());
        }

        if (!produtoId || isNaN(quantidade) || quantidade <= 0) {
            alert("Selecione um produto e insira uma quantidade válida.");
            return;
        }

        // Verificar duplicação de produto
        const linhaExistente = tabelaProdutos.find(`tr[data-id="${produtoId}"]`);
        if (linhaExistente.length > 0) {
            alert("Produto já adicionado. Edite a quantidade diretamente na lista.");
            return;
        }

        const precoTotal = precoUnitario * quantidade;
        totalCompra += precoTotal;

        const novaLinha = $(`
            <tr data-id="${produtoId}">
                <td>${produtoNome}</td>
                <td><input type="number" class="quantidade-editar" value="${quantidade}" min="1"></td>
                <td>R$ ${precoUnitario.toFixed(2)} Kg</td>
                <td class="preco-total">R$ ${precoTotal.toFixed(2)}</td>
                <td><button type="button" class="remover-produto">Remover</button></td>
            </tr>
        `);

        tabelaProdutos.append(novaLinha);
        atualizarTotalCompra();

        // Resetar campos
        produtoSelect.val("").trigger("change");
        quantidadeInput.val("");
        quantidadeQuilosInput.val("");
        quantidadeGramasInput.val("");

        novaLinha.find(".remover-produto").on("click", () => {
            totalCompra -= precoTotal;
            atualizarTotalCompra();
            novaLinha.remove();
        });

        // Atualizar total ao editar a quantidade
        novaLinha.find(".quantidade-editar").on("input", () => {
            const novaQuantidade = parseFloat(novaLinha.find(".quantidade-editar").val());
            const novoPrecoTotal = precoUnitario * novaQuantidade;
            novaLinha.find(".preco-total").text(`R$ ${novoPrecoTotal.toFixed(2)}`);
            totalCompra = 0;
            tabelaProdutos.find("tr").each((_, row) => {
                const rowEl = $(row);
                const preco = parseFloat(rowEl.find(".preco-total").text().replace("R$ ", ""));
                totalCompra += preco;
            });
            atualizarTotalCompra();
        });
    });

    // Atualizar campos ao carregar a página, se necessário
    atualizarCamposQuantidade();

    $("#form-compra").on("submit", async (e) => {
        e.preventDefault();
        const tipoPagamento = $("#tipo-pagamento").val();
        const nomeCliente = $("#cliente").val();

        if (!tipoPagamento) {
            alert("Selecione o tipo de pagamento.");
            return;
        }

        if (tipoPagamento === "fiado" && !nomeCliente) {
            alert("O nome do cliente é obrigatório para pagamento fiado.");
            return;
        }

        const itens = [];
        $("#tabela-produtos tbody tr").each((_, row) => {
            const rowEl = $(row);
            itens.push({
                id_produto: rowEl.data("id"),
                quantidade: parseInt(rowEl.find("td:nth-child(2) input").val()), // Editar a quantidade
                preco_unitario: parseFloat(rowEl.find("td:nth-child(3)").text().replace("R$ ", ""))
            });
        });

        if (itens.length === 0) {
            alert("Adicione pelo menos um produto à compra.");
            return;
        }

        const idCliente = $("#cliente").val();

        const compraData = {
            tipo_pagamento: tipoPagamento,
            id_cliente: idCliente || null, // Enviar o ID do cliente
            itens,
        };

        try {
            const response = await fetch("/finalizar-compra", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(compraData),
            });

            if (response.ok) {
                alert("Compra registrada com sucesso!");
                window.location.reload();
            } else {
                const errorData = await response.json();
                alert(`Erro ao registrar compra: ${errorData.erro}`);
            }
        } catch (error) {
            alert("Erro ao registrar compra. Tente novamente.");
        }
    });
});