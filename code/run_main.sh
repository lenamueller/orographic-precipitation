#!/bin/bash

# exit on first error
set -e


# explaination of arguments:
# 1) my_config = area of interest
# 2) min_dry_period = dry period length between independent storms
# 3) min_percentile = percentile to be fitted
# 4) min_event_length = min event length of independent storms to extract ordinary events
# 5) min_intensity_values = min number of values needed for fitting Weibull
# 6) first_timesteps = number of durations to plot (10 min, 20 min, 30 min, 1 h, 2 h, 3 h, 6 h)


python code/main.py ERZGEBIRGE 36 70 3 15 5 & 
# python code/main.py HARZ 36 70 3 15 5 & 
# python code/main.py SCHWARZWALD 36 70 3 15 5 & 