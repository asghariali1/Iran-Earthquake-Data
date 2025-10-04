#!/usr/bin/env python3
"""
Sort earthquake data by timestamp
This script ensures the JSON file is properly sorted by timestamp (newest first)
"""

import json
import os
from datetime import datetime

def sort_earthquake_data():
    """Sort the earthquake JSON file by timestamp"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(script_dir, 'data.json')
    
    if not os.path.exists(json_file_path):
        print("❌ No data.json file found")
        return False
    
    print("🔄 Loading earthquake data...")
    earthquakes = []
    
    try:
        # Load all earthquake data
        with open(json_file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line:
                    try:
                        eq_data = json.loads(line)
                        earthquakes.append(eq_data)
                    except json.JSONDecodeError as e:
                        print(f"⚠️  Skipping invalid JSON on line {line_num}: {e}")
        
        print(f"📊 Loaded {len(earthquakes)} earthquakes")
        
        if not earthquakes:
            print("❌ No valid earthquake data found")
            return False
        
        # Check current order
        print("🔍 Checking current sort order...")
        is_sorted = True
        for i in range(len(earthquakes) - 1):
            if earthquakes[i].get('time', 0) < earthquakes[i + 1].get('time', 0):
                is_sorted = False
                break
        
        if is_sorted:
            print("✅ Data is already sorted correctly (newest first)")
        else:
            print("🔄 Sorting earthquakes by timestamp (newest first)...")
            earthquakes.sort(key=lambda x: x.get('time', 0), reverse=True)
        
        # Show timestamp range
        if earthquakes:
            newest_time = datetime.fromtimestamp(earthquakes[0]['time'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            oldest_time = datetime.fromtimestamp(earthquakes[-1]['time'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            print(f"📅 Date range: {oldest_time} to {newest_time}")
        
        # Write sorted data back
        print("💾 Saving sorted data...")
        with open(json_file_path, 'w', encoding='utf-8') as f:
            for earthquake in earthquakes:
                json.dump(earthquake, f, separators=(',', ':'))
                f.write('\n')
        
        print("✅ Earthquake data sorted and saved successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error processing earthquake data: {e}")
        return False

if __name__ == '__main__':
    print("🔧 Earthquake Data Sorter")
    print("=" * 30)
    
    success = sort_earthquake_data()
    
    if success:
        print("\n🎉 Sorting completed successfully!")
    else:
        print("\n❌ Sorting failed!")