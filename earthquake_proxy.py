#!/usr/bin/env python3
"""
Simple CORS proxy server for USGS earthquake data
This server fetches earthquake data and serves it with CORS headers enabled
"""

from flask import Flask, jsonify, Response
import requests
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/earthquake-data')
def get_earthquake_data():
    """
    Fetch earthquake data from USGS and return with CORS headers
    """
    try:
        # USGS daily earthquake feed
        usgs_url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson'
        
        print(f"Fetching data from: {usgs_url}")
        
        # Fetch data from USGS
        response = requests.get(usgs_url, timeout=30)
        response.raise_for_status()
        
        # Return the JSON data with CORS headers
        return Response(
            response.content,
            mimetype='application/json',
            headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Cache-Control': 'no-cache'
            }
        )
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching earthquake data: {e}")
        return jsonify({
            'error': 'Failed to fetch earthquake data',
            'message': str(e)
        }), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'USGS Earthquake Proxy'
    })

if __name__ == '__main__':
    print("🌍 Starting USGS Earthquake Proxy Server")
    print("📡 Proxy will be available at: http://localhost:5001/earthquake-data")
    print("🔍 Health check at: http://localhost:5001/health")
    print("⏹️  Press Ctrl+C to stop")
    
    app.run(debug=False, host='0.0.0.0', port=5001)