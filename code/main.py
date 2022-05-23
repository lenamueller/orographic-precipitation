import pickle
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import proplot as pplt

from read_files import read_station_ids, read_station_data, read_owk, read_intensities_st
from split_events import find_precipitation_events
from rolling_window import rolling_intensity
from enums import CONFIG


my_config = CONFIG.ERZGEBIRGE.name
min_dry_period = 18 # number of 10min - time steps 
min_event_length = 3 # reducing noise
min_percentile = 75 # focus on right-tail characteristics
min_intensity_values = 5 # min data points for fitting
first_timesteps = 4 # how many durations should be plotted (10min, 20min, 30min, 1h, 2h, 3h, 6h)

# read station IDs for each zone
stations_z1, stations_z2, stations_z3, stations_all = read_station_ids(my_config)

# read OWK dates and create a datetime list of selected synoptic situations
owk, owk_all = read_owk(my_config)
    
print(my_config, "\nNumber of stations:", len(stations_all), "Number of OWK days:", len(owk_all))
# create empty zone dictionary for intensity values -> dict : {"id:[intensities], ..."}
z1:dict = {}
z2:dict = {}
z3:dict = {}

for st in stations_all:
    st_list:list[list[float]] = [[],[],[],[],[],[],[]]
    # counter for events which match the synoptic situation
    c = 0
    # read station data and create data frame
    df_st = read_station_data(st)
    # extract independent storms and its datetime
    events, events_dates = find_precipitation_events(df_st["RWS_10"].tolist(), df_st["MESS_DATUM"].tolist(), min_dry_period, min_event_length)
    # keys are number of time steps which are the duration if multiplied by 10 min
    for e,d in zip(events, events_dates):
        date_begin = d[0]
        date_end = d[-1]
        # ! Use date instead of datetime
        if (date_begin.date() in owk_all) and (date_end.date() in owk_all):
            c += 1
            # calculate max precipitation sums for each window size of each event
            event_dict = rolling_intensity(e)
            # add event intensities to station list
            for i,ws in zip(np.arange(0,7,1),[1,2,3,6,12,18,36]):
                st_list[i].extend(event_dict[ws])
    
    # append station list to zone dict
    if st in stations_z1:   
        z1[st] = st_list
    if st in stations_z2:
        z2[st] = st_list
    if st in stations_z3:
        z3[st] = st_list
    # print(f"station {st} -  events (total): {len(events)} - events (OWK): {c}")

# save zone dictionaries to files
# with open(f'metdata/intensities/intensities_{my_config}_z1.pkl', 'wb') as f:
#     pickle.dump(z1, f)
# with open(f'metdata/intensities/intensities_{my_config}_z2.pkl', 'wb') as f:
#     pickle.dump(z2, f)
# with open(f'metdata/intensities/intensities_{my_config}_z3.pkl', 'wb') as f:
#     pickle.dump(z3, f)

# read zone data
# z1, z2, z3 = read_intensities_st(my_config)

# define curve to fit
def func(x,scale,shape):
    """ modified weibull distribution function"""
    return 1-np.exp(-pow(base=x/scale,exp=shape))

def weibull_fit(intensites:list[float], info):
    # calc and plot histogram values
    _, ax = plt.subplots(nrows=1, ncols=1, figsize=(6,6))
    n, bins, _ = ax.hist(intensites, bins=np.arange(0,20,0.25), density=True, cumulative=True, histtype='stepfilled', alpha=0.2)
    xdata = bins[:-1]
    ydata = n[:]
    # fit function and plot data and fitted lines
    try:
        if len(intensites) >= min_intensity_values:
            popt, _ = curve_fit(func, xdata, ydata)
            plt.plot(xdata, ydata, 'b-', label='data') # data as line
            plt.plot(xdata, func(xdata, *popt), 'r-', label=f'fit: scale={round(popt[0],3)}, shape={round(popt[1],3)}') # fitted line
            plt.legend()
            plt.savefig(f"images/{my_config}/fit_st{info[0]}_ws{info[1]}.png", dpi=300, bbox_inches="tight")
            if popt[1] < 0.00001:
                return (False,False)
            else:
                return popt
        else:
            return (False,False) # No fitting due to shortage of data
    except (RuntimeError, ValueError): # RuntimeError: The least-squares minimization fails. ValueError: ydata or xdata contain NaNs.
        return (False,False)    

# create new dict for {"id":[(scale_10min, shape_10min), ... , (scale_6h,shape_6h)]}
def calc_params(datadict):
    params:dict = {}
    for station_i in datadict.keys():
        ws_values: list = []
        for ws in range(len(datadict[station_i])):
            intensities = datadict[station_i][ws]
            if intensities != []:
                # reduce intensities to 75. percentile
                p75 = np.percentile(intensities, min_percentile)
                intensities = [i for i in intensities if i >= p75]            
                scale,shape = weibull_fit(intensities, info=(station_i,ws))
                ws_values.append((scale,shape))
            params[station_i] = ws_values
    return params

z1_params = calc_params(z1)
z2_params = calc_params(z2)
z3_params = calc_params(z3)
z_params = [z1_params, z2_params, z3_params]

print("z1_params =", z1_params)
print("z2_params =", z2_params)
print("z3_params =", z3_params)

# plot 
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(10,3))
labels = ["10min", "20min", "30min", "1h", "2h"]
colors = ["y", "orange", "red", "darkred", "brown"]
titles = ["Z1: 0 - 200 m AMSL", "Z2: 200 - 400 m AMSL", "Z3: 400 m AMSL <"]
for z in range(3):
    params_dict = z_params[z]
    for st_i,tuples_i in params_dict.items():
        # select only tuples for the wanted time steps
        tuples_i = tuples_i[:first_timesteps]
        # remove (False,False) tuples
        for t in range(len(tuples_i)):
            x_lineplot, y_lineplot = [],[]
            if tuples_i[t] != (False,False):
                ax[z].scatter(tuples_i[t][0], tuples_i[t][1], marker=".", s=8, c=colors[t], label=labels[t]) # plot markers
                x_lineplot.append(tuples_i[t][0])
                y_lineplot.append(tuples_i[t][1])
        ax[z].plot(x_lineplot, y_lineplot, linewidth=1, alpha=0.5, color="gray") # plot line
        ax[z].set_title(titles[z])
        ax[z].set_xscale('log')
        ax[z].set_xlim([0,20])
        ax[z].set_ylim([0,10])

plt.savefig(f"images/Scatter/{my_config}_dry{min_dry_period}_len{min_event_length}_p{min_percentile}_nb{min_intensity_values}.png", dpi=400, bbox_inches="tight")

print("Done")