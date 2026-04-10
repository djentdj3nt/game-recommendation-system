const TOKEN_KEY = "playnext_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

export async function api(path, options = {}) {
  const { method = "GET", body, auth = true } = options;
  const headers = {
    "Content-Type": "application/json",
  };

  if (auth && getToken()) {
    headers.Authorization = `Bearer ${getToken()}`;
  }

  const response = await fetch(`/api${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  const contentType = response.headers.get("content-type") || "";
  const data = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const message = typeof data === "object" && data !== null ? data.detail || data.message : data;
    if (response.status === 401 && auth) {
      clearToken();
      if (!window.location.pathname.endsWith("/index.html") && window.location.pathname !== "/") {
        window.location.href = "/index.html";
      }
    }
    throw new Error(message || "Request failed.");
  }

  return data;
}

export function showToast(message) {
  const toast = document.getElementById("toast");
  if (!toast) {
    return;
  }

  toast.textContent = message;
  toast.classList.add("show");
  window.clearTimeout(toast._timeoutId);
  toast._timeoutId = window.setTimeout(() => {
    toast.classList.remove("show");
  }, 2600);
}

export function requireAuth() {
  if (!getToken()) {
    window.location.href = "/index.html";
    return false;
  }
  return true;
}

export function logout() {
  clearToken();
  window.location.href = "/index.html";
}

export function formatDate(value) {
  return new Date(value).toLocaleDateString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

export function initialsFromName(name) {
  return (name || "P")
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}

export function stars(value) {
  return `${value}/5`;
}

export function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

export function renderGameCard(game) {
  const matchBadge =
    game.recommended_score > 0
      ? `<span class="match-badge">Match ${game.recommended_score}</span>`
      : "";

  const myRating =
    game.my_rating !== null
      ? `<span class="meta-muted">Your rating: ${stars(game.my_rating)}</span>`
      : `<span class="meta-muted">No personal rating yet</span>`;

  return `
    <article class="game-card">
      <img src="${escapeHtml(game.cover_path)}" alt="${escapeHtml(game.title)} cover" />
      <div class="game-card-body">
        ${matchBadge}
        <h3>${escapeHtml(game.title)}</h3>
        <p>${escapeHtml(game.short_description)}</p>
        <div class="genres-row">
          ${game.genres.map((genre) => `<span class="genre-chip">${escapeHtml(genre)}</span>`).join("")}
        </div>
        <div class="game-card-meta">
          <span class="meta-rating">${stars(Math.round(game.average_rating || 0))}</span>
          <span class="meta-muted">${game.average_rating.toFixed(1)} average</span>
        </div>
        <div class="card-footer">
          <span class="meta-muted">${game.reviews_count} reviews</span>
          <a class="link-button" href="/game.html?id=${game.id}">Open Page</a>
        </div>
        <div class="card-footer">
          ${myRating}
        </div>
      </div>
    </article>
  `;
}

export async function loadCurrentUser() {
  return api("/auth/me");
}
