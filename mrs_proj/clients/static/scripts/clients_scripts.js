document.getElementById('toggleFormBtn').addEventListener('click', function () {
    document.getElementById('addClientForm').style.display = 'block';
});

function toggleForm() {
    var form = document.getElementById('addClientForm');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

function cancelAddClient() {
    var form = document.getElementById('addClientForm');
    form.style.display = 'none';
}

function toggleForm() {
    var form = document.getElementById('addClientForm');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

function cancelAddClient() {
    var form = document.getElementById('addClientForm');
    form.style.display = 'none';
}

// Function to validate the client form
function validateClientForm() {
    // Get form inputs
    var firstName = $('#id_first_name').val().trim();
    var lastName = $('#id_last_name').val().trim();
    var patronymic = $('#id_patronymic').val().trim();
    var age = $('#id_age').val().trim();
    var bodyMassIndex = $('#id_body_mass_index').val().trim();
    var SPO2 = $('#id_SPO2').val().trim();

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

    // Validate body mass index (should be a positive number)
    if (!bodyMassIndex || isNaN(bodyMassIndex) || parseFloat(bodyMassIndex) < 0) {
        alert('Please enter a valid body mass index.');
        return false;
    }

    // Validate SPO2 (should be a number between 0 and 100)
    if (!SPO2 || isNaN(SPO2) || parseFloat(SPO2) < 0 || parseFloat(SPO2) > 100) {
        alert('Please enter a valid SPO2 value between 0 and 100.');
        return false;
    }

    // If all validations pass, return true
    return true;
}




