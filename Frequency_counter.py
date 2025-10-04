#get the scrript directory
import os
script_dir = os.path.dirname(os.path.abspath(__file__))

#import the data from the data directory
data_file_path = os.path.join(script_dir, 'data.json')

#read the json file
import pandas as pd
data = pd.read_json(data_file_path, lines=True)

#get the lowest date
min_date = data['time'].min()
#get the highest date
max_date = data['time'].max()

print(f"Data ranges from {min_date} to {max_date}")

#convert time column from Unix timestamp (milliseconds) to datetime and extract date
data['time'] = pd.to_datetime(data['time'], unit='ms')
data['date'] = data['time'].dt.date
data['time_only'] = data['time'].dt.time

print(data.head())

#count the frequency of each date
date_counts = data['date'].value_counts().sort_index()

#save the frequency counts to a new csv file in the same directory as the script
output_file_path = os.path.join(script_dir, 'date_frequency_counts_all.csv')
date_counts.to_csv(output_file_path, header=['count'])

#count the frequency for those only with mag >= 5
data_mag_5 = data[data['mag'] >= 5]
date_counts_mag_5 = data_mag_5['date'].value_counts().sort_index()

#save the frequency counts to a new csv file in the same directory as the script
output_file_path_mag_5 = os.path.join(script_dir, 'date_frequency_counts_mag_5.csv')
date_counts_mag_5.to_csv(output_file_path_mag_5, header=['count'])

# count the frequency for those only with mag >= 3
data_mag_3 = data[data['mag'] >= 3]
date_counts_mag_3 = data_mag_3['date'].value_counts().sort_index()

#save the frequency counts to a new csv file in the same directory as the script
output_file_path_mag_3 = os.path.join(script_dir, 'date_frequency_counts_mag_3.csv')
date_counts_mag_3.to_csv(output_file_path_mag_3, header=['count'])

#plot the time series of the frequency counts
import matplotlib.pyplot as plt 
plt.figure(figsize=(12, 6))
plt.plot(date_counts.index, date_counts.values, label='All Magnitudes', color='blue')
plt.plot(date_counts_mag_5.index, date_counts_mag_5.values, label='Magnitude >= 5', color='red')
plt.plot(date_counts_mag_3.index, date_counts_mag_3.values, label='Magnitude >= 3', color='green')
plt.xlabel('Date')
plt.ylabel('Frequency Count')
plt.title('Daily Frequency Counts of Events')
plt.legend()
plt.grid()
#save the plot to the same directory as the script
output_plot_path = os.path.join(script_dir, 'date_frequency_counts.png')
plt.savefig(output_plot_path)

#make a json file of the main data 
import json
data_json_path = os.path.join(script_dir, 'data.json')
data.to_json(data_json_path, orient='records', lines=True)