import glob
import sys
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from split_events import find_precipitation_events
from read_station import read_station
from rolling_window import get_max_pr_sum
from read_owk import read_owk

# configure list of stations and zones
stations_z1 = [633, 721, 1001, 2928, 2932, 3426, 3811, 5629]
stations_z2 = [222, 550, 853, 1048, 1612, 1684, 2985, 3279, 3946]
stations_z3 = [840, 1358, 2233, 2261, 2274, 3166, 4109, 4464, 4818, 5779]
stations = stations_z1 + stations_z2 + stations_z3

# example case
# stations = [633, 721]
# stations_z1 = [633, 721]
# stations_z2 = []
# stations_z3 = []

# create empty dict for precipitation sums of corresponding window size
z1:dict = {1:[],2:[],3:[],6:[],12:[],18:[],36:[]}
z2:dict = {1:[],2:[],3:[],6:[],12:[],18:[],36:[]}
z3:dict = {1:[],2:[],3:[],6:[],12:[],18:[],36:[]}

# read OWK data and create a datetime list of selected synoptic situations
owk = read_owk()
owk_all = owk["NWAZF"]+ owk["NWZAF"] + owk["NWZZF"] + owk["NOZAF"]  + owk["NOAZF"] + owk["NOZZF"]
print("number of owk days: ", len(owk_all))
    
# iterate through stations
for st in stations:
    # counter for events which match the synoptic situation
    c = 0
    
    # read data and create data frame
    df_st = read_station(st)
    
    # get precipitation and datetime list from data frame and extract independent storms and its date and time
    events, events_dates = find_precipitation_events(df_st["RWS_10"].tolist(), df_st["MESS_DATUM"].tolist())
    
    # keys are number of time steps which are the duration if multiplied by 10 min
    maxval_dict: dict = {1:[],2:[],3:[],6:[],12:[],18:[],36:[]}
    for e,d in zip(events, events_dates):
        date_begin = d[0]
        date_end = d[-1]
        
        # ! Use date instead of datetime
        if date_end.date() in owk_all:
            
            # counter for considered events
            c += 1
            # calculate max precipitation sum for each window size
            maxval_dict_station = get_max_pr_sum(e,maxval_dict)
            
            # add station intensities to zone intensities
            if st in stations_z1:
                for ws in z1.keys():
                    z1[ws].extend(maxval_dict_station[ws])
            if st in stations_z2:
                for ws in z1.keys():
                    z2[ws].extend(maxval_dict_station[ws])
            if st in stations_z3:
                for ws in z1.keys():
                    z3[ws].extend(maxval_dict_station[ws])
    
    print(f"station {st} -  total number of events: {len(events)} - considered number of events: {c}")