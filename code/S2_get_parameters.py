import pickle
import numpy as np
import surpyval as surv

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

def calc_params(datadict, min_intensity_values, min_percentile):
    """
    Calculate parameters for each station and windowsize
    return params with shape: {"id":[(scale_10min, shape_10min), ... , (scale_6h,shape_6h)]}
    """
    params:dict = {}
    for station_i in datadict.keys():
        ws_values: list = []
        for ws in range(len(datadict[station_i])):
            intensities = datadict[station_i][ws]
            if intensities not in [[],[0.0],[0]] and len(intensities) >= min_intensity_values:
                # left-censoring up to 75 % percentile
                censored = get_censored_list(intensities, min_percentile)
                # fit weibull
                model = surv.Weibull.fit(intensities, c=censored)
                scale, shape = model.params
                ws_values.append((scale,shape))
        params[station_i] = ws_values
    return params

def get_parameters(my_config, min_percentile, min_dry_period, min_intensity_values):
    # read zone data
    z1, z2, z3 = read_intensities(my_config, min_dry_period)

    # calculate scale and shape parameters
    z1_params = calc_params(z1, min_intensity_values, min_percentile)
    z2_params = calc_params(z2, min_intensity_values, min_percentile)
    z3_params = calc_params(z3, min_intensity_values, min_percentile)

    # save zone dictionaries to files
    with open(f'metdata/parameters/intensities_{my_config}_z1_DRY{min_dry_period}_PER{min_percentile}.pkl', 'wb') as f:
        pickle.dump(z1_params, f)
    with open(f'metdata/parameters/intensities_{my_config}_z2_DRY{min_dry_period}_PER{min_percentile}.pkl', 'wb') as f:
        pickle.dump(z2_params, f)
    with open(f'metdata/parameters/intensities_{my_config}_z3_DRY{min_dry_period}_PER{min_percentile}.pkl', 'wb') as f:
        pickle.dump(z3_params, f)

    print("S2_get_patameters.py done")