document.addEventListener('DOMContentLoaded', (event) => {
    const modal = document.getElementById('modal');
    const modalBody = document.getElementById('modal-body');
    const closeButton = document.querySelector('.close-button');

    document.querySelectorAll('.show-spoiler-button').forEach(button => {
        button.addEventListener('click', function () {
            const clientUrl = this.getAttribute('data-client-url');

            fetch(clientUrl)
                .then(response => response.text())
                .then(data => {
                    modalBody.innerHTML = data;
                    modal.style.display = 'block';
                })
                .catch(error => console.error('Error:', error));
        });
    });

    closeButton.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });
});


document.getElementById('toggleFormBtn').addEventListener('click', function () {
    document.getElementById('addClientForm').style.display = 'block';
});

function toggleForm() {
    let form = document.getElementById('addClientForm');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

function cancelAddClient() {
    let form = document.getElementById('addClientForm');
    form.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');

    // Event listener to enlarge the input field when typing
    searchInput.addEventListener('input', function () {
        if (searchInput.value.trim() !== '') {
            searchInput.classList.add('enlarged');
        } else {
            searchInput.classList.remove('enlarged');
        }
    });


    let filterCheckboxes = document.querySelectorAll('input[type="checkbox"]');

    document.addEventListener('DOMContentLoaded', function () {
        const filterForm = document.querySelector('.filter-form'); // Получаем форму фильтров
        const filterButton = filterForm.querySelector('.btn-filter'); // Получаем кнопку "Применить фильтры"

        // Обработчик события клика на кнопку "Применить фильтры"
        filterButton.addEventListener('click', function (event) {
            event.preventDefault(); // Предотвращаем стандартное действие кнопки

            filterCheckboxes = []; // Создаем пустой массив для хранения выбранных фильтров

            // Получаем все выбранные фильтры чекбоксов
            filterForm.querySelectorAll('input[type="checkbox"]:checked').forEach(checkbox => {
                filterCheckboxes.push(checkbox.name); // Добавляем имя выбранного фильтра в массив
            });

            // Теперь можно использовать массив filterCheckboxes, который содержит имена выбранных фильтров
            console.log(filterCheckboxes);
        });
    });

    const tableLinks = document.querySelectorAll('.table a');
// Получаем все ссылки в таблице

// Добавляем обработчик клика на каждую ссылку
// Получаем кнопки управления сортировкой
    const sortButtons = document.querySelectorAll('.table th a');

// Добавляем обработчик клика на каждую кнопку сортировки
    sortButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault(); // Предотвращаем стандартное действие ссылки
            const urlParams = new URLSearchParams(window.location.search);
            const sortParam = this.getAttribute('href').split('?')[1]; // Получаем параметры сортировки из ссылки
            const sortParamParts = sortParam.split('&');
            const sortValue = sortParamParts[0].split('=')[1];
            const orderValue = sortParamParts[1].split('=')[1];
            // Сохраняем текущие параметры фильтрации
            const filterParams = [];
            document.querySelectorAll('input[type="checkbox"]:checked').forEach(checkbox => {
                filterParams.push(checkbox.name + '=1');
            });
            // Устанавливаем параметры сортировки
            urlParams.set('sort', sortValue);
            urlParams.set('order', orderValue);
            // Добавляем параметры фильтрации обратно
            filterParams.forEach(filter => {
                urlParams.append(filter.split('=')[0], filter.split('=')[1]);
            });
            // Обновляем URL страницы с новыми параметрами сортировки и фильтрации
            window.location.href = '?' + urlParams.toString();
        });
    });


    function goToPage() {
        const pageNumber = document.getElementById('page-input').value;
        const currentPageUrl = window.location.href;

        // Создаем новый URL объект на основе текущего URL
        const url = new URL(currentPageUrl);

        // Устанавливаем параметр 'page' равным номеру страницы
        url.searchParams.set('page', pageNumber);

        // Перенаправляем на новый URL
        window.location.href = url.toString();
    }
})
