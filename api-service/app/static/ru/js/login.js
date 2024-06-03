const loginForm = document.getElementById('loginForm');
const tokenUrl = "/user/token/";
const registerFormUrl = "/ru/html/register-form.html";
const registerScriptUrl = "/ru/js/register.js";

async function getLoginValues(event){
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
    let { email, password } = await getLoginValues(event);

    if (!email.trim()) {
        showError('Необходимо ввести почту');
        return;
    }

    if (!isValidEmail(email)){
        showError('Введите корректную почту.');
        return;
    }

    if (!password.trim()) {
        showError('Необходимо ввести пароль.');
        return;
    }

    if (password.length < 8) {
        showError('Пароль должен содержать не менее 8 символов.');
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

document.getElementById('link').addEventListener('click', async function (event) {
    showError();
    event.preventDefault();
    let html = await fetch(registerFormUrl, {method: 'GET'})
    .then(response => {
        if (response.ok) {
            return response.text();
        } else {
            showError('Не удалось загрузить форму регистрации.');
            return null;
        }
    })
    .catch(error => {
        console.error(error);
        return null;
    });

    if (html) {
        showMain(html);
        const script = document.createElement('script');
        script.src = registerScriptUrl;
        document.body.appendChild(script);
    }
});
