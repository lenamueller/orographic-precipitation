import pandas as pd


def read_owk():
    # read file
    path_owk = '/home/lena/Documents/Master/Sem_2/FachvorträgeHydro/orographic_precipitation/metdata/owk/wlkvorhersage.txt'
    owk_df = pd.read_csv(path_owk, sep=',', names=["datetime", "owk_number", "owk_abbreviation"], header=None)
    
    # convert MESS_DATUM into datetime object
    owk_df['datetime'] = pd.to_datetime(owk_df['datetime'], format='%Y%m%d')
    
    # create subset which matches synoptic situations
    owk = {"NWAZF":[], "NWZAF":[], "NWZZF":[], # Erzgebirge
           "SWAZF":[], "SWZAF":[], "SWZZF":[], # Thüringer Wald, Harz
           }
    for index, row in owk_df.iterrows():
        owk_i = row["owk_abbreviation"]
        owk_datetime = row["datetime"]
        if owk_i in owk.keys():
            owk[owk_i].append(owk_datetime.date())

    return owk