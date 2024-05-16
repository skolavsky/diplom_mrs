var page = 1;
var emptyPage = false;
var blockRequest = false;

let filters


function updateTable(clear_url = false) {

    var m_url = page_url + '?table_only=1&'; // Формирование URL с учётом номера страницы

    if (clear_url === true) {

    } else {
        m_url = m_url + 'page=' + page + '&' + filters;
    }


    console.log(m_url)
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
    } else if (isForwardButton) {
        page += 1;
    } else if (isLastFirst) {
        page = 1;
    } else {
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

document.querySelectorAll('.sort-link').forEach(link => {
    link.addEventListener('click', function (event) {
        event.preventDefault(); // Предотвращаем стандартное действие ссылки

        const sortField = this.dataset.sort; // Получаем поле для сортировки из атрибута data-sort
        const sortOrder = this.dataset.order; // Получаем порядок сортировки из атрибута data-order

        // Формируем URL для асинхронного запроса с учетом параметров сортировки
        const url = `${page_url}?sort=${sortField}&order=${sortOrder}&table_only=1`;

        // Вызываем функцию обновления таблицы с новым URL
        updateTable(url);
    });
});


document.querySelectorAll('.btn-filter').forEach(link => {
    link.addEventListener('click', function (event) {
        event.preventDefault(); // Предотвращаем стандартное действие кнопки
        const filterCheckboxes = document.querySelectorAll('.filter-group input[type="checkbox"]:checked');
        filters = Array.from(filterCheckboxes).map(checkbox => checkbox.name + '=1').join('&');
        // Теперь у вас есть строка параметров с выбранными значениями чекбоксов
        filters += '&' + 'search=' + document.getElementById('searchInput').value;
        console.log(filters); // Пример вывода в консоль для проверки

        updateTable()
        // Здесь можете добавить код для использования переменной filters
    });
});

const resetButton = document.getElementById('resetButton');

resetButton.addEventListener('click', function (event) {
    event.preventDefault(); // Предотвращаем стандартное действие кнопки
    const checkboxes = document.querySelectorAll('.filter-group input[type="checkbox"]');
    filters = ''
    // Снимаем галки с каждого чекбокса
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
    });

    updateTable(true)
});


const searchButton = document.getElementById('searchButton');
searchButton.addEventListener('click', function (event) {
    // Предотвращаем стандартное действие кнопки
    event.preventDefault();

    // Получаем значение из поля ввода
    filters += '&' + 'search=' + document.getElementById('searchInput').value;

    // Теперь у вас есть значение из поля ввода, которое можно использовать
    updateTable()
});

const tableHeaders = document.querySelectorAll('.table th');
document.querySelectorAll('.table th a').forEach(link => {
    link.onclick = function (event) {
        event.preventDefault(); // Предотвращаем стандартное действие ссылки
        const href = this.getAttribute('href'); // Получаем URL-адрес из атрибута href
        const urlParams = new URLSearchParams(href.split('?')[1]); // Получаем параметры из URL-адреса
        const sortValue = urlParams.get('sort'); // Получаем значение параметра sort
        const orderValue = urlParams.get('order'); // Получаем значение параметра order
        const currentSortOrder = `sort=${sortValue}&order=${orderValue}`; // Формируем текущую сортировку и порядок
        filters += '&' + currentSortOrder;
        updateTable();

        // Возвращаем false, чтобы предотвратить переход по ссылке
        return false;
    };
});

document.addEventListener('click', function (event) {
    if (event.target.classList.contains('show-spoiler-button')) {
        const button = event.target;
        const clientUrl = button.dataset.clientUrl;
        const clientId = clientUrl.split('/')[1];
        const clientDataDiv = document.getElementById(clientId);

        if (clientDataDiv.style.display === 'block') {
            // Если спойлер открыт, закрываем его
            clientDataDiv.style.display = 'none';
        } else {
            // Если спойлер закрыт, отправляем запрос на сервер для получения данных
            fetch(clientUrl, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                },
            })
                .then(response => response.text())
                .then(html => {
                    // Вставляем полученный HTML внутрь div для клиента
                    clientDataDiv.innerHTML = html;

                    // Показываем спойлер с данными
                    clientDataDiv.style.display = 'block';
                })
                .catch(error => console.error('Ошибка при отправке запроса:', error));
        }
    }
});


function extractClientId(href) {
    // Регулярное выражение для извлечения UUID из URL
    const regex = /\/([^/]+)\/$/;
    const match = regex.exec(href);
    return match ? match[1] : null;
}

document.addEventListener('click', function (event) {
    const saveButton = document.querySelector('button[name="action"][value="update_client"]');

    if (saveButton) {
        saveButton.addEventListener('click', function (event) {
            updateTable(false)
        });
    }
});