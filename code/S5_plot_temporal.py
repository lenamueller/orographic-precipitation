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

z1_all:list = []
z2_all:list = []
z3_all:list = []

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
                # z1[len(e)*10].append(e)
                z1_all.append(e)
            if st in stations_z2:
                # z2[len(e)*10].append(e)
                z2_all.append(e)
            if st in stations_z3:
                # z3[len(e)*10].append(e)
                z3_all.append(e)


z_all = [z1_all, z2_all, z3_all]

# plot events
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(10,4))
mins, means, maxs = [],[],[]
for i in range(3):
    z_i = z_all[i]
    zeros_list = []
    if z_i:
        for event in z_i:
            if 8 <= len(event) <= 12:
                max_index = event.index(max(event)) # get index with max. intensity
                event_len = len(event)
                n_before = (9-max_index)
                zeros_before = [0] * n_before
                zeros_after = [0] * (19-n_before-event_len)
                zeros_list.append(zeros_before+event+zeros_after)
    means.append(np.mean(np.array(zeros_list), axis=0))
    mins.append(np.min(np.array(zeros_list), axis=0))            
    maxs.append(np.max(np.array(zeros_list), axis=0))            

print(means[0])

# axs[0].plot(np.arange(-9,10,1), means[0], color="k")
axs[0].plot(np.arange(-9,10,1), mins[0], color="g")
axs[0].plot(np.arange(-9,10,1), maxs[0], color="r")
# axs[1].plot(np.arange(-9,10,1), means[1], color="k")
axs[1].plot(np.arange(-9,10,1), mins[1], color="g")
axs[1].plot(np.arange(-9,10,1), maxs[1], color="r")
# axs[2].plot(np.arange(-9,10,1), means[2], color="k")
axs[2].plot(np.arange(-9,10,1), mins[2], color="g")
axs[2].plot(np.arange(-9,10,1), maxs[2], color="r")
            
for i in range(3):
    axs[i].set_xticks(np.arange(-10,10,2))
    axs[i].set_xticklabels(np.arange(-100,100,20))
    axs[i].set_xlim([-10,10])
    axs[i].set_ylim([0,20])
axs[0].set_ylabel("Niederschlag [mm/h]")
axs[1].set_xlabel("Minuten vor und nach der max. Intensität")

plt.savefig(f"images/plots/temporal_{my_config}_DRY{min_dry_period}_MIN{min_mean_int}.png", dpi=300, bbox_inches="tight")