const deleteUrl = "/user/delete/";
const deleteForm = document.getElementById('deleteForm');
const publicKeyUrl = "/user/public-key/";

document.getElementById('info').addEventListener('change', function () {
    if (this.checked) {
        document.getElementById('delete-button').disabled = false;
    } else {
        document.getElementById('delete-button').disabled = true;
    }
});

function showError(error = null) {
    if (error) {
    document.getElementById('error-container').hidden = false;
    document.getElementById('error-detail').innerHTML = error;
    }
    else {
        document.getElementById('error-container').hidden = true;
    }
}

async function getPublicKey() {
    let publicKey = await fetch(publicKeyUrl, {method: 'GET'})
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            showError('Failed to load public key');
            return {'key': null};
        }
    })
    .catch(error => {
        console.error(error);
        return {'key': null};
    });
    return publicKey['key'];
}

async function getDeleteValues(event) {
    let password = event.target.password.value;
    let info = event.target.info.checked;
    return { password, info };
}

deleteForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    showError();

    let { password, info } = await getDeleteValues(event);

    if (!password.trim()) {
        showError('Password is required');
        return;
    }

    if (password.length < 8) {
        showError('Password must be at least 8 characters long');
        return;
    }

    let publicKey = await getPublicKey();
    if (!publicKey) {
        showError('Failed to load public key');
        return;
    }

    publicKey = await importPublicKey(publicKey);

    password = await Encrypt(password, publicKey);

    if (!info) {
        showError('Agree for account deletion');
        return;
    }

    showError();
    
    fetch(deleteUrl, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            password: password
        })
    })
    .then(response => {
        if (response.ok) {
            window.location.href = "/";
        } else {
            response.json().then(data => {
                if (data && data['detail']) {
                    showError(data['detail']);
                }else {
                    showError('Failed to delete');
                }
            return;
            })  
        }
    })
})
