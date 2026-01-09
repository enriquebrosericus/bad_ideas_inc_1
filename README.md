# Azure Blob Storage Log Retrieval System - Mock-up

This is a mock-up implementation of a log retrieval system designed to handle log files that exceed the Azure Log Analytics Workspace (LAW) 64KB line limit.

## The Problem

Your Azure-hosted applications generate logs processed by Log Analytics Workspace. When individual log lines exceed 64KB, they get truncated, losing critical data.

## The Proposed Solution

1. Use Azure CLI to sync log files to Azure Blob Storage
2. Store metadata about these logs in a searchable format
3. Provide a Grafana-like dashboard where developers can:
   - Select a server
   - Select a log file name
   - Select a date range
   - Retrieve download links to the actual log files in Blob Storage

## This Mock-up Implementation

This project provides a working demonstration with:

- **Flask API**: Mock backend serving log metadata from SQLite database
- **Interactive Web Dashboard**: Beautiful UI for searching and retrieving log files
- **Grafana Integration**: Provisioned Grafana instance with dashboard (optional)
- **Docker Compose**: Everything runs in containers

## Architecture

```
┌─────────────────┐
│   Web Browser   │
│  (Dashboard)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│   Flask API     │◄────►│  SQLite DB       │
│  (Port 5000)    │      │  (Log Metadata)  │
└─────────────────┘      └──────────────────┘
         │
         ▼
┌─────────────────┐
│    Grafana      │
│  (Port 3000)    │
└─────────────────┘
```

## Quick Start

### Prerequisites

- Docker Desktop running
- Ports 3000 and 5001 available

### Start the System

```bash
# Start all services
docker compose up --build

# Or run in background
docker compose up -d --build
```

### Access the Dashboards

**Primary Dashboard (Recommended):**
- URL: http://localhost:5001
- This is the main interactive dashboard with full functionality

**Grafana Dashboard (Alternative):**
- URL: http://localhost:3000
- Username: `admin`
- Password: `admin`
- Navigate to Dashboards → Azure Blob Storage Log Retrieval

## Features

### Web Dashboard (http://localhost:5001)

The main dashboard provides:

1. **Statistics Overview**
   - Total log files available
   - Number of servers
   - Number of log types
   - Date range coverage

2. **Search Filters**
   - Server name dropdown
   - Log file type dropdown
   - Date range picker (from/to dates)
   - Search and reset buttons

3. **Results Table**
   - Sortable columns
   - Clickable blob storage URLs
   - Copy-to-clipboard functionality
   - File size information

### API Endpoints

The Flask API provides the following endpoints:

- `GET /api/stats` - Get statistics about available logs
- `GET /api/servers` - List all servers
- `GET /api/logfiles` - List all log file types
- `GET /api/logs` - Search logs with filters
  - Query params: `server`, `logfile`, `date`, `from_date`, `to_date`

Example:
```bash
# Get all logs for app-server-01
curl "http://localhost:5001/api/logs?server=app-server-01"

# Get error logs from a specific date
curl "http://localhost:5001/api/logs?logfile=error.log&date=2025-12-15"

# Get logs in a date range
curl "http://localhost:5001/api/logs?from_date=2025-12-01&to_date=2025-12-31"
```

## Mock Data

The system generates mock data on startup:

- **Servers**: 5 mock servers (app-server-01, app-server-02, app-server-03, web-server-01, api-server-01)
- **Log Types**: application.log, error.log, access.log, debug.log, audit.log
- **Date Range**: Last 30 days
- **Blob URLs**: Mock Azure Blob Storage URLs in the format:
  ```
  https://logstorageaccount.blob.core.windows.net/logs/{server}/{date}/{logfile}
  ```

## Project Structure

```
.
├── docker-compose.yml          # Docker orchestration
├── api/                        # Flask API service
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py                  # Main Flask application
│   ├── init_db.py              # Database initialization script
│   └── static/
│       └── index.html          # Web dashboard
├── grafana/                    # Grafana configuration
│   ├── provisioning/
│   │   ├── datasources/        # Auto-provisioned data sources
│   │   └── dashboards/         # Auto-provisioned dashboards
│   └── dashboards/
│       └── log-retrieval-dashboard.json
└── README.md
```

## How to Use (Developer Workflow)

1. **Start the system**: `docker compose up -d --build`
2. **Open the dashboard**: Navigate to http://localhost:5001
3. **Search for logs**:
   - Select a server (or leave as "All Servers")
   - Select a log file type (or leave as "All Log Files")
   - Choose a date range
   - Click "Search Logs"
4. **Retrieve log files**:
   - Click on blob storage URLs in the results table
   - Or use the "Copy" button to copy URLs to clipboard
5. **In production**: These URLs would link to actual files in Azure Blob Storage

## Stopping the System

```bash
# Stop all services
docker compose down

# Stop and remove volumes (reset database)
docker compose down -v
```

## Customization

### Modify Mock Data

Edit [api/init_db.py](api/init_db.py) to change:
- Server names
- Log file types
- Date ranges
- Blob storage URL patterns

### Modify the Dashboard

Edit [api/static/index.html](api/static/index.html) to customize the UI.

### Add Real Data

To connect to real data:
1. Replace SQLite with your actual database
2. Update API endpoints to query your real data source
3. Update blob URLs to point to actual Azure Blob Storage

## Converting to Production

To implement this for real:

1. **Azure CLI Sync**: Create a scheduled job to sync logs to Blob Storage
   ```bash
   az storage blob upload-batch \
     --destination logs \
     --source /var/log/apps \
     --account-name logstorageaccount
   ```

2. **Metadata Collection**: Parse uploaded files and store metadata in:
   - Azure SQL Database
   - Cosmos DB
   - Or continue using Log Analytics for metadata only

3. **Authentication**: Add Azure AD authentication to both API and dashboard

4. **SAS Tokens**: Generate short-lived SAS tokens for blob URLs instead of public URLs

5. **Deploy**: Host the API in Azure App Service or Container Apps

## Notes

- This is a **mock-up** - blob URLs are fake and won't download anything
- In production, you'd want authentication, SAS tokens, and real blob storage
- The Grafana integration is basic - the custom HTML dashboard is more functional
- Database is reset every time containers are rebuilt

## Why This Might Actually Work

This approach:
- ✅ Solves the 64KB truncation problem
- ✅ Keeps logs accessible long-term
- ✅ Provides familiar interface for developers
- ✅ Leverages existing Azure infrastructure
- ✅ Could integrate with existing monitoring tools

The main challenges:
- 🔧 Sync reliability and timing
- 🔧 Storage costs for large log volumes
- 🔧 Search performance at scale (metadata only, not full-text)
- 🔧 Access control and security

## License

This is a mock-up demonstration project. Use at your own discretion.
