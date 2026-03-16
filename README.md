# Recommender System

A production-ready e-commerce recommendation engine built with modern web technologies and ML. This repository provides a complete MVP scaffold with a Next.js frontend, FastAPI backend, PostgreSQL/Redis persistence, and an ML training pipeline.

## Overview

This system implements a hybrid recommendation approach combining collaborative filtering and content-based similarity. It is designed for local development, evaluation, and production deployment to cloud infrastructure.

## Demo Screenshot

![Recommender System Demo - Home](Screenshot%202026-03-16%20160610.png)

![Recommender System Demo - Product](Screenshot%202026-03-16%20154049.png)

**Key capabilities:**
- Real-time product recommendations with Redis caching
- User authentication and session management (JWT)
- A/B testing framework for experimentation
- Interaction tracking and analytics
- Containerized architecture (Docker Compose)

## Architecture

```text
┌─────────────────┐
│  Next.js (UI)   │
└────────┬────────┘
         │ HTTP
┌────────▼──────────────┐
│ FastAPI (REST API)    │
└────────┬──────────────┘
         │ SQL / Cache
┌────────▼──────────────────────────────┐
│ PostgreSQL | Redis | ML Model         │
└───────────────────────────────────────┘
```

## Technology Stack

| Component  | Technology                          |
| ---------- | ----------------------------------- |
| Frontend   | Next.js 14, TailwindCSS, shadcn/ui |
| Backend    | FastAPI, Python 3.11+, Uvicorn    |
| Database   | PostgreSQL, Redis                  |
| ML         | scikit-learn, PyTorch              |
| DevOps     | Docker, Docker Compose             |
| Security   | JWT, bcrypt, input validation      |

## Project Structure

```text
.
├── backend/                    # FastAPI service
│   ├── app/
│   │   ├── main.py            # Application entry point
│   │   ├── database.py        # Database setup
│   │   ├── models.py          # SQLAlchemy models
│   │   ├── schemas.py         # Pydantic schemas
│   │   ├── routes/            # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── products.py
│   │   │   ├── recommend.py
│   │   │   └── ab_test.py
│   ├── requirements.txt
│   ├── requirements-local.txt
│   ├── seed_data.py           # Database seeding
│   └── Dockerfile
│
├── frontend/                   # Next.js application
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── admin/
│   │   └── providers.tsx
│   ├── components/
│   │   ├── product-grid.tsx
│   │   ├── recommendation-section.tsx
│   │   └── ui/
│   ├── lib/
│   │   ├── api-client.ts
│   │   └── utils.ts
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
│
├── ml/                        # Machine learning pipeline
│   ├── train_model.ipynb      # Training notebook
│   ├── preprocess.py          # Data preprocessing
│   ├── utils.py
│   └── requirements.txt
│
├── docker-compose.yml         # Multi-container orchestration
├── LICENSE
└── README.md
```

## Quick Start

### Prerequisites

- Docker & Docker Compose, or
- Node.js 18+, Python 3.11+, PostgreSQL, Redis (for local development)

### Using Docker Compose (Recommended)

```bash
docker-compose up --build -d
```

Then access the application:

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

### Local Development

**Backend setup:**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements-local.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend setup:**

```bash
cd frontend
npm install
npm run dev
```

**ML environment:**

```bash
cd ml
pip install -r requirements.txt
python preprocess.py
jupyter notebook train_model.ipynb
```

## Configuration

### Environment Variables

Create `.env` files in `backend/` and `frontend/` directories (not tracked by git):

**`backend/.env`:**

```env
DATABASE_URL=postgresql://user:password@localhost:5432/recommender
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key-change-in-production
ENVIRONMENT=development
```

**`frontend/.env.local`:**

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENABLE_ANALYTICS=true
```

### Database Setup

Populate development database with sample data:

```bash
python backend/seed_data.py
```

## API Reference

View interactive API documentation at `/docs` after starting the backend.

**Common endpoints:**

| Method | Endpoint                | Description                          |
| ------ | ----------------------- | ------------------------------------ |
| GET    | `/products/`            | List all products                    |
| GET    | `/products/{id}`        | Get product details                  |
| POST   | `/auth/login`           | Authenticate user (returns JWT)      |
| GET    | `/recommend/{user_id}`  | Get personalized recommendations     |
| POST   | `/track_click`          | Record user interaction              |
| GET    | `/ab-test/results`      | Retrieve A/B test metrics            |

**Example request:**

```bash
curl -X GET "http://localhost:8000/recommend/123"
```

## Testing

**Backend:**

```bash
cd backend
pytest
```

**Frontend:**

```bash
cd frontend
npm test
```

## Development Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make changes and test locally

3. Commit with descriptive messages:
   ```bash
   git commit -m "feat: add new recommendation algorithm"
   ```

4. Push and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

## Docker Commands

**Start services:**

```bash
docker-compose up -d
```

**Stop services:**

```bash
docker-compose down
```

**View logs:**

```bash
docker-compose logs -f [service-name]
```

**Rebuild images:**

```bash
docker-compose build --no-cache
```

## Troubleshooting

| Issue                          | Solution                                        |
| ------------------------------ | ----------------------------------------------- |
| Port already in use            | Change port in `docker-compose.yml` or local service config |
| Database connection failed     | Verify `DATABASE_URL` in `.env` and database is running |
| ML model file not found        | Run `python backend/seed_data.py` to initialize |
| Node modules issues            | Delete `node_modules/` and `package-lock.json`, then `npm install` |
| Python import errors           | Verify virtualenv is activated and packages are installed |

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
