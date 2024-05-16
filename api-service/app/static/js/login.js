function loginRequest() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('http://0.0.0.0:8888/users/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to register');
        }
    })
    .then(data => {
        alert(data.message);
    })
}
