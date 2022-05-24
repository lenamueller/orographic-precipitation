import pickle
from typing import Tuple
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

from reading_functions import read_intensities

from MYCONFIG import my_config, min_intensity_values, min_percentile, min_dry_period


# read zone data
z1, z2, z3 = read_intensities(my_config)


def func(x,scale,shape):
    """ modified weibull distribution function"""
    return 1-np.exp(-pow(base=x/scale,exp=shape))

def take_percentile(values: list[float], per: int):
    """reduce list to top 25 percent"""
    p75 = np.percentile(values, per)
    return [i for i in values if i >= p75]  

def weibull_fit(intensites:list[float], info:Tuple):
    """ 
    Calculate histogram values for intensities. Fit the function. Plot data as histogram and line. Plot fitted CDF as line.
    Exception for RuntimeError (The least-squares minimization fails) and ValueError (ydata or xdata contain NaNs).
    min_intensity prevents fitting with not enough data.
    """
    _, ax = plt.subplots(nrows=1, ncols=1, figsize=(6,6))
    n, bins, _ = ax.hist(intensites, bins=np.arange(0,20,0.25), density=True, cumulative=True, histtype='stepfilled', alpha=0.2)
    xdata = bins[:-1]
    ydata = n[:]
    try:
        if len(intensites) >= min_intensity_values:
            popt, _ = curve_fit(func, xdata, ydata, p0=(1,3))
            plt.plot(xdata, ydata, 'b-', label='data') # data as line
            plt.plot(xdata, func(xdata, *popt), 'r-', label=f'fit: scale={round(popt[0],3)}, shape={round(popt[1],3)}') # fitted line
            plt.legend()
            # plt.savefig(f"images/{my_config}/fit_ID{info[0]}_DRY{min_dry_period}_PER{min_percentile}_WS{info[1]}.png", dpi=300, bbox_inches="tight")            
            if popt[1] >= 0.00001: # prevents data points in the lower left corner
                return popt
    except (RuntimeError, ValueError):
        pass
    return (False,False)

def calc_params(datadict):
    """
    Calculate parameters for each station and windowsize
    return params with shape: {"id":[(scale_10min, shape_10min), ... , (scale_6h,shape_6h)]}
    """
    params:dict = {}
    for station_i in datadict.keys():
        ws_values: list = []
        for ws in range(len(datadict[station_i])):
            intensities = datadict[station_i][ws]
            if intensities != []:
                # reduce intensities to 75. percentile
                intensities = take_percentile(intensities, min_percentile)
                # fit weibull
                scale,shape = weibull_fit(intensities, info=(station_i,ws))
                ws_values.append((scale,shape))
            params[station_i] = ws_values
    return params

z1_params = calc_params(z1)
z2_params = calc_params(z2)
z3_params = calc_params(z3)

# save zone dictionaries to files
with open(f'metdata/parameters/intensities_{my_config}_z1_DRY{min_dry_period}_PER{min_percentile}.pkl', 'wb') as f:
    pickle.dump(z1_params, f)
with open(f'metdata/parameters/intensities_{my_config}_z2_DRY{min_dry_period}_PER{min_percentile}.pkl', 'wb') as f:
    pickle.dump(z2_params, f)
with open(f'metdata/parameters/intensities_{my_config}_z3_DRY{min_dry_period}_PER{min_percentile}.pkl', 'wb') as f:
    pickle.dump(z3_params, f)

print("Done")