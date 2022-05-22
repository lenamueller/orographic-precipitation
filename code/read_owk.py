import pandas as pd
import matplotlib.pyplot as plt
import collections


def read_owk():
    # read file
    path_owk = '/home/lena/Documents/Master/Sem_2/FachvorträgeHydro/orographic_precipitation/metdata/owk/wlkvorhersage.txt'
    owk_df = pd.read_csv(path_owk, sep=',', names=["datetime", "owk_number", "owk_abbreviation"], header=None)
    
    # convert MESS_DATUM into datetime object
    owk_df['datetime'] = pd.to_datetime(owk_df['datetime'], format='%Y%m%d')
    
    # create subset which matches synoptic situations
    owk = {"NWAZF":[], "NWZAF":[], "NWZZF":[], # Erzgebirge
           "SWAZF":[], "SWZAF":[], "SWZZF":[], # Thüringer Wald, Harz
           "XXZZF":[], "XXZAF":[], "XXAZF":[] # alle
           }
    for index, row in owk_df.iterrows():
        owk_i = row["owk_abbreviation"]
        owk_datetime = row["datetime"]
        if owk_i in owk.keys():
            owk[owk_i].append(owk_datetime.date())

    return owk

def owk_stats():
    path_owk = '/home/lena/Documents/Master/Sem_2/FachvorträgeHydro/orographic_precipitation/metdata/owk/wlkvorhersage.txt'
    owk_df = pd.read_csv(path_owk, sep=',', names=["datetime", "owk_number", "owk_abbreviation"], header=None)
    data = owk_df["owk_abbreviation"]
    freq = collections.Counter(data)
    freq_sorted = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))
    names = list(freq_sorted.keys())
    values = list(freq_sorted.values())
    plt.bar(range(len(freq_sorted)), values, tick_label=names)
    plt.title("Objektive Wetterklassifikation 12.09.1979 - 16.05.2022")
    plt.xticks(rotation=90)
    plt.savefig("images/owk_hist.png", dpi=300, bbox_inches="tight")