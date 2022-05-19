from scipy import stats 
import matplotlib.pyplot as plt
import numpy as np
import proplot as pplt

from read_intensities import read_intensities
# read zone data
z1, z2, z3 = read_intensities()

data = z1[1]

# plot histogram of data
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6,6))
ax.hist(data, bins=50, density=True, cumulative=False, histtype='stepfilled', alpha=0.2)

# fit distribution
# `loc`: initial guess of the distribution's location parameter.
# `scale`: initial guess of the distribution's scale parameter.
# shape parameter beta: 0.5
# scale parameter: je kleiner, desto steiler und weiter links
a,b,c,d = stats.exponweib.fit(data, scale=1, loc=1)
print("scale: ", a, "shape: ", b, "other: ", c, d)

# plot Weibull fit
x = np.arange(0,20,0.1)
fitted_values = stats.exponweib.pdf(x,a,b,c,d)
ax.set_xlim([-1,20])
ax.plot(x, fitted_values, lw=0.5, c="red")
plt.savefig("images/Weibull_z1.png", dpi=300, bbox_inches="tight")

# plot box plot (todo: side by side for each zone)
dict1 = z1
fig2, ax2 = plt.subplots(nrows=1, ncols=1, figsize=(8,4))
# labels, data = [*zip(*dict1.items())]
labels, data = dict1.keys(), dict1.values()
plt.boxplot(data)
plt.xticks(range(1, len(labels) + 1), labels)
plt.savefig("images/boxplot_z1.png", dpi=300, bbox_inches="tight")