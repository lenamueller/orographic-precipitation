import matplotlib.pyplot as plt
import proplot as pplt
from scipy import stats
import numpy as np 

from reading_functions import read_parameters, read_station_heights

from main import my_config, min_dry_period, min_percentile


z1_params, z2_params, z3_params = read_parameters(my_config, min_dry_period, min_percentile)
z_params = [z1_params, z2_params, z3_params]

height_dict = read_station_heights(my_config)

pplt.rc.update(grid=True, titleloc='uc', titleweight='bold', titlecolor='grey', labelweight='bold', labelcolor='grey', labelsize=10)
fig, ax = plt.subplots(nrows=2, ncols=4, figsize=(12,8), sharex=False, sharey=False)
fig.subplots_adjust(wspace=0.35, hspace=0.15)

titles:list[str]=["10 min", "30 min", "60 min"]
markers = [".", "s", "^"]
colors = ["dimgrey", "g", "b"]
markersizes = [5,4,5]

scale_list:list[list[float]] = [[],[],[],[],[],[]]
shape_list:list[list[float]] = [[],[],[],[],[],[]]
scale_height_list:list[list[float]] = [[],[],[],[],[],[]]
shape_height_list:list[list[float]] = [[],[],[],[],[],[]]

for z in range(3):
    params_dict = z_params[z]
    # read tuples for every station
    for station_i,tuples_i in params_dict.items():
        if (station_i in height_dict.keys()) and (tuples_i != (False, False)):
            # get height of station
            h = height_dict[station_i]    
            # get scale and shape of station for 10 min, 30 min, 60 min
            par = params_dict[station_i]
            par_10 = par[0]
            par_20 = par[1]
            par_30 = par[2]
            par_60 = par[3]
            par_120 = par[4]
            if (False not in par_10):
                ax[0,0].plot(h, par[0][0], marker=markers[z], c=colors[z], markersize=markersizes[z])
                ax[1,0].plot(h, par[0][1], marker=markers[z], c=colors[z], markersize=markersizes[z])
                scale_list[0].append(par_10[0])
                shape_list[0].append(par_10[1])
                scale_height_list[0].append(h)
                shape_height_list[0].append(h)
            if (False not in par_20):
                scale_list[1].append(par_20[0])
                shape_list[1].append(par_20[1])
                scale_height_list[1].append(h)
                shape_height_list[1].append(h)
            if (False not in par_30):                
                ax[0,1].plot(h, par[2][0], marker=markers[z], c=colors[z], markersize=markersizes[z])
                ax[1,1].plot(h, par[2][1], marker=markers[z], c=colors[z], markersize=markersizes[z])
                scale_list[2].append(par_30[0])
                shape_list[2].append(par_30[1])
                scale_height_list[2].append(h)
                shape_height_list[2].append(h)
            if (False not in par_60):
                ax[0,2].plot(h, par[3][0], marker=markers[z], c=colors[z], markersize=markersizes[z])
                ax[1,2].plot(h, par[3][1], marker=markers[z], c=colors[z], markersize=markersizes[z])
                scale_list[3].append(par_60[0])
                shape_list[3].append(par_60[1])
                scale_height_list[3].append(h)
                shape_height_list[3].append(h)
            if (False not in par_120):
                scale_list[4].append(par_120[0])
                shape_list[4].append(par_120[1])
                scale_height_list[4].append(h)
                shape_height_list[4].append(h)

for i in range(3):
    ax[0,i].set_ylim(0,7)
    ax[1,i].set_ylim(0,2)
    ax[0,i].set_title(titles[i])    
    ax[1,i].set_xlabel("elevation [m AMSL]")
    for j in range(2):
        ax[j,i].set_xlim(0,1000)

           
ax[0,0].set_ylabel("scale $\lambda$")          
ax[1,0].set_ylabel("shape $\kappa$")
ax[0,3].set_ylabel("Sen's slope [x10⁻³]")          
ax[1,3].set_ylabel("Sen's slope [x10⁻³]")
ax[1,3].set_xlabel("duration [min]")

# Theil-Sen Regression
slopes:list[float] = []
intercepts:list[float] = []
x  = np.arange(0,950,1)

# scale
# 10min
sen_coeff = stats.theilslopes(scale_list[0], scale_height_list[0])
slopes.append(sen_coeff[0])
intercepts.append(sen_coeff[1])
ax[0,0].plot(x, sen_coeff[0]*x+sen_coeff[1], linestyle="--", linewidth=1.5, color="k")
# 20min
sen_coeff = stats.theilslopes(scale_list[1], scale_height_list[1])
slopes.append(sen_coeff[0])
intercepts.append(sen_coeff[1])
# 30min
sen_coeff = stats.theilslopes(scale_list[2], scale_height_list[2])
slopes.append(sen_coeff[0])
intercepts.append(sen_coeff[1])
ax[0,1].plot(x, sen_coeff[0]*x+sen_coeff[1], linestyle="--", linewidth=1.5, color="k")
# 60 min
sen_coeff = stats.theilslopes(scale_list[3], scale_height_list[3])
slopes.append(sen_coeff[0])
intercepts.append(sen_coeff[1])
ax[0,2].plot(x, sen_coeff[0]*x+sen_coeff[1], linestyle="--", linewidth=1.5, color="k")
# 120 min
if scale_list[4] != []:
    sen_coeff = stats.theilslopes(scale_list[4], scale_height_list[4])
    slopes.append(sen_coeff[0])
    intercepts.append(sen_coeff[1])

durs = [10,20,30,60,120]
slopes = [x*1000 for x in slopes]
ax[0,3].plot(np.arange(4), slopes, marker=".", markersize=12, c="grey")

slopes:list[float] = []

# shape
# 10min
sen_coeff = stats.theilslopes(shape_list[0], shape_height_list[0])
slopes.append(sen_coeff[0])
intercepts.append(sen_coeff[1])
ax[1,0].plot(x, sen_coeff[0]*x+sen_coeff[1], linestyle="--", linewidth=1.5, color="k")
# 20min
sen_coeff = stats.theilslopes(shape_list[1], shape_height_list[1])
slopes.append(sen_coeff[0])
intercepts.append(sen_coeff[1])
# 30min
sen_coeff = stats.theilslopes(shape_list[2], shape_height_list[2])
slopes.append(sen_coeff[0])
intercepts.append(sen_coeff[1])
ax[1,1].plot(x, sen_coeff[0]*x+sen_coeff[1], linestyle="--", linewidth=1.5, color="k")
# 60 min
sen_coeff = stats.theilslopes(shape_list[3], shape_height_list[3])
slopes.append(sen_coeff[0])
intercepts.append(sen_coeff[1])
ax[1,2].plot(x, sen_coeff[0]*x+sen_coeff[1], linestyle="--", linewidth=1.5, color="k")
# 120 min
if scale_list[4] != []:
    sen_coeff = stats.theilslopes(shape_list[4], shape_height_list[4])
    slopes.append(sen_coeff[0])
    intercepts.append(sen_coeff[1])

slopes = [x*1000 for x in slopes]
ax[1,3].plot(np.arange(4), slopes, marker=".", markersize=12, c="grey")

for i in range(2):
    ax[i,3].set_xticks(np.arange(5),["10", "20", "30", "60", "120"])

ax[0,0].scatter(-1,-1,marker=".", s=200, c="dimgrey", label="Tiefland")
ax[0,0].scatter(-1,-1,marker="s", c="g", label="Hügelland")
ax[0,0].scatter(-1,-1,marker="^", c="b", label="Gebirge")
ax[0,0].legend(loc=4)

# todo fix error list index out of range for HARZ; SCHWARZWALD

plt.savefig(f"images/Scatter/Scatter2_{my_config}_DRY{min_dry_period}_PER{min_percentile}.png", dpi=600, bbox_inches="tight")
print("Done")
