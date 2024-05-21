const loginForm = document.getElementById('loginForm');
const loginUrl = "/users/login/"
const publicKeyUrl = "/users/publickey/"

loginForm.addEventListener('submit', async function (event) {
    event.preventDefault();
    let { email, password } = event.target.elements;

    email = email.value;
    password = password.value;

    if (!email.trim()) {
        alert('Email is required');
        return;
    }

    if (!isValidEmail(email)){
        alert('Please enter a valid email address');
        return;
    }

    if (!password.trim()) {
        alert('Password is required');
        return;
    }

    if (password.length < 8) {
        alert('Password must be at least 8 characters long');
        return;
    }
    
    let publicKey = await fetch(publicKeyUrl, {method: 'GET'})
    .then(response => {
        if (response.ok) {
            return response.text();
        } else {
            throw new Error('Failed to fetch public key');
        }
    })
    .then(publicKey => {
        if (!publicKey) {
            throw new Error('No public key found');
        }
        return JSON.parse(publicKey)['key'];
    })
    .catch(error => {
        alert(error.message);
    });

    publicKey = await importPublicKey(publicKey);
    email = await Encrypt(email, publicKey);
    password = await Encrypt(password, publicKey);

    fetch(loginUrl, {
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
            alert('Login successful');
            return response.json();
        } else if (response.status === 404) {
            return response.text().then(text => { throw new Error(text) });
        }
        else {
            return response.text().then(text => { throw new Error(text) });
        }
    })
    .catch(error => {
        alert(JSON.parse(error.message)['detail']);
    });
});

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function isStrongPassword(password) {
    return /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$/.test(password);
}
