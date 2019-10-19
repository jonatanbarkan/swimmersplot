import csv
from typing import Union, List

from matplotlib import pyplot as plt
from numpy import array


def adjust_legend(legend: Union[plt.legend, List[plt.legend]]):
    if not isinstance(legend, list):
        legend = [legend]
    for lg in legend:
        lg.get_frame().set_linewidth(1.0)
        lg.get_frame().set_edgecolor('k')


def split_spines(axes):
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.spines['left'].set_position(('outward', 10))
    axes.spines['bottom'].set_position(('outward', 10))


def read_csv(file_path, func, delimiter=';'):
    temp = list()
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            temp.append(array([func(r) if r else "" for r in row]))
    return temp


def label_bin_values(bins, name):
    names = ['{} < {}'.format(name, bins[0])] + \
            ['{} <= {} < {}'.format(bins[i], name, bins[i + 1]) for i in range(len(bins) - 1)] \
            + ['{} < {}'.format(bins[-1], name)]
    return names
