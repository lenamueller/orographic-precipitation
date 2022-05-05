import numpy as np
import matplotlib.pyplot as plt
import proplot as pplt


def del_missing_values(list):
    list_corr = []
    c = 0
    for i in list:
        if i == -999.00:
            c+=1
        else:
            list_corr.append(i)
    print(f"-999 occur {c} times")
    return list_corr

def del_zeros(list):
    list_corr = []
    for i in list:
        if i != 0:
            list_corr.append(i)
    return list_corr

files = ["data/DWD_RR_Stationen/p_z1", "data/DWD_RR_Stationen/p_z2", "data/DWD_RR_Stationen/p_z3"]

# consistency analysis
# wertebereich
# primär statistiken
# 25% percentil auswählen

# read data
data_z1 = np.loadtxt(files[0])
data_z2 = np.loadtxt(files[1])
data_z3 = np.loadtxt(files[2])

# correct data
data_corr_1 = del_missing_values(data_z1)
data_corr_2 = del_missing_values(data_z2)
data_corr_3 = del_missing_values(data_z3)

data_corr_1 = del_zeros(data_corr_1)
data_corr_2 = del_zeros(data_corr_2)
data_corr_3 = del_zeros(data_corr_3)

# plot data
f, ((ax1, ax2, ax3)) = plt.subplots(ncols=3, figsize=(12,4))
ax1.hist(data_corr_1, bins=50)
ax2.hist(data_corr_2, bins=50)
ax3.hist(data_corr_3, bins=50)
ax1.set_title("0 - 200 m ASL")
ax2.set_title("200 - 400 m ASL")
ax3.set_title("400 m ASL <")
for ax in [ax1, ax2, ax3]:
    ax.set_yscale('log')
plt.savefig("images/hist_sn.png", dpi=300, bbox_inches = "tight")