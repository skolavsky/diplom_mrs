const noteUrl = '{% url "clients:note" %}';

document.addEventListener('click', function (event) {
    if (event.target.classList.contains('note-button')) {
        var button = event.target;
        var clientId = button.getAttribute('data-client-id');
        var action = 'note'; // Заметить клиента

        // Создаем FormData для отправки данных
        var formData = new FormData();
        formData.append('id', clientId);
        formData.append('action', action);
        formData.append('csrfmiddlewaretoken', csrftoken);

        // Параметры запроса
        var noteOptions = {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            }
        };

        // Отправляем AJAX-запрос
        fetch(noteUrl, noteOptions)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    // Обновите интерфейс или выполните другие действия
                    var buttonText = button.textContent.trim();
                    if (buttonText === 'Сделать заметку') {
                        button.textContent = 'Удалить заметку';
                    } else {
                        button.textContent = 'Сделать заметку';
                    }
                } else {
                    console.error('Ошибка при отметке клиента');
                }
            })
            .catch(error => {
                console.error('Error occurred while noting client:', error);
                alert('Error occurred while noting client');
            });
    }
});