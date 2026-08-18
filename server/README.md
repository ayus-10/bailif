# PostgreSQL + pgvector Quick Setup

## 1. Start the container

```bash
podman run --name pg-dev --replace \
  -e POSTGRES_USER=aayush \
  -e POSTGRES_PASSWORD=1234 \
  -e POSTGRES_DB=local \
  -p 5432:5432 \
  -v pg-dev-data:/var/lib/postgresql/data \
  -d docker.io/pgvector/pgvector:pg16
```

## 2. Enable the vector extension

```bash
podman exec -it pg-dev psql -U aayush -d local -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

## 3. Connect interactively

```bash
podman exec -it pg-dev psql -U aayush -d local
```
