from scipy import stats 
import matplotlib.pyplot as plt
import numpy as np
import proplot as pplt
import sys
import math

from read_intensities import read_intensities_st


region = "ERZ"

# read zone data
z1, z2, z3 = read_intensities_st(region)

print("z1 number stations:", len(z1.keys()), z1.keys())
print("z2 number stations:", len(z2.keys()), z2.keys())
print("z3 number stations:", len(z3.keys()), z3.keys())

para_z1:dict = {"shape":[[],[],[],[],[],[],[]],"scale":[[],[],[],[],[],[],[]]}
para_z2:dict = {"shape":[[],[],[],[],[],[],[]],"scale":[[],[],[],[],[],[],[]]}
para_z3:dict = {"shape":[[],[],[],[],[],[],[]],"scale":[[],[],[],[],[],[],[]]}

# fit Weibull
for st, i in zip(z1.keys(),np.arange(0,7,1)):
    intensities = z1[st]
    for i in range(7):
        if intensities[i]:
            scale,shape,c,d = stats.exponweib.fit(intensities[i])
            para_z1["scale"][i].append(scale)
            para_z1["shape"][i].append(shape)
            # print(f"\nPARAMETER station {st} Z1: scale {scale}, shape {shape}")
        else:
            print(f"\nPARAMETER station {st} Z1 can not be calculated because list is empty.")

for st, i in zip(z2.keys(),np.arange(0,7,1)):
    intensities = z2[st]
    for i in range(7):
        if intensities[i]:
            scale,shape,c,d = stats.exponweib.fit(intensities[i])
            para_z2["scale"][i].append(scale)
            para_z2["shape"][i].append(shape)
            # print(f"\nPARAMETER station {st} Z2: scale {scale}, shape {shape}")
        else:
            # print(f"\nPARAMETER station {st} Z2 can not be calculated because list is empty.")
            continue
            
for st, i in zip(z3.keys(),np.arange(0,7,1)):
    intensities = z3[st]
    for i in range(7):
        if intensities[i]:
            scale,shape,c,d = stats.exponweib.fit(intensities[i])
            para_z3["scale"][i].append(scale)
            para_z3["shape"][i].append(shape)
            # print(f"\nPARAMETER station {st} Z3: scale {scale}, shape {shape}")
        else:
            # print(f"\nPARAMETER station {st} Z3 can not be calculated because list is empty.")
            continue

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(10,4))

ax[0].scatter(para_z1["scale"][0], para_z1["shape"][0],s=5, marker = "^", c="b", alpha = 0.8, label="Z1 10 min")
ax[0].scatter(para_z1["scale"][2], para_z1["shape"][2],s=5, marker = "o", c="b", alpha = 0.8, label="Z1 30 min")
ax[0].scatter(para_z1["scale"][3], para_z1["shape"][3],s=5, marker = "o", facecolor='none', edgecolor="b", alpha = 0.8, label="Z1 1 h")
ax[0].scatter(para_z2["scale"][0], para_z2["shape"][0],s=5, marker = "^", c="g", alpha = 0.1, label="Z2 10 min")
ax[0].scatter(para_z2["scale"][2], para_z2["shape"][2],s=5, marker = "o", c="g", alpha = 0.1, label="Z2 30 min")
ax[0].scatter(para_z2["scale"][3], para_z2["shape"][3],s=5, marker = "o", facecolor='none', edgecolor="g", alpha = 0.1, label="Z2 1 h")
ax[0].scatter(para_z3["scale"][0], para_z3["shape"][0],s=5, marker = "^", c="r", alpha = 0.1, label="Z3 10 min")
ax[0].scatter(para_z3["scale"][2], para_z3["shape"][2],s=5, marker = "o", c="r", alpha = 0.1, label="Z3 30 min")
ax[0].scatter(para_z3["scale"][3], para_z3["shape"][3],s=5, marker = "o", facecolor='none', edgecolor="r", alpha = 0.1, label="Z3 1 h")

ax[1].scatter(para_z1["scale"][0], para_z1["shape"][0],s=5, marker = "^", c="b", alpha = 0.1, label="Z1 10 min")
ax[1].scatter(para_z1["scale"][2], para_z1["shape"][2],s=5, marker = "o", c="b", alpha = 0.1, label="Z1 30 min")
ax[1].scatter(para_z1["scale"][3], para_z1["shape"][3],s=5, marker = "o", facecolor='none', edgecolor="b", alpha = 0.1, label="Z1 1 h")
ax[1].scatter(para_z2["scale"][0], para_z2["shape"][0],s=5, marker = "^", c="g", alpha = 0.8, label="Z2 10 min")
ax[1].scatter(para_z2["scale"][2], para_z2["shape"][2],s=5, marker = "o", c="g", alpha = 0.8, label="Z2 30 min")
ax[1].scatter(para_z2["scale"][3], para_z2["shape"][3],s=5, marker = "o", facecolor='none', edgecolor="g", alpha = 0.8, label="Z2 1 h")
ax[1].scatter(para_z3["scale"][0], para_z3["shape"][0],s=5, marker = "^", c="r", alpha = 0.1, label="Z3 10 min")
ax[1].scatter(para_z3["scale"][2], para_z3["shape"][2],s=5, marker = "o", c="r", alpha = 0.1, label="Z3 30 min")
ax[1].scatter(para_z3["scale"][3], para_z3["shape"][3],s=5, marker = "o", facecolor='none', edgecolor="r", alpha = 0.1, label="Z3 1 h")

ax[2].scatter(para_z1["scale"][0], para_z1["shape"][0],s=5, marker = "^", alpha = 0.1,c="b", label="Z1 10 min")
ax[2].scatter(para_z1["scale"][2], para_z1["shape"][2],s=5, marker = "o", facecolor='none', alpha = 0.1,edgecolor="b", label="Z1 30 min")
ax[2].scatter(para_z1["scale"][3], para_z1["shape"][3],s=5, marker = "s", alpha = 0.1,c="b", label="Z1 1 h")
ax[2].scatter(para_z2["scale"][0], para_z2["shape"][0],s=5, marker = "^", alpha = 0.1,c="g", label="Z2 10 min")
ax[2].scatter(para_z2["scale"][2], para_z2["shape"][2],s=5, marker = "o", facecolor='none', alpha = 0.1,edgecolor="g", label="Z2 30 min")
ax[2].scatter(para_z2["scale"][3], para_z2["shape"][3],s=5, marker = "s", alpha = 0.1,c="g", label="Z2 1 h")
ax[2].scatter(para_z3["scale"][0], para_z3["shape"][0],s=5, marker = "^", c="r", alpha = 0.8, label="Z3 10 min")
ax[2].scatter(para_z3["scale"][2], para_z3["shape"][2],s=5, marker = "o", c="r", alpha = 0.8, label="Z3 30 min")
ax[2].scatter(para_z3["scale"][3], para_z3["shape"][3],s=5, marker = "o", facecolor='none', edgecolor="r", alpha = 0.8, label="Z3 1 h")

ax[0].set_title("Z1: 0 - 200 m AMSL")
ax[1].set_title("Z2: 200 - 400 m AMSL")
ax[2].set_title("Z3: 400 m AMSL <")
ax[0].set_xlabel(r'scale $\lambda$')
ax[0].set_ylabel(r'shape $\kappa$')
plt.setp(ax, xlim=[0,7], ylim=[0.2,1.2])
# plt.setp(ax, xlim=[0,15], ylim=[0,2])
ax[0].legend()
ax[1].legend()
ax[2].legend()
plt.savefig(f"images/Erzgebirge/Scatter_{region}_2.png", dpi=400, bbox_inches="tight")

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