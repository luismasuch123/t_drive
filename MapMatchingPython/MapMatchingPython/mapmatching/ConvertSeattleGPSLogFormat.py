"""
Script to convert the SeattleGPSLogFormat to the UTSGPSLogFormat.

@author: Luis Masuch Ibanez (luismasuchibanez@googlemail.com)
"""

import pandas as pd
import os

def convert_to_uts_format(input_dir, output_dir):
    path = input_dir
    if os.path.exists(path):
        df = pd.read_csv(path,
                         sep=' ',
                         header=None,
                         names=['DateTime(UTC)', 'Latitude', 'Longitude'],
                         skiprows=[0])
        print('Convert file gps_track.txt')
        print("DateTime(UTC): " + str(df['DateTime(UTC)']))
        print("Latitude: " + str(df['Latitude']))
        print("Longitude: " + str(df['Longitude']))
        if not df.empty:
            # convert Data(UTC) and Time(UTC) to UTS
            #df['UTS'] = df['DateTime(UTC)'].replace("\t", " ")
            df['UTS'] = df['DateTime(UTC)']
            print("UTS: " + str(df['UTS']))
            df.drop(columns=['DateTime(UTC)'], inplace=True)
            df = df[['UTS', 'Latitude', 'Longitude']]
            for row_index, row in df.iterrows():
                ts = row[0]
                df.loc[row_index, 'UTS'] = int(pd.Timestamp(ts).timestamp())
            df.to_csv(os.path.join(output_dir, 'gps_track.txt'), index=False, sep=' ')
            # print(df)

to_uts_format = True

input_dir = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/data/Seattle/gps_data_test.txt'
output_dir = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/mapmatching/output/Seattle_Converted_GPS_Logs/uts_format'
convert_to_uts_format(input_dir, output_dir)


