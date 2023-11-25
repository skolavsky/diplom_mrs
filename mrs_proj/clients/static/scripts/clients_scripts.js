// JavaScript to toggle the visibility of the add client form
document.getElementById('toggleFormBtn').addEventListener('click', function () {
    document.getElementById('addClientForm').style.display = 'block';
});

// JavaScript to hide the add client form when canceled
function cancelAddClient() {
    document.getElementById('addClientForm').style.display = 'none';
}

// in clients_scripts.js
function confirmDelete(token) {
    // Check if the element exists before attempting to access its style property
    var confirmationPopup = document.getElementById('delete-confirmation');
    if (confirmationPopup) {
        // Show the confirmation popup
        confirmationPopup.style.display = 'block';
        // Store the token in a global variable to use it when deleting
        window.deleteToken = token;
    }
}

function deleteClientConfirmed() {
    // Check if the element exists before attempting to access its style property
    var confirmationPopup = document.getElementById('delete-confirmation');
    if (confirmationPopup) {
        // Hide the confirmation popup
        confirmationPopup.style.display = 'none';
        // Delete the client using the stored token
        window.location.href = `/delete-client/${window.deleteToken}/`;
    }
}

function cancelDelete() {
    // Check if the element exists before attempting to access its style property
    var confirmationPopup = document.getElementById('delete-confirmation');
    if (confirmationPopup) {
        // Hide the confirmation popup
        confirmationPopup.style.display = 'none';
    }
}


