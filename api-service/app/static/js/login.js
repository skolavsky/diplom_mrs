const loginForm = document.getElementById('loginForm');
const tokenUrl = "/user/token/";

async function getEPvalues(event){
    let { email, password } = event.target.elements;
    return { email: email.value, password: password.value };
}

async function getRefreshToken(email, password) {
    return await fetch(tokenUrl, {
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
            return true;
        } else {
            response.json().then(data => {
                if (data && data['detail']) {
                    showError(data['detail']);
                }
                return null;
            })
        }
    })
    .catch(error => {
        console.error(error);
        return null;
    });
}

loginForm.addEventListener('submit', async function (event) {
    event.preventDefault();
    showError();
    let { email, password } = await getEPvalues(event);

    if (!email.trim()) {
        showError('Email is required');
        return;
    }

    if (!isValidEmail(email)){
        showError('Please enter a valid email address');
        return;
    }

    if (!password.trim()) {
        showError('Password is required');
        return;
    }

    if (password.length < 8) {
        showError('Password must be at least 8 characters long');
        return;
    }
    
    document.getElementById('error-container').hidden = true;

    let publicKey = await getPublicKey();
    if (!publicKey)
        return;

    publicKey = await importPublicKey(publicKey);
    email = await Encrypt(email, publicKey);
    password = await Encrypt(password, publicKey);

    let got = await getRefreshToken(email, password);
    if (got)
        loadUserPage();
});

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function isStrongPassword(password) {
    return /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$/.test(password);
}
