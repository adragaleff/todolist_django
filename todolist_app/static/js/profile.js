document.addEventListener('DOMContentLoaded', function () {
    var modal = document.getElementById("telegramModal");
    var openModalButton = document.getElementById("openModalButton");
    var closeModalButton = document.querySelector(".close-button");

    // Открытие модального окна
    openModalButton.onclick = function(event) {
        event.preventDefault(); // Предотвращает сабмит формы
        modal.style.display = "block";
    }

    // Закрытие модального окна при нажатии на "x"
    closeModalButton.onclick = function() {
        modal.style.display = "none";
    }

    // Закрытие модального окна при клике вне его содержимого
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});