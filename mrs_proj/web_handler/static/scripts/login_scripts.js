// login_scripts.js
function show_hide_password(target) {
    var input = target.parentElement.previousElementSibling.querySelector('input');
    var eyeIcon = target.querySelector('i');

    if (input.type === 'password') {
        input.type = 'text';
        eyeIcon.classList.remove('fa-eye');
        eyeIcon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        eyeIcon.classList.remove('fa-eye-slash');
        eyeIcon.classList.add('fa-eye');
    }
    return false;
}

function clock() {
    var t = new Date(),
        minutes = t.getMinutes() * 6,
        hours = t.getHours() % 12 / 12 * 360 + (minutes / 12);
    document.querySelector(".hour").style.transform = "rotate(" + hours + "deg)";
    document.querySelector(".minute").style.transform = "rotate(" + minutes + "deg)";
}

function refreshClock() {
    clock();
    setTimeout(refreshClock, 1000);
}

document.addEventListener('DOMContentLoaded', function () {
    refreshClock();
});
