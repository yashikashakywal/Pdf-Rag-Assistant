// Shared by login.html, signup.html, and index.html so the token handling
// and API base logic live in exactly one place.
const API = window.API_BASE_URL || "/api";
const TOKEN_KEY = "marginalia_token";

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}
