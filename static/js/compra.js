$(document).ready(() => {
    // Inicializar Select2 no campo de produtos
    $('#produto').select2({
        placeholder: "Pesquise ou selecione um produto",
        allowClear: true,
        width: '100%'
    });

    const tabelaProdutos = $("#tabela-produtos tbody");
    const totalCompraEl = $("#total-compra");
    let totalCompra = 0;

    const toggleNomeClienteField = () => {
        const tipoPagamentoSelect = $("#tipo-pagamento").val();
        const nomeClienteSection = $(".nome-cliente-section");
        const nomeClienteInput = $("#nome-cliente");

        if (tipoPagamentoSelect === "fiado") {
            nomeClienteSection.show();
            nomeClienteInput.attr("required", "required");
        } else {
            nomeClienteSection.hide();
            nomeClienteInput.removeAttr("required");
        }
    };

    $("#tipo-pagamento").on("change", toggleNomeClienteField);
    toggleNomeClienteField();

    $("#adicionar-produto").on("click", () => {
        const produtoSelect = $("#produto");
        const quantidadeInput = $("#quantidade");

        const produtoId = produtoSelect.val();
        const produtoNome = produtoSelect.find(":selected").text();
        const precoUnitario = parseFloat(produtoSelect.find(":selected").data("preco") || 0);
        const quantidade = parseInt(quantidadeInput.val());

        if (!produtoId || isNaN(quantidade) || quantidade <= 0) {
            alert("Selecione um produto e insira uma quantidade válida.");
            return;
        }

        const precoTotal = precoUnitario * quantidade;
        totalCompra += precoTotal;

        const novaLinha = $(`
            <tr>
                <td>${produtoNome}</td>
                <td>${quantidade}</td>
                <td>R$ ${precoUnitario.toFixed(2)}</td>
                <td>R$ ${precoTotal.toFixed(2)}</td>
                <td><button type="button" class="remover-produto">Remover</button></td>
            </tr>
        `);

        tabelaProdutos.append(novaLinha);
        totalCompraEl.text(totalCompra.toFixed(2));

        produtoSelect.val("").trigger("change");
        quantidadeInput.val("");

        novaLinha.find(".remover-produto").on("click", () => {
            totalCompra -= precoTotal;
            totalCompraEl.text(totalCompra.toFixed(2));
            novaLinha.remove();
        });
    });

    $("#form-compra").on("submit", (e) => {
        e.preventDefault();
        const tipoPagamento = $("#tipo-pagamento").val();
        const nomeCliente = $("#nome-cliente").val();

        if (!tipoPagamento) {
            alert("Selecione o tipo de pagamento.");
            return;
        }

        if (tipoPagamento === "fiado" && !nomeCliente) {
            alert("O nome do cliente é obrigatório para pagamento fiado.");
            return;
        }

        alert("Compra registrada com sucesso!");
        // Aqui você pode enviar os dados para o backend via fetch ou AJAX
    });
});