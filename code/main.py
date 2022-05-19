import pickle

from read_station import read_station
from read_owk import read_owk
from read_stationids import read_stationids
from split_events import find_precipitation_events
from rolling_window import rolling_intensity


# read zone stations
stations_z1, stations_z2, stations_z3, stations_all = read_stationids()

# create empty dict for precipitation sums of corresponding window size
z1:dict = {1:[],2:[],3:[],6:[],12:[],18:[],36:[]}
z2:dict = {1:[],2:[],3:[],6:[],12:[],18:[],36:[]}
z3:dict = {1:[],2:[],3:[],6:[],12:[],18:[],36:[]}

# read OWK data and create a datetime list of selected synoptic situations
owk = read_owk()
owk_all = owk["NWAZF"]+ owk["NWZAF"] + owk["NWZZF"] + owk["NOZAF"]  + owk["NOAZF"] + owk["NOZZF"]
print("Number of OWK days: ", len(owk_all))
    
# iterate through stations
for st in stations_all:
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
            
            # add event intensities to zone intensities
            for ws in [1,2,3,6,12,18,36]:
                if st in stations_z1:   
                    z1[ws].extend(event_dict[ws])
                if st in stations_z2:
                    z2[ws].extend(event_dict[ws])                    
                if st in stations_z3:
                    z3[ws].extend(event_dict[ws])
    
    print(f"station {st} -  total number of events: {len(events)} - considered number of events: {c}")

# save zone dictionaries to files
with open('metdata/intensities_z1.pkl', 'wb') as f:
    pickle.dump(z1, f)
with open('metdata/intensities_z2.pkl', 'wb') as f:
    pickle.dump(z2, f)
with open('metdata/intensities_z3.pkl', 'wb') as f:
    pickle.dump(z3, f)
    
print("Done")