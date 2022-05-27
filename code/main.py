from enum import Enum
import sys

from S1_read_intensities import get_intensities
from S2_get_parameters import get_parameters
from S3_plot_scale_shape import plot_scale_shape

class CONFIG(Enum):
    ERZGEBIRGE = 1
    HARZ = 2
    SCHWARZWALD = 3
    THUERINGERWALD = 4

# ! configure ! area of interest
my_config = str(sys.argv[1])

# ! configure ! number of 10min - time steps  -> 36 (6h), 30 (5h) 24 (4h), 18 (3h)
min_dry_period = int(sys.argv[2])

# ! configure ! focus on right-tail characteristics
min_percentile = int(sys.argv[3])

# minimum lenth for independent storms to reduce noise
min_event_length = int(sys.argv[4])

# minimum number of data points for fitting
min_intensity_values = int(sys.argv[5])

# how many durations should be plotted (10min, 20min, 30min, 1h, 2h, 3h, 6h)
# duraions_min = [10,20,30,60,120,180,260]
first_timesteps = int(sys.argv[6])

if my_config not in CONFIG.__members__:
    print("Area not found")
else:
    print(my_config, min_dry_period, min_percentile, min_event_length, min_intensity_values, first_timesteps)
    get_intensities(my_config, min_dry_period, min_event_length)
    get_parameters(my_config, min_percentile, min_dry_period, min_intensity_values)
    plot_scale_shape(my_config, min_dry_period, min_percentile, first_timesteps)