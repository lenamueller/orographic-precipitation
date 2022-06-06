import pickle
import numpy as np
import surpyval as surv
# from lifelines.fitters.weibull_fitter import WeibullFitter
from reading_functions import read_intensities


def func(x,scale,shape):
    """ modified weibull distribution function"""
    return 1-np.exp(-pow(base=x/scale,exp=shape))

def get_censored_list(values: list[float], per: int):
    """reduce list to top 25 percent"""
    nb_values = len(values)
    p75 = np.percentile(values, per)
    censored = np.zeros(nb_values)
    for i in range(nb_values):
        if values[i] < p75:
            censored[i] = -1
    return censored

def get_parameters(my_config, min_percentile, min_dry_period, min_intensity_values):
    # read zone data
    z1, z2, z3 = read_intensities(my_config, min_dry_period)
    
    # calculate scale and shape parameters
    for i in range(3):
        datadicts = [z1, z2, z3]
        datadict = datadicts[i]
        params:dict = {}
        for station_i in datadict.keys():
            ws_values: list = []
            for ws in range(len(datadict[station_i])):
                p = ()
                intensities = datadict[station_i][ws]
                if intensities not in [[],[0.0],[0]] and len(intensities) >= min_intensity_values:
                    # left-censoring up to 75 % percentile
                    censored = get_censored_list(intensities, min_percentile)
                    # fit weibull
                    model = surv.Weibull.fit(intensities, c=censored)
                    scale, shape = model.params
                    p = (scale,shape)
                ws_values.append(p)
            params[station_i] = ws_values
        print("i", i, params.keys())

        # save zone dictionary to files
        with open(f'metdata/parameters/intensities_{my_config}_z{i+1}_DRY{min_dry_period}_PER{min_percentile}.pkl', 'wb') as f:
            pickle.dump(params, f)
        
    print("S2_get_patameters.py done")