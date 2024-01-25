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


// Function to validate the client form
function validateClientForm() {
    // Get form inputs
    let firstName = $('#id_first_name').val().trim();
    let lastName = $('#id_last_name').val().trim();
    let patronymic = $('#id_patronymic').val().trim();
    let age = $('#id_age').val().trim();

    // Validate first name
    if (!firstName) {
        alert('Please enter a valid first name.');
        return false;
    }

    // Validate last name
    if (!lastName) {
        alert('Please enter a valid last name.');
        return false;
    }

    // Validate patronymic
    if (!patronymic) {
        alert('Please enter a valid patronymic.');
        return false;
    }

    // Validate age (should be a positive integer)
    if (!age || isNaN(age) || parseInt(age) < 0) {
        alert('Please enter a valid age.');
        return false;
    }

    // If all validations pass, return true
    return true;
}




