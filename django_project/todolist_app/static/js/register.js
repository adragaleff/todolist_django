document.addEventListener('DOMContentLoaded', function() {
  const showPasswordIcon = document.querySelector('.bx.bxs-lock-alt');
  const passwordInput = document.querySelector('[name="password1"]');

  showPasswordIcon.addEventListener('click', function() {
      if (passwordInput.type === 'password') {
          passwordInput.type = 'text';
          showPasswordIcon.classList.remove('bxs-lock-alt');
          showPasswordIcon.classList.add('bxs-lock-open');
      } else {
          passwordInput.type = 'password';
          showPasswordIcon.classList.remove('bxs-lock-open');
          showPasswordIcon.classList.add('bxs-lock-alt');
      }
  });
});