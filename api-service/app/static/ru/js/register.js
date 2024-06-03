const registerForm = document.getElementById('registerForm');
const signupUrl = "/user/signup/";

document.getElementById('info').addEventListener('change', function () {
    if (this.checked) {
        document.getElementById('register-button').disabled = false;
    } else {
        document.getElementById('register-button').disabled = true;
    }
});

async function getRegisterValues(){
    let { email, password, confPassword, info } = registerForm.elements;
    return { email: email.value, password: password.value, confirmPassword: confPassword.value, info: info.checked };
}

registerForm.addEventListener('submit', async function (event) {
    event.preventDefault();
    showError();

    let { email, password, confirmPassword, info } = await getRegisterValues();

    if (!email.trim()) {
        showError('Необходимо ввести почту.');
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

    if (password !== confirmPassword) {
        showError('Пароли не совпадают.');
        return;
    }

    if (!info) {
        showError('Пожалуйста, согласитесь с политикой конфиденциальности.');
        return;
    }

    let publicKey = await getPublicKey();
    if (!publicKey)
        return;

    publicKey = await importPublicKey(publicKey);
    email = await Encrypt(email, publicKey);
    password = await Encrypt(password, publicKey);

    await registerRequest(email, password);
});

async function registerRequest(email, password) {
    fetch(signupUrl, {
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
        if (response.status === 201) {
            let reg_status = document.getElementById('registration-status');
            reg_status.hidden = false;
            reg_status.innerHTML = 'Вы успешно зарегистрировались.\nПожалуйста вернитесь и войдите в систему.';
            return;
        } else {
            response.json().then(data => {
                if (data && data['detail']) {
                    showError(data['detail']);
                }else {
                showError('Не удалось зарегистрироваться.');
                }
            return;
            })  
        }
    })
}
