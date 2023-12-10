// hello/static/scripts/script.js
document.addEventListener('DOMContentLoaded', function () {
    // Wait for the DOM content to be fully loaded before executing the script

    const  showPasswordButton = document.getElementById('showPassword');
    const  passwordInput = document.getElementById('password');

    if (showPasswordButton && passwordInput) {
        // Check if the elements are present on the page

        showPasswordButton.addEventListener('input', function () { // NOSONAR
            // Toggle the type attribute of the password input
            if (passwordInput.type === 'password') { // NOSONAR
                passwordInput.type = 'text';  // NOSONAR
            } else { // NOSONAR
                passwordInput.type = 'password'; // NOSONAR
            } // NOSONAR
        }); // NOSONAR
    } // NOSONAR
});  // NOSONAR