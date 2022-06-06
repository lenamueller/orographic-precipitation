import matplotlib.pyplot as plt
import proplot as pplt

from reading_functions import read_parameters


def plot_scale_shape(my_config, min_dry_period, min_percentile, first_timesteps):
    # read parameters
    z1_params, z2_params, z3_params = read_parameters(my_config, min_dry_period, min_percentile)
    z_params = [z1_params, z2_params, z3_params]

    # configure plot
    pplt.rc.update(grid=True, titleloc='uc', titleweight='bold', titlecolor='grey', labelweight='bold', labelcolor="grey")
    _, axs = plt.subplots(ncols=3, figsize=(10,3), sharex=True, sharey=True)
    
    labels = ["10 min", "20 min", "30 min", "60 min"]
    colors = ["#ffc300", "#ff5733", "#c70039", "#571845"]
    titles = ["Tiefland [0 - 200 m AMSL]", "Hügelland [200 - 400 m AMSL]", "Gebirge [400 m AMSL <]"]

    for z in range(3):
        params_dict = z_params[z]

        # read tuples for every station
        for station_i,tuples_i in params_dict.items():
            x_lineplot, y_lineplot = [],[]

            # select only first durations (10min, 20min, 30min, 60min, ...)
            tuples_i = tuples_i[:first_timesteps]

            # select number of data spots per station
            nb_windowsizes = min(len(tuples_i), len(colors))
            # print("station", station_i, "windowsizes", nb_windowsizes, "tuples", tuples_i)
            if nb_windowsizes > 1:
                for duration in range(nb_windowsizes):
                    if tuples_i[duration] not in [(False,False), ()]:
                        axs[z].scatter(tuples_i[duration][0], tuples_i[duration][1], marker=".", s=8, c=colors[duration], zorder=3)
                        x_lineplot.append(tuples_i[duration][0])
                        y_lineplot.append(tuples_i[duration][1])

            # plot lines between scatter
            axs[z].plot(x_lineplot, y_lineplot, linewidth=0.5, alpha=0.5, color="gray", zorder=1)

        axs[z].set_title(titles[z])
        axs[z].set_xscale('log', base=2)
        axs[z].set_ylim([0,1.4])
        axs[z].set_xlim([0,18])
       

    axs[0].set_xlabel("scale $\lambda$")
    axs[0].set_ylabel("shape $\kappa$")

    for i in range(len(labels)):
        axs[2].scatter(-1,-1,c=colors[i],label=labels[i])
    plt.legend()

    plt.savefig(f"images/Scatter/Scatter_{my_config}_DRY{min_dry_period}_PER{min_percentile}.png", dpi=600, bbox_inches="tight")

    print("S3_plot_scale_shape.py done")