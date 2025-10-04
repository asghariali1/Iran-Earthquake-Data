#!/usr/bin/env python3
"""
Simple HTTP server for the Historical Earthquakes website
"""

import http.server
import socketserver
import os
import webbrowser
import subprocess
import sys
from threading import Timer
from datetime import datetime

def update_earthquake_data():
    """Update earthquake data with latest weekly data from USGS"""
    try:
        print(f"🔄 Updating earthquake data... ({datetime.now().strftime('%H:%M:%S')})")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        update_script = os.path.join(script_dir, 'update_earthquake_data.py')
        
        # Use the same Python executable that's running this script
        result = subprocess.run([sys.executable, update_script], 
                              capture_output=True, text=True, cwd=script_dir)
        
        if result.returncode == 0:
            print("✅ Earthquake data updated successfully")
        else:
            print("⚠️  Data update completed with warnings")
            
        # Print any output for debugging
        if result.stdout:
            print("Update output:", result.stdout.strip())
        if result.stderr:
            print("Update errors:", result.stderr.strip())
            
    except Exception as e:
        print(f"❌ Error updating earthquake data: {e}")

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler that updates data on first request"""
    
    _data_updated = False
    
    def do_GET(self):
        # Update data on first request or when explicitly requested
        if not CustomHTTPRequestHandler._data_updated or self.path == '/update-data':
            update_earthquake_data()
            CustomHTTPRequestHandler._data_updated = True
            
            # If it was an update request, redirect to home
            if self.path == '/update-data':
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
                return
        
        # Handle normal requests
        super().do_GET()

def open_browser():
    """Open the website in the default browser after a short delay"""
    webbrowser.open('http://localhost:8000')

if __name__ == "__main__":
    # Change to the directory containing the HTML files
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    PORT = 8000
    
    # Create a simple HTTP server with custom handler
    Handler = CustomHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🌍 Historical Earthquakes Website Server")
        print(f"📡 Server running at: http://localhost:{PORT}")
        print(f"📂 Serving files from: {os.getcwd()}")
        print(f"🚀 Opening browser automatically...")
        print(f"⏹️  Press Ctrl+C to stop the server")
        
        # Open browser after 2 seconds
        Timer(2.0, open_browser).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n🛑 Server stopped by user")
            httpd.shutdown()