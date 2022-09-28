"""
Script to convert the PortoGPSLogFormat to the UTSGPSLogFormat.

@author: Luis Masuch Ibanez (luismasuchibanez@googlemail.com)
"""

import pandas as pd
import os

def convert_to_uts_format(input_dir, output_dir):
    for i in range(0, 9):
        # path = os.path.join(input_dir, str(file))
        path = os.path.join(input_dir, "trip_" + str(i) + '.txt')
        # 295.txt ist in originalen Logs leer, weshalb die Datei im standard_format nicht existiert
        if os.path.exists(path):
            df = pd.read_csv(path,
                             sep=',',
                             header=None,
                             names=['A', 'Latitude', 'Longitude', 'UTS', 'B', 'C'],
                             skiprows=[0])
            print('Convert file ' + str(i) + '.txt')
            df = df[['UTS', 'Latitude', 'Longitude']]
            df.to_csv(os.path.join(output_dir, str(i) + '.txt'), index=False, sep=' ')

input_dir = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/data/Porto/trips'
output_dir = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/mapmatching/output/Porto_Converted_GPS_Logs/uts_format'
convert_to_uts_format(input_dir, output_dir)


