 // JavaScript to toggle the visibility of the add client form
    document.getElementById('toggleFormBtn').addEventListener('click', function() {
        document.getElementById('addClientForm').style.display = 'block';
    });

    // JavaScript to hide the add client form when canceled
    function cancelAddClient() {
        document.getElementById('addClientForm').style.display = 'none';
    }