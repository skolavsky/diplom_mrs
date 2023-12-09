// hello/static/scripts/script.js
document.addEventListener('DOMContentLoaded', function () {
    // Wait for the DOM content to be fully loaded before executing the script

    var showPasswordButton = document.getElementById('showPassword');
    var passwordInput = document.getElementById('password');

    if (showPasswordButton && passwordInput) {
        // Check if the elements are present on the page

        showPasswordButton.addEventListener('click', function () {
            // Toggle the type attribute of the password input
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
            } else {
                passwordInput.type = 'password';
            }
        });
    }
});