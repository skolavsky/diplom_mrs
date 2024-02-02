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