import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset

from helperfunctions import windrichtung, calculate_euclidean_distance, read_track_list, i_j_indices_to_coord, get_color


# read radolan coorinates. lon: i_index_cell bzw. i_cell_center, lat: j_index_cell bzw. j_cell_center
fh = Dataset('data/radolan_coordinates.nc', mode='r')
lat = fh.variables['lat'][:] # lat(lat, lon) with shape = (1100,900) > bottom left coordinate
lon = fh.variables['lon'][:] # lon(lat, lon) with shape = (1100,900) > bottom left coordinate
lat_plot = fh.variables['lat_plot'][:] # lat_plot: lat_plot(lat, lon, corners) with shape = (1100, 900, 4)
lon_plot = fh.variables['lon_plot'][:] # lon_plot(lat, lon, corners) with shape = (1100, 900, 4)
   
# create map object
fig = plt.figure(figsize=(6,6))
map = Basemap(projection='laea', ellps='WGS84',
              lat_0 = (49.75+52)/2, lon_0 = (11+15.5)/2,
              resolution = 'h', area_thresh = 500,
              llcrnrlon=11, llcrnrlat=49.75, urcrnrlon=15.5, urcrnrlat=52)

# map.readshapefile("data/Grenze_SN_WGS84", 'Grenze_SN_WGS84', linewidth=0.5, zorder=8) # add saxony shape
map.drawmeridians(np.arange(0,360,1),color='silver', linewidth=0.3, dashes=(None,None),labels=[0,0,0,1], size=8, zorder=4)
map.drawparallels(np.arange(-90,90,0.5),color='silver', linewidth=0.3, dashes=(None, None),labels=[0,1,0,0], size=8, zorder=4)
map.drawcountries(linewidth=0.3, zorder=6)

# read cell tracks
track_cache = read_track_list("data/results_cells_200101010000_201612312355_Saxony_corr.trackslena", 
                              keylist=["i_cell_center", "j_cell_center", "v_max"])

# ! configure min distance (km) and min number of time steps (one time step has 5 min)
mindist = 20
mintimesteps = 5

counter = 0
for track in range(len(track_cache['i_cell_center'])):
    if track%500000 == 0:
        print("plot track no.", track)
    
    # calculate number of timesteps
    nb_timesteps = len(track_cache["i_cell_center"][track])
    if nb_timesteps >= mintimesteps:
        # calculate track distance        
        dist = calculate_euclidean_distance(track_cache,track)
        if dist >= mindist:    
            # calculate track direction
            i_in = track_cache["i_cell_center"][track]
            j_in = track_cache["j_cell_center"][track]
            wind_dir = windrichtung(dx = i_in[-1]-i_in[0], dy = j_in[-1]-j_in[0])
            # ! configure direction (erzgebirge 254°)
            if ((344-30 < wind_dir <344+30-360) # from north
                or (164-30< wind_dir < 154+30)): # from south
                # read precipitation intensity
                v_max_list = track_cache["v_max"][track]            
                # convert indices to lat/lon coordinates
                lats = []
                lons = []
                cols = []
                for timestep in range(nb_timesteps):
                    lat, lon = i_j_indices_to_coord(fh, i_in[timestep], j_in[timestep])
                    lats.append(lat)
                    lons.append(lon)
                    cols.append(get_color(v_max_list[timestep]))
                x, y = map(lons, lats)
                # plot track as black line and timesteps as colored dots
                counter += 1
                map.plot(x,y,linestyle="-", color="k", alpha=0.8, linewidth=0.2, zorder=1)
                for timestep in range(nb_timesteps):
                    map.plot(x[timestep],y[timestep],".", markersize=2, color=cols[timestep], fillstyle="full", zorder=2, alpha=0.7)

plt.title(f"n = {counter}", y=1, x=0.07, pad=-10, fontsize=10)
plt.savefig(f"tracks_{mindist}km_{mintimesteps}timesteps.png", dpi=600, bbox_inches='tight', transparent=False)