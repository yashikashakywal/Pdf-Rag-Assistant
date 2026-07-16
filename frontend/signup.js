const els = {
  authForm: document.getElementById("authForm"),
  authEmail: document.getElementById("authEmail"),
  authPassword: document.getElementById("authPassword"),
  authError: document.getElementById("authError"),
  authSubmit: document.getElementById("authSubmit"),
};

function showAuthError(message) {
  els.authError.textContent = message;
  els.authError.hidden = false;
}

els.authForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = els.authEmail.value.trim();
  const password = els.authPassword.value;

  if (password.length < 8) {
    showAuthError("Password must be at least 8 characters.");
    return;
  }

  els.authSubmit.disabled = true;
  els.authError.hidden = true;

  try {
    const res = await fetch(`${API}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json();

    if (!res.ok) {
      showAuthError(data.detail || "Something went wrong. Please try again.");
      return;
    }

    setToken(data.access_token);
    window.location.href = "index.html";
  } catch {
    showAuthError("Couldn't reach the backend. Is the server running?");
  } finally {
    els.authSubmit.disabled = false;
  }
});

// If already signed in with a valid token, skip straight to the app.
(async function redirectIfSignedIn() {
  const token = getToken();
  if (!token) return;
  try {
    const res = await fetch(`${API}/auth/me`, { headers: { Authorization: `Bearer ${token}` } });
    if (res.ok) window.location.href = "index.html";
    else clearToken();
  } catch {
    // Backend unreachable — let the person sign up manually once it's up.
  }
})();
