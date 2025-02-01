document.querySelector('.menu-icon').addEventListener('click', function() {
    const navbarLinks = document.querySelector('.navbar-links');
    navbarLinks.classList.toggle('open');
    this.classList.toggle('change'); // Para a animação do ícone de hambúrguer
});