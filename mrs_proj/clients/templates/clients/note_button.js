const note_url = '{% url "clients:note" %}';

const note_options = {
    method: 'POST',
    headers: {'X-CSRFToken': csrftoken},
    mode: 'same-origin'
};

$(document).ready(function () {
    $(document).on('click', '.note-button', function () {
        var button = $(this);
        var clientId = button.data('client-id');
        var action = 'note'; // Заметить клиента

        // Создаем FormData для отправки данных
        var formData = new FormData();
        formData.append('id', clientId);
        formData.append('action', action);

        // Добавляем CSRF-токен в данные запроса
        formData.append('csrfmiddlewaretoken', csrftoken);

        // Обновляем параметры запроса
        note_options.body = formData;

        // Отправляем AJAX-запрос
        fetch(note_url, note_options)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    // Обновите интерфейс или выполните другие действия
                    if (button.text() === 'Забыть') {
                        button.text('Отметить');
                    } else {
                        button.text('Забыть');
                    }
                } else {
                }
            })
            .catch(error => {
                console.error('Error occurred while noting client:', error);
                alert('Error occurred while noting client');
            });
    });
});
