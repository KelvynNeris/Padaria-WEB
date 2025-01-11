$(document).ready(function () {
    // Se o popup for exibido, defina um temporizador para escondê-lo após 3 segundos
    if ($('.popup-container').is(':visible')) {
        setTimeout(function () {
            $('.popup-container').fadeOut(); // Usamos fadeOut para uma transição suave
        }, 3000); // Esconde após 3000ms (3 segundos)
    }
});