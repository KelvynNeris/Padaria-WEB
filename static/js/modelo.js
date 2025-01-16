function toggleMenu(x) {
    // Alternar animação do botão hambúrguer
    x.classList.toggle("change");

    // Abrir ou fechar o menu
    const menu = document.getElementById("menu");
    menu.classList.toggle("open");
}
