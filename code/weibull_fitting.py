from scipy import stats 
import matplotlib.pyplot as plt
import numpy as np
import proplot as pplt
import sys
import math

from read_intensities import read_intensities_st
from enums import CONFIG


my_config = CONFIG.ERZ.name

# read zone data -> dict : {"id:[intensities], ..."}
z1, z2, z3 = read_intensities_st(my_config)
print("z1 number stations:", len(z1.keys()))
print("z2 number stations:", len(z2.keys()))
print("z3 number stations:", len(z3.keys()))

# fit Weibull
def fit_weibull(data):
    # create new dict for {"id":[(scale_10min, shape_10min), ... , (scale_6h,shape_6h)]}
    params:dict = {}
    for st, i in zip(data.keys(),np.arange(0,7,1)):
        intensities = data[st]
        ws_values = []
        for i in range(7):
            if intensities[i]:
                scale,shape,c,d = stats.exponweib.fit(intensities[i])
                ws_values.append((scale,shape))
                # print(f"\nPARAMETER station {st} Z1: scale {scale}, shape {shape}")
            else:
                print(f"\nPARAMETER station {st} Z1 can not be calculated because list is empty.")
        params[st] = ws_values
    return params        

para_z1 = fit_weibull(z1)
para_z2 = fit_weibull(z2)
para_z3 = fit_weibull(z3)

print(para_z1, type(para_z1))

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(10,4))

for st, vals in para_z1.items():
    ax[0].plot(vals[:3], linewidth=0.5, color="blue")
    # ax[0].scatter(vals[0], linewidth=0.5, color="blue", marker="^")
    # ax[0].scatter(vals[1], linewidth=0.5, color="blue", marker="o")
    # ax[0].scatter(vals[2], linewidth=0.5, color="blue", marker=".")
    # for tup in vals:
    #     scales, shapes = zip(*tup)
    #     ax[0].plot(vals)
    #     ax[0].plot(scales, shapes)
        


# ax[0].scatter(para_z1["scale"][0], para_z1["shape"][0],s=5, marker = "^", c="b", alpha = 0.8, label="Z1 10 min")
# ax[0].scatter(para_z1["scale"][2], para_z1["shape"][2],s=5, marker = "o", c="b", alpha = 0.8, label="Z1 30 min")
# ax[0].scatter(para_z1["scale"][3], para_z1["shape"][3],s=5, marker = "o", facecolor='none', edgecolor="b", alpha = 0.8, label="Z1 1 h")
# ax[0].scatter(para_z2["scale"][0], para_z2["shape"][0],s=5, marker = "^", c="g", alpha = 0.1, label="Z2 10 min")
# ax[0].scatter(para_z2["scale"][2], para_z2["shape"][2],s=5, marker = "o", c="g", alpha = 0.1, label="Z2 30 min")
# ax[0].scatter(para_z2["scale"][3], para_z2["shape"][3],s=5, marker = "o", facecolor='none', edgecolor="g", alpha = 0.1, label="Z2 1 h")
# ax[0].scatter(para_z3["scale"][0], para_z3["shape"][0],s=5, marker = "^", c="r", alpha = 0.1, label="Z3 10 min")
# ax[0].scatter(para_z3["scale"][2], para_z3["shape"][2],s=5, marker = "o", c="r", alpha = 0.1, label="Z3 30 min")
# ax[0].scatter(para_z3["scale"][3], para_z3["shape"][3],s=5, marker = "o", facecolor='none', edgecolor="r", alpha = 0.1, label="Z3 1 h")

# ax[1].scatter(para_z1["scale"][0], para_z1["shape"][0],s=5, marker = "^", c="b", alpha = 0.1, label="Z1 10 min")
# ax[1].scatter(para_z1["scale"][2], para_z1["shape"][2],s=5, marker = "o", c="b", alpha = 0.1, label="Z1 30 min")
# ax[1].scatter(para_z1["scale"][3], para_z1["shape"][3],s=5, marker = "o", facecolor='none', edgecolor="b", alpha = 0.1, label="Z1 1 h")
# ax[1].scatter(para_z2["scale"][0], para_z2["shape"][0],s=5, marker = "^", c="g", alpha = 0.8, label="Z2 10 min")
# ax[1].scatter(para_z2["scale"][2], para_z2["shape"][2],s=5, marker = "o", c="g", alpha = 0.8, label="Z2 30 min")
# ax[1].scatter(para_z2["scale"][3], para_z2["shape"][3],s=5, marker = "o", facecolor='none', edgecolor="g", alpha = 0.8, label="Z2 1 h")
# ax[1].scatter(para_z3["scale"][0], para_z3["shape"][0],s=5, marker = "^", c="r", alpha = 0.1, label="Z3 10 min")
# ax[1].scatter(para_z3["scale"][2], para_z3["shape"][2],s=5, marker = "o", c="r", alpha = 0.1, label="Z3 30 min")
# ax[1].scatter(para_z3["scale"][3], para_z3["shape"][3],s=5, marker = "o", facecolor='none', edgecolor="r", alpha = 0.1, label="Z3 1 h")

# ax[2].scatter(para_z1["scale"][0], para_z1["shape"][0],s=5, marker = "^", alpha = 0.1,c="b", label="Z1 10 min")
# ax[2].scatter(para_z1["scale"][2], para_z1["shape"][2],s=5, marker = "o", facecolor='none', alpha = 0.1,edgecolor="b", label="Z1 30 min")
# ax[2].scatter(para_z1["scale"][3], para_z1["shape"][3],s=5, marker = "s", alpha = 0.1,c="b", label="Z1 1 h")
# ax[2].scatter(para_z2["scale"][0], para_z2["shape"][0],s=5, marker = "^", alpha = 0.1,c="g", label="Z2 10 min")
# ax[2].scatter(para_z2["scale"][2], para_z2["shape"][2],s=5, marker = "o", facecolor='none', alpha = 0.1,edgecolor="g", label="Z2 30 min")
# ax[2].scatter(para_z2["scale"][3], para_z2["shape"][3],s=5, marker = "s", alpha = 0.1,c="g", label="Z2 1 h")
# ax[2].scatter(para_z3["scale"][0], para_z3["shape"][0],s=5, marker = "^", c="r", alpha = 0.8, label="Z3 10 min")
# ax[2].scatter(para_z3["scale"][2], para_z3["shape"][2],s=5, marker = "o", c="r", alpha = 0.8, label="Z3 30 min")
# ax[2].scatter(para_z3["scale"][3], para_z3["shape"][3],s=5, marker = "o", facecolor='none', edgecolor="r", alpha = 0.8, label="Z3 1 h")

ax[0].set_title("Z1: 0 - 200 m AMSL")
ax[1].set_title("Z2: 200 - 400 m AMSL")
ax[2].set_title("Z3: 400 m AMSL <")
ax[0].set_xlabel(r'scale $\lambda$')
ax[0].set_ylabel(r'shape $\kappa$')
plt.setp(ax, xlim=[0,20], ylim=[0.2,5])
# plt.setp(ax, xlim=[0,15], ylim=[0,2])
ax[0].legend()
ax[1].legend()
ax[2].legend()
plt.savefig(f"images/Erzgebirge/Scatter_{my_config}_new.png", dpi=400, bbox_inches="tight")

sys.exit()
# plotting example
data = z1[445][0]

# plot histogram of data
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6,6))
ax.hist(data, bins=50, density=True, cumulative=False, histtype='stepfilled', alpha=0.2)

# fit distribution
""" 
`loc`: initial guess of the distribution's location parameter.
`scale`: initial guess of the distribution's scale parameter.
"""
scale,shape,c,d = stats.exponweib.fit(data)
print("\nPARAMETER\nscale: ", scale, "\nshape: ", shape)

# plot Weibull fit
x = np.arange(0,20,0.1)
fitted_values = stats.exponweib.pdf(x,scale,shape,c,d)
ax.plot(x, fitted_values, lw=0.8, c="red")
plt.title(f"Weibull fitting (scale:{round(scale,3)}, shape: {round(shape,3)})")
plt.savefig("images/Erzgebirge/Weibull.png", dpi=300, bbox_inches="tight")