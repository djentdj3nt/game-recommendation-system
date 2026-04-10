import {
  api,
  formatDate,
  initialsFromName,
  loadCurrentUser,
  logout,
  renderGameCard,
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
const gamesGrid = document.getElementById("gamesGrid");
const gamesEmpty = document.getElementById("gamesEmpty");
const recommendationHint = document.getElementById("recommendationHint");
const genresGrid = document.getElementById("genresGrid");
const saveGenresButton = document.getElementById("saveGenresButton");
const favoriteGamesGrid = document.getElementById("favoriteGamesGrid");
const favoritesEmpty = document.getElementById("favoritesEmpty");
const headerUser = document.getElementById("headerUser");
const profileAvatar = document.getElementById("profileAvatar");
const profileUsername = document.getElementById("profileUsername");
const profileEmail = document.getElementById("profileEmail");
const profileCreatedAt = document.getElementById("profileCreatedAt");
const statsGrid = document.getElementById("statsGrid");
const passwordModal = document.getElementById("passwordModal");
const openPasswordModal = document.getElementById("openPasswordModal");
const closePasswordModal = document.getElementById("closePasswordModal");
const passwordForm = document.getElementById("passwordForm");
const deleteAccountButton = document.getElementById("deleteAccountButton");

let games = [];
let allGenres = [];
let selectedGenres = [];

function activatePanel(panelName) {
  panels.forEach((panel) => {
    panel.classList.toggle("active", panel.dataset.panel === panelName);
  });
  navButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.panelTarget === panelName);
  });
  window.location.hash = panelName;
}

function renderGames() {
  const query = searchInput.value.trim().toLowerCase();
  const filteredGames = games.filter((game) => {
    const searchable = `${game.title} ${game.genres.join(" ")}`.toLowerCase();
    return searchable.includes(query);
  });

  gamesGrid.innerHTML = filteredGames.map(renderGameCard).join("");
  gamesEmpty.classList.toggle("hidden", filteredGames.length > 0);
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

function renderFavoriteGames(items) {
  favoriteGamesGrid.innerHTML = items.map(renderGameCard).join("");
  favoritesEmpty.classList.toggle("hidden", items.length > 0);
}

function renderProfile(profile) {
  headerUser.textContent = profile.username;
  profileAvatar.textContent = initialsFromName(profile.username);
  profileUsername.textContent = profile.username;
  profileEmail.textContent = profile.email;
  profileCreatedAt.textContent = formatDate(profile.created_at);

  const stats = [
    ["Rated Games", profile.rated_games_count],
    ["Written Reviews", profile.reviews_count],
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

async function refreshData() {
  const [profile, genresResponse, preferences, gamesResponse] = await Promise.all([
    loadCurrentUser(),
    api("/genres"),
    api("/users/me/preferences"),
    api("/games"),
  ]);

  allGenres = genresResponse;
  selectedGenres = preferences.favorite_genres;
  games = gamesResponse;

  recommendationHint.textContent =
    selectedGenres.length > 0
      ? `Recommendations are tuned for: ${selectedGenres.join(", ")}.`
      : "Popular titles sorted by community rating.";

  renderProfile(profile);
  renderGenres();
  renderFavoriteGames(preferences.favorite_games);
  renderGames();
}

navButtons.forEach((button) => {
  button.addEventListener("click", () => activatePanel(button.dataset.panelTarget));
});

searchInput.addEventListener("input", renderGames);

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

logoutButton.addEventListener("click", logout);

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
