import matplotlib
import matplotlib.pyplot as plt
import proplot as pplt
import numpy as np 

from reading_functions import read_station_ids, read_owk, read_station_data
from split_events import find_precipitation_events
# from main import my_config, min_dry_period, min_event_length
my_config = "HARZ"
min_dry_period = 36
min_event_length = 3


min_mean_int = 1

stations_z1, stations_z2, stations_z3, stations_all = read_station_ids(my_config)
_, owk_all = read_owk(my_config)
    
keys = np.arange(40,210,10)
z1:dict = dict((x,[]) for x in keys)
z2:dict = dict((x,[]) for x in keys)
z3:dict = dict((x,[]) for x in keys)

# get events
for st in stations_all:
    df_st = read_station_data(st)
    events, events_dates = find_precipitation_events(df_st["RWS_10"].tolist(), df_st["MESS_DATUM"].tolist(), min_dry_period, min_event_length)
    for e,d in zip(events, events_dates):
        date_begin = d[0]
        date_end = d[-1]
        # ! event must have min mean intensity
        if (date_begin.date() in owk_all) and (date_end.date() in owk_all) and len(e) <= 20 and np.mean(e) > min_mean_int:
            if st in stations_z1:   
                z1[len(e)*10].append(e)
            if st in stations_z2:
                z2[len(e)*10].append(e)
            if st in stations_z3:
                z3[len(e)*10].append(e)


# plot events
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(10,4))

z = [z1,z2,z3]
colors = ["r", "g", "b"]

for len_i in range(40,190,10): # for each duration
    for i in range(3):
        z_i = z[i]
        # empty list would create nan mean
        if z_i[len_i] != []:
            # calculate mean intensity
            event_mean = np.mean(np.array(z_i[len_i]), axis=0)
            event_mean = event_mean.tolist()
            event_max = max(event_mean)
            ev_max_i = event_mean.index(event_max) # get index with max. intensity
            x = np.arange(-ev_max_i, len(event_mean)-ev_max_i, 1) # center max. intensity at x = 0
            axs[i].plot(x,event_mean, color=colors[i], lw=0.5)
            
for i in range(3):
    axs[i].set_xticks(np.arange(-10,10,2))
    axs[i].set_xticklabels(np.arange(-100,100,20))
    axs[i].set_xlim([-10,10])
    axs[i].set_ylim([0,20])
axs[0].set_ylabel("Niederschlag [mm/h]")
axs[1].set_xlabel("Minuten vor und nach der max. Intensität")

plt.savefig(f"images/plots/temporal_{my_config}_DRY{min_dry_period}_MIN{min_mean_int}.png", dpi=300, bbox_inches="tight")