#!/bin/bash

echo "🚀 Starting Azure Blob Storage Log Retrieval Mock-up..."
echo ""
echo "Building and starting containers..."
docker compose up -d --build

echo ""
echo "Waiting for services to start..."
sleep 5

echo ""
echo "✅ Services started!"
echo ""
echo "📊 Access the dashboards at:"
echo "   • Main Dashboard:    http://localhost:5001"
echo "   • Grafana Dashboard: http://localhost:3000 (admin/admin)"
echo ""
echo "📖 API Documentation:"
echo "   • Health Check:  http://localhost:5001/health"
echo "   • Statistics:    http://localhost:5001/api/stats"
echo "   • Servers:       http://localhost:5001/api/servers"
echo "   • Log Files:     http://localhost:5001/api/logfiles"
echo ""
echo "🛑 To stop: docker compose down"
echo "🗑️  To reset: docker compose down -v"
echo ""
