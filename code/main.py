import pickle
import numpy as np

from read_files import read_station_ids, read_station_data, read_owk
from split_events import find_precipitation_events
from rolling_window import rolling_intensity
from enums import CONFIG


my_config = CONFIG.ERZGEBIRGE.name

""" 
ERZGEBIRGE: 82 stations, 1213 synoptic days
SCHWARZWALD: 40 stations, 1213 synoptic days
HARZ: 38 stations, 3149 synoptic days
"""

# read station IDs for each zone
stations_z1, stations_z2, stations_z3, stations_all = read_station_ids(my_config)
print("Number of stations:", len(stations_all))

# read OWK dates and create a datetime list of selected synoptic situations
owk, owk_all = read_owk(my_config)
print("Number of OWK days:", len(owk_all))
    
# create empty zone dictionary for intensity values
z1:dict = {}
z2:dict = {}
z3:dict = {}

for st in stations_all:
    st_list:list[list[float]] = [[],[],[],[],[],[],[]]

    # counter for events which match the synoptic situation
    c = 0
    
    # read station data and create data frame
    df_st = read_station_data(st)
    
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
    if c >=1:
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