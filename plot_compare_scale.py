import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from copy import deepcopy
import pandas as pd
import numpy as np

plt.rcParams['font.family'] = 'Open Sans'

URL = 'https://data.giss.nasa.gov/gistemp/graphs/graph_data/Global_Mean_Estimates_based_on_Land_and_Ocean_Data/graph.txt'

df = pd.read_fwf(
    URL,
    skiprows=(0, 1, 2, 4),
    index_col=0,
)
year_mean = df['No_Smoothing']
max_abs = np.max(np.abs(year_mean))


fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)


cmap = plt.get_cmap('RdBu_r')

rectangles = [Rectangle((year, 0), 1, 1) for year in year_mean.index]


col1 = PatchCollection(rectangles)
col1.set_array(year_mean)
col1.set_cmap(cmap)
col2 = deepcopy(col1)
col2.set_clim(-max_abs, max_abs)

ax1.add_collection(col1)
ax2.add_collection(col2)

for ax in (ax1, ax2):
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlim(1880, 2019)

ax1.set_title('Color scale over full range')
ax2.set_title('Color scale centered at 0°C')
fig.colorbar(col1, ax=ax1, label='GTA / °C')
fig.colorbar(col2, ax=ax2, label='GTA / °C')
fig.tight_layout()
fig.savefig('comparison.png', bbox_inches='tight')
