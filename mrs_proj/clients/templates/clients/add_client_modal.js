// Обработчик для отправки формы создания клиента
document.getElementById('addClientForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const formData = new FormData(this);

    alert(page_url);
    console.log(page_url);


    fetch(page_url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken,  // Получаем токен CSRF из формы
            'X-Requested-With': 'XMLHttpRequest'  // Кастомный заголовок для обозначения асинхронного запроса

        }
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Что-то пошло не так');
        })
        .then(data => {
            console.log('Success:', data);
            // Закрываем модальное окно
            document.getElementById('addClientModal').style.display = 'none';
            // Обновляем таблицу клиентов
            updateTable();
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
