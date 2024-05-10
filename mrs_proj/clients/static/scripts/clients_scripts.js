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
    const resetSortingButton = document.getElementById('resetSortingButton');

    resetSortingButton.addEventListener('click', function () {
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.delete('sort');  // Remove the 'sort' parameter
        currentUrl.searchParams.delete('search');  // Remove the 'search' parameter
        window.location.href = currentUrl.toString();
    });
});

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

    const resetSortingButton = document.getElementById('resetSortingButton');

    resetSortingButton.addEventListener('click', function () {
        const currentUrl = new URL(window.location.href);
        const searchParamIndex = currentUrl.href.indexOf('?search');

        if (searchParamIndex !== -1) {
            const baseUrl = currentUrl.href.substring(0, searchParamIndex);
            window.location.href = baseUrl;
        }
    });
});


function openGoToPageModal() {
    document.getElementById('goToPageModal').style.display = 'block';
}

function closeGoToPageModal() {
    document.getElementById('goToPageModal').style.display = 'none';
}

window.onclick = function (event) {
    let modal = document.getElementById('goToPageModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
};

const filterCheckboxes = document.querySelectorAll('input[type="checkbox"]');

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form[method="get"]');
    const checkboxes = form.querySelectorAll('input[type="checkbox"]');
    const submitButton = form.querySelector('button[type="submit"]');

    // Обработчик события клика на кнопку "Применить фильтры"
    submitButton.addEventListener('click', function(event) {
        event.preventDefault(); // Предотвращаем стандартное действие кнопки
        const checkedValues = Array.from(checkboxes)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.name + '_1');
        const queryParams = new URLSearchParams(window.location.search);
        checkedValues.forEach(value => {
            queryParams.append(value, '1');
        });
        window.location.href = window.location.pathname + '?' + queryParams.toString();
    });
});



// Получаем все ссылки в таблице
const tableLinks = document.querySelectorAll('.table a');

// Добавляем обработчик клика на каждую ссылку
tableLinks.forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault(); // Предотвращаем стандартное действие ссылки
        const urlParams = new URLSearchParams(window.location.search);
        const sortParam = this.getAttribute('href').split('?')[1]; // Получаем параметры сортировки из ссылки
        const sortParamParts = sortParam.split('&');
        const sortValue = sortParamParts[0].split('=')[1];
        const orderValue = sortParamParts[1].split('=')[1];
        urlParams.set('sort', sortValue);
        urlParams.set('order', orderValue);
        // Обновляем URL страницы с новыми параметрами сортировки
        window.history.replaceState(null, null, '?' + urlParams.toString());
        // Перезагружаем страницу с новыми параметрами сортировки
        window.location.reload();
    });
});
