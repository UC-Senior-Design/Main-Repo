# run locally, not on the pi
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import json

# Fixing random state for reproducibility
np.random.seed(19680801)

filename = ""
raw = []
with open(filename) as json_file:
    data = json.load(json_file)
    for scan_group in data:
        for scan in scan_group["cells"]:
            print(f"scan raw: {scan['distance']['raw']}")
            raw.append(scan['distance']['raw'])

n_bins = 20

n, bins, patches = plt.hist(raw, n_bins)
plt.show()

print(f"max: {max(raw)}\nmin: {min(raw)}\nrange: {max(raw) - min(raw)}")
