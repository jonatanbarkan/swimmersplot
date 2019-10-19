from collections import namedtuple

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt, patches as mpatches
from matplotlib import style

from utils import split_spines, adjust_legend, read_csv, label_bin_values, combine
from argparse import ArgumentParser
style.use('seaborn-paper')
colors = ['r', 'b', 'g', 'c', 'o']
markers = [">", "*", "s", '8', "P", "1"]

if __name__ == '__main__':
    dfs = pd.read_excel('demo.xlsx', sheet_name=None, header=None, )
    dfs = {k.lower(): df for k, df in dfs.items()}
    months = dfs['months']
    values = dfs['values']
    types = dfs['types'].fillna('')
    # months_path = 'months_demo.csv'
    # months = read_csv(months_path, int)
    # values_path = 'values_demo.csv'
    # values = read_csv(values_path, int)
    # types_path = 'types_demo.csv'
    # types = read_csv(types_path, str)

    base_name = 'EF'
    value_bins = [50]
    # kinds = ['a', 'b', 'c', 'dd']
    value_names = label_bin_values(value_bins, base_name)
    Point = namedtuple('Point', "patient month value binned kind")
    points = []
    kinds = set()
    M = 0
    for i, (m, v, t) in enumerate(zip(months.values, values.values, types.values)):
        print('patient {}'.format(i, ))
        m = m[np.isfinite(m)]
        v = v[np.isfinite(v)]
        length = len(m)
        if length > M:
            M = length
        binned_v = np.digitize(v, value_bins)
        for j in range(length):
            try:
                tp = t[j]
            except IndexError:
                tp = ""
            kinds.add(tp)
            points.append(Point(i + 1, m[j], v[j], binned_v[j], tp))
    kinds.remove("")
    kinds = list(kinds)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    count_patients = 0
    first = 0
    last_marker = -1
    for p1, p2 in zip(points[:-1], points[1:]):
        if p1.binned != p2.binned or p2.kind:
            if p2.kind:
                ax.plot(p2.month, p2.patient, marker=markers[kinds.index(p2.kind)], c='k', markeredgewidth=1, markeredgecolor='k')
                last_marker = p2.month
            if p1.patient == p2.patient:
                # ax.plot([first, p2.month], [p1.patient, p1.patient], c=colors[p1.binned], lw=10, alpha=0.3, solid_capstyle='projecting', solid_joinstyle='miter')
                ax.plot([first, p2.month], [p1.patient, p1.patient], c=colors[p1.binned], lw=10, alpha=0.3, solid_capstyle='projecting')
            first = p2.month + 1
        if p1.patient != p2.patient:
            count_patients += 1
            # ax.plot([first, max(last_marker, p1.month)], [p1.patient, p1.patient], c=colors[p1.binned], lw=10, alpha=0.3, solid_capstyle='projecting', solid_joinstyle='miter')
            ax.plot([first, max(last_marker, p1.month)], [p1.patient, p1.patient], c=colors[p1.binned], lw=10, alpha=0.3, solid_capstyle='projecting')
            first = 0
            last_marker = -1

    split_spines(ax)
    ax.set_xlabel('Months')
    ax.set_ylabel('Patients')

    values_handle = [mpatches.Patch(color=c, label=l, alpha=0.3) for (c, l) in zip(colors, value_names)]
    marker_handle = [plt.plot([], [], marker=mark, ms=10, ls="", mec=None, color='k', label=kind)[0] for mark, kind in zip(markers, kinds)]
    lg = plt.legend(handles=values_handle + marker_handle)
    adjust_legend(lg)
    ax.add_artist(lg)
    plt.pause(1)
    a = 0
