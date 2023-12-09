function toggleForm() {
    var form = document.getElementById('editForm');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

function confirmDelete() {
    document.getElementById('confirmDeletionDiv').style.display = 'block';
}

function cancelDelete() {
    document.getElementById('client_delete').style.display = 'none';
}

function cancelEdit() {
    var editForm = document.getElementById('editForm');
    editForm.style.display = 'none';
}

function highlightChangedValues() {
    // Iterate through each change item
    document.querySelectorAll('.change-item').forEach(function (changeItem) {
        var currentSPO2 = changeItem.dataset.spo2;
        var currentResult = changeItem.dataset.result;

        // Check if there is a previous entry
        var prevChangeItem = changeItem.previousElementSibling;
        if (prevChangeItem) {
            var prevSPO2 = prevChangeItem.dataset.spo2;
            var prevResult = prevChangeItem.dataset.result;

            // Compare current and previous values
            if (currentSPO2 !== prevSPO2) {
                changeItem.querySelector('.spo2').classList.add('changed-value');
            }

            if (currentResult !== prevResult) {
                changeItem.querySelector('.result').classList.add('changed-value');
            }
        }
    });
}

// Call the new function after the page is loaded
document.addEventListener('DOMContentLoaded', function () {
    highlightChangedValues();
});