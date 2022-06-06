import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import exponweib


fig,axs = plt.subplots(2,2,sharex=True, sharey=True, figsize=(10,10))

x = np.linspace(0,20,1000)
# plains
axs[0,0].plot(x, exponweib.pdf(x, 10, 1.1), c='k', lw=1, alpha=0.6, label='10 min')
axs[0,0].plot(x, exponweib.pdf(x, 5, 0.9), c='y', lw=1, alpha=0.6, label='1h')
axs[0,0].plot(x, exponweib.pdf(x, 1.6, 0.7), c='r', lw=1, alpha=0.6, label='6h')
axs[0,0].set_title("Plains")

# hills
axs[0,1].plot(x, exponweib.pdf(x, 10, 1.1), c='k', lw=1, alpha=0.6, label='10 min')
axs[0,1].plot(x, exponweib.pdf(x, 5, 1.1), c='y', lw=1, alpha=0.6, label='1h')
axs[0,1].plot(x, exponweib.pdf(x, 1.6, 1.1), c='r', lw=1, alpha=0.6, label='6h')
axs[0,1].set_title("Hills")

# mountains
axs[1,0].plot(x, exponweib.pdf(x, 10, 1), c='k', lw=1, alpha=0.6, label='10 min')
axs[1,0].plot(x, exponweib.pdf(x, 5, 1.4), c='y', lw=1, alpha=0.6, label='1h')
axs[1,0].plot(x, exponweib.pdf(x, 5, 1), c='y', linestyle="dotted", lw=1, alpha=0.6, label='1h with shape=1')
axs[1,0].plot(x, exponweib.pdf(x, 1.6, 1), c='r', lw=1, alpha=0.6, label='6h')
axs[1,0].set_title("Mountains")
axs[1,0].set_xlabel("Intensität [mm/h]")
axs[1,0].set_ylabel("Wahrscheinlichkeitsdichte")

# rift
axs[1,1].plot(x, exponweib.pdf(x, 5, 0.7), c='k', lw=1, alpha=0.6, label='10 min')
axs[1,1].plot(x, exponweib.pdf(x, 2, 0.8), c='y', lw=1, alpha=0.6, label='1h')
axs[1,1].plot(x, exponweib.pdf(x, 0.5, 0.9), c='r', lw=1, alpha=0.6, label='6h')
axs[1,1].set_title("Rift")

for i in range(2):
    for j in range(2):
        axs[i,j].legend()

plt.xlim([0,7])
plt.savefig("images/Parameters_Fig2.png", dpi=300, bbox_inches="tight")


import numpy as np
from surpyval import Weibull
from lifelines.fitters.weibull_fitter import WeibullFitter


intensities = np.array([1,2,3,1,2,3,2,10,12,2,1,2,1,1])
intensities2 = np.array([1,2,3,1,2,3,2,2,1,2,1,1])
censored = np.array([0,0,0,0,0,0,0,-1, -1, 0, 0, 0, 0, 0])
censored2 = np.array([0,0,0,0,0,0,0,0,0,0,0,0])

# model = Weibull.fit(x=intensities, c=censored)
# print(model.params) # lamda, kappa
# model = Weibull.fit(x=intensities, tl=censored)
# print(model.params) # lamda, kappa
# model = Weibull.fit(x=intensities2, tl=censored2)
# print(model.params) # lamda, kappa

