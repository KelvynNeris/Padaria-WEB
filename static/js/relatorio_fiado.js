function descontar(transacao_id) {
    var valor_pago = document.getElementById('valor_pago_' + transacao_id).value;

    if (valor_pago && parseFloat(valor_pago) > 0) {
        valor_pago = parseFloat(valor_pago).toFixed(2);

        $.ajax({
            url: '/atualizar_pagamento/' + transacao_id,
            method: 'POST',
            contentType: 'application/json',  // Corrigido para JSON
            data: JSON.stringify({ valor_pago: valor_pago }),
            dataType: 'json',  // Garante que a resposta será tratada corretamente
            success: function(response) {
                console.log("Resposta da API:", response);
                if (response && response.success) {  // Evita erro se a resposta for null
                    alert(response.message || 'Pagamento atualizado com sucesso!');
                    location.reload();
                } else {
                    alert('Erro ao atualizar pagamento: ' + (response.message || 'Desconhecido'));
                }
            },
            error: function(xhr, status, error) {
                console.log("Erro AJAX:", xhr.responseText);
                alert('Erro na comunicação com o servidor: ' + error);
            }
        });
    } else {
        alert('Por favor, insira um valor válido');
    }
}