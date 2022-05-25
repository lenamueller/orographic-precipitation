import matplotlib.pyplot as plt
import proplot as pplt

from reading_functions import read_parameters
from MYCONFIG import my_config, min_dry_period, min_percentile, first_timesteps


z1_params, z2_params, z3_params = read_parameters(my_config, min_dry_period, min_percentile)
z_params = [z1_params, z2_params, z3_params]



pplt.rc.update(grid=True, titleloc='uc', titleweight='bold', titlecolor='grey')
fig, ax = plt.subplots(ncols=3, figsize=(10,3), sharex=True, sharey=True)

labels = ["10 min", "20 min", "30 min", "60 min"]
colors = ["#ffc300", "#ff5733", "#c70039", "#571845"]
titles = ["Tiefland [0 - 200 m AMSL]", "Hügelland [200 - 400 m AMSL]", "Gebirge [400 m AMSL <]"]

for z in range(3):
    params_dict = z_params[z]
    # read tuples for every station
    for _,tuples_i in params_dict.items():
        x_lineplot, y_lineplot = [],[]
        # select only first durations (10min, 20min, 30min, 60min, ...)
        tuples_i = tuples_i[:first_timesteps]
        # select number of data spots per station
        if len(tuples_i) > len(colors):
            n = len(colors)
        else:
            n = n = len(tuples_i)
        for t in range(n):
            # remove (False,False) tuples
            if tuples_i[t] != (False,False):
                ax[z].scatter(tuples_i[t][0], tuples_i[t][1], marker=".", s=8, c=colors[t], zorder=3)
                x_lineplot.append(tuples_i[t][0])
                y_lineplot.append(tuples_i[t][1])
        # plot lines between scatter
        ax[z].plot(x_lineplot, y_lineplot, linewidth=0.5, alpha=0.5, color="gray", zorder=1)
    ax[z].set_title(titles[z])
    ax[z].set_xscale('log', base=2)
    ax[z].set_xlim([0,9])
    ax[z].set_ylim([0,3])
    

for i in range(len(labels)):
    ax[2].scatter(-1,-1,c=colors[i],label=labels[i])

plt.legend()
plt.savefig(f"images/Scatter/Scatter_{my_config}_DRY{min_dry_period}_PER{min_percentile}.png", dpi=600, bbox_inches="tight")

print("Done")