import sys
import pandas as pd
import numpy as np
import glob
import datetime
import concurrent.futures


# stations for height zones
stations_z1 = [633, 721, 1001, 2928, 2932, 3426, 3811, 5629] # deleted: 2878
stations_z2 = [222, 550, 853, 1048, 1612, 1684, 2985, 3279, 3946] # deleted: 6268
stations_z3 = [840, 1358, 2233, 2261, 2274, 3166, 4109, 4464, 4818, 5779]
nb_stations = len(stations_z1) + len(stations_z2) + len(stations_z3)

# read OWK data and create a subset with OWK NWCCW and dates earlier than 2003
fn_owk = 'data/OWK_ERA-Interim.txt'
df_owk = pd.read_csv(fn_owk, sep=' ', header=0)
dates_nwccw = df_owk[df_owk["OWK"] == "NWCCW"]
dates_nwccw = dates_nwccw[dates_nwccw["Date"] > 20030000]["Date"].values.tolist()
dates_nwccw = [datetime.datetime.strptime(str(d), '%Y%m%d') for d in dates_nwccw]
nb_dates = len(dates_nwccw)
print("number stations", nb_stations, "number days", nb_dates)

# check if enough data files exist
datafiles = glob.glob("data/DWD_RR_Stationen/p_*")
if len(datafiles) < nb_stations:
    sys.exit("Missing data files.")

def get_p_for_zone(zone):
    p_zone = {"10":[], "20":[], "30":[], "40":[], "50":[], "60":[], "70":[], "80":[], 
              "90":[], "100":[], "110":[], "120":[], "130":[], "140":[], "inf":[]}
    for station in zone:
        
        # read precipitation data file
        data_temp = pd.read_csv(f"data/DWD_RR_Stationen/p_{str(station).zfill(5)}.txt", sep=';',header=0)
        
        # convert MESS_DATUM from str to datetime
        data_temp["MESS_DATUM"] = [datetime.datetime.strptime(str(x), '%Y%m%d%H%M') for x in data_temp["MESS_DATUM"].tolist()]
        
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

     
np.savetxt(f"data/DWD_RR_Stationen/p_z1", dict_z1, delimiter=",", fmt='%1.2f')
np.savetxt(f"data/DWD_RR_Stationen/p_z2", dict_z2, delimiter=",", fmt='%1.2f')
np.savetxt(f"data/DWD_RR_Stationen/p_z3", dict_z3, delimiter=",", fmt='%1.2f')