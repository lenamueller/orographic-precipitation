from scipy import stats 
from scipy.optimize import curve_fit
import sys
import matplotlib.pyplot as plt
import numpy as np
import proplot as pplt

from read_intensities import read_intensities_st
from enums import CONFIG


my_config = CONFIG.ERZGEBIRGE.name

# read zone data -> dict : {"id:[intensities], ..."}
z1, z2, z3 = read_intensities_st(my_config)

# define curve to fit
def func(x,scale,shape):
    """ modified weibull distribution function"""
    return 1-np.exp(-pow(base=x/scale,exp=shape))

def weibull_fit(intensites:list[float], info):
    # create plot
    _, ax = plt.subplots(nrows=1, ncols=1, figsize=(6,6))
    # calculate histogram values
    n, bins, _ = ax.hist(intensites, bins=np.arange(0,20,0.25), density=True, cumulative=True, histtype='stepfilled', alpha=0.2)
    # modifiy histogram range (min. 4 mm precipitation)
    xdata = bins[20:-1]
    ydata = n[20:]
    # fit function
    try:
        popt, _ = curve_fit(func, xdata, ydata)
        print("Optimal values for the parameters (popt)", popt, "(station/ws)", info, "number of values", len(intensites))
        # plot
        plt.plot(xdata, ydata, 'b-', label='data') # data as line
        plt.plot(xdata, func(xdata, *popt), 'r-', label=f'fit: scale={round(popt[0],3)}, shape={round(popt[1],3)}') # fitted line
        plt.legend()
        plt.savefig(f"images/{my_config}/fit_st{info[0]}_ws{info[1]}.png", dpi=300, bbox_inches="tight")
        return popt
    except RuntimeError:
        print("\nThe least-squares minimization fails.\n")
        return (False,False)        
    except ValueError:
        print("\nydata or xdata contain NaNs.\n")
        return (False,False)        
    
# create new dict for {"id":[(scale_10min, shape_10min), ... , (scale_6h,shape_6h)]}
def calc_params(datadict):
    params:dict = {}
    for station_i in datadict.keys():
        ws_values: list = []
        for ws in range(len(datadict[station_i])):
            intensities = datadict[station_i][ws]
            scale,shape = weibull_fit(intensities, info=(station_i,ws))
            ws_values.append((scale,shape))
        params[station_i] = ws_values
    return params

z1_params = calc_params(z1)
z2_params = calc_params(z2)
z3_params = calc_params(z3)

print("z1_params", z1_params)
print("z2_params", z2_params)
print("z3_params", z3_params)