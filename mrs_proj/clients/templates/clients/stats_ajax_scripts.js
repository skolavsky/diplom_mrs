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

var page = 1;
var emptyPage = false;
var blockRequest = false;

function updateTable() {
    const m_url = page_url + '?table_only=1&page=' + page; // Формирование URL с учётом номера страницы
    fetch(m_url)
        .then(response => response.text())
        .then(html => {
            if (html === '') {
                emptyPage = true;
            } else {
                blockRequest = false;
                const externalTableWrapper = document.getElementById('clientTableWrapper');
                externalTableWrapper.innerHTML = html;

                // Удаляем предыдущие обработчики событий для кнопок пагинации
                document.querySelectorAll('.pagination a').forEach(link => {
                    link.removeEventListener('click', handlePaginationClick);
                });

                // Устанавливаем обработчики событий для кнопок пагинации заново
                document.querySelectorAll('.pagination a').forEach(link => {
                    link.addEventListener('click', handlePaginationClick);
                });
            }

        })
        .catch(error => {
            console.error('Ошибка при загрузке данных:', error);
        });
}

// Функция для обработки клика по кнопкам пагинации
function handlePaginationClick(event) {
    const isBackButton = this.classList.contains('btn-back');
    const isForwardButton = this.classList.contains('btn-forward');
    const isLastFirst = this.classList.contains('btn-first');

    if (isBackButton) {
        page -= 1;
    }
    else if (isForwardButton) {
        page += 1;
    }
    else if(isLastFirst)
    {
        page = 1;
    }
    else {
        page = last_page_number;
    }
    event.preventDefault();
    blockRequest = true;
    updateTable(); // Вызываем функцию обновления таблицы для новой ссылки и страницы
}

// Устанавливаем обработчики событий для кнопок пагинации
document.querySelectorAll('.pagination a').forEach(link => {
    link.addEventListener('click', handlePaginationClick);

});



