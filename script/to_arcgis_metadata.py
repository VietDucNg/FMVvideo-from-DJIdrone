# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 09:41:00 2025

@author: Viet Nguyen
"""

import pandas as pd
import glob

# read metadata
meta_paths = glob.glob('**/*csv', recursive=True)

#### function to process
def func(path):
    # case 1: metadata from Airdata
    if 'Airdata' in path:
        # get file name
        name = path.split('-Airdata.csv')[0].split('\\')[-1]
        # read airdata metadata
        meta_df = pd.read_csv(path, usecols=['datetime(utc)','latitude','longitude'])
        
        #### caculate unix time stamp
        # covert datetime column to datetime type
        meta_df['datetime(utc)'] = pd.to_datetime(meta_df['datetime(utc)'], format='%Y-%m-%d %H:%M:%S')
        # convert to UNIX timestamp microseconds
        meta_df['Precision Time Stamp'] = meta_df['datetime(utc)'].astype(int) // 1000
        
        # rename
        meta_df = meta_df.rename(columns={'latitude':'Sensor Latitude','longitude':'Sensor Longitude'}).drop('datetime(utc)',axis=1)
        
    # case 2: metadata from drone harmony
    else:
        # get file name
        name = path.split('.')[0].split('\\')[-1]
        # read airdata metadata
        meta_df = pd.read_csv(path, usecols=['Time(millis)','Latitude','Longitude'])
        
        #### caculate unix time stamp
        # get start flight time from file name
        start_time = pd.to_datetime(name, format='%Y-%m-%d_%H_%M_%S')
        # convert to microseconds
        meta_df['Precision Time Stamp'] = (int(start_time.timestamp()) + meta_df['Time(millis)']) * 1000
        
        # rename
        meta_df = meta_df.rename(columns={'Latitude':'Sensor Latitude','Longitude':'Sensor Longitude'}).drop('Time(millis)',axis=1)

    # write to disk
    meta_df.to_csv(f'{name}-arcgis.csv', index=False)

# apply funciton
[func(path) for path in meta_paths]
