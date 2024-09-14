# KamiBOT
Bot for Kami that will help teach students.

### Installing:
```
poetry install --no-root
```
```
pre-commit install
```
```
cp .env-example .env
```

### Run checkers:
```
poetry run ruff check --fix .
```
```
poetry run mypy .
```
```
pre-commit run --all-files
```

### Create migration:
```
poetry run alembic revision --autogenerate -m 'migration name'
```

### Run migrations:
```
poetry run alembic upgrade head
```

### Run in Docker:
```
docker compose up --build -d
```

### Run locally:
```
poetry run python -m kami
```

#### © Eugene Denkevich, 2024.
