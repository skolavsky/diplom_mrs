document.addEventListener('DOMContentLoaded', function () {
    const jwtCookie = document.cookie.split(';').find(cookie => cookie.trim().startsWith('jwt='));
    var loginUrl = '/html/login-form.html'
    if (!jwtCookie) { //if no token, load login page
        fetch(loginUrl, {
            headers: {
                'Access-Control-Allow-Origin': 'http://0.0.0.0:8888'
            }
        })
        .then(response => response.text())
        .then(html => {
            document.querySelector('.main').innerHTML = html
            document.querySelector('.loader-container').style.display = 'none'
            const script = document.createElement('script');
            script.src = 'js/login.js';
            document.body.appendChild(script);
            const rsa_script = document.createElement('script');
            rsa_script.src = 'js/rsa.js';
            document.body.appendChild(rsa_script);
        })
    }
    else {
        // load client data
    }
})
