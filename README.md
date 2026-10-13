# Recommender System

This project is a small e-commerce recommendation stack built with FastAPI, Next.js 14, PostgreSQL, Redis, and a lightweight ML recommendation fallback. It is designed to run locally with Docker Compose and to deploy behind a single nginx frontend for production.

## Overview

The backend provides product listings, auth, recommendation endpoints, and health checks. The frontend is a Next.js app that calls the backend over either an absolute URL or a relative `/api` base. In development, the app uses local Docker services. In production, the backend is served behind nginx with `/api` stripped at the proxy layer.

## Architecture

```text
Browser
  -> nginx (single origin) or localhost:3000
  -> Next.js frontend
  -> FastAPI backend on /api
  -> PostgreSQL + Redis + ML artifacts
```

## Run locally

### Docker Compose

1. Copy the root sample environment file:

```bash
cp .env.example .env
```

2. Update the generated values in `.env` before the first run. The defaults are safe for local Docker use and will point to the `postgres` and `redis` service names inside Compose.

3. Start everything:

```bash
docker compose up --build
```

Then open:

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

### Local host development without Docker

Install Python and Node dependencies and run each service directly on your machine:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-local.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

```bash
cd frontend
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

If you want to seed demo data:

```bash
cd backend
ALLOW_SEED=true ENVIRONMENT=development python seed_data.py
```

## Demo ML artifacts

A fresh clone does not include trained model files. The backend will use a deterministic popularity fallback until the model artifacts exist. To generate the minimal demo model artifacts, run:

```bash
cd ml
python export_demo_model.py
```

This creates the files needed under `ml/models` and does not require the notebook.

## Deploy to a single server

Production deployment is handled by `docker-compose.prod.yml` and `deploy/nginx.conf`.

- nginx is the only port published to the host.
- the frontend is built as a standalone Next.js image.
- `/api/` is routed to the backend with the `/api` prefix stripped.
- `/` is routed to the frontend.
- `/healthz` returns a lightweight 200 status without touching the app.

Example:

```bash
cp .env.example .env
# set production values, then
docker compose -f docker-compose.prod.yml up --build
```

Then open the host on port 80 or the value of `HTTP_PORT`.

## Environment variables

| Variable | Default | Required in production | Notes |
| --- | --- | --- | --- |
| POSTGRES_USER | recommender_user | No | Database username |
| POSTGRES_PASSWORD | change_me | Yes | Database password |
| POSTGRES_DB | recommender_db | No | Database name |
| DATABASE_URL | postgresql://recommender_user:change_me@postgres:5432/recommender_db | Yes | Container DB URL |
| REDIS_URL | redis://redis:6379 | No | Redis connection URL |
| JWT_SECRET | change_this_to_a_32_character_or_longer_secret | Yes | Must be at least 32 chars |
| ENVIRONMENT | development | No | `development` or `production` |
| FRONTEND_URL | http://localhost:3000 | No | Allowed frontend origin |
| CORS_ORIGINS | http://localhost:3000,http://127.0.0.1:3000 | No | Comma-separated list of allowed origins |
| NEXT_PUBLIC_API_URL | http://localhost:8000 | No | Frontend backend URL |
| MODEL_PATH | ./ml/models | No | ML artifact directory |
| ALLOW_SEED | true | No | Demo-only seeding override |
| COOKIE_SECURE | false | No | Force secure cookies in production |
| ROOT_PATH | empty | No | Reverse proxy prefix such as /api |

## Default demo accounts

- alice@example.com / password123
- bob@example.com / password123
- admin@example.com / admin123

## API reference

The backend exposes the following main endpoints:

- GET /health
- GET /api/v1/products/
- GET /api/v1/products/{id}
- POST /api/v1/auth/register
- POST /api/v1/auth/login
- GET /api/v1/auth/me
- GET /api/v1/recommend/{user_id}
- POST /api/v1/track_click

## Testing

Backend:

```bash
cd backend
python -m pytest tests -q
```

Frontend:

```bash
cd frontend
npm test
npm run lint
npm run build
```

## Notes

- The project uses a production-safe JSON health check and a graceful Redis fallback.
- Model artifacts are not committed by default. The demo export script is intended to create them locally for development.
- No `.env` file is committed. Secrets should remain in the local root `.env` or in the host environment.
docker-compose build --no-cache
```

## Troubleshooting

| Issue                          | Solution                                        |
| ------------------------------ | ----------------------------------------------- |
| Port already in use            | Change port in `docker-compose.yml` or local service config |
| Database connection failed     | Verify `DATABASE_URL` in `.env` and database is running |
| ML model file not found        | Run `python backend/seed_data.py` to initialize |
| Node modules issues            | Delete `node_modules/` and `package-lock.json`, then `npm install` |
| Node modules issues            | Delete `node_modules/` and `package-lock.json`, then `npm install` |
| Python import errors           | Verify virtualenv is activated and packages are installed |

## Security Best Practices

### Production Security Quickstart
1. **JWT Secret:** Generate a strong random secret (`openssl rand -hex 32`) and set it as `JWT_SECRET` in your `.env` (at least 32 characters; 64 hex characters recommended).
2. **Cookies:** The application relies on HttpOnly cookies. Ensure your production environment uses HTTPS, or the `Secure` flag on cookies will prevent logins.
3. **Seed Data:** Do NOT run `seed_data.py` in production; it is restricted to `ENVIRONMENT=development` and uses randomly generated passwords.
4. **Database Credentials:** Restrict PostgreSQL and Redis with strong, automatically-rotated credentials when deploying to the cloud.

### Incident Response
- **Secret Compromise:** Rotate `JWT_SECRET` immediately. This will invalidate all newly-issued tokens but current sessions might remain active depending on the payload.
- **Session Revocation:** For active sessions, individual users logouts are tracked via an in-memory denylist (or Redis). In emergencies, bounce the backend service (if using in-memory) or clear the Redis cache to forcefully reset all sessions.
- **Infrastructure Compromise:** Rotate DB, Redis passwords, and redeploy containers.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or suggestions, please open an [issue](https://github.com/your-repo/issues) on GitHub.
