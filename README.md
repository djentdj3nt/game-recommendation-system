# PlayNext

PlayNext is a client-server web application for discovering games, saving favorite genres, rating titles, and writing reviews.

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python, FastAPI, SQLAlchemy
- Database: PostgreSQL
- Web server: Nginx
- Infrastructure: Docker Compose

## Main Features

- User registration and login with JWT authentication
- Explore page with game cards and cover images
- Game details page with description, genres, system requirements, ratings, and reviews
- User rating from 1 to 5 stars
- One personal review per game, with update support
- Preferences page with favorite genres
- Favorite games list based on 5-star ratings
- Profile page with account information and user statistics

## Project Structure

```text
backend/              FastAPI backend application
frontend/             Static frontend files
nginx/                Nginx Dockerfile and configuration
covers/               Game cover images
docker-compose.yml    Docker Compose services
```

## First Start

Run these commands from the project root:

```bash
docker compose up --build
```

Then open the application in a browser:

```text
http://localhost:8080
```

On the first start, the backend creates the database tables and fills the catalog with games, genres, ratings, and reviews.

## Stop the Project

```bash
docker compose down
```

This stops and removes the containers, but keeps the PostgreSQL data volume.

## Start Again Without Resetting Data

Use this when you want to continue with the same database:

```bash
docker compose up
```

If you changed code or static files, rebuild the images:

```bash
docker compose up --build
```

If the browser still shows old frontend files, rebuild Nginx without cache:

```bash
docker compose build --no-cache nginx
docker compose up
```

## Full Reset

Use this when you want to start from a clean database:

```bash
docker compose down -v --remove-orphans
docker compose up --build
```

The `-v` flag removes the PostgreSQL volume, so all registered users, ratings, and reviews created during local testing will be deleted.

## Useful Checks

Show container status:

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
