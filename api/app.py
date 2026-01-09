from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')
CORS(app)

def get_db():
    conn = sqlite3.connect('logs.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "log-metadata-api"})

@app.route('/search', methods=['POST'])
def search():
    """Grafana Simple JSON datasource search endpoint"""
    return jsonify([
        {"text": "Servers", "value": "servers"},
        {"text": "Log Files", "value": "logfiles"}
    ])

@app.route('/query', methods=['POST'])
def query():
    """Grafana Simple JSON datasource query endpoint"""
    data = request.get_json()
    targets = data.get('targets', [])
    time_range = data.get('range', {})

    results = []

    for target in targets:
        target_type = target.get('target')

        if target_type == 'servers':
            # Return list of servers
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT server_name FROM log_metadata ORDER BY server_name')
            servers = [row['server_name'] for row in cursor.fetchall()]
            conn.close()

            results.append({
                "target": "servers",
                "datapoints": [[len(servers), datetime.now().timestamp() * 1000]],
                "servers": servers
            })

    return jsonify(results)

@app.route('/api/servers', methods=['GET'])
def get_servers():
    """Get list of all servers"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT server_name FROM log_metadata ORDER BY server_name')
    servers = [row['server_name'] for row in cursor.fetchall()]
    conn.close()
    return jsonify(servers)

@app.route('/api/logfiles', methods=['GET'])
def get_logfiles():
    """Get list of log files, optionally filtered by server"""
    server = request.args.get('server')

    conn = get_db()
    cursor = conn.cursor()

    if server:
        cursor.execute(
            'SELECT DISTINCT log_file_name FROM log_metadata WHERE server_name = ? ORDER BY log_file_name',
            (server,)
        )
    else:
        cursor.execute('SELECT DISTINCT log_file_name FROM log_metadata ORDER BY log_file_name')

    logfiles = [row['log_file_name'] for row in cursor.fetchall()]
    conn.close()
    return jsonify(logfiles)

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get log metadata with optional filters"""
    server = request.args.get('server')
    logfile = request.args.get('logfile')
    date = request.args.get('date')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    # Handle Grafana's $__all variable
    if server == '$__all':
        server = None
    if logfile == '$__all':
        logfile = None

    # Handle Grafana's multi-value format: {value1,value2,value3}
    if server and server.startswith('{') and server.endswith('}'):
        server = None  # Treat multi-select "All" as no filter
    if logfile and logfile.startswith('{') and logfile.endswith('}'):
        logfile = None  # Treat multi-select "All" as no filter

    conn = get_db()
    cursor = conn.cursor()

    query = 'SELECT * FROM log_metadata WHERE 1=1'
    params = []

    if server:
        query += ' AND server_name = ?'
        params.append(server)

    if logfile:
        query += ' AND log_file_name = ?'
        params.append(logfile)

    if date:
        query += ' AND log_date = ?'
        params.append(date)

    if from_date:
        query += ' AND log_date >= ?'
        params.append(from_date)

    if to_date:
        query += ' AND log_date <= ?'
        params.append(to_date)

    query += ' ORDER BY log_date DESC, server_name, log_file_name'

    cursor.execute(query, params)
    rows = cursor.fetchall()

    logs = []
    for row in rows:
        logs.append({
            'id': row['id'],
            'server_name': row['server_name'],
            'log_file_name': row['log_file_name'],
            'log_date': row['log_date'],
            'blob_url': row['blob_url'],
            'file_size_mb': row['file_size_mb'],
            'created_at': row['created_at']
        })

    conn.close()
    return jsonify(logs)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics about logs"""
    server = request.args.get('server')
    logfile = request.args.get('logfile')

    # Handle Grafana's $__all variable
    if server == '$__all':
        server = None
    if logfile == '$__all':
        logfile = None

    # Handle Grafana's multi-value format: {value1,value2,value3}
    if server and server.startswith('{') and server.endswith('}'):
        server = None  # Treat multi-select "All" as no filter
    if logfile and logfile.startswith('{') and logfile.endswith('}'):
        logfile = None  # Treat multi-select "All" as no filter

    conn = get_db()
    cursor = conn.cursor()

    # Build count query with filters
    count_query = 'SELECT COUNT(*) as total FROM log_metadata WHERE 1=1'
    params = []

    if server:
        count_query += ' AND server_name = ?'
        params.append(server)

    if logfile:
        count_query += ' AND log_file_name = ?'
        params.append(logfile)

    cursor.execute(count_query, params)
    total = cursor.fetchone()['total']

    cursor.execute('SELECT COUNT(DISTINCT server_name) as server_count FROM log_metadata')
    server_count = cursor.fetchone()['server_count']

    cursor.execute('SELECT COUNT(DISTINCT log_file_name) as logfile_count FROM log_metadata')
    logfile_count = cursor.fetchone()['logfile_count']

    cursor.execute('SELECT MIN(log_date) as earliest, MAX(log_date) as latest FROM log_metadata')
    date_range = cursor.fetchone()

    conn.close()

    return jsonify({
        'total_logs': total,
        'server_count': server_count,
        'logfile_count': logfile_count,
        'earliest_date': date_range['earliest'],
        'latest_date': date_range['latest']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
