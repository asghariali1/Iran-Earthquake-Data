#!/usr/bin/env python3
"""
Quick test and backup system for earthquake data
"""

import json
import os
import shutil
from datetime import datetime

def backup_data():
    """Create a backup of the current data file"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(script_dir, 'data.json')
    
    if os.path.exists(data_file):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(script_dir, f'data_backup_{timestamp}.json')
        shutil.copy2(data_file, backup_file)
        print(f"✅ Backup created: {backup_file}")
        return backup_file
    else:
        print("❌ No data file found to backup")
        return None

def get_data_stats():
    """Get statistics about the current data"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(script_dir, 'data.json')
    
    if not os.path.exists(data_file):
        print("❌ No data file found")
        return
    
    earthquake_count = 0
    years = set()
    magnitudes = []
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    eq_data = json.loads(line)
                    earthquake_count += 1
                    
                    # Extract year
                    if 'time' in eq_data:
                        year = datetime.fromtimestamp(eq_data['time'] / 1000).year
                        years.add(year)
                    
                    # Extract magnitude
                    if 'mag' in eq_data and eq_data['mag'] is not None:
                        magnitudes.append(eq_data['mag'])
        
        if magnitudes:
            avg_mag = sum(magnitudes) / len(magnitudes)
            max_mag = max(magnitudes)
            min_mag = min(magnitudes)
        else:
            avg_mag = max_mag = min_mag = 0
        
        print(f"📊 Dataset Statistics:")
        print(f"   📈 Total earthquakes: {earthquake_count:,}")
        print(f"   📅 Year range: {min(years) if years else 'N/A'} - {max(years) if years else 'N/A'}")
        print(f"   📏 Magnitude range: {min_mag:.1f} - {max_mag:.1f}")
        print(f"   📊 Average magnitude: {avg_mag:.1f}")
        
    except Exception as e:
        print(f"❌ Error reading data: {e}")

if __name__ == '__main__':
    print("🔧 Earthquake Data Management Tool")
    print("=" * 40)
    
    # Show current statistics
    get_data_stats()
    
    print("\n" + "=" * 40)
    
    # Create backup
    backup_file = backup_data()
    
    print(f"\n✅ Data management completed!")
    print(f"💡 To update data, run: python3 update_earthquake_data.py")