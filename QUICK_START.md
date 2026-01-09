# Quick Start Guide

## Start the System

```bash
docker compose up -d --build
```

## Access Points

- **Main Dashboard**: http://localhost:5001
- **Grafana**: http://localhost:3000 (admin/admin)
- **API Health**: http://localhost:5001/health

## Sample API Calls

```bash
# Get statistics
curl http://localhost:5001/api/stats | jq

# List all servers
curl http://localhost:5001/api/servers | jq

# Search logs for specific server
curl "http://localhost:5001/api/logs?server=app-server-01" | jq

# Search error logs
curl "http://localhost:5001/api/logs?logfile=error.log" | jq

# Search with date range
curl "http://localhost:5001/api/logs?from_date=2026-01-01&to_date=2026-01-08" | jq
```

## Stop the System

```bash
# Stop containers
docker compose down

# Stop and reset database
docker compose down -v
```

## What's Running?

Check status:
```bash
docker compose ps
```

View logs:
```bash
docker compose logs -f
docker compose logs log-metadata-api
docker compose logs grafana
```

## Mock Data

- **517 log entries** across 30 days
- **5 servers**: app-server-01, app-server-02, app-server-03, web-server-01, api-server-01
- **5 log types**: application.log, error.log, access.log, debug.log, audit.log
- **Mock blob URLs**: https://logstorageaccount.blob.core.windows.net/logs/...

## Project Structure

```
api/
  ├── app.py              # Flask API
  ├── init_db.py          # Database setup
  └── static/
      └── index.html      # Web dashboard

grafana/
  ├── provisioning/       # Auto-config
  └── dashboards/         # Dashboard JSON

docker-compose.yml        # Container orchestration
```

## Next Steps

1. Open http://localhost:5001 in your browser
2. Use the filters to search for logs
3. Click on blob URLs to see the mock Azure Blob Storage links
4. Explore the Grafana dashboard at http://localhost:3000
