// JavaScript to toggle the visibility of the add client form

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




