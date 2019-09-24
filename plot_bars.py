import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap
import pandas as pd
import requests
from io import StringIO
from argparse import ArgumentParser
import rdbu_uniform

URL = 'https://www.metoffice.gov.uk/hadobs/hadcrut4/data/current/time_series/HadCRUT.4.6.0.0.annual_ns_avg.txt'
FIRST = 1850
LAST = 2018  # inclusive

# Reference period for the center of the color scale
FIRST_REFERENCE = 1971
LAST_REFERENCE = 2000
LIM = 0.7

cmap = ListedColormap([
    '#deebf7',
    '#c6dbef',
    '#9ecae1',
    '#6baed6',
    '#4292c6',
    '#2171b5',
    '#08519c',
    '#08306b',
][::-1] + [
    '#fee0d2',
    '#fcbba1',
    '#fc9272',
    '#fb6a4a',
    '#ef3b2c',
    '#cb181d',
    '#a50f15',
    '#67000d',
])


parser = ArgumentParser()
parser.add_argument('outputfile')
parser.add_argument('--width', help='width in inches', default=4, type=float)
parser.add_argument('--height', help='height in inches', default=4, type=float)
parser.add_argument('--dpi', help='dots per inch', default=300, type=float)


if __name__ == '__main__':
    args = parser.parse_args()

    r = requests.get(URL)
    df = pd.read_fwf(
        StringIO(r.text),
        index_col=0,
        usecols=(0, 1),
        names=['year', 'anomaly'],
        header=None,
    )

    year_median = df.loc[FIRST:LAST, 'anomaly'].dropna()
    center = year_median.loc[FIRST_REFERENCE:LAST_REFERENCE].mean()

    fig = plt.figure(figsize=(args.width, args.height))

    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()

    rectangles = [
        Rectangle((year, 0), 1, 1)
        for year in year_median.loc[FIRST:LAST].index
    ]
    col = PatchCollection(rectangles)
    col.set_array(year_median)
    col.set_cmap(cmap)
    col.set_clim(center - LIM, center + LIM)

    ax.add_collection(col)

    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlim(FIRST, LAST + 1)

    fig.savefig(args.outputfile, dpi=args.dpi)
