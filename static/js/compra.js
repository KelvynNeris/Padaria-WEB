document.addEventListener("DOMContentLoaded", () => {
    const tabelaProdutos = document.getElementById("tabela-produtos").querySelector("tbody");
    const totalCompraEl = document.getElementById("total-compra");
    let totalCompra = 0;

    // Função para mostrar ou esconder o campo de nome do cliente
    const toggleNomeClienteField = () => {
        const tipoPagamentoSelect = document.getElementById("tipo-pagamento");
        const nomeClienteSection = document.querySelector(".nome-cliente-section");
        const nomeClienteInput = document.getElementById("nome-cliente");

        if (tipoPagamentoSelect.value === "fiado") {
            nomeClienteSection.style.display = "block";
            nomeClienteInput.setAttribute("required", "required");
        } else {
            nomeClienteSection.style.display = "none";
            nomeClienteInput.removeAttribute("required");
        }
    };

    // Monitorar mudanças no tipo de pagamento
    document.getElementById("tipo-pagamento").addEventListener("change", toggleNomeClienteField);

    // Iniciar com a configuração correta
    toggleNomeClienteField();

    document.getElementById("adicionar-produto").addEventListener("click", () => {
        const produtoSelect = document.getElementById("produto");
        const quantidadeInput = document.getElementById("quantidade");

        const produtoId = produtoSelect.value;
        const produtoNome = produtoSelect.options[produtoSelect.selectedIndex].text;
        const precoUnitario = parseFloat(produtoSelect.options[produtoSelect.selectedIndex].dataset.preco);
        const quantidade = parseInt(quantidadeInput.value);

        if (!produtoId || !quantidade || quantidade <= 0) {
            alert("Selecione um produto e insira uma quantidade válida.");
            return;
        }

        const precoTotal = precoUnitario * quantidade;
        totalCompra += precoTotal;

        // Adiciona o produto na tabela
        const novaLinha = document.createElement("tr");
        novaLinha.innerHTML = `
            <td>${produtoNome}</td>
            <td>${quantidade}</td>
            <td>R$ ${precoUnitario.toFixed(2)}</td>
            <td>R$ ${precoTotal.toFixed(2)}</td>
            <td><button type="button" class="remover-produto">Remover</button></td>
        `;
        tabelaProdutos.appendChild(novaLinha);

        totalCompraEl.textContent = totalCompra.toFixed(2);

        // Limpa os campos
        produtoSelect.value = "";
        quantidadeInput.value = "";

        // Remove produto
        novaLinha.querySelector(".remover-produto").addEventListener("click", () => {
            totalCompra -= precoTotal;
            totalCompraEl.textContent = totalCompra.toFixed(2);
            tabelaProdutos.removeChild(novaLinha);
        });
    });

    // Finalizar Compra
    document.getElementById("form-compra").addEventListener("submit", (e) => {
        e.preventDefault();
        const tipoPagamento = document.getElementById("tipo-pagamento").value;
        const nomeCliente = document.getElementById("nome-cliente").value;

        if (!tipoPagamento) {
            alert("Selecione o tipo de pagamento.");
            return;
        }

        if (tipoPagamento === "fiado" && !nomeCliente) {
            alert("O nome do cliente é obrigatório para pagamento fiado.");
            return;
        }

        alert("Compra registrada com sucesso!");
        // Aqui você pode enviar os dados para o backend via fetch
    });
});