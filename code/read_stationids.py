import pandas as pd


def read_stationids():
    path_stations = 'geodata/DWD_RR_Stationen/Stationen_Selektion.csv'
    stations = pd.read_csv(path_stations, delimiter=',')
    ids = stations["id"].tolist() #int
    zones = stations["height"].tolist() #str

    stations_z1, stations_z2, stations_z3 = [], [], []
    for id,zone in zip(ids,zones):
        match zone:
            case "Z1":
                stations_z1.append(id)
            case "Z2":
                stations_z2.append(id)
            case "Z3":
                stations_z3.append(id)
                
    stations_all = stations_z1 + stations_z2 + stations_z3   
    return stations_z1, stations_z2, stations_z3, stations_all