#!/usr/bin/env python3
"""
GitHub Actions version of earthquake data updater
This script is optimized for GitHub Actions environment
"""

import json
import requests
import os
from datetime import datetime
import sys

def load_existing_data(json_file_path):
    """Load existing earthquake data from JSON file"""
    existing_data = []
    existing_ids = set()
    
    if os.path.exists(json_file_path):
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        eq_data = json.loads(line)
                        existing_data.append(eq_data)
                        eq_id = eq_data.get('id', f"{eq_data.get('time', '')}_{eq_data.get('latitude', '')}_{eq_data.get('longitude', '')}")
                        existing_ids.add(eq_id)
            print(f"📊 Loaded {len(existing_data)} existing earthquake records")
        except Exception as e:
            print(f"⚠️  Error loading existing data: {e}")
    else:
        print("📂 No existing data file found, will create new one")
    
    return existing_data, existing_ids

def fetch_weekly_usgs_data():
    """Fetch latest weekly earthquake data from USGS"""
    url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson'
    
    try:
        print(f"🌍 Fetching weekly earthquake data from USGS...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Successfully fetched {len(data['features'])} earthquakes from the last week")
        return data['features']
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching USGS data: {e}")
        return None

def convert_usgs_to_format(usgs_feature):
    """Convert USGS GeoJSON feature to our data format"""
    props = usgs_feature['properties']
    geometry = usgs_feature['geometry']
    
    earthquake = {
        'time': props['time'],
        'latitude': geometry['coordinates'][1],
        'longitude': geometry['coordinates'][0],
        'depth': geometry['coordinates'][2] if len(geometry['coordinates']) > 2 else 0,
        'mag': props.get('mag', 0),
        'magType': props.get('magType', ''),
        'nst': props.get('nst'),
        'gap': props.get('gap'),
        'dmin': props.get('dmin'),
        'rms': props.get('rms'),
        'net': props.get('net', 'us'),
        'id': props.get('ids', f"usgs_{props['time']}_{geometry['coordinates'][1]}_{geometry['coordinates'][0]}"),
        'updated': props.get('updated', ''),
        'place': props.get('place', ''),
        'type': props.get('type', 'earthquake'),
        'horizontalError': props.get('horizontalError'),
        'depthError': props.get('depthError'),
        'magError': props.get('magError'),
        'magNst': props.get('magNst'),
        'status': props.get('status', 'automatic'),
        'locationSource': props.get('locationSource', 'us'),
        'magSource': props.get('magSource', 'us')
    }
    
    return earthquake

def is_in_target_region(lat, lon):
    """Check if earthquake is within the target geographic region"""
    # Target region boundaries (Iran area)
    # Latitude: 25.205°N to 40.447°N
    # Longitude: 41.045°E to 63.984°E
    return 25.205 <= lat <= 40.447 and 41.045 <= lon <= 63.984

def update_json_file(json_file_path, existing_data, new_earthquakes):
    """Update the JSON file with new earthquake data"""
    
    print(f"🔄 Merging {len(existing_data)} existing + {len(new_earthquakes)} new earthquakes...")
    
    # Combine all data
    all_data = existing_data + new_earthquakes
    
    # Sort by timestamp (newest first)
    print("🔄 Sorting all earthquakes by timestamp (newest first)...")
    all_data.sort(key=lambda x: x.get('time', 0), reverse=True)
    
    # Debug: Show timestamp range after sorting
    if all_data:
        newest_time = datetime.fromtimestamp(all_data[0]['time'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        oldest_time = datetime.fromtimestamp(all_data[-1]['time'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        print(f"📅 Date range after sorting: {oldest_time} to {newest_time}")
    
    # Write sorted data back to file
    try:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            for earthquake in all_data:
                json.dump(earthquake, f, separators=(',', ':'))
                f.write('\n')
        
        print(f"💾 Successfully updated {json_file_path}")
        print(f"📈 Total earthquakes in dataset: {len(all_data)}")
        print(f"🆕 New earthquakes added: {len(new_earthquakes)}")
        print("✅ All data sorted by timestamp (newest first)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing to file: {e}")
        return False

def main():
    """Main function to update earthquake data for GitHub Actions"""
    json_file_path = 'data.json'  # Use relative path for GitHub Actions
    
    print("🌍 GitHub Actions - Historical Earthquakes Data Updater")
    print("=" * 60)
    print(f"📅 Update time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    
    # Load existing data
    existing_data, existing_ids = load_existing_data(json_file_path)
    
    # Fetch new weekly data
    usgs_features = fetch_weekly_usgs_data()
    if not usgs_features:
        print("❌ Failed to fetch new data, keeping existing dataset")
        return False
    
    # Process new earthquakes with geographic filtering
    new_earthquakes = []
    duplicate_count = 0
    filtered_out_count = 0
    
    for feature in usgs_features:
        earthquake = convert_usgs_to_format(feature)
        earthquake_id = earthquake['id']
        
        # Check if earthquake is in target region
        if not is_in_target_region(earthquake['latitude'], earthquake['longitude']):
            filtered_out_count += 1
            continue
        
        # Check if this earthquake already exists
        if earthquake_id not in existing_ids:
            new_earthquakes.append(earthquake)
            existing_ids.add(earthquake_id)
            print(f"✅ New earthquake in target region: M{earthquake['mag']:.1f} - {earthquake['place']}")
        else:
            duplicate_count += 1
    
    print(f"🔍 Found {len(new_earthquakes)} new earthquakes in target region")
    print(f"🌍 Filtered out {filtered_out_count} earthquakes outside target region")
    print(f"⚠️  Skipped {duplicate_count} duplicates")
    
    # Update the JSON file (always re-sort and save to ensure proper ordering)
    if new_earthquakes:
        success = update_json_file(json_file_path, existing_data, new_earthquakes)
        if success:
            print("🎉 GitHub Actions: Data update completed successfully!")
            # Set output for GitHub Actions
            if 'GITHUB_OUTPUT' in os.environ:
                with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
                    f.write(f"new_earthquakes={len(new_earthquakes)}\n")
            return True
        else:
            print("❌ Failed to update data file")
            return False
    else:
        # Even if no new earthquakes, re-sort existing data to ensure proper order
        print("ℹ️  No new earthquakes to add, but re-sorting existing data...")
        success = update_json_file(json_file_path, existing_data, [])
        if success:
            print("✅ Existing data re-sorted successfully!")
            return True
        else:
            print("❌ Failed to re-sort existing data")
            return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)