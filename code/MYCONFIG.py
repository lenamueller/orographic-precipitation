from enum import Enum


class CONFIG(Enum):
    ERZGEBIRGE = 1
    HARZ = 2
    SCHWARZWALD = 3
    THUERINGERWALD = 4


# ! configure ! area of interest
my_config = CONFIG.SCHWARZWALD.name

# ! configure ! number of 10min - time steps  -> 36 (6h), 30 (5h) 24 (4h), 18 (3h)
min_dry_period = 36        

# ! configure ! focus on right-tail characteristics
min_percentile = 0

# minimum lenth for independent storms to reduce noise
min_event_length = 3

# minimum number of data points for fitting
min_intensity_values = 20

# how many durations should be plotted (10min, 20min, 30min, 1h, 2h, 3h, 6h)
# duraions_min = [10,20,30,60,120,180,260]
first_timesteps = 5