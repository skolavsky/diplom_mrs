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
        console.log(filters); // Пример вывода в консоль для проверки
        updateTable()
        // Здесь можете добавить код для использования переменной filters
    });
});

const resetButton = document.getElementById('resetButton');

resetButton.addEventListener('click', function (event) {
    event.preventDefault(); // Предотвращаем стандартное действие кнопки
    const checkboxes = document.querySelectorAll('.filter-group input[type="checkbox"]');

    // Снимаем галки с каждого чекбокса
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
    });

    updateTable(true)
});


const searchButton = document.getElementById('searchButton');
searchButton.addEventListener('click', function(event) {
    // Предотвращаем стандартное действие кнопки
    event.preventDefault();

    // Получаем значение из поля ввода
    filters += 'search='+document.getElementById('searchInput').value;

    // Теперь у вас есть значение из поля ввода, которое можно использовать
    updateTable()
});
