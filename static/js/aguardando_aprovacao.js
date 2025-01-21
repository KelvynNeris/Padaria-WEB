document.addEventListener("DOMContentLoaded", () => {
    const card = document.querySelector(".card");

    // Verifica no localStorage se é o primeiro carregamento
    if (!localStorage.getItem("pageLoaded")) {
        localStorage.setItem("pageLoaded", "true"); // Marca que a página foi carregada
        if (card) {
            card.classList.add("animate"); // Adiciona a animação no primeiro carregamento
        }
    }
});

// Atualiza a página a cada 10 segundos
setInterval(() => {
    window.location.reload();
}, 10000);
