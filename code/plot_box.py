import matplotlib.pyplot as plt
import proplot as pplt

from read_intensities import read_intensities


# read zone data
z1, z2, z3 = read_intensities()

# create plot
fig = plt.figure(figsize=(6,4))
ax = fig.add_axes([0,0,1,1,])

# set properties for fliers and median
flierprops = dict(marker=None, markersize=0.1,linestyle='none', alpha=0.5)
medianprops = dict(linestyle='solid', linewidth=0.5, color='k')    

# plot boxes
bp=ax.boxplot([z1[1],z1[2],z1[3],z1[6],z1[12],z1[18],z1[36]], notch=True, patch_artist=True, 
              positions=[0,4,8,12,16,20,24], capprops=dict(color="b", linewidth=0.3), boxprops=dict(facecolor = "b", color="k", linewidth=0.2), whiskerprops=dict(color="b",linewidth=0.3), widths=0.75, showfliers=True, flierprops=flierprops, medianprops=medianprops)
bp=ax.boxplot([z2[1],z2[2],z2[3],z2[6],z2[12],z2[18],z2[36]], notch=True, patch_artist=True, 
              positions=[1,5,9,13,17,21,25], capprops=dict(color="g", linewidth=0.3), boxprops=dict(facecolor = "g", color="k", linewidth=0.2), whiskerprops=dict(color="g",linewidth=0.3), widths=0.75, showfliers=True, flierprops=flierprops, medianprops=medianprops)
bp=ax.boxplot([z3[1],z3[2],z3[3],z3[6],z3[12],z3[18],z3[36]], notch=True, patch_artist=True, 
              positions=[2,6,10,14,18,22,26], capprops=dict(color="r", linewidth=0.3), boxprops=dict(facecolor = "r", color="k", linewidth=0.2), whiskerprops=dict(color="r",linewidth=0.3), widths=0.75, showfliers=True, flierprops=flierprops, medianprops=medianprops)

# set label, limitation and ticks of axes
plt.xlabel('duration of life or window size [min]')
plt.ylabel('precipitation sum [mm]')
ax.set_ylim([0,21])
ax.set_xticks([1,5,9,13,17,21,25], ['10','20','30','60','120','180', '360'])

# legend
hB, = plt.plot([-1,-1],'b-', lw=0.7)
hG, = plt.plot([-1,-1],'g-', lw=0.7)
hR, = plt.plot([-1,-1],'r-', lw=0.7)
plt.legend((hB, hG, hR),('Z1', 'Z2', 'Z3'), loc=2, frameon=False)

fig.savefig("images/Erzgebirge/boxplot.png", dpi=400, bbox_inches='tight')