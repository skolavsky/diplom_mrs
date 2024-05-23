var page = 1;
var emptyPage = false;
var blockRequest = false;
var last_page_number = document.getElementById('last_page_number').value;


function updateTable(clear_url = false) {

    var m_url = page_url + '?table_only=1&'; // Формирование URL с учётом номера страницы
    if (clear_url === true) {
        filters = '';  // Очищаем фильтры, если указан clear_url
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


