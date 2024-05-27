function toggleForm() {
    var formDiv = document.getElementById('data-edit');
    var editButton = document.getElementById('client_edit');

    if (formDiv.style.display === 'none' || formDiv.style.display === '') {
        formDiv.style.display = 'block';
        editButton.textContent = 'Отменить редактирование';
    } else {
        formDiv.style.display = 'none';
        editButton.textContent = 'Редактировать данные';
    }
}

function toggleEditForm() {
    var formDiv = document.getElementById('confirmEditDiv');
    var editButton = document.getElementById('edit');

    if (formDiv.style.display === 'none' || formDiv.style.display === '') {
        formDiv.style.display = 'block';
        editButton.textContent = 'Отменить редактирование персональных данных';
    } else {
        formDiv.style.display = 'none';
        editButton.textContent = 'Редактировать персональные данные';
    }
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


// Call the new function after the page is loaded
document.addEventListener('DOMContentLoaded', function () {
    highlightChangedValues();
});