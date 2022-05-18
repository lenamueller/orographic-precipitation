import os
import pandas as pd


path_dwddata = 'metdata/opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/precipitation/historical/'
data_files = [file for file in os.listdir(path_dwddata) if file.startswith("produkt_zehn_min_rr_")]

def read_station(station_id:int)->pd.DataFrame:    
    """
    Creates a pandas DataFrame from the station id
    header: STATIONS_ID;MESS_DATUM;QN;RWS_DAU_10;RWS_10;RWS_IND_10
    """
    
    # get a list of filesnames matching the station
    data_files_st = [file for file in os.listdir(path_dwddata) if file.endswith(f"_{str(station_id).zfill(5)}.txt")]

    # read files into df
    frames = []
    for fn in data_files_st:
        frames.append(pd.read_csv(path_dwddata+fn, delimiter=";"))

    # concatenate frames
    df_st = pd.concat(frames)
    
    # convert MESS_DATUM into datetime object
    df_st['MESS_DATUM'] = pd.to_datetime(df_st['MESS_DATUM'], format='%Y%m%d%H%M')

    # sort rows by datetime column
    df_st = df_st.sort_values(by='MESS_DATUM')
    
    return df_st