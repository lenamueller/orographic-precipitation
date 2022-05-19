from pickletools import optimize
from scipy import stats 
import matplotlib.pyplot as plt
import numpy as np
import proplot as pplt
import sys

from read_intensities import read_intensities_st


# read zone data
z1, z2, z3 = read_intensities_st()

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
            print(f"\nPARAMETER station {st} Z2 can not be calculated because list is empty.")
            
for st, i in zip(z3.keys(),np.arange(0,7,1)):
    intensities = z3[st]
    for i in range(7):
        if intensities[i]:
            scale,shape,c,d = stats.exponweib.fit(intensities[i])
            para_z3["scale"][i].append(scale)
            para_z3["shape"][i].append(shape)
            # print(f"\nPARAMETER station {st} Z3: scale {scale}, shape {shape}")
        else:
            print(f"\nPARAMETER station {st} Z3 can not be calculated because list is empty.")


fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(6,6))
ax[0,0].scatter(para_z1["scale"][0], para_z1["shape"][0],s=5, c="b", label="10 min")
ax[0,0].scatter(para_z2["scale"][0], para_z2["shape"][0],s=5, c="g", label="10 min")
ax[0,0].scatter(para_z3["scale"][0], para_z3["shape"][0],s=5, c="r", label="10 min")

ax[1,0].scatter(para_z1["scale"][2], para_z1["shape"][2],s=5, c="b", label="30 min")
ax[1,0].scatter(para_z2["scale"][2], para_z2["shape"][2],s=5, c="g", label="30 min")
ax[1,0].scatter(para_z3["scale"][2], para_z3["shape"][2],s=5, c="r", label="30 min")

ax[0,1].scatter(para_z1["scale"][3], para_z1["shape"][3],s=5, c="b", label="1 h")
ax[0,1].scatter(para_z2["scale"][3], para_z2["shape"][3],s=5, c="g", label="1 h")
ax[0,1].scatter(para_z3["scale"][3], para_z3["shape"][3],s=5, c="r", label="1 h")

ax[1,1].scatter(para_z1["scale"][5], para_z1["shape"][5],s=5, c="b", label="3 h")
ax[1,1].scatter(para_z2["scale"][5], para_z2["shape"][5],s=5, c="g", label="3 h")
ax[1,1].scatter(para_z3["scale"][5], para_z3["shape"][5],s=5, c="r", label="3 h")


# for ws,lab in zip(range(7),[10,20,30,60,120,180,360]):
#     plt.scatter(para_z1["scale"][ws], para_z1["shape"][ws], c="b")
# for ws,lab in zip(range(7),[10,20,30,60,120,180,360]):
#     plt.scatter(para_z2["scale"][ws], para_z2["shape"][ws], c="g")
# for ws,lab in zip(range(7),[10,20,30,60,120,180,360]):
#     plt.scatter(para_z3["scale"][ws], para_z3["shape"][ws], c="r")

# for i in (ax[0,0],ax[1,0],ax[0,1],ax[1,1]):
#     ax.set_xlim([-2,10])
#     ax.set_ylim([-1,2])
#     ax.set_xlabel("scale")
#     ax.set_ylabel("shape")
#     plt.legend()
ax[0,0].set_title("10 min")
ax[1,0].set_title("30 min")
ax[0,1].set_title("1 h")
ax[1,1].set_title("3 h")
plt.setp(ax, xlim=[-2,10], ylim=[0,2.5], xlabel="scale", ylabel="shape")
    
plt.savefig("images/Erzgebirge/Scatter.png")

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