# Grafana Manual Setup Guide

## Step 1: Access Grafana

1. Open your browser and go to: **http://localhost:3000**
2. Login with:
   - Username: `admin`
   - Password: `admin`
3. Skip changing the password (or change it if you want)

## Step 2: Add the JSON API Datasource

1. Click the **menu icon** (☰) in the top-left corner
2. Go to **Connections** → **Data sources**
3. Click **"Add data source"** button
4. Search for **"JSON API"** (it should show "JSON API" by Marcus Olsson)
5. Click on **"JSON API"**

## Step 3: Configure the Datasource

Fill in the following settings:

### Basic Settings:
- **Name**: `Log Metadata API`
- **URL**: `http://log-metadata-api:5000`
  - ⚠️ Use `log-metadata-api` (container name), NOT `localhost`
  - This is the internal Docker network hostname

### HTTP Settings:
- **Access**: Leave as **"Server (default)"**

### Custom HTTP Headers: (Optional - not needed for this demo)
- Leave empty

### Authentication: (Optional - not needed)
- Leave as **"No Auth"**

### Additional JSON Data settings:
- You can leave these as default

## Step 4: Test the Connection

1. Scroll to the bottom
2. Click **"Save & test"**
3. You should see: ✅ **"Data source is working"**

## Step 5: Import the Dashboard

### Option A: Manual Import (Recommended)

1. Click the menu icon (☰) → **Dashboards**
2. Click **"New"** → **"Import"**
3. Click **"Upload JSON file"**
4. Select the file: `/Users/edawg/gitsome/bad_ideas_inc_1/grafana/dashboards/log-retrieval-working.json`
5. Click **"Import"**

The dashboard should now load with data!

### Option B: If Dashboard Auto-Loaded But Shows "No Data"

If the dashboard already appears (from provisioning) but shows no data:

1. Go to the dashboard
2. Click the **gear icon** (⚙️) in the top-right to edit dashboard settings
3. Go to **Variables** (if any) and update datasource references
4. Or edit each panel:
   - Click the panel title → **Edit**
   - Change the datasource to **"Log Metadata API"**
   - Click **Apply**

## Step 6: Verify the Dashboard

You should now see:

### Panel 1: Dashboard Information
- Text panel explaining the dashboard

### Panel 2: Total Log Files (Gauge)
- Shows ~500+ logs

### Panel 3: Servers Monitored (Stat)
- Shows 5 servers

### Panel 4: Log File Types (Stat)
- Shows 5 log types

### Panel 5: Available Servers (Table)
- Lists all server names

### Panel 6: Log Files in Azure Blob Storage (Table)
- Shows recent log files with:
  - Server name
  - Log file name
  - Date
  - File size
  - Clickable blob URLs

## Troubleshooting

### "Data source not found" error
- Make sure you completed Step 2-4 to add the datasource manually
- The datasource name must be exactly: `Log Metadata API`

### "Cannot connect" error
- Verify the API is running: `docker compose ps`
- Check the URL is: `http://log-metadata-api:5000` (NOT localhost)

### Dashboard shows no data
- Click on a panel → Edit
- Verify the datasource is set to "Log Metadata API"
- Check the URL path is correct (e.g., `/api/stats`, `/api/servers`, `/api/logs`)

### Plugin not found
- The plugin should auto-install on startup
- Verify it's installed: Go to Connections → Plugins → search for "JSON API"
- If not installed, check Docker logs: `docker compose logs grafana | grep json`

## Testing the API Endpoints Directly

Before setting up Grafana, you can test the API:

```bash
# Test stats endpoint
curl http://localhost:5001/api/stats | jq

# Test servers endpoint
curl http://localhost:5001/api/servers | jq

# Test logs endpoint
curl http://localhost:5001/api/logs | jq | head -50
```

All should return JSON data.

## Quick Reset

If something goes wrong:

```bash
# Stop everything and reset Grafana storage
docker compose down -v

# Start fresh
docker compose up -d

# Wait 15 seconds for startup
sleep 15

# Access Grafana and follow steps above
open http://localhost:3000
```

## Panel Configuration Details

If you need to recreate panels manually, here are the settings:

### Total Log Files Panel:
- Type: Gauge
- Query: GET `/api/stats`
- JSON Path: `$.total_logs`

### Servers Monitored Panel:
- Type: Stat
- Query: GET `/api/stats`
- JSON Path: `$.server_count`

### Log File Types Panel:
- Type: Stat
- Query: GET `/api/stats`
- JSON Path: `$.logfile_count`

### Available Servers Panel:
- Type: Table
- Query: GET `/api/servers`
- JSON Path: `$[*]`

### Log Files Table:
- Type: Table
- Query: GET `/api/logs`
- JSON Paths:
  - `$[*].server_name`
  - `$[*].log_file_name`
  - `$[*].log_date`
  - `$[*].file_size_mb`
  - `$[*].blob_url`

## Success!

Once configured, your Grafana dashboard will display all the log metadata and provide clickable links to the blob storage URLs, exactly as stakeholders requested! 🎉
