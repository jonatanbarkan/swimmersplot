from collections import namedtuple

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt, patches as mpatches
from matplotlib import style
from matplotlib.collections import LineCollection

from utils import split_spines, adjust_legend

style.use('seaborn-paper')

color_dict = dict(under='r', drop='y', both='darkorange', normal='b')
base_name = 'EF'
under = 50
drop = 10
color_label_dict = dict(
    under='{} < {}'.format(base_name, under),
    drop='{} < Decline'.format(drop),
    both='{} < {}'.format(base_name, under) + ', ' + '{} < Decline'.format(drop),
    normal='Normal {}'.format(base_name))
marker_dict = {
    'cessation of treatment': "s",
    'disease progression, resume treatment': "$>>$",
    'resume treatment': ">",
    'temporary cessation': "$||$",
}


def select_color(d, u):
    if d and u:
        return color_dict['both']
    if d:
        return color_dict['under']
    if u:
        return color_dict['drop']
    return color_dict['normal']


if __name__ == '__main__':
    dfs = pd.read_excel('demo.xlsx', sheet_name=None, header=None, )
    dfs = {k.lower(): df for k, df in dfs.items()}
    months = dfs['months']
    values = dfs['values']
    types = dfs['types'].fillna('')

    Point = namedtuple('Point', 'x y kind')
    points = []
    lines = []
    colors = []
    kinds = set()
    M = 0
    for i, (m, v, t) in enumerate(zip(months.values, values.values, types.values)):
        current_patient = i + 1
        m = m[np.isfinite(m)]
        v = v[np.isfinite(v)]
        length = len(m)
        current_month = m[0]
        last_month = m[-1]
        first_value = v[0]
        v_drop = first_value - v > drop
        v_under = v < under
        current_drop = v_drop[0]
        current_under = v_under[0]
        current_color = select_color(current_drop, current_under)
        if length > M:
            M = length
        for j in range(length):
            # add point for markers
            try:
                k = t[j].strip()
                if k:
                    points.append(Point(m[j], current_patient, k))
                    kinds.add(k)
            except IndexError:
                pass
            dr = current_drop != v_drop[j]
            un = current_under != v_under[j]
            if dr or un:
                lines.append([(current_month, current_patient), (m[j], current_patient)])
                colors.append(current_color)
                current_month = m[j]
                current_under = v_under[j]
                current_drop = v_drop[j]
                current_color = select_color(dr, un)
        if current_month != last_month:
            lines.append([(current_month, current_patient), (last_month, current_patient)])
            colors.append(current_color)

    kinds = list(kinds)

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111)
    alpha = 0.5
    lc = LineCollection(lines, colors=colors, linewidths=10)
    lc.set_alpha(alpha)
    ax.add_collection(lc)
    # ax.autoscale()
    split_spines(ax)
    ax.set_xlabel('Months')
    ax.set_ylabel('Patients')
    for p in points:
        ax.plot(p.x, p.y, marker=marker_dict[p.kind], c='k', markeredgewidth=1, markeredgecolor='k')
    values_handle = [mpatches.Patch(color=c, label=color_label_dict[l], alpha=alpha) for (l, c) in color_dict.items()]
    marker_handle = [plt.plot([], [], marker=mark, ms=10, ls="", mec=None, color='k', label=kind, markeredgewidth=1, markeredgecolor='k')[0] for kind, mark in marker_dict.items()]
    lg = plt.legend(handles=values_handle + marker_handle, loc='lower right')
    adjust_legend(lg)
    ax.add_artist(lg)
    # plt.pause(1)
    plt.show()
