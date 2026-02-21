
function registerUser() {
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  if (!name || !email || !password) {
    alert("Fill all fields");
    return;
  }

  localStorage.setItem(
    "user",
    JSON.stringify({ name, email, password })
  );

  alert("Registered successfully");
  window.location.href = "login.html";
}

function loginUser() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const user = JSON.parse(localStorage.getItem("user"));

  if (!user) {
    alert("No user found. Please register.");
    return;
  }

  if (user.email === email && user.password === password) {
    localStorage.setItem("token", "demo-auth-token");
    alert("Login successful");
    window.location.href = "index.html";
  } else {
    alert("Invalid credentials");
  }
}

function logoutUser() {
  localStorage.removeItem("token");
  alert("Logged out");
  window.location.href = "login.html";
}