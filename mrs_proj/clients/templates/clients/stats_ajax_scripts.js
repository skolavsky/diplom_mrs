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
    .addEventListener('click', function (e) {
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
    let statsHTML = '<h3>Статистика пациентов:</h3>';
    statsHTML += '<ul>';
    statsHTML += `<li>Всего пациентов: ${statsData.total_clients}</li>`;
    statsHTML += `<li>Пациенты без исхода: ${statsData.active_clients}</li>`;
// Форматирование процентов с помощью toFixed()
    statsHTML += '</ul>';
    statsHTML += '<input type="number" id="percentInput" placeholder="Процент">';
    statsHTML += '<button id="submitPercentBtn" class="button">Установить порог прогноза</button>';


    // Обновляем содержимое спойлера
    statsSpoiler.innerHTML = statsHTML;

    // Переключаем видимость спойлера, если он скрыт
    if (statsSpoiler.style.display === 'none') {
        statsSpoiler.style.display = 'block';
    }
    document.getElementById("submitPercentBtn").addEventListener("click", function () {
        var percentValue = document.getElementById("percentInput").value;
        alert("Введённый процент: " + percentValue);
        param_url = url + '?percent=' + encodeURIComponent(percentValue);
        fetch(param_url, options)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
        .then(data => {
            if ('ready_in_week' in data) {
                alert('Ready in week: ' + data.ready_in_week);
                statsHTML += `<li>Выпишутся: ${data.ready_in_week}</li>`; // Обновляем HTML содержимое только здесь
                statsSpoiler.innerHTML = statsHTML;

            } else {
                alert('Ready in week не найден в ответе от сервера');
            }
        })
                .catch(error => {
                    console.error('There has been a problem with your fetch operation:', error);
                });


    });
}