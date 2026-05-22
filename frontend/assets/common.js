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

function extractErrorMessage(data) {
  if (typeof data === "string") {
    return data;
  }

  if (data === null || typeof data !== "object") {
    return "Request failed.";
  }

  const detail = data.detail ?? data.message ?? data.error;

  if (Array.isArray(detail)) {
    const messages = detail
      .map((item) => {
        if (typeof item === "string") {
          return item;
        }

        if (item && typeof item === "object") {
          const location = Array.isArray(item.loc)
            ? item.loc.filter((part) => part !== "body").join(".")
            : "";
          const message = item.msg || item.message || JSON.stringify(item);
          return location ? `${location}: ${message}` : message;
        }

        return String(item);
      })
      .filter(Boolean);

    return messages.join(" | ") || "Request failed.";
  }

  if (detail && typeof detail === "object") {
    return detail.message || JSON.stringify(detail);
  }

  return String(detail || "Request failed.");
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
    const message = extractErrorMessage(data);
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

export function avatarPathForUser(username) {
  return username === "DemoPlayer" ? "/avatar.jpg" : null;
}

export function renderUserAvatar(element, username) {
  const avatarPath = avatarPathForUser(username);
  if (!element) {
    return;
  }

  if (avatarPath) {
    element.classList.add("has-image");
    element.innerHTML = `<img src="${avatarPath}" alt="${escapeHtml(username)} avatar" />`;
    return;
  }

  element.classList.remove("has-image");
  element.textContent = initialsFromName(username);
}

export function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

export function renderGameCard(game, options = {}) {
  const { compact = false, contextLabel = "" } = options;
  const matchBadge =
    game.recommended_score > 0
      ? `<span class="match-badge">Match ${game.recommended_score}</span>`
      : "";

  const ratingBadge =
    game.my_rating !== null
      ? `<span class="soft-badge">Your rating ${stars(game.my_rating)}</span>`
      : "";

  const matchedGenres =
    game.matched_genres && game.matched_genres.length > 0
      ? `<p class="card-context">Because you like ${escapeHtml(game.matched_genres.join(", "))}</p>`
      : "";

  const manualContext = contextLabel
    ? `<p class="card-context">${escapeHtml(contextLabel)}</p>`
    : "";

  return `
    <article class="game-card ${compact ? "compact-card" : ""}">
      <a class="game-cover-link" href="/game.html?id=${game.id}" aria-label="Open ${escapeHtml(game.title)}">
        <img src="${escapeHtml(game.cover_path)}" alt="${escapeHtml(game.title)} cover" />
      </a>
      <div class="game-card-body">
        <div class="card-badges">
          ${matchBadge}
          ${ratingBadge}
        </div>
        <h3><a class="game-title-link" href="/game.html?id=${game.id}">${escapeHtml(game.title)}</a></h3>
        <p>${escapeHtml(game.short_description)}</p>
        ${matchedGenres || manualContext}
        <div class="genres-row">
          ${game.genres.map((genre) => `<span class="genre-chip">${escapeHtml(genre)}</span>`).join("")}
        </div>
        <div class="game-card-meta">
          <span class="meta-rating">${game.average_rating.toFixed(1)} average</span>
          <span class="meta-muted">${game.ratings_count} ratings</span>
          <span class="meta-muted">${game.reviews_count} reviews</span>
        </div>
      </div>
    </article>
  `;
}

export function renderGameTile(game, options = {}) {
  const { contextLabel = "" } = options;
  const context = contextLabel ? `<p class="tile-context">${escapeHtml(contextLabel)}</p>` : "";

  return `
    <article class="game-tile">
      <a class="game-cover-link" href="/game.html?id=${game.id}" aria-label="Open ${escapeHtml(game.title)}">
        <img src="${escapeHtml(game.cover_path)}" alt="${escapeHtml(game.title)} cover" />
      </a>
      <div class="game-tile-body">
        <h3><a class="game-title-link" href="/game.html?id=${game.id}">${escapeHtml(game.title)}</a></h3>
        ${context}
        <div class="tile-meta">
          <span>${game.average_rating.toFixed(1)}</span>
          <span>${game.reviews_count} reviews</span>
        </div>
      </div>
    </article>
  `;
}

export function renderGameListItem(game) {
  return `
    <article class="game-list-item">
      <a class="game-list-cover-link" href="/game.html?id=${game.id}" aria-label="Open ${escapeHtml(game.title)}">
        <img class="game-list-thumb" src="${escapeHtml(game.cover_path)}" alt="${escapeHtml(game.title)} cover" />
      </a>
      <div class="game-list-body">
        <strong><a class="game-title-link" href="/game.html?id=${game.id}">${escapeHtml(game.title)}</a></strong>
        <span>${game.average_rating.toFixed(1)} average</span>
      </div>
    </article>
  `;
}

export function renderEmptyCard(title, description) {
  return `
    <div class="empty-state">
      <strong>${escapeHtml(title)}</strong>
      <p>${escapeHtml(description)}</p>
    </div>
  `;
}

export async function loadCurrentUser() {
  return api("/auth/me");
}
