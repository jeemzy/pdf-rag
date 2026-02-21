# n8n with PostgreSQL - Docker Compose Infrastructure

Self-hosted n8n workflow automation with PostgreSQL database backend.

## Quick Start

1. **Copy environment file:**
   ```bash
   cp env.example .env
   ```

2. **Edit `.env` with secure credentials:**
   ```bash
   # Generate encryption key
   openssl rand -hex 32
   ```

3. **Start services:**
   ```bash
   docker compose up -d
   ```

4. **Access n8n:**
   Open http://localhost:5678

## Architecture

```
┌─────────────────────────────────────┐
│         Docker Compose              │
│  ┌─────────┐      ┌──────────────┐  │
│  │   n8n   │─────▶│  PostgreSQL  │  │
│  │  :5678  │      │              │  │
│  └─────────┘      └──────────────┘  │
│       │                  │          │
│       ▼                  ▼          │
│  n8n_storage      n8n_postgres_data │
│   (volume)            (volume)      │
└─────────────────────────────────────┘
```

## Volume Management

### Data Durability

Named volumes persist across:
- `docker compose stop` / `start`
- `docker compose down` / `up`
- Container recreation
- Image updates

**CRITICAL:** Never use `docker compose down -v` in production - the `-v` flag deletes volumes!

### Volume Operations

```bash
# List volumes
docker volume ls | grep n8n

# Inspect volume
docker volume inspect n8n_postgres_data

# Volume location (Linux)
/var/lib/docker/volumes/n8n_postgres_data/_data
```

### Post-Deployment Hardening (Optional)

After initial deployment, you can mark volumes as external to prevent any Compose operation from affecting them:

```yaml
volumes:
  n8n_postgres_data:
    external: true
  n8n_storage:
    external: true
```

## Deployment

### Manual Deployment

```bash
# Pull latest images
docker compose pull

# Recreate containers (volumes preserved)
docker compose up -d

# Check status
docker compose ps
docker compose logs -f
```

### CI/CD via GitHub Actions

Configure these secrets in your GitHub repository:
- `SERVER_HOST` - Server IP or hostname
- `SERVER_USER` - SSH username
- `SERVER_SSH_KEY` - Private SSH key
- `DEPLOY_PATH` - Path to project on server

The workflow triggers on push to `main` branch.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `POSTGRES_USER` | PostgreSQL superuser |
| `POSTGRES_PASSWORD` | PostgreSQL superuser password |
| `POSTGRES_DB` | Database name |
| `POSTGRES_NON_ROOT_USER` | n8n database user (limited privileges) |
| `POSTGRES_NON_ROOT_PASSWORD` | n8n database user password |
| `N8N_ENCRYPTION_KEY` | Encryption key for stored credentials |

### Important: N8N_ENCRYPTION_KEY

This key encrypts all credentials stored in n8n workflows. If lost:
- All stored credentials become unreadable
- Workflows using credentials will fail
- You must re-enter all credentials

**Store this key securely outside the repository.**

## Common Operations

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f n8n
docker compose logs -f postgres
```

### Restart Services

```bash
# Restart all
docker compose restart

# Restart specific service
docker compose restart n8n
```

### Access PostgreSQL

```bash
docker compose exec postgres psql -U postgres -d n8n
```

### Stop Services (Data Preserved)

```bash
docker compose down
```

## Troubleshooting

### n8n won't start

1. Check PostgreSQL is healthy:
   ```bash
   docker compose ps
   docker compose logs postgres
   ```

2. Verify environment variables:
   ```bash
   docker compose config
   ```

### Database connection errors

1. Ensure PostgreSQL is fully initialized:
   ```bash
   docker compose logs postgres | grep "ready to accept connections"
   ```

2. Check credentials match between services

### Permission issues on init-data.sh

```bash
# Make script executable
chmod +x init-data.sh
```

