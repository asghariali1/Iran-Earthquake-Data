#!/bin/bash

echo "🌍 Historical Earthquakes Data Explorer with Real-time Monitoring"
echo "=============================================================="
echo ""

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $PROXY_PID $WEBSITE_PID 2>/dev/null
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Make sure we're in the right directory
cd "$(dirname "$0")"

echo "🚀 Starting earthquake proxy server on port 5001..."
"/home/ali/Desktop/Kalak/cloned/Historical Earthquakes/.venv/bin/python" earthquake_proxy.py &
PROXY_PID=$!

# Wait a moment for proxy to start
sleep 2

echo "🌐 Starting main website server on port 8000..."
python3 server.py &
WEBSITE_PID=$!

echo ""
echo "✅ Both servers are running:"
echo "   📡 Earthquake Proxy: http://localhost:5001/earthquake-data"
echo "   🌍 Main Website: http://localhost:8000"
echo ""
echo "⏹️  Press Ctrl+C to stop both servers"
echo ""

# Wait for background processes
wait