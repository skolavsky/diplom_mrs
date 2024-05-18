// Ваш существующий код

const saveButton = document.querySelector('button[name="action"][value="update_client"]');
const modal = document.getElementById('modal');
const modalBody = document.getElementById('modal-body');
const closeButton = document.querySelector('.close-button');

const clientTableWrapper = document.getElementById('clientTableWrapper');

clientTableWrapper.addEventListener('click', function (event) {
    if (event.target.classList.contains('show-spoiler-button')) {
        const clientUrl = event.target.getAttribute('data-client-url');

        fetch(clientUrl)
            .then(response => response.text())
            .then(data => {
                modalBody.innerHTML = data;
                modal.style.display = 'block';
            })
            .catch(error => console.error('Error:', error));
    }
});

closeButton.addEventListener('click', () => {
    modal.style.display = 'none';
});

// Добавляем обработчик событий для кнопки "Сохранить"
if (saveButton) {
    saveButton.addEventListener('click', () => {
        modal.style.display = 'none';
    });
}
