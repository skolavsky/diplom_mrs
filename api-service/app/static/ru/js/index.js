const loginFormUrl = '/ru/html/login-form.html';
const loginUrl = '/user/login/';
const userUrl = '/ru/html/user-page.html';
const publicKeyUrl = "/user/public-key/";
const logoutUrl = '/user/logout/';
const changePasswordUrl = '/user/change-password/';
const loginScriptUrl = '/ru/js/login.js';


function showError(error = null) {
    if (error) {
    document.getElementById('error-container').hidden = false;
    document.getElementById('error-detail').innerHTML = error;
    }
    else {
        document.getElementById('error-container').hidden = true;
    }
}

function showMain(html = null) {
    document.getElementById('error-container').hidden = true;
    if (html === null) {
        document.getElementById('main-container').hidden = true;
        document.getElementById('loader-container').hidden = false;
    } else {
        main = document.getElementById('main-container');
        main.hidden = false;
        main.innerHTML = html;
        document.getElementById('loader-container').hidden = true;
    }
}

async function loadLoginForm() {
    fetch(loginFormUrl, {})
    .then(response => {
        if (response.ok) {
            return response.text();
        }
        else {
            throw new Error('Не удалось загрузить форму входа.');
        }
    })
    .then(html => {
        showMain(html);
        const script = document.createElement('script');
        script.src = loginScriptUrl;
        document.body.appendChild(script);
    })
    .catch(error => {
        showError(error);
        console.error(error);
        return;
    });
}

async function loadUserPage() {
    let user = await fetch(loginUrl, {method: 'GET'})
    .then(response => {
        if (response.ok) {
            return response.json();
        } else if (response.status === 401) {
            return 401;
        } else{
            response.json()
            .then(data => {
                if (data && data['detail']) {
                    showError(data['detail']);
                }
            })
            return null;
        }
    })
    .catch(error => {
        console.error(error);
        return null;
    });

    if (user === 401) {
        showMain();
        loadLoginForm();
        return null;
    } else if (!user) {
        return null;
    } else {
        showMain();
        var html = await fetch(userUrl, {method: 'GET'})
        .then(response => {
            if (response.ok) {
                return response.text();
            } else {
                throw new Error('Не удалось загрузить страницу пользователя.');
            }
        })
        .catch(error => {
            console.error(error);
            return null;
        });
        if (!html) {
            return null;
        }
        showMain(html);
        document.getElementById('title').innerText = `Добро пожаловать ${user['email']}!`;
        let date = (new Date(user['created_at'])).toLocaleDateString(navigator.language, {day: '2-digit', month: 'long', year: 'numeric'});
        document.getElementById('created-at').innerText = `Вы создали этот аккаунт\n ${date}.`;
    }
    
    document.getElementById('change-password-form').addEventListener('submit', async function (event) {
        event.preventDefault();
        showError();
        let currentPassword = document.getElementById('current-password').value;
        let newPassword = document.getElementById('new-password').value;
        const confirmPassword = document.getElementById('confirm-new-password').value;
        
        if (!currentPassword.trim()) {
            showError('Введите ваш пароль.');
            return;
        }
    
        if (!newPassword.trim()) {
            showError('Введите новый пароль.');
            return;
        }
        
        if (currentPassword.length < 8) {
            showError('Пароль должен содержать не менее 8 символов.');
            return;
        }

        if (newPassword.length < 8) {
            showError('Пароль должен содержать не менее 8 символов.');
            return;
        }

        if (newPassword !== confirmPassword) {
            showError('Новый пароль не совпадает.');
            return;
        }
    
        let publicKey = await getPublicKey();
        if (!publicKey)
            return;
    
        publicKey = await importPublicKey(publicKey);
        currentPassword = await Encrypt(currentPassword, publicKey);
        newPassword = await Encrypt(newPassword, publicKey);
    
        fetch(changePasswordUrl, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                current_password: currentPassword,
                new_password: newPassword
            })
        })
        .then(response => {
            if (response.ok) {
                document.getElementById('change-password-status').hidden = false;
                document.getElementById('change-password-status').innerText = 'Password changed successfully';
            } else if (response.status === 401) {
                loadUserPage();
            } else {
                response.json().then(data => {
                    if (data && data['detail']) {
                        showError(data['detail']);
                    }
                })
            }
        })
    })
}

document.addEventListener('DOMContentLoaded', async function () {
    if (navigator.language.includes('en')) {
        window.location.href = "/";
    }
    await loadUserPage();
})

async function logout() {
    fetch(logoutUrl, {method: 'GET'})
    .then(response => {
        if (response.ok) {
            location.reload();
        }
    })
    .catch(error => {
        console.error(error);
    });
}

async function getPublicKey() {
    let publicKey = await fetch(publicKeyUrl, {method: 'GET'})
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            showError('Не удалось загрузить публичный ключ.');
            return {'key': null};
        }
    })
    .catch(error => {
        console.error(error);
        return {'key': null};
    });
    return publicKey['key'];
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function isStrongPassword(password) {
    return /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$/.test(password);
}