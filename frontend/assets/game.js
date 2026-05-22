import {
  api,
  escapeHtml,
  formatDate,
  loadCurrentUser,
  logout,
  renderEmptyCard,
  renderGameTile,
  renderUserAvatar,
  requireAuth,
  showToast,
  stars,
} from "./common.js";

if (!requireAuth()) {
  throw new Error("Authentication required");
}

const params = new URLSearchParams(window.location.search);
const gameId = params.get("id");

const headerAvatar = document.getElementById("headerAvatar");
const headerUser = document.getElementById("headerUser");
const logoutButton = document.getElementById("logoutButton");
const gameHero = document.getElementById("gameHero");
const starPicker = document.getElementById("starPicker");
const ratingStatus = document.getElementById("ratingStatus");
const reviewForm = document.getElementById("reviewForm");
const reviewInput = document.getElementById("reviewInput");
const matchSummary = document.getElementById("matchSummary");
const ratingBreakdown = document.getElementById("ratingBreakdown");
const relatedGamesGrid = document.getElementById("relatedGamesGrid");
const reviewsList = document.getElementById("reviewsList");
const reviewsCounter = document.getElementById("reviewsCounter");

let currentGame = null;
let allGames = [];

if (!gameId) {
  showToast("Game id is missing.");
  window.location.href = "/app.html";
  throw new Error("Game id is missing");
}

function renderHero(game) {
  const matchedBadge = game.matched_genres.length
    ? `<div class="callout-row"><span class="match-badge">Matches ${game.matched_genres.length}</span><span class="meta-muted">Because you like ${escapeHtml(game.matched_genres.join(", "))}</span></div>`
    : `<div class="callout-row"><span class="soft-badge">Featured Pick</span><span class="meta-muted">A strong title from the current catalog.</span></div>`;

  gameHero.innerHTML = `
    <div class="game-hero-inner">
      <div class="hero-cover-column">
        <img class="details-cover" src="${escapeHtml(game.cover_path)}" alt="${escapeHtml(game.title)} cover" />
      </div>
      <div class="hero-main-column">
        <h1 class="game-title">${escapeHtml(game.title)}</h1>
        <p class="game-subtitle">${escapeHtml(game.short_description)}</p>
        ${matchedBadge}
        <div class="genres-row">
          ${game.genres.map((genre) => `<span class="genre-chip">${escapeHtml(genre)}</span>`).join("")}
        </div>
        <div class="details-meta">
          <div class="stat-item"><strong>${game.average_rating.toFixed(1)}</strong><span>average rating</span></div>
          <div class="stat-item"><strong>${game.ratings_count}</strong><span>ratings</span></div>
          <div class="stat-item"><strong>${game.reviews_count}</strong><span>reviews</span></div>
        </div>
        <p class="hero-text">${escapeHtml(game.description)}</p>
        <div class="requirements-box">
          <h3 class="subsection-title">System Requirements</h3>
          <pre>${escapeHtml(game.system_requirements)}</pre>
        </div>
      </div>
    </div>
  `;
}

function renderStarPicker(currentRating) {
  starPicker.innerHTML = Array.from({ length: 5 }, (_, index) => {
    const value = index + 1;
    return `
      <button
        class="star-button ${currentRating >= value ? "active" : ""}"
        data-rating-value="${value}"
        type="button"
      >
        &#9733;
      </button>
    `;
  }).join("");

  ratingStatus.textContent =
    currentRating !== null
      ? `Your current rating: ${stars(currentRating)}`
      : "You have not rated this game yet.";

  starPicker.querySelectorAll("[data-rating-value]").forEach((button) => {
    button.addEventListener("click", async () => {
      const value = Number(button.dataset.ratingValue);
      try {
        await api(`/games/${gameId}/rating`, {
          method: "POST",
          body: { value },
        });
        showToast(`Saved ${value} star${value > 1 ? "s" : ""}.`);
        await loadGame();
      } catch (error) {
        showToast(error.message);
      }
    });
  });
}

function renderMatchSummary(game) {
  const cards = [
    {
      label: "Why it may fit",
      value: game.matched_genres.length
        ? `This game overlaps with your saved genres: ${game.matched_genres.join(", ")}.`
        : "This game is currently shown because it performs well in the catalog.",
    },
    {
      label: "Ratings",
      value: `${game.average_rating.toFixed(1)} average from ${game.ratings_count} ratings and ${game.reviews_count} reviews.`,
    },
    {
      label: "Your status",
      value:
        game.my_rating !== null
          ? `You rated this game ${stars(game.my_rating)}${game.my_review ? " and already left a review." : "."}`
          : "You have not rated this game yet.",
    },
  ];

  matchSummary.innerHTML = cards
    .map(
      (card) => `
        <article class="insight-card">
          <strong>${escapeHtml(card.label)}</strong>
          <p>${escapeHtml(card.value)}</p>
        </article>
      `,
    )
    .join("");
}

function renderRatingBreakdown(game) {
  const maxCount = Math.max(...game.rating_breakdown.map((item) => item.count), 1);

  ratingBreakdown.innerHTML = `
    <h3 class="subsection-title">Rating Breakdown</h3>
    ${game.rating_breakdown
      .map(
        (item) => `
          <div class="breakdown-row">
            <span>${item.stars} stars</span>
            <div class="breakdown-bar">
              <div class="breakdown-fill" style="width: ${(item.count / maxCount) * 100}%"></div>
            </div>
            <strong>${item.count}</strong>
          </div>
        `,
      )
      .join("")}
  `;
}

function renderRelatedGames() {
  const currentGenres = new Set(currentGame.genres);
  const related = [...allGames]
    .filter((game) => game.id !== currentGame.id)
    .map((game) => {
      const sharedGenres = game.genres.filter((genre) => currentGenres.has(genre));
      return { ...game, sharedGenres };
    })
    .sort(
      (left, right) =>
        right.sharedGenres.length - left.sharedGenres.length ||
        right.average_rating - left.average_rating ||
        right.reviews_count - left.reviews_count ||
        left.title.localeCompare(right.title),
    )
    .slice(0, 4);

  relatedGamesGrid.innerHTML = related.length
    ? related
        .map((game) =>
          renderGameTile(game, {
            contextLabel: game.sharedGenres.length > 0 ? `Shared genres: ${game.sharedGenres.join(", ")}` : "",
          }),
        )
        .join("")
    : renderEmptyCard("No related games found", "This section will fill in as the catalog grows.");
}

function renderReviews(game) {
  reviewsCounter.textContent = `${game.reviews_count} review${game.reviews_count === 1 ? "" : "s"} for this title.`;

  reviewsList.innerHTML = game.reviews.length
    ? game.reviews
        .map(
          (review) => `
            <article class="review-card">
              <div class="review-top">
                <div>
                  <strong>${escapeHtml(review.username)}</strong>
                  <p>${formatDate(review.updated_at)}${review.is_mine ? " - Your review" : ""}</p>
                </div>
                <span class="review-rating">${review.rating ? stars(review.rating) : "No rating"}</span>
              </div>
              <p>${escapeHtml(review.content)}</p>
            </article>
          `,
        )
        .join("")
    : renderEmptyCard("No reviews yet", "Be the first player to add a review for this title.");
}

async function loadGame() {
  currentGame = await api(`/games/${gameId}`);
  renderHero(currentGame);
  renderStarPicker(currentGame.my_rating);
  reviewInput.value = currentGame.my_review || "";
  renderMatchSummary(currentGame);
  renderRatingBreakdown(currentGame);
  renderRelatedGames();
  renderReviews(currentGame);
}

logoutButton.addEventListener("click", logout);

reviewForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const content = reviewInput.value.trim();
  if (content.length < 3) {
    showToast("Write at least a short review.");
    return;
  }

  try {
    await api(`/games/${gameId}/review`, {
      method: "POST",
      body: { content },
    });
    showToast("Review saved.");
    await loadGame();
  } catch (error) {
    showToast(error.message);
  }
});

Promise.all([loadCurrentUser(), api("/games"), loadGame()])
  .then(([profile, gamesResponse]) => {
    headerUser.textContent = profile.username;
    renderUserAvatar(headerAvatar, profile.username);
    allGames = gamesResponse;
    renderRelatedGames();
  })
  .catch((error) => {
    showToast(error.message);
  });
