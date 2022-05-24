import pickle
import os
import pandas as pd
import matplotlib.pyplot as plt
import collections


def read_owk(my_config):
    # read file
    path_owk = '/home/lena/Documents/Master/Sem_2/FachvorträgeHydro/orographic_precipitation/metdata/owk/wlkvorhersage.txt'
    owk_df = pd.read_csv(path_owk, sep=',', names=["datetime", "owk_number", "owk_abbreviation"], header=None)
    
    # convert MESS_DATUM into datetime object
    owk_df['datetime'] = pd.to_datetime(owk_df['datetime'], format='%Y%m%d')
    
    # create subset which matches synoptic situations
    # dict with dates according to abbreviation
    if (my_config == "ERZGEBIRGE") or (my_config == "SCHWARZWALD"):
        owk = {"NWAZF":[], "NWZAF":[], "NWZZF":[], "XXZZF":[], "XXZAF":[], "XXAZF":[]}

    if (my_config == "HARZ") or (my_config == "THUERINGERWALD"):
        owk = {"SWAZF":[], "SWZAF":[], "SWZZF":[], "XXZZF":[], "XXZAF":[], "XXAZF":[]}    
    
    for _, row in owk_df.iterrows():
        owk_i = row["owk_abbreviation"]
        owk_datetime = row["datetime"]
        if owk_i in owk.keys():
            owk[owk_i].append(owk_datetime.date())
    
    # all dates merged
    owk_all = []
    for abbr in owk.keys():
        owk_all.extend(owk[abbr])
    
    return owk, owk_all

def owk_stats():
    path_owk = '/home/lena/Documents/Master/Sem_2/FachvorträgeHydro/orographic_precipitation/metdata/owk/wlkvorhersage.txt'
    owk_df = pd.read_csv(path_owk, sep=',', names=["datetime", "owk_number", "owk_abbreviation"], header=None)
    data = owk_df["owk_abbreviation"]
    freq = collections.Counter(data)
    freq_sorted = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))
    names = list(freq_sorted.keys())
    values = list(freq_sorted.values())
    plt.bar(range(len(freq_sorted)), values, tick_label=names)
    plt.title("Objektive Wetterklassifikation 12.09.1979 - 16.05.2022")
    plt.xticks(rotation=90)
    plt.savefig("images/owk_hist.png", dpi=300, bbox_inches="tight")
    
    
def read_station_ids(my_config):
    path_stations = f'geodata/DWD_RR_Stationen/Stationen_Selektion_{my_config}.csv'
    stations = pd.read_csv(path_stations, delimiter=',')
    ids = stations["id"].tolist() #int
    zones = stations["height"].tolist() #str

    stations_z1, stations_z2, stations_z3 = [], [], []
    for id,zone in zip(ids,zones):
        match zone:
            case "Z1":
                stations_z1.append(id)
            case "Z2":
                stations_z2.append(id)
            case "Z3":
                stations_z3.append(id)
                
    stations_all = stations_z1 + stations_z2 + stations_z3   
    return stations_z1, stations_z2, stations_z3, stations_all

def read_station_heights(my_config):
    path_stations = f'geodata/DWD_RR_Stationen/Stationen_Selektion_{my_config}.csv'
    height_dict = {}
    stations = pd.read_csv(path_stations, delimiter=',')
    ids = stations["id"].tolist() #int
    hoehen = stations["hoehe"].tolist() #int
    for i in range(len(ids)):
        height_dict[ids[i]] = hoehen[i]
    return height_dict

path_dwddata = 'metdata/opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/precipitation/historical/'
data_files = [file for file in os.listdir(path_dwddata) if file.startswith("produkt_zehn_min_rr_")]

def read_station_data(station_id:int)->pd.DataFrame:    
    """
    Creates a pandas DataFrame from the station id
    header: STATIONS_ID;MESS_DATUM;QN;RWS_DAU_10;RWS_10;RWS_IND_10
    """
    
    # get a list of filesnames matching the station
    data_files_st = [file for file in os.listdir(path_dwddata) if file.endswith(f"_{str(station_id).zfill(5)}.txt")]

    # read files into df
    number_files = len(data_files_st)
    # print("number files", number_files, "for station", station_id)
    
    if number_files == 0:
        print("NO FILES FOUND FOR STATION NO.", station_id)
    
    else: 
        if number_files == 1: 
            df_st = pd.read_csv(path_dwddata+data_files_st[0], delimiter=";")
        else:    
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


def read_intensities(region:str, min_dry_period:int):
    # output: dictionaries z1 = {"7394:[[],[],[],[],[],[],[]]"} with intensities in each list (window size)
    with open(f'metdata/intensities/intensities_{region}_z1_DRY{min_dry_period}.pkl', 'rb') as f:
        z1 = pickle.load(f)
    with open(f'metdata/intensities/intensities_{region}_z2_DRY{min_dry_period}.pkl', 'rb') as f:
        z2 = pickle.load(f)
    with open(f'metdata/intensities/intensities_{region}_z3_DRY{min_dry_period}.pkl', 'rb') as f:
        z3 = pickle.load(f)
    return z1, z2, z3

def read_parameters(region:str, min_dry_period:int, min_percentile:int):
    # output: dictionaries z1_params = {"id":[(scale_10min, shape_10min), ... , (scale_6h,shape_6h)]}
    with open(f'metdata/parameters/intensities_{region}_z1_DRY{min_dry_period}_PER{min_percentile}.pkl', 'rb') as f:
        z1_params = pickle.load(f)
    with open(f'metdata/parameters/intensities_{region}_z2_DRY{min_dry_period}_PER{min_percentile}.pkl', 'rb') as f:
        z2_params = pickle.load(f)
    with open(f'metdata/parameters/intensities_{region}_z3_DRY{min_dry_period}_PER{min_percentile}.pkl', 'rb') as f:
        z3_params = pickle.load(f)
    return z1_params, z2_params, z3_params