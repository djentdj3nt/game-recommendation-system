import { api, getToken, setToken, showToast } from "./common.js";

const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");
const authTitle = document.getElementById("authTitle");
const authSubtitle = document.getElementById("authSubtitle");
const tabButtons = document.querySelectorAll("[data-auth-tab]");

if (getToken()) {
  window.location.href = "/app.html";
}

function switchTab(tabName) {
  const isLogin = tabName === "login";
  loginForm.classList.toggle("hidden", !isLogin);
  registerForm.classList.toggle("hidden", isLogin);
  authTitle.textContent = isLogin ? "Welcome back" : "Create account";
  authSubtitle.textContent = isLogin ? "Sign in to continue." : "Create an account to continue.";

  tabButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.authTab === tabName);
  });
}

async function loginWithCredentials(email, password) {
  const response = await api("/auth/login", {
    method: "POST",
    auth: false,
    body: { email, password },
  });
  setToken(response.access_token);
  window.location.href = "/app.html";
}

tabButtons.forEach((button) => {
  button.addEventListener("click", () => switchTab(button.dataset.authTab));
});

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(loginForm);

  try {
    await loginWithCredentials(formData.get("email"), formData.get("password"));
  } catch (error) {
    showToast(error.message);
  }
});

registerForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(registerForm);

  try {
    const response = await api("/auth/register", {
      method: "POST",
      auth: false,
      body: {
        username: formData.get("username"),
        email: formData.get("email"),
        password: formData.get("password"),
      },
    });
    setToken(response.access_token);
    window.location.href = "/app.html";
  } catch (error) {
    showToast(error.message);
  }
});
