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
stations = [633, 721]
stations_z1 = [633, 721]
stations_z2 = []
stations_z3 = []

# create empty dict for precipitation sums of corresponding window size
z1:dict = {1:[],2:[],3:[],6:[],12:[],18:[],36:[]}
z2:dict = {1:[],2:[],3:[],6:[],12:[],18:[],36:[]}
z3:dict = {1:[],2:[],3:[],6:[],12:[],18:[],36:[]}

# iterate through stations
for st in stations:
    # counter for events which match the synoptic situation
    c = 0
    
    # read data and create data frame
    df_st = read_station(st)
    
    # get precipitation and datetime list from data frame and extract independent storms and its date and time
    events, events_dates = find_precipitation_events(df_st["RWS_10"].tolist(), df_st["MESS_DATUM"].tolist())
    
    # read OWK data and create a datetime list of selected synoptic situations
    owk_list: list[datetime.datetime] = []

    # keys are number of time steps which are the duration if multiplied by 10 min
    maxval_dict: dict = {1:[],2:[],3:[],6:[],12:[],18:[],36:[]}
    for e,d in zip(events, events_dates):
        date_begin = d[0]
        date_end = d[-1]
        if (date_begin not in owk_list) and (date_end not in owk_list):
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


sys.exit()
# stations for height zones
stations_z1 = [633, 721, 1001, 2928, 2932, 3426, 3811, 5629]  # deleted: 2878
stations_z2 = [222, 550, 853, 1048, 1612,
               1684, 2985, 3279, 3946]  # deleted: 6268
stations_z3 = [840, 1358, 2233, 2261, 2274, 3166, 4109, 4464, 4818, 5779]
nb_stations = len(stations_z1) + len(stations_z2) + len(stations_z3)

# read OWK data and create a subset with OWK NWCCW and dates earlier than 2003
fn_owk = 'data/OWK_ERA-Interim.txt'
df_owk = pd.read_csv(fn_owk, sep=' ', header=0)
dates_nwccw = df_owk[df_owk["OWK"] == "NWCCW"]
dates_nwccw = dates_nwccw[dates_nwccw["Date"]
                          > 20030000]["Date"].values.tolist()
dates_nwccw = [datetime.datetime.strptime(
    str(d), '%Y%m%d') for d in dates_nwccw]
nb_dates = len(dates_nwccw)
print("number stations", nb_stations, "number days", nb_dates)

# check if enough data files exist
datafiles = glob.glob("data/DWD_RR_data/p_*")
if len(datafiles) < nb_stations:
    sys.exit("Missing data files.")


def get_p_for_zone(zone):
    p_zone = {"10": [], "20": [], "30": [], "40": [], "50": [], "60": [], "70": [], "80": [],
              "90": [], "100": [], "110": [], "120": [], "130": [], "140": [], "inf": []}
    for station in zone:

        # read precipitation data file
        data_temp = pd.read_csv(
            f"data/DWD_RR_data/p_{str(station).zfill(5)}.txt", sep=';', header=0)

        # convert MESS_DATUM from str to datetime
        data_temp["MESS_DATUM"] = [datetime.datetime.strptime(
            str(x), '%Y%m%d%H%M') for x in data_temp["MESS_DATUM"].tolist()]

        for date in dates_nwccw:
            # select rows matching the date
            date_plus1 = date + datetime.timedelta(days=1)
            p_data_untilday = data_temp.loc[data_temp["MESS_DATUM"] < date_plus1]
            p_data_subset = p_data_untilday.loc[p_data_untilday["MESS_DATUM"] >= date]
            p_data_subset = np.array(p_data_subset["RWS_10"].tolist())

            # add zero to end
            list_with_zeros = p_data_subset

            # add zero to begin and end
            list_with_zeros = [0] + list_with_zeros + [0]

            # get indices of zeros
            indices = []
            for i in range(len(list_with_zeros)):
                if list_with_zeros[i] == 0:
                    indices.append(i)

            # slice list at zero indices
            for i in range(len(indices)-1):
                sublist = list_with_zeros[indices[i]+1:indices[i+1]]

                # check if list is not empty and allocate lists to dict
                if 0 < len(sublist) < 15:
                    duration = str(len(sublist)*10)
                    p_zone[duration].append(sublist)
                if len(sublist) >= 15:
                    p_zone["inf"].append(sublist)
    return p_zone


dict_z1 = get_p_for_zone(stations_z1)
dict_z2 = get_p_for_zone(stations_z2)
dict_z3 = get_p_for_zone(stations_z3)


# plot data
f, ((ax1, ax2, ax3)) = plt.subplots(ncols=3, figsize=(12, 4))
ax1.hist(dict_z1["10"], bins=50)
ax2.hist(dict_z2["10"], bins=50)
ax3.hist(dict_z3["10"], bins=50)
ax1.set_title("0 - 200 m ASL")
ax2.set_title("200 - 400 m ASL")
ax3.set_title("400 m ASL <")
for ax in [ax1, ax2, ax3]:
    ax.set_yscale('log')
plt.savefig("images/hist_10min.png", dpi=300, bbox_inches="tight")

# np.savetxt(f"data/DWD_RR_Stationen/p_z1", dict_z1, delimiter=",", fmt='%1.2f')
# np.savetxt(f"data/DWD_RR_Stationen/p_z2", dict_z2, delimiter=",", fmt='%1.2f')
# np.savetxt(f"data/DWD_RR_Stationen/p_z3", dict_z3, delimiter=",", fmt='%1.2f')

# TODO: Only one dry 10min slot enough for splitting into ordinary events?
