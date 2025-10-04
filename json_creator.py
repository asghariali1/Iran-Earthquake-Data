#get the script directory
import os
script_dir = os.path.dirname(os.path.abspath(__file__))

#import the csv file
data_file_path = os.path.join(script_dir, 'data.csv')
import pandas as pd
data = pd.read_csv(data_file_path)
data['time'] = pd.to_datetime(data['time'])
data = data.sort_values(by='time', ascending=False)
data = data.reset_index(drop=True)

#save file as json in the same directory as the script
output_file_path = os.path.join(script_dir, 'data.json')
data.to_json(output_file_path, orient='records', lines=True)