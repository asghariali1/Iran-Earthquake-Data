#!/bin/bash

echo "🌍 Historical Earthquakes Data Explorer"
echo "======================================"
echo ""
echo "Starting the web server..."
echo ""

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Start the Python server
python3 server.py