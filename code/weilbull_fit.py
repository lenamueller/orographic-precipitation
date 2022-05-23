from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import proplot as pplt

from read_files import read_intensities_st
from enums import CONFIG

my_config = CONFIG.ERZGEBIRGE.name
first_timesteps = 4 # for plotting
perc = 75
min_intensity_values = 5

# read zone data -> dict : {"id:[intensities], ..."}
z1, z2, z3 = read_intensities_st(my_config)

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
            if popt[1] < 0.001:
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
                p75 = np.percentile(intensities, perc)
                intensities = [i for i in intensities if i >= p75]            
                if len(intensities) > 0:
                    scale,shape = weibull_fit(intensities, info=(station_i,ws))
                    ws_values.append((scale,shape))
            params[station_i] = ws_values
    return params

z1_params = calc_params(z1)
z2_params = calc_params(z2)
z3_params = calc_params(z3)
z_params = [z1_params, z2_params, z3_params]

# print("z1_params =", z1_params)
# print("z2_params =", z2_params)
# print("z3_params =", z3_params)

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
            ax[z].plot(x_lineplot, y_lineplot, linewidth=0.5, alpha=0.6, color="gray") # plot line
            ax[z].set_title(titles[z])
            ax[z].set_xscale('log')
            ax[z].set_xlim([0,20])
            ax[z].set_ylim([0,10])

plt.savefig(f"images/{my_config}/Scatter_{perc}.png", dpi=400, bbox_inches="tight")
print("Done")