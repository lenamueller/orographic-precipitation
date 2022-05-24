import matplotlib.pyplot as plt
import proplot as pplt

from reading_functions import read_parameters, read_station_heights

from MYCONFIG import my_config, min_dry_period, min_percentile, first_timesteps


z1_params, z2_params, z3_params = read_parameters(my_config, min_dry_period, min_percentile)
z_params = [z1_params, z2_params, z3_params]

height_dict = read_station_heights(my_config)

pplt.rc.update(grid=True, titleloc='uc', titleweight='bold', titlecolor='grey', labelweight='bold', labelcolor='grey')
fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(10,6), sharex=True, sharey=True)

labels = ["Tiefland [0 - 200 m AMSL]", "Hügelland [200 - 400 m AMSL]", "Gebirge [400 m AMSL <]"]
markers = [".", "s", "^"]
colors = ["k", "b", "g"]

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
            par_30 = par[2]
            par_60 = par[3]
            # plot non false values
            if (False not in par_10):
                ax[0,0].scatter(h, par[0][0], marker=markers[z], c=colors[z])
                ax[1,0].scatter(h, par[0][1], marker=markers[z], c=colors[z])
            if (False not in par_30):                
                ax[0,1].scatter(h, par[2][0], marker=markers[z], c=colors[z])
                ax[1,1].scatter(h, par[2][1], marker=markers[z], c=colors[z])
            if (False not in par_60):
                ax[0,2].scatter(h, par[3][0], marker=markers[z], c=colors[z])
                ax[0,2].scatter(h, par[3][1], marker=markers[z], c=colors[z])

ax[0,0].set_title("10 min")          
ax[0,1].set_title("30 min")          
ax[0,2].set_title("60 min")
ax[0,0].set_ylabel("scale $\lambda$")          
ax[1,0].set_ylabel("shape $\kappa$")   

# todo: legend, last plot empty?, fix error list index out of range for HARZ; SCHWARZWALD
# r i in range(len(labels)):
#     ax[2].scatter(-1,-1,c=colors[i],label=labels[i])
# plt.legend()
plt.savefig(f"images/Scatter/Scatter2_{my_config}_DRY{min_dry_period}_PER{min_percentile}.png", dpi=600, bbox_inches="tight")
print("Done")