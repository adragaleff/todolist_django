const password = document.getElementById('password');
const showpass = document.getElementById('showpass');
showpass.addEventListener('change', function() {
if (showpass.checked) {
password.type = 'text';
} else {
password.type = 'password';
}
});