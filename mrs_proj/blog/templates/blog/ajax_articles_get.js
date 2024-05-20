var page = 1;
var emptyPage = false;
var blockRequest = false;
window.addEventListener('scroll', function (e) {
    var margin = document.body.clientHeight - window.innerHeight - 100;
    if (window.pageYOffset > margin && !emptyPage && !blockRequest) {
        blockRequest = true;
        page += 1;
        fetch('?posts_only=1&page=' + page)
            .then(response => response.text())
            .then(html => {
                if (html === '') {
                    emptyPage = true;
                } else {
                    var postsList = document.getElementById('posts-list');
                    postsList.insertAdjacentHTML('beforeEnd', html);
                }
                blockRequest = false;
            });
    }
});
// Запустить события прокрутки
const scrollEvent = new Event('scroll');
window.dispatchEvent(scrollEvent);