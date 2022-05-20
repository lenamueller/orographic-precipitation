from datetime import datetime
import pickle
import sys
import numpy as np

from read_station import read_station
from read_owk import read_owk
from read_stationids import read_stations_erzgebirge
from split_events import find_precipitation_events
from rolling_window import rolling_intensity


my_config = "ERZ"

if my_config == "ERZ":
    path_stations = 'geodata/DWD_RR_Stationen/Stationen_Selektion_Erzgebirge.csv'
    owk_abbr = ["NWAZF", "NWZAF", "SWZZF"]

if my_config == "HARZ":
    path_stations = 'geodata/DWD_RR_Stationen/Stationen_Selektion_Harz.csv'
    owk_abbr = ["SWAZF", "SWZAF", "SWZZF"]

if my_config == "THUE":
    path_stations = 'geodata/DWD_RR_Stationen/Stationen_Selektion_ThueringerWald.csv'
    owk_abbr = ["SWAZF", "SWZAF", "SWZZF"]


# read zone stations
stations_z1, stations_z2, stations_z3, stations_all = read_stations_erzgebirge(path_stations)

z1:dict = {}
z2:dict = {}
z3:dict = {}

# read OWK data and create a datetime list of selected synoptic situations
owk = read_owk()
owk_all = []
for abbr in owk_abbr:
    owk_all.extend(owk[abbr])
    
print("Number of OWK days: ", len(owk_all))
    
# iterate through stations
for st in stations_all:
    st_list:list[list[float]] = [[],[],[],[],[],[],[]]

    # counter for events which match the synoptic situation
    c = 0
    
    # read data and create data frame
    df_st = read_station(st)
    
    # extract independent storms and its datetime
    events, events_dates = find_precipitation_events(df_st["RWS_10"].tolist(), df_st["MESS_DATUM"].tolist())
    
    # keys are number of time steps which are the duration if multiplied by 10 min
    for e,d in zip(events, events_dates):
        date_begin = d[0]
        date_end = d[-1]
        # ! Use date instead of datetime
        if (date_begin.date() in owk_all) and (date_end.date() in owk_all):
            c += 1

            # calculate max precipitation sums for each window size of each event
            event_dict = rolling_intensity(e)
            
            # add event intensities to station list
            for i,ws in zip(np.arange(0,7,1),[1,2,3,6,12,18,36]):
                st_list[i].extend(event_dict[ws])
    
    # stations must contain at least 30 events
    if c >=30:
        # append station list to zone dict
        if st in stations_z1:   
            z1[st] = st_list
        if st in stations_z2:
            z2[st] = st_list
        if st in stations_z3:
            z3[st] = st_list
        print(f"station {st} -  events (total): {len(events)} - events (OWK): {c}")
    else:
        print(f"station {st} -  events (total): {len(events)} - events (OWK): {c} - NOT USED")

# save zone dictionaries to files
with open(f'metdata/intensities/intensities_{my_config}_z1.pkl', 'wb') as f:
    pickle.dump(z1, f)
with open(f'metdata/intensities/intensities_{my_config}_z2.pkl', 'wb') as f:
    pickle.dump(z2, f)
with open(f'metdata/intensities/intensities_{my_config}_z3.pkl', 'wb') as f:
    pickle.dump(z3, f)
    
print("Done")