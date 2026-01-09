import sqlite3
from datetime import datetime, timedelta
import random

# Create database and populate with mock data
conn = sqlite3.connect('logs.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS log_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    server_name TEXT NOT NULL,
    log_file_name TEXT NOT NULL,
    log_date DATE NOT NULL,
    blob_url TEXT NOT NULL,
    file_size_mb REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Clear existing data
cursor.execute('DELETE FROM log_metadata')

# Mock servers and log types
servers = ['app-server-01', 'app-server-02', 'app-server-03', 'web-server-01', 'api-server-01']
log_types = ['application.log', 'error.log', 'access.log', 'debug.log', 'audit.log']

# Generate mock data for the last 30 days
base_date = datetime.now() - timedelta(days=30)

print("Generating mock log metadata...")
for day_offset in range(30):
    current_date = base_date + timedelta(days=day_offset)
    date_str = current_date.strftime('%Y-%m-%d')

    for server in servers:
        for log_type in log_types:
            # Not every server has every log every day
            if random.random() > 0.3:  # 70% chance of having the log
                file_size = round(random.uniform(10, 500), 2)
                blob_url = f"https://logstorageaccount.blob.core.windows.net/logs/{server}/{date_str}/{log_type}"

                cursor.execute('''
                    INSERT INTO log_metadata (server_name, log_file_name, log_date, blob_url, file_size_mb)
                    VALUES (?, ?, ?, ?, ?)
                ''', (server, log_type, date_str, blob_url, file_size))

conn.commit()

# Print summary
cursor.execute('SELECT COUNT(*) FROM log_metadata')
count = cursor.fetchone()[0]
print(f"Created {count} log metadata entries")

cursor.execute('SELECT DISTINCT server_name FROM log_metadata')
servers = cursor.fetchall()
print(f"Servers: {[s[0] for s in servers]}")

conn.close()
print("Database initialization complete!")
