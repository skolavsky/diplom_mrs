// Создаем объект запроса
const options = {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json' // Указываем тип контента JSON
    },
    mode: 'same-origin'
};

document.getElementById('statsToggleBtn')
    .addEventListener('click', function(e) {
        e.preventDefault();

        // Получаем спойлер и текст кнопки
        const statsSpoiler = document.getElementById('statsSpoiler');
        const toggleBtn = document.getElementById('statsToggleBtn');

        // Проверяем текущее состояние спойлера
        if (statsSpoiler.style.display === 'none') {
            // Если спойлер скрыт, отправляем запрос и отображаем его
            fetch(url, options)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    // Обрабатываем полученные данные и обновляем спойлер
                    updateStatsSpoiler(data);
                    // Изменяем текст кнопки на "Скрыть статистику"
                    toggleBtn.textContent = 'Скрыть статистику';
                })
                .catch(error => {
                    console.error('There has been a problem with your fetch operation:', error);
                });
        } else {
            // Если спойлер открыт, скрываем его
            statsSpoiler.style.display = 'none';
            // Изменяем текст кнопки на "Показать статистику"
            toggleBtn.textContent = 'Показать статистику';
        }
    });

// Функция для обновления содержимого спойлера с данными статистики
function updateStatsSpoiler(statsData) {
    const statsSpoiler = document.getElementById('statsSpoiler');
    let statsHTML = '<h3>Статистика клиентов:</h3>';
    statsHTML += '<ul>';
    statsHTML += `<li>Всего записей: ${statsData.total_clients}</li>`;
    statsHTML += `<li>Активные записи: ${statsData.active_clients}</li>`;
// Форматирование процентов с помощью toFixed()
    const percentReadyInWeek = statsData.percent_ready_in_week.toFixed(3);
    statsHTML += `<li>Готовые в течение недели: ${statsData.ready_in_week} (${percentReadyInWeek} % от всех активных записей)</li>`;    // Другие данные статистики
    statsHTML += '</ul>';

    // Обновляем содержимое спойлера
    statsSpoiler.innerHTML = statsHTML;

    // Переключаем видимость спойлера, если он скрыт
    if (statsSpoiler.style.display === 'none') {
        statsSpoiler.style.display = 'block';
    }
}