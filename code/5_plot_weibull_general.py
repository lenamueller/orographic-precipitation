import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import exponweib


fig = plt.figure(figsize=(5,5))
x = np.linspace(0,20,1000)
plt.plot(x, exponweib.pdf(x, 1, 1.0), c='k', lw=1, alpha=0.6, label='scale = 1, shape = 1.1')
plt.plot(x, exponweib.pdf(x, 1, 1.5), c='y', lw=1, alpha=0.6, label='scale = 1, shape = 1.5')
plt.plot(x, exponweib.pdf(x, 1, 0.5), c='r', lw=1, alpha=0.6, label='scale = 1, shape = 0.8')
plt.plot(x, exponweib.pdf(x, 5, 1), c='lightblue', lw=1, alpha=0.6, label='scale = 5, shape = 1')
plt.plot(x, exponweib.pdf(x, 2, 1), c='b', lw=1, alpha=0.6, label='scale = 2, shape = 1')
plt.xlabel("Intensität [mm/h]")
plt.ylabel("Wahrscheinlichkeitsdichte")
plt.legend(loc='best', frameon=False)
plt.xlim([0,7])
plt.savefig("images/parameters.png", dpi=300, bbox_inches="tight")

fig, ax = plt.subplots(1, 1)
x = np.linspace(0,20,1000)
ax.plot(x, exponweib.pdf(x, 10, 1.2), 'r-', lw=1, alpha=0.6, label='10min')
ax.plot(x, exponweib.pdf(x, 5, 1.4), 'b-', lw=1, alpha=0.6, label='1h')
ax.plot(x, exponweib.pdf(x, 1.5, 1), 'g-', lw=1, alpha=0.6, label='6h')
plt.xlabel("Intensität [mm/h]")
plt.ylabel("Wahrscheinlichkeitsdichte")
plt.title("Einfluss des scale-Parameters auf die Weibull PDF")
ax.legend(loc='best', frameon=False)
plt.savefig("images/1h.png", dpi=300, bbox_inches="tight")