function show_hide_password(target){
	var input = document.getElementById('password');
    var element = document.getElementById('eye');

	if (input.getAttribute('type') == 'password') 
    {
		target.classList.add('view');
		input.setAttribute('type', 'text');
		element.className = 'fas fa-eye-slash';
	} 
    else 
    {
		target.classList.remove('view');
		input.setAttribute('type', 'password');
        element.className = 'fas fa-eye';
	}

	return false;
}