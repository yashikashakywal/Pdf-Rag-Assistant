// auth-common.js (loaded before this file) defines API, TOKEN_KEY, getToken,
// setToken, and clearToken — shared with login.html and signup.html.
//
// Same-origin by default: works when this frontend is served by the FastAPI
// app itself (the default setup — see backend/app/main.py), including on Render.
//
// Running the frontend and backend as two separate servers locally (e.g. via
// `python -m http.server`)? Override this before auth-common.js loads, e.g.
// add `<script>window.API_BASE_URL = "http://127.0.0.1:8000/api"</script>`
// in index.html, just above the <script src="auth-common.js"> tag.

const els = {
  appRoot: document.getElementById("appRoot"),
  accountEmail: document.getElementById("accountEmail"),
  logoutBtn: document.getElementById("logoutBtn"),
  chatBox: document.getElementById("chatBox"),
  chatEmpty: document.getElementById("chatEmpty"),
  askForm: document.getElementById("askForm"),
  question: document.getElementById("question"),
  askBtn: document.getElementById("askBtn"),
  dropzone: document.getElementById("dropzone"),
  pdfFile: document.getElementById("pdfFile"),
  uploadProgress: document.getElementById("uploadProgress"),
  uploadStatus: document.getElementById("uploadStatus"),
  fileList: document.getElementById("fileList"),
  docCount: document.getElementById("docCount"),
  statusDot: document.getElementById("statusDot"),
  statusText: document.getElementById("statusText"),
  resetBtn: document.getElementById("resetBtn"),
};

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

// ================= Auth =================
// Sign in and sign up now live on their own pages (login.html / signup.html).
// This page only needs to guard itself: require a valid token, or send the
// person to login.html.

els.logoutBtn.addEventListener("click", () => {
  clearToken();
  goToLogin();
});

function goToLogin() {
  clearToken();
  window.location.href = "login.html";
}

/**
 * Wraps fetch() with the Authorization header. If the token is missing,
 * expired, or invalid, the user is sent back to the login page.
 */
async function authFetch(path, options = {}) {
  const token = getToken();
  const headers = new Headers(options.headers || {});
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const res = await fetch(`${API}${path}`, { ...options, headers });

  if (res.status === 401) goToLogin();

  return res;
}

async function showApp(email) {
  els.appRoot.hidden = false;
  els.accountEmail.textContent = email;
  checkHealth();
  refreshDocumentList();
}

/** Validates any stored token and either shows the app or redirects to login.
 * Runs once on load. */
async function enterApp() {
  const token = getToken();
  if (!token) {
    goToLogin();
    return;
  }

  try {
    const res = await authFetch("/auth/me");
    if (!res.ok) return; // authFetch already redirected to login.html on 401
    const data = await res.json();
    await showApp(data.email);
  } catch {
    // Backend unreachable — nothing to show yet; let the health check (once
    // reachable) or a manual refresh sort it out rather than bouncing the
    // person to login.html while offline.
  }
}

// ---------- Backend connection status ----------

async function checkHealth() {
  try {
    const res = await fetch(`${API}/health`);
    if (!res.ok) throw new Error();
    els.statusDot.className = "status-dot online";
    els.statusText.textContent = "Backend connected";
  } catch {
    els.statusDot.className = "status-dot offline";
    els.statusText.textContent = "Backend unreachable — is it running?";
  }
}

// ---------- Document list ----------

async function refreshDocumentList() {
  try {
    const res = await authFetch("/documents");
    if (!res.ok) return;
    const data = await res.json();
    renderFiles(data.documents || []);
  } catch {
    // Health indicator already communicates the backend is down.
  }
}

function renderFiles(files) {
  els.docCount.textContent = `(${files.length})`;
  els.fileList.innerHTML = "";

  if (files.length === 0) {
    const li = document.createElement("li");
    li.className = "empty-state";
    li.textContent = "No documents yet. Upload a PDF to begin.";
    els.fileList.appendChild(li);
    return;
  }

  files.forEach((name) => {
    const li = document.createElement("li");
    li.textContent = name;
    els.fileList.appendChild(li);
  });
}

// ---------- Upload ----------

async function uploadFiles(fileArray) {
  if (fileArray.length === 0) return;

  els.uploadProgress.hidden = false;

  for (const file of fileArray) {
    els.uploadStatus.textContent = `Indexing ${file.name}…`;
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await authFetch("/upload", { method: "POST", body: formData });
      const data = await res.json();

      if (!res.ok) {
        addMessage(`Couldn't index **${escapeHtml(file.name)}**: ${escapeHtml(data.detail || "unknown error")}`, "error");
        continue;
      }
    } catch {
      addMessage(`Couldn't reach the backend while uploading ${escapeHtml(file.name)}.`, "error");
    }
  }

  els.uploadProgress.hidden = true;
  els.pdfFile.value = "";
  refreshDocumentList();
}

els.pdfFile.addEventListener("change", () => uploadFiles(Array.from(els.pdfFile.files)));

["dragenter", "dragover"].forEach((evt) =>
  els.dropzone.addEventListener(evt, (e) => {
    e.preventDefault();
    els.dropzone.classList.add("drag-over");
  })
);
["dragleave", "drop"].forEach((evt) =>
  els.dropzone.addEventListener(evt, (e) => {
    e.preventDefault();
    els.dropzone.classList.remove("drag-over");
  })
);
els.dropzone.addEventListener("drop", (e) => {
  const files = Array.from(e.dataTransfer.files).filter((f) => f.type === "application/pdf");
  uploadFiles(files);
});

// ---------- Chat ----------

function addMessage(html, type) {
  els.chatEmpty.style.display = "none";
  const div = document.createElement("div");
  div.className = `message ${type}`;
  div.innerHTML = html;
  els.chatBox.appendChild(div);
  els.chatBox.scrollTop = els.chatBox.scrollHeight;
  return div;
}

els.askForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = els.question.value.trim();
  if (!question) return;

  addMessage(escapeHtml(question), "user");
  els.question.value = "";
  els.askBtn.disabled = true;

  const pending = addMessage("Thinking…", "pending");

  try {
    const res = await authFetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const data = await res.json();
    pending.remove();

    if (!res.ok) {
      addMessage(escapeHtml(data.detail || "Something went wrong."), "error");
      return;
    }

    let html = escapeHtml(data.answer);
    if (data.sources && data.sources.length > 0) {
      const chips = data.sources
        .map((s) => `<span class="source-tab">${escapeHtml(s.file)} · p.${s.page}</span>`)
        .join("");
      html += `<div class="sources">${chips}</div>`;
    }
    addMessage(html, "bot");
  } catch {
    pending.remove();
    addMessage("Couldn't reach the backend. Is the FastAPI server running?", "error");
  } finally {
    els.askBtn.disabled = false;
    els.question.focus();
  }
});

// ---------- Reset ----------

els.resetBtn.addEventListener("click", async () => {
  if (!confirm("This clears every uploaded document and the search index. Continue?")) return;

  try {
    await authFetch("/reset", { method: "DELETE" });
    els.chatBox.innerHTML = "";
    els.chatBox.appendChild(els.chatEmpty);
    els.chatEmpty.style.display = "block";
    refreshDocumentList();
  } catch {
    addMessage("Couldn't reach the backend to reset.", "error");
  }
});

// ---------- Init ----------

enterApp();
setInterval(() => {
  if (!els.appRoot.hidden) checkHealth();
}, 15000);
