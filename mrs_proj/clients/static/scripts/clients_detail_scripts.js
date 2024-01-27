function toggleForm() {
    let form = document.getElementById('editForm');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

function highlightChangedValues() {
    // Iterate through each change item
    document.querySelectorAll('.change-item').forEach(function (changeItem) {
        let currentSPO2 = changeItem.dataset.spo2;
        let currentResult = changeItem.dataset.result;

        // Check if there is a previous entry
        let prevChangeItem = changeItem.previousElementSibling;
        if (prevChangeItem) {
            let prevSPO2 = prevChangeItem.dataset.spo2;
            let prevResult = prevChangeItem.dataset.result;

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

function showConfirmation() {
    document.getElementById('confirmEditDiv').style.display = 'block';
}
function confirmEdit() {
    document.getElementById('client_personal_edit').submit();
}

function cancelEdit() {
    document.getElementById('confirmEditDiv').style.display = 'none';
    document.getElementById('client_personal_edit').reset();
}


// Call the new function after the page is loaded
document.addEventListener('DOMContentLoaded', function () {
    highlightChangedValues();
});