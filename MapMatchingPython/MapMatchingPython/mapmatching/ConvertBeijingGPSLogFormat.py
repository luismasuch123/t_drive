"""
Script to convert the BeijingGPSLogFormat to the UTSGPSLogFormat or StandardGPSLogFormat
by deleting the first column and changing the datetime-format.

@author: Luis Masuch Ibanez (luismasuchibanez@googlemail.com)
"""

import pandas as pd
import os

def convert_to_standard_format(input_dir, output_dir):
    files = os.listdir(input_dir)

    # for file in files:
    for i in range(1, 10358):
        # path = os.path.join(input_dir, str(file))
        path = os.path.join(input_dir, str(i) + '.txt')
        df = pd.read_csv(path,
                         sep=',',
                         header=None,
                         names=['logNumber', 'Data(UTC)/Time(UTC)', 'Latitude', 'Longitude'],
                         skiprows=0)
        print('Convert file ' + str(i) + '.txt')
        if not df.empty:
            df.drop(['logNumber'], axis=1, inplace=True)
            df.replace(',', '', regex=True, inplace=True)
            # seperate Date and Time
            new = df['Data(UTC)/Time(UTC)'].str.split(" ", n=1, expand=True)
            df['Data(UTC)'] = new[0]
            df['Time(UTC)'] = new[1]
            df.drop(columns=['Data(UTC)/Time(UTC)'], inplace=True)
            # change date format
            df['Data(UTC)'] = pd.to_datetime(df['Data(UTC)'])
            df['Data(UTC)'] = df['Data(UTC)'].dt.strftime('%d-%b-%Y')
            df = df[['Data(UTC)', 'Time(UTC)', 'Latitude', 'Longitude']]

            df.to_csv(os.path.join(output_dir, str(i) + '.txt'), index=False, sep=' ')
            # print(df)

def convert_to_uts_format(input_dir, output_dir):
    #files = os.listdir(input_dir)

    # for file in files:
    for i in range(1, 10358):
        # path = os.path.join(input_dir, str(file))
        path = os.path.join(input_dir, str(i) + '.txt')
        #295.txt ist in originalen Logs leer, weshalb die Datei im standard_format nicht existiert
        if os.path.exists(path):
            df = pd.read_csv(path,
                             sep=' ',
                             header=None,
                             names=['Data(UTC)', 'Time(UTC)', 'Latitude', 'Longitude'],
                             skiprows=[0])
            print('Convert file ' + str(i) + '.txt')
            if not df.empty:
                # convert Data(UTC) and Time(UTC) to UTS
                df['UTS'] = df['Data(UTC)'] + " " + df['Time(UTC)']
                df.drop(columns=['Data(UTC)'], inplace=True)
                df.drop(columns=['Time(UTC)'], inplace=True)
                df = df[['UTS', 'Longitude', 'Latitude']]
                for row_index, row in df.iterrows():
                    ts = row[0]
                    df.loc[row_index, 'UTS'] = int(pd.Timestamp(ts).timestamp())
                df.to_csv(os.path.join(output_dir, str(i) + '.txt'), index=False, sep=' ')
                # print(df)

to_standard_format = False
to_uts_format = True

if to_standard_format:
    input_dir = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/data/Beijing/taxi_log_2008_by_id'
    output_dir = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/mapmatching/output/Beijing_Converted_GPS_Logs/standard_format'
    convert_to_standard_format(input_dir, output_dir)

if to_uts_format:
    input_dir = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/data/Beijing/Beijing_Converted_GPS_Logs/standard_format'
    output_dir = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/mapmatching/output/Beijing_Converted_GPS_Logs/uts_format'
    convert_to_uts_format(input_dir, output_dir)


