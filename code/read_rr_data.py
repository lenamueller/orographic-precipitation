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
    p_zone = []
    zone_missing_rows = 0
    for station in zone:
        station_missing_rows = 0
        # read precipitation data file
        data_temp = pd.read_csv(f"data/DWD_RR_Stationen/p_{str(station).zfill(5)}.txt", sep=';',header=0)
        
        # convert MESS_DATUM from str to datetime
        data_temp["MESS_DATUM"] = [datetime.datetime.strptime(str(x), '%Y%m%d%H%M') for x in data_temp["MESS_DATUM"].tolist()]
        
        for date in dates_nwccw:
            # select rows matching date
            date_plus1 = date + datetime.timedelta(days=1)
            p_data = data_temp.loc[data_temp["MESS_DATUM"] < date_plus1]
            p_data = p_data.loc[p_data["MESS_DATUM"] >= date]
            p_data = p_data["RWS_10"].tolist()
            # check for missing rows, fill them with 0mm and add values to p_zone
            if len(p_data) == 144:
                p_zone.extend(p_data)
            else:
                missing = 144 - len(p_data)
                zone_missing_rows += missing
                station_missing_rows += missing
                p_zone.extend(p_data + [0]*missing)
        print("station:", station, " - missing rows:", station_missing_rows)
    print("zone missing rows:", zone_missing_rows)
    # save p_zone into file
    return p_zone

with concurrent.futures.ProcessPoolExecutor(max_workers=24) as executor:
    results = executor.map(get_p_for_zone, [stations_z1, stations_z2, stations_z3])

results_arr = np.array(list(results))
     
np.savetxt(f"data/DWD_RR_Stationen/p_z1", results_arr[0], delimiter=",", fmt='%1.2f')
np.savetxt(f"data/DWD_RR_Stationen/p_z2", results_arr[1], delimiter=",", fmt='%1.2f')
np.savetxt(f"data/DWD_RR_Stationen/p_z3", results_arr[2], delimiter=",", fmt='%1.2f')