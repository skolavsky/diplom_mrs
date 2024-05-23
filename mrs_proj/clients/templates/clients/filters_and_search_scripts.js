const resetButton = document.getElementById('resetButton');

resetButton.addEventListener('click', function (event) {
    event.preventDefault(); // Предотвращаем стандартное действие кнопки
    const checkboxes = document.querySelectorAll('.filter-group input[type="checkbox"]');
    filters = '';  // Очищаем фильтры
    // Снимаем галки с каждого чекбокса
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
    });

    updateTable(true);
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

document.querySelectorAll('.btn-filter').forEach(link => {
    link.addEventListener('click', function (event) {
        event.preventDefault(); // Предотвращаем стандартное действие кнопки

        const filterCheckboxes = document.querySelectorAll('.filter-group input[type="checkbox"]:checked');
        filters = Array.from(filterCheckboxes).map(checkbox => checkbox.name + '=1').join('&');
        const search = document.getElementById('searchInput').value;
        // Добавляем значение порога прогноза
        const forecastThreshold = document.getElementById('forecast_threshold').value;
        if (forecastThreshold) {
            filters += '&forecast_threshold=' + forecastThreshold;
        }
        //строка поиска
        if (search) {
            filters += '&' + 'search=' + search;
        }

        console.log(filters); // Пример вывода в консоль для проверки

        updateTable();
    });
});
