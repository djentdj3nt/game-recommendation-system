from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload

from .auth import create_access_token, get_current_user, hash_password, verify_password
from .database import Base, SessionLocal, engine, get_db
from .models import ActivityLog, Game, Genre, Rating, Review, User
from .schemas import (
    ChangePasswordRequest,
    GameCardOut,
    GameDetailOut,
    GenreOut,
    LoginRequest,
    MessageResponse,
    PreferencesResponse,
    PreferencesUpdateRequest,
    ProfileResponse,
    RatingBreakdownItem,
    RatingRequest,
    RegisterRequest,
    ReviewOut,
    ReviewRequest,
    TokenResponse,
)
from .seed import seed_database


app = FastAPI(title="PlayNext API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


def log_action(db: Session, user_id: int | None, action: str, details: str):
    db.add(ActivityLog(user_id=user_id, action=action, details=details))


def serialize_review(review: Review, current_user_id: int | None) -> ReviewOut:
    rating_value = None
    for rating in review.game.ratings:
        if rating.user_id == review.user_id:
            rating_value = rating.value
            break

    return ReviewOut(
        id=review.id,
        username=review.user.username,
        rating=rating_value,
        content=review.content,
        created_at=review.created_at,
        updated_at=review.updated_at,
        is_mine=current_user_id == review.user_id,
    )


def get_rating_breakdown(game: Game) -> list[RatingBreakdownItem]:
    counts = {stars: 0 for stars in range(5, 0, -1)}
    for rating in game.ratings:
        if rating.value in counts:
            counts[rating.value] += 1
    return [RatingBreakdownItem(stars=stars, count=counts[stars]) for stars in range(5, 0, -1)]


def serialize_game(game: Game, current_user: User | None, preferred_genres: set[str]) -> GameCardOut:
    genre_names = sorted(genre.name for genre in game.genres)
    ratings = [rating.value for rating in game.ratings]
    average_rating = round(sum(ratings) / len(ratings), 1) if ratings else 0.0
    my_rating = None
    if current_user is not None:
        for rating in game.ratings:
            if rating.user_id == current_user.id:
                my_rating = rating.value
                break
    matched_genres = sorted(genre for genre in genre_names if genre in preferred_genres)
    recommended_score = len(matched_genres)

    return GameCardOut(
        id=game.id,
        title=game.title,
        short_description=game.short_description,
        cover_path=game.cover_path,
        genres=genre_names,
        average_rating=average_rating,
        ratings_count=len(game.ratings),
        reviews_count=len(game.reviews),
        my_rating=my_rating,
        recommended_score=recommended_score,
        matched_genres=matched_genres,
    )


def get_games_query(db: Session):
    return (
        db.query(Game)
        .options(
            joinedload(Game.genres),
            joinedload(Game.ratings),
            joinedload(Game.reviews).joinedload(Review.user),
        )
        .order_by(Game.title.asc())
    )


def build_profile_response(db: Session, user: User) -> ProfileResponse:
    refreshed_user = (
        db.query(User)
        .options(
            joinedload(User.favorite_genres),
            joinedload(User.ratings),
            joinedload(User.reviews),
        )
        .filter(User.id == user.id)
        .first()
    )
    favorite_games_count = sum(1 for rating in refreshed_user.ratings if rating.value == 5)
    return ProfileResponse(
        username=refreshed_user.username,
        email=refreshed_user.email,
        role=refreshed_user.role,
        created_at=refreshed_user.created_at,
        rated_games_count=len(refreshed_user.ratings),
        reviews_count=len(refreshed_user.reviews),
        favorite_genres_count=len(refreshed_user.favorite_genres),
        favorite_games_count=favorite_games_count,
        favorite_genres=sorted(genre.name for genre in refreshed_user.favorite_genres),
    )


def get_user_with_preferences(db: Session, user_id: int) -> User:
    return (
        db.query(User)
        .options(joinedload(User.favorite_genres))
        .filter(User.id == user_id)
        .first()
    )


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/auth/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = (
        db.query(User)
        .filter((User.email == payload.email) | (User.username == payload.username))
        .first()
    )
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists.",
        )

    user = User(
        username=payload.username,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role="player",
    )
    db.add(user)
    db.flush()
    log_action(db, user.id, "register", f"New account: {user.email}")
    db.commit()
    return TokenResponse(access_token=create_access_token(user.id))


@app.post("/api/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    log_action(db, user.id, "login", "User signed in")
    db.commit()
    return TokenResponse(access_token=create_access_token(user.id))


@app.get("/api/auth/me", response_model=ProfileResponse)
def get_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return build_profile_response(db, current_user)


@app.post("/api/auth/change-password", response_model=MessageResponse)
def change_password(
    payload: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not verify_password(payload.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect.",
        )

    current_user.password_hash = hash_password(payload.new_password)
    log_action(db, current_user.id, "change_password", "Password updated")
    db.commit()
    return MessageResponse(message="Password updated successfully.")


@app.delete("/api/auth/me", response_model=MessageResponse)
def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    username = current_user.username
    db.delete(current_user)
    db.commit()
    return MessageResponse(message=f"Account {username} was deleted.")


@app.get("/api/genres", response_model=list[GenreOut])
def list_genres(db: Session = Depends(get_db)):
    return db.query(Genre).order_by(Genre.name.asc()).all()


@app.get("/api/games", response_model=list[GameCardOut])
def list_games(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user = get_user_with_preferences(db, current_user.id)
    preferred_genres = {genre.name for genre in current_user.favorite_genres}
    games = [serialize_game(game, current_user, preferred_genres) for game in get_games_query(db).all()]

    if preferred_genres:
        games.sort(
            key=lambda item: (
                -item.recommended_score,
                -item.average_rating,
                -item.reviews_count,
                item.title,
            )
        )
    else:
        games.sort(key=lambda item: (-item.average_rating, -item.reviews_count, item.title))
    return games


@app.get("/api/games/{game_id}", response_model=GameDetailOut)
def get_game_details(
    game_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    game = get_games_query(db).filter(Game.id == game_id).first()
    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found.")

    ratings = [rating.value for rating in game.ratings]
    average_rating = round(sum(ratings) / len(ratings), 1) if ratings else 0.0
    my_rating = next((rating.value for rating in game.ratings if rating.user_id == current_user.id), None)
    my_review_obj = next((review for review in game.reviews if review.user_id == current_user.id), None)
    ordered_reviews = sorted(game.reviews, key=lambda review: review.updated_at, reverse=True)
    current_user = get_user_with_preferences(db, current_user.id)
    preferred_genres = {genre.name for genre in current_user.favorite_genres}
    game_genres = sorted(genre.name for genre in game.genres)

    log_action(db, current_user.id, "view_game", game.title)
    db.commit()

    return GameDetailOut(
        id=game.id,
        title=game.title,
        short_description=game.short_description,
        description=game.description,
        cover_path=game.cover_path,
        system_requirements=game.system_requirements,
        genres=game_genres,
        average_rating=average_rating,
        ratings_count=len(game.ratings),
        reviews_count=len(game.reviews),
        my_rating=my_rating,
        my_review=my_review_obj.content if my_review_obj else None,
        matched_genres=sorted(genre for genre in game_genres if genre in preferred_genres),
        rating_breakdown=get_rating_breakdown(game),
        reviews=[serialize_review(review, current_user.id) for review in ordered_reviews],
    )


@app.post("/api/games/{game_id}/rating", response_model=MessageResponse)
def upsert_rating(
    game_id: int,
    payload: RatingRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    game = db.get(Game, game_id)
    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found.")

    rating = (
        db.query(Rating)
        .filter(Rating.user_id == current_user.id, Rating.game_id == game_id)
        .first()
    )

    if rating is None:
        db.add(Rating(user_id=current_user.id, game_id=game_id, value=payload.value))
        message = "Rating added."
    else:
        rating.value = payload.value
        rating.updated_at = datetime.utcnow()
        message = "Rating updated."

    log_action(db, current_user.id, "rate_game", f"{game.title}: {payload.value} stars")
    db.commit()
    return MessageResponse(message=message)


@app.post("/api/games/{game_id}/review", response_model=MessageResponse)
def upsert_review(
    game_id: int,
    payload: ReviewRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    game = db.get(Game, game_id)
    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found.")

    review = (
        db.query(Review)
        .filter(Review.user_id == current_user.id, Review.game_id == game_id)
        .first()
    )
    cleaned_content = payload.content.strip()
    if len(cleaned_content) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Review must contain at least 3 non-space characters.",
        )

    if review is None:
        db.add(Review(user_id=current_user.id, game_id=game_id, content=cleaned_content))
        message = "Review added."
    else:
        review.content = cleaned_content
        review.updated_at = datetime.utcnow()
        message = "Review updated."

    log_action(db, current_user.id, "review_game", game.title)
    db.commit()
    return MessageResponse(message=message)


@app.get("/api/users/me/preferences", response_model=PreferencesResponse)
def get_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .options(joinedload(User.favorite_genres), joinedload(User.ratings))
        .filter(User.id == current_user.id)
        .first()
    )
    preferred_genres = {genre.name for genre in user.favorite_genres}

    favorite_game_ids = [rating.game_id for rating in user.ratings if rating.value == 5]
    if favorite_game_ids:
        favorite_games = [
            serialize_game(game, user, preferred_genres)
            for game in get_games_query(db).filter(Game.id.in_(favorite_game_ids)).all()
        ]
    else:
        favorite_games = []

    return PreferencesResponse(
        favorite_genres=sorted(preferred_genres),
        favorite_games=sorted(favorite_games, key=lambda item: item.title),
    )


@app.put("/api/users/me/preferences", response_model=MessageResponse)
def update_preferences(
    payload: PreferencesUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    requested_genres = sorted(set(payload.genres))
    genres = db.query(Genre).filter(Genre.name.in_(requested_genres)).all()
    found_genres = {genre.name for genre in genres}
    missing = [genre for genre in requested_genres if genre not in found_genres]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown genres: {', '.join(missing)}",
        )

    user = (
        db.query(User)
        .options(joinedload(User.favorite_genres))
        .filter(User.id == current_user.id)
        .first()
    )
    user.favorite_genres = genres
    log_action(db, current_user.id, "update_preferences", ", ".join(requested_genres) or "no genres")
    db.commit()
    return MessageResponse(message="Favorite genres updated.")


@app.get("/api/users/me/recently-viewed", response_model=list[GameCardOut])
def get_recently_viewed(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = get_user_with_preferences(db, current_user.id)
    preferred_genres = {genre.name for genre in user.favorite_genres}
    activity_logs = (
        db.query(ActivityLog)
        .filter(ActivityLog.user_id == current_user.id, ActivityLog.action == "view_game")
        .order_by(ActivityLog.created_at.desc())
        .all()
    )

    unique_titles = []
    seen_titles = set()
    for log_item in activity_logs:
        if log_item.details not in seen_titles:
            unique_titles.append(log_item.details)
            seen_titles.add(log_item.details)
        if len(unique_titles) == 6:
            break

    if not unique_titles:
        return []

    game_lookup = {
        game.title: game
        for game in get_games_query(db).filter(Game.title.in_(unique_titles)).all()
    }
    return [
        serialize_game(game_lookup[title], user, preferred_genres)
        for title in unique_titles
        if title in game_lookup
    ]
