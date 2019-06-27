import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import pandas as pd

plt.rcParams['font.family'] = 'Open Sans'

URL = 'https://data.giss.nasa.gov/gistemp/graphs/graph_data/Global_Mean_Estimates_based_on_Land_and_Ocean_Data/graph.txt'

df = pd.read_fwf(
    URL,
    skiprows=(0, 1, 2, 4),
    index_col=0,
)
year_mean = df['No_Smoothing']


fig = plt.figure(figsize=(12, 3), constrained_layout=True)
ax = fig.add_subplot(1, 1, 1)


cmap = plt.get_cmap('RdBu_r')

rectangles = [Rectangle((year, 0), 1, 1) for year in year_mean.index]
col = PatchCollection(rectangles)
col.set_array(year_mean)
col.set_cmap(cmap)
ax.add_collection(col)

ax.set_ylim(0, 1)
ax.set_yticks([])
ax.set_xlim(1880, 2019)
fig.colorbar(col, ax=ax, label='GTA / °C')
fig.savefig('bars.png')
