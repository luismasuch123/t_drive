"""
Script to convert the Melbourne-GPSLogFormat to the Seattle-GPSLogFormat(standard)
or just converting the utc-time to local-time.

@author: Luis Masuch Ibanez (luismasuchibanez@googlemail.com)
"""

import pandas as pd
import os
from datetime import datetime

def convert_to_standard_format(input_dir, gps_track):
    path = os.path.join(input_dir, gps_track)
    df = pd.read_csv(path,
                     sep=' ',
                     header=None,
                     names=['UTS', 'Latitude', 'Longitude'],
                     skiprows=[0])
    print('Read file ' + gps_track)
    if not df.empty:
        #convert to Date and Time
        for row_index, row in df.iterrows():
            ts = int(row[0])
            df.loc[row_index, 'UTS'] = datetime.utcfromtimestamp(ts).strftime('%d-%b-%Y %H:%M:%S')
        new = df['UTS'].str.split(" ", n=1, expand=True)
        df['Data(UTC)'] = new[0]
        df['Time(UTC)'] = new[1]
        df.drop(columns=['UTS'], inplace=True)
        df = df[['Data(UTC)', 'Time(UTC)', 'Latitude', 'Longitude']]
    return df

to_standard_format = True

input_dir = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/data/Melbourne/GPS_Logs/UTS_format'
output_dir = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/mapmatching/output/Melbourne_Converted_GPS_Logs/standard_format'

files = os.listdir(input_dir)

for gps_track in files:
    if to_standard_format:
        converted_gps_track = convert_to_standard_format(input_dir, gps_track)
        converted_gps_track.to_csv(os.path.join(output_dir, gps_track), index=False, sep=' ')



