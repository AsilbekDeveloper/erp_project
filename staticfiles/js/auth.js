document.getElementById('loginForm').onsubmit = async function(e) {
  e.preventDefault();
  const username = document.getElementById('username');
  const password = document.getElementById('password');
  const usernameErr = document.getElementById('usernameErr');
  const passwordErr = document.getElementById('passwordErr');
  const loginAlert = document.getElementById('loginAlert');

  // Clear errors
  usernameErr.innerText = '';
  passwordErr.innerText = '';
  loginAlert.innerText = '';

  // Client-side validation
  if (!username.value.trim()) {
    usernameErr.innerText = 'Enter your username';
    username.focus();
    return false;
  }
  if (!password.value.trim()) {
    passwordErr.innerText = 'Enter your password';
    password.focus();
    return false;
  }

  // Demo mode: replace with real AJAX to Django backend
  // Example:
  /*
  const resp = await fetch('/login/', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({username: username.value, password: password.value})
  });
  if (resp.status === 200) {
    window.location = '/dashboard/';
  } else {
    loginAlert.innerText = 'Invalid username or password';
  }
  */

  // For demo (success if username==password)
  if (username.value === password.value) {
    window.location = '/dashboard/';
  } else {
    loginAlert.innerText = 'Invalid username or password';
  }
};