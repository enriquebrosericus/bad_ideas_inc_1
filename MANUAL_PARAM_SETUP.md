# Manual Parameter Setup for Grafana Dashboard

## Issue: Query Parameters Not Auto-Loading

The `queryParams` setting in the JSON dashboard file doesn't automatically populate in the marcusolsson-json-datasource plugin. You need to manually add parameters in the Grafana UI.

## Fix for "Total Log Files" Gauge

1. **Edit the "Total Log Files" panel**
   - Click panel title → **Edit**

2. **Navigate to Query section**
   - Make sure you're on the **Query** tab
   - Look for the **Params** section

3. **Add two parameters**:

   **First parameter:**
   - Click **Add param**
   - Key: `server`
   - Value: `${server}`

   **Second parameter:**
   - Click **Add param**
   - Key: `logfile`
   - Value: `${logfile}`

4. **Verify Fields section**:
   - Make sure the **Fields** tab shows:
     - JSONPath: `$.total_logs`
     - Type: Number

5. **Apply changes**
   - Click **Apply** button (top-right)

## Fix for "Log Files in Azure Blob Storage" Table

1. **Edit the table panel**
   - Click panel title → **Edit**

2. **Add the same parameters** in the Params section:
   - Key: `server`, Value: `${server}`
   - Key: `logfile`, Value: `${logfile}`

3. **Verify Fields section**:
   - Should have these JSONPath entries:
     - `$[*].server_name`
     - `$[*].log_file_name`
     - `$[*].log_date`
     - `$[*].file_size_mb`
     - `$[*].blob_url`

4. **IMPORTANT - Check Field Names**:
   - Click on each field in the Fields list
   - Make sure the **Name** field is NOT empty
   - If empty, click and add the name:
     - First field → Name: `server_name`
     - Second field → Name: `log_file_name`
     - Third field → Name: `log_date`
     - Fourth field → Name: `file_size_mb`
     - Fifth field → Name: `blob_url`

5. **Apply changes**

## Troubleshooting "Blank Rows When All Selected"

If you see blank rows when "All" is selected:

### Check 1: Field Mapping
- Edit the panel
- Go to Fields/Transformations
- Ensure field names match the JSON response keys exactly

### Check 2: Test the API Directly
```bash
# Test with "All" filter
curl "http://localhost:5001/api/logs?server=\$__all&logfile=\$__all" | jq | head -50

# Should return data with these fields:
# - server_name
# - log_file_name
# - log_date
# - file_size_mb
# - blob_url
```

### Check 3: Verify Query Inspector
1. While in edit mode, click **Query inspector** button (top-right, near Apply)
2. Look at the **Data** tab
3. Check if data is being returned from the API
4. If data exists but table is blank, it's a field mapping issue

### Check 4: Field Name Case Sensitivity
- The JSONPath might be case-sensitive
- Verify field names in the Fields section exactly match the API response:
  - `server_name` (not `Server_Name` or `serverName`)
  - `log_file_name` (not `logFileName`)
  - etc.

## Complete Working Configuration

### Gauge Panel Query:
- **URL Path**: `/api/stats`
- **Method**: GET
- **Params**:
  - `server` = `${server}`
  - `logfile` = `${logfile}`
- **Fields**:
  - JSONPath: `$.total_logs`
  - Name: `Total Logs`
  - Type: Number

### Table Panel Query:
- **URL Path**: `/api/logs`
- **Method**: GET
- **Params**:
  - `server` = `${server}`
  - `logfile` = `${logfile}`
- **Fields**:
  - JSONPath: `$[*].server_name`, Name: `server_name`
  - JSONPath: `$[*].log_file_name`, Name: `log_file_name`
  - JSONPath: `$[*].log_date`, Name: `log_date`
  - JSONPath: `$[*].file_size_mb`, Name: `file_size_mb`
  - JSONPath: `$[*].blob_url`, Name: `blob_url`

## Testing After Setup

1. **Select specific server and log file**:
   - Server: app-server-03
   - Log File: audit.log
   - Should show ~20-30 entries
   - Gauge should show ~20-30

2. **Select "All" for both**:
   - Server: All
   - Log File: All
   - Should show all ~527 entries
   - Gauge should show 527

3. **Mix and match**:
   - Server: All, Log File: error.log
   - Should show error.log from all servers
   - Gauge should show total error.log count (~100-110)

## If Still Showing Blank Rows

Try these steps in order:

1. **Delete and re-add fields**:
   - In Fields section, remove all fields
   - Click **Add field** for each one
   - Carefully type the JSONPath and Name

2. **Check for transformation conflicts**:
   - Look for a **Transform** tab
   - Disable any transformations temporarily
   - See if data appears

3. **Reimport the dashboard**:
   - Save your changes to dashboard settings/variables
   - Delete the entire dashboard
   - Reimport from [log-dashboard-import.json](log-dashboard-import.json)
   - Manually add params again (they won't auto-populate)

4. **Check Grafana logs**:
   ```bash
   docker compose logs grafana | grep -i error
   ```

## Expected Behavior

- **All + All**: Shows all 527 log entries
- **Specific server + All**: Shows all logs from that server
- **All + Specific log file**: Shows that log file from all servers
- **Specific + Specific**: Shows only matching entries

The gauge number should always match the row count in the table.
