import {
  api,
  formatDate,
  loadCurrentUser,
  logout,
  renderEmptyCard,
  renderGameCard,
  renderGameListItem,
  renderGameTile,
  renderUserAvatar,
  requireAuth,
  showToast,
} from "./common.js";

if (!requireAuth()) {
  throw new Error("Authentication required");
}

const panels = document.querySelectorAll("[data-panel]");
const navButtons = document.querySelectorAll("[data-panel-target]");
const logoutButton = document.getElementById("logoutButton");
const searchInput = document.getElementById("searchInput");
const recommendationHint = document.getElementById("recommendationHint");
const spotlightCard = document.getElementById("spotlightCard");
const forYouSection = document.getElementById("forYouSection");
const forYouGrid = document.getElementById("forYouGrid");
const recentlyViewedSection = document.getElementById("recentlyViewedSection");
const recentlyViewedGrid = document.getElementById("recentlyViewedGrid");
const topRatedSection = document.getElementById("topRatedSection");
const topRatedGrid = document.getElementById("topRatedGrid");
const searchResultsSection = document.getElementById("searchResultsSection");
const searchResultsHint = document.getElementById("searchResultsHint");
const searchResultsGrid = document.getElementById("searchResultsGrid");
const catalogSection = document.getElementById("catalogSection");
const gamesGrid = document.getElementById("gamesGrid");
const genresGrid = document.getElementById("genresGrid");
const saveGenresButton = document.getElementById("saveGenresButton");
const favoriteGamesGrid = document.getElementById("favoriteGamesGrid");
const headerAvatar = document.getElementById("headerAvatar");
const headerUser = document.getElementById("headerUser");
const profileAvatar = document.getElementById("profileAvatar");
const profileUsername = document.getElementById("profileUsername");
const profileEmail = document.getElementById("profileEmail");
const profileCreatedAt = document.getElementById("profileCreatedAt");
const profileGenres = document.getElementById("profileGenres");
const statsGrid = document.getElementById("statsGrid");
const profileRecentGrid = document.getElementById("profileRecentGrid");
const passwordModal = document.getElementById("passwordModal");
const openPasswordModal = document.getElementById("openPasswordModal");
const closePasswordModal = document.getElementById("closePasswordModal");
const passwordForm = document.getElementById("passwordForm");
const deleteAccountButton = document.getElementById("deleteAccountButton");

let games = [];
let allGenres = [];
let selectedGenres = [];
let favoriteGames = [];
let currentProfile = null;
let recentlyViewed = [];

function activatePanel(panelName) {
  panels.forEach((panel) => {
    panel.classList.toggle("active", panel.dataset.panel === panelName);
  });
  navButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.panelTarget === panelName);
  });
  window.location.hash = panelName;
}

function compareTopRated(left, right) {
  return (
    right.average_rating - left.average_rating ||
    right.reviews_count - left.reviews_count ||
    right.ratings_count - left.ratings_count ||
    left.title.localeCompare(right.title)
  );
}

function compareRecommended(left, right) {
  return (
    right.recommended_score - left.recommended_score ||
    right.average_rating - left.average_rating ||
    right.reviews_count - left.reviews_count ||
    left.title.localeCompare(right.title)
  );
}

function getRecommendedGames() {
  const items = [...games];
  return selectedGenres.length > 0 ? items.sort(compareRecommended) : items.sort(compareTopRated);
}

function getSearchQuery() {
  return searchInput.value.trim().toLowerCase();
}

function getCatalogGames() {
  const query = getSearchQuery();
  const filtered = games.filter((game) =>
    `${game.title} ${game.genres.join(" ")}`.toLowerCase().includes(query),
  );
  return selectedGenres.length > 0
    ? [...filtered].sort(compareRecommended)
    : [...filtered].sort(compareTopRated);
}

function renderCardGrid(target, items, options = {}) {
  const { emptyTitle, emptyDescription } = options;
  if (items.length === 0) {
    target.innerHTML = renderEmptyCard(
      emptyTitle || "Nothing here yet",
      emptyDescription || "Try a different search.",
    );
    return;
  }

  target.innerHTML = items.map((item) => renderGameCard(item)).join("");
}

function renderTileGrid(target, items, options = {}) {
  const { emptyTitle, emptyDescription, contextLabel } = options;
  if (items.length === 0) {
    target.innerHTML = renderEmptyCard(
      emptyTitle || "Nothing here yet",
      emptyDescription || "Try again after more activity.",
    );
    return;
  }

  target.innerHTML = items
    .map((item) => renderGameTile(item, { contextLabel: contextLabel?.(item) || "" }))
    .join("");
}

function renderList(target, items, options = {}) {
  const { emptyTitle, emptyDescription } = options;
  if (items.length === 0) {
    target.innerHTML = renderEmptyCard(
      emptyTitle || "Nothing here yet",
      emptyDescription || "Try again later.",
    );
    return;
  }

  target.innerHTML = items.map(renderGameListItem).join("");
}

function renderSpotlight() {
  const featured =
    getRecommendedGames().find((game) => game.recommended_score > 0) ||
    favoriteGames[0] ||
    getRecommendedGames()[0];

  if (!featured) {
    spotlightCard.innerHTML = renderEmptyCard(
      "Featured game unavailable",
      "A featured title will appear here after the catalog loads.",
    );
    return;
  }

  const matchedGenres = featured.genres.filter((genre) => selectedGenres.includes(genre));
  const reason = matchedGenres.length > 0
    ? `Based on your saved genres: ${matchedGenres.join(", ")}`
    : selectedGenres.length > 0
      ? "Selected from the strongest matches in your current recommendations"
      : "Selected from the highest-rated games in the catalog";
  const spotlightStats = [
    ["Average Rating", featured.average_rating.toFixed(1)],
    ["Player Ratings", `${featured.ratings_count}`],
    ["Reviews", `${featured.reviews_count}`],
  ];

  spotlightCard.innerHTML = `
    <div class="spotlight-layout">
      <div class="spotlight-cover-panel">
        <a class="spotlight-media" href="/game.html?id=${featured.id}" aria-label="Open ${featured.title}">
          <img class="spotlight-cover" src="${featured.cover_path}" alt="${featured.title} cover" />
        </a>
      </div>
      <div class="spotlight-main">
        <span class="soft-badge">Featured Game</span>
        <h2><a class="game-title-link spotlight-title-link" href="/game.html?id=${featured.id}">${featured.title}</a></h2>
        <p>${featured.short_description}</p>
        <div class="spotlight-inline-note">${reason}</div>
        <div class="genres-row spotlight-genres">
          ${featured.genres.map((genre) => `<span class="genre-chip">${genre}</span>`).join("")}
        </div>
        <div class="spotlight-bottom">
          <div class="spotlight-stat-grid">
            ${spotlightStats
              .map(
                ([label, value]) => `
                  <article class="spotlight-stat-card">
                    <span>${label}</span>
                    <strong>${value}</strong>
                  </article>
                `,
              )
              .join("")}
          </div>
        </div>
      </div>
    </div>
  `;
}

function renderCatalog() {
  const items = getCatalogGames();

  renderCardGrid(gamesGrid, items, {
    emptyTitle: "No matching games",
    emptyDescription: "Try another title or genre.",
  });
}

function renderSearchResults() {
  const query = getSearchQuery();
  const isSearching = query.length > 0;

  searchResultsSection.classList.toggle("hidden", !isSearching);
  forYouSection.classList.toggle("hidden", isSearching);
  topRatedSection.classList.toggle("hidden", isSearching);
  catalogSection.classList.toggle("hidden", isSearching);
  recentlyViewedSection.classList.toggle("hidden", isSearching || recentlyViewed.length === 0);

  if (!isSearching) {
    recommendationHint.textContent =
      selectedGenres.length > 0
        ? `Recommended titles are influenced by your favorite genres: ${selectedGenres.join(", ")}.`
        : "Search across the full catalog by title or genre.";
    return;
  }

  const items = getCatalogGames();
  recommendationHint.textContent = "Press backspace to return to the default shelves.";
  searchResultsHint.textContent =
    items.length === 1 ? "1 game matched your search." : `${items.length} games matched your search.`;

  renderCardGrid(searchResultsGrid, items, {
    emptyTitle: "No matching games",
    emptyDescription: "Try another title or genre.",
  });
}

function renderShelves() {
  const recommended = getRecommendedGames();
  const forYou = recommended.slice(0, 6);
  const topRated = [...games].sort(compareTopRated).slice(0, 4);

  renderCardGrid(forYouGrid, forYou, {
    emptyTitle: "No recommendations yet",
    emptyDescription: "Save a few favorite genres to shape this shelf.",
  });

  renderTileGrid(topRatedGrid, topRated, {
    emptyTitle: "No top-rated games yet",
    emptyDescription: "Ratings will appear here after the catalog loads.",
  });

  recentlyViewedSection.classList.toggle("hidden", recentlyViewed.length === 0);
  renderList(recentlyViewedGrid, recentlyViewed, {
    emptyTitle: "No recently viewed games",
    emptyDescription: "Open a game page and it will appear here.",
  });

  renderCatalog();
  renderSearchResults();
}

function renderGenres() {
  genresGrid.innerHTML = allGenres
    .map(
      (genre) => `
        <label class="genre-option">
          <input
            type="checkbox"
            value="${genre.name}"
            ${selectedGenres.includes(genre.name) ? "checked" : ""}
          />
          <span>${genre.name}</span>
        </label>
      `,
    )
    .join("");

  genresGrid.querySelectorAll("input").forEach((input) => {
    input.addEventListener("change", () => {
      selectedGenres = Array.from(genresGrid.querySelectorAll("input:checked")).map(
        (checkbox) => checkbox.value,
      );
    });
  });
}

function renderFavoriteGames() {
  renderTileGrid(favoriteGamesGrid, favoriteGames, {
    emptyTitle: "No favorite games yet",
    emptyDescription: "Give a game 5 stars to place it here.",
  });
}

function renderProfile(profile) {
  currentProfile = profile;
  headerUser.textContent = profile.username;
  renderUserAvatar(headerAvatar, profile.username);
  renderUserAvatar(profileAvatar, profile.username);
  profileUsername.textContent = profile.username;
  profileEmail.textContent = profile.email;
  profileCreatedAt.textContent = formatDate(profile.created_at);
  profileGenres.innerHTML = profile.favorite_genres.length
    ? profile.favorite_genres.map((genre) => `<span class="genre-chip">${genre}</span>`).join("")
    : `<span class="meta-muted">No favorite genres saved yet.</span>`;

  const stats = [
    ["Rated Games", profile.rated_games_count],
    ["Reviews", profile.reviews_count],
    ["Favorite Genres", profile.favorite_genres_count],
    ["Favorite Games", profile.favorite_games_count],
  ];

  statsGrid.innerHTML = stats
    .map(
      ([label, value]) => `
        <div class="stat-card">
          <strong>${value ?? 0}</strong>
          <span>${label}</span>
        </div>
      `,
    )
    .join("");
}

function renderProfileRecent() {
  renderList(profileRecentGrid, recentlyViewed, {
    emptyTitle: "No recent activity yet",
    emptyDescription: "Open a few game pages and they will appear here.",
  });
}

function renderEverything() {
  renderProfile(currentProfile);
  renderSpotlight();
  renderGenres();
  renderFavoriteGames();
  renderShelves();
  renderProfileRecent();
}

async function refreshData() {
  const [profile, genresResponse, preferences, gamesResponse, recentResponse] = await Promise.all([
    loadCurrentUser(),
    api("/genres"),
    api("/users/me/preferences"),
    api("/games"),
    api("/users/me/recently-viewed"),
  ]);

  currentProfile = profile;
  allGenres = genresResponse;
  selectedGenres = preferences.favorite_genres;
  favoriteGames = preferences.favorite_games;
  games = gamesResponse;
  recentlyViewed = recentResponse;

  renderEverything();
}

navButtons.forEach((button) => {
  button.addEventListener("click", () => activatePanel(button.dataset.panelTarget));
});

window.addEventListener("hashchange", () => {
  const panelName = window.location.hash.replace("#", "");
  if (["explore", "preferences", "profile"].includes(panelName)) {
    activatePanel(panelName);
  }
});

searchInput.addEventListener("input", renderShelves);
logoutButton.addEventListener("click", logout);

saveGenresButton.addEventListener("click", async () => {
  try {
    await api("/users/me/preferences", {
      method: "PUT",
      body: {
        genres: selectedGenres,
      },
    });
    showToast("Favorite genres saved.");
    await refreshData();
    activatePanel("explore");
  } catch (error) {
    showToast(error.message);
  }
});

openPasswordModal.addEventListener("click", () => {
  passwordModal.classList.remove("hidden");
});

closePasswordModal.addEventListener("click", () => {
  passwordModal.classList.add("hidden");
  passwordForm.reset();
});

passwordModal.addEventListener("click", (event) => {
  if (event.target === passwordModal) {
    passwordModal.classList.add("hidden");
    passwordForm.reset();
  }
});

passwordForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(passwordForm);

  try {
    await api("/auth/change-password", {
      method: "POST",
      body: {
        current_password: formData.get("currentPassword"),
        new_password: formData.get("newPassword"),
      },
    });
    passwordModal.classList.add("hidden");
    passwordForm.reset();
    showToast("Password updated.");
  } catch (error) {
    showToast(error.message);
  }
});

deleteAccountButton.addEventListener("click", async () => {
  const confirmed = window.confirm(
    "Delete this account permanently? Ratings, reviews, and profile data will be removed.",
  );
  if (!confirmed) {
    return;
  }

  try {
    await api("/auth/me", { method: "DELETE" });
    showToast("Account deleted.");
    logout();
  } catch (error) {
    showToast(error.message);
  }
});

const initialPanel = window.location.hash.replace("#", "") || "explore";
activatePanel(["explore", "preferences", "profile"].includes(initialPanel) ? initialPanel : "explore");

refreshData().catch((error) => {
  showToast(error.message);
});
