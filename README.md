# PlayNext

PlayNext is a client-server web application for game discovery. It lets players browse a curated catalog, save favorite genres, rate games, write one review per game, and view a lightweight player profile.

The project is intentionally simple enough for a junior developer to maintain, but polished enough to present as a believable product prototype.

## Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python, FastAPI, SQLAlchemy
- Database: PostgreSQL
- Web server / reverse proxy: Nginx
- Infrastructure: Docker Compose

## Current MVP Scope

- Registration and login with JWT authentication
- Demo account for quick presentations
- Explore page with featured shelves and search
- Game detail page with ratings, reviews, and related games
- Preferences page with favorite genres
- Favorite games shelf based on 5-star ratings
- Profile page with account statistics and recent activity

## Project Structure

```text
backend/              FastAPI application
frontend/             Static frontend files served by Nginx
nginx/                Nginx Dockerfile and reverse proxy config
covers/               Local game cover images
public/               Favicon assets
docker-compose.yml    Multi-container setup
```

## Run the Project

From the project root:

```bash
cp .env.example .env
docker compose up --build
```

Open the application in a browser:

```text
http://localhost:8080
```

## Demo Account

You can log in with the prepared demo account:

```text
Email: demo@playnext.com
Password: demo12345
```

The demo account is seeded with favorite genres, ratings, reviews, favorites, and recent activity to make product presentations easier.

## Data Seeding

On startup the backend:

- creates database tables
- seeds genres and games
- adds demo users
- adds sample ratings and reviews
- prepares recent activity for the demo account

If the PostgreSQL volume already exists, previously saved local data is preserved.

## Stop the Project

```bash
docker compose down
```

## Start Again

```bash
docker compose up
```

## Full Reset

Use this when you want a clean database:

```bash
docker compose down -v --remove-orphans
docker compose up --build
```

## Optional Configuration

You can edit `.env` before startup. Useful variables:

```text
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
JWT_SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES
APP_PORT
```

## Useful Commands

Check running containers:

```bash
docker compose ps
```

Show backend logs:

```bash
docker compose logs backend --tail=100
```

Show Nginx logs:

```bash
docker compose logs nginx --tail=100
```
