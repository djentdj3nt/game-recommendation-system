import {
  api,
  escapeHtml,
  formatDate,
  loadCurrentUser,
  logout,
  requireAuth,
  showToast,
  stars,
} from "./common.js";

if (!requireAuth()) {
  throw new Error("Authentication required");
}

const params = new URLSearchParams(window.location.search);
const gameId = params.get("id");

const headerUser = document.getElementById("headerUser");
const logoutButton = document.getElementById("logoutButton");
const gameHero = document.getElementById("gameHero");
const starPicker = document.getElementById("starPicker");
const ratingStatus = document.getElementById("ratingStatus");
const reviewForm = document.getElementById("reviewForm");
const reviewInput = document.getElementById("reviewInput");
const reviewsList = document.getElementById("reviewsList");
const reviewsEmpty = document.getElementById("reviewsEmpty");
const reviewsCounter = document.getElementById("reviewsCounter");

let currentGame = null;

if (!gameId) {
  showToast("Game id is missing.");
  window.location.href = "/app.html";
  throw new Error("Game id is missing");
}

function renderHero(game) {
  const requirements = escapeHtml(game.system_requirements);
  gameHero.innerHTML = `
    <div class="game-hero-inner">
      <img class="details-cover" src="${escapeHtml(game.cover_path)}" alt="${escapeHtml(game.title)} cover" />
      <div>
        <span class="eyebrow">Game Page</span>
        <h1 class="game-title">${escapeHtml(game.title)}</h1>
        <p class="game-subtitle">${escapeHtml(game.short_description)}</p>
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
          <pre>${requirements}</pre>
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

function renderReviews(game) {
  reviewsCounter.textContent = `${game.reviews_count} community review${game.reviews_count === 1 ? "" : "s"}.`;

  if (game.reviews.length === 0) {
    reviewsList.innerHTML = "";
    reviewsEmpty.classList.remove("hidden");
    return;
  }

  reviewsEmpty.classList.add("hidden");
  reviewsList.innerHTML = game.reviews
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
    .join("");
}

async function loadGame() {
  currentGame = await api(`/games/${gameId}`);
  renderHero(currentGame);
  renderStarPicker(currentGame.my_rating);
  reviewInput.value = currentGame.my_review || "";
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

Promise.all([loadCurrentUser(), loadGame()])
  .then(([profile]) => {
    headerUser.textContent = profile.username;
  })
  .catch((error) => {
    showToast(error.message);
  });
