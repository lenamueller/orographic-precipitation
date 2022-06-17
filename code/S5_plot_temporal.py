import math
import statistics
import matplotlib.pyplot as plt
import proplot as pplt
import numpy as np

from reading_functions import read_station_ids, read_owk, read_station_data
from split_events import find_precipitation_events


def normalize_list_against_maximum(input_list):
    list_max = max(input_list)
    norm_list=[x/list_max for x in input_list]
    return norm_list

def plot_temporal(my_config, min_dry_period, min_event_length):
    stations_z1, stations_z2, stations_z3, stations_all = read_station_ids(my_config)
    _, owk_all = read_owk(my_config)

    z1_all: list = []
    z2_all: list = []
    z3_all: list = []        

    # get events
    for st in stations_all:
        df_st = read_station_data(st)
        events, events_dates = find_precipitation_events(df_st["RWS_10"].tolist(
        ), df_st["MESS_DATUM"].tolist(), min_dry_period, min_event_length)
        for e, d in zip(events, events_dates):
            date_begin = d[0]
            date_end = d[-1]
            # ! event must have min mean intensity
            if (date_begin.date() in owk_all) and (date_end.date() in owk_all) and len(e) <= 20 and np.mean(e) > 1:
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
    fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(5, 8))
    plot_dict: dict = {"mins": [], "maxs": [],
                    "mean": [], "p25": [], "p75": [], "median": []}
    for i in range(3):
        z_i = z_all[i]
        zeros_list = []
        if z_i:
            for event in z_i:
                if len(event) >= 5:
                    # new nan list
                    new_entry = [np.nan for i in range(40)]
                    middle = 20
                    # get index with max intensity
                    max_index = event.index(max(event))
                    # split into two parts
                    first_part = event[:max_index]
                    second_part = event[max_index:]
                    # add parts to nan list
                    new_entry[middle-len(first_part):middle] = first_part
                    new_entry[middle: middle+len(second_part)] = second_part
                    # replace remaining nan with 0
                    new_entry2 = [0 if math.isnan(x) else x for x in new_entry]
                    zeros_list.append(new_entry2)

        # means.append(np.mean(np.array(zeros_list), axis=0))
        plot_dict["mins"].append(np.min(np.array(zeros_list), axis=0))
        plot_dict["maxs"].append(np.max(np.array(zeros_list), axis=0))
        plot_dict["p25"].append([np.percentile(col, 25) for col in np.array(zeros_list).T])
        plot_dict["p75"].append([np.percentile(col, 75) for col in np.array(zeros_list).T])
        plot_dict["median"].append([statistics.median(col) for col in np.array(zeros_list).T])

    cols = ["b", "g", "r"]
    labels = ["Tiefland", "Hügelland", "Gebirge"]
    x = np.arange(-20, 20, 1)
    for i in range(3):
        axs[0].fill_between(x, plot_dict["p75"][i], plot_dict["p25"][i], color=cols[i], alpha=0.2)
        axs[0].plot(x, plot_dict["median"][i], color=cols[i], label=labels[i], lw=0.8)
        axs[1].fill_between(x, normalize_list_against_maximum(plot_dict["p75"][i]), normalize_list_against_maximum(plot_dict["p25"][i]), color=cols[i], alpha=0.2)
        axs[1].plot(x, normalize_list_against_maximum(plot_dict["median"][i]), color=cols[i], label=labels[i], lw=0.8)
        
    for i in range(2):
        axs[i].set_xticks(np.arange(-10, 10, 2))
        axs[i].set_xticklabels(np.arange(-100, 100, 20))
        axs[i].set_xlim([-9, 10])
    
    axs[0].set_title(my_config)
    axs[0].set_ylim([0, 10])
    axs[1].set_ylim([0, 1])
    axs[0].set_ylabel("Niederschlag [mm/h]")
    axs[1].set_ylabel("normierter Niederschlag [-]")
    axs[0].set_xlabel("Zeit im Abstand der max. Intensität [min]")
    axs[1].set_xlabel("Zeit im Abstand der max. Intensität [min]")
    axs[0].legend()

    plt.savefig(
        f"images/plots/temporal_{my_config}_DRY{min_dry_period}_MIN1.png", dpi=300, bbox_inches="tight")

print("S5_plot_temporal.py done")