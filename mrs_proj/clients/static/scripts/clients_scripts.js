document.getElementById('toggleFormBtn').addEventListener('click', function () {
    document.getElementById('addClientForm').style.display = 'block';
});

document.addEventListener('DOMContentLoaded', function () {
    const searchButton = document.getElementById('searchButton');

    searchButton.addEventListener('click', function () {
        const searchInput = document.getElementById('searchInput');
        const searchQuery = searchInput.value.trim();  // Trim to remove leading/trailing spaces

        if (searchQuery !== '') {
            const currentUrl = new URL(window.location.href);
            currentUrl.searchParams.set('search', searchQuery);
            window.location.href = currentUrl.toString();
        }
    });
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


    const filterCheckboxes = document.querySelectorAll('input[type="checkbox"]');

    document.addEventListener('DOMContentLoaded', function () {
        const form = document.querySelector('form[method="get"]');
        const checkboxes = form.querySelectorAll('input[type="checkbox"]');
        const submitButton = form.querySelector('button[type="submit"]');

        // Обработчик события клика на кнопку "Применить фильтры"
        submitButton.addEventListener('click', function (event) {
            event.preventDefault(); // Предотвращаем стандартное действие кнопки
            const checkedValues = Array.from(checkboxes)
                .filter(checkbox => checkbox.checked)
                .map(checkbox => checkbox.name + '_1');
            const queryParams = new URLSearchParams(); // Создаем новый объект URLSearchParams
            checkedValues.forEach(value => {
                queryParams.append(value, '1');
            });
            window.location.href = window.location.pathname + '?' + queryParams.toString();
        });
    });


// Получаем все ссылки в таблице
    const tableLinks = document.querySelectorAll('.table a');

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
