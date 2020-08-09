#! /usr/bin/env python3
import os
import sys
import matplotlib.pylab as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import ScalarFormatter, FuncFormatter


buildfs_data = sys.argv[1]
mkcheck_data = sys.argv[2]
buildfs_times = {}
with open(buildfs_data) as f:
    for l in f:
        l = l.strip()
        p, bt, _, fdt = l.split(',')
        bt = float(bt)
        fdt = float(fdt)
        buildfs_times[p] = (bt, fdt, bt + fdt)

mkcheck_times = {}
with open(mkcheck_data) as f:
    for l in f:
        l = l.strip()
        p, bt, ft, rt = l.split(',')
        bt = float(bt)
        ft = float(ft)
        rt = float(rt)
        mkcheck_times[p] = (bt, ft + rt, bt + rt + ft)


sns.set(style="whitegrid")
plt.rcParams['font.family'] = 'Ubuntu'
plt.rcParams['font.serif'] = 'Ubuntu'
plt.rcParams['font.monospace'] = 'Inconsolata Medium'
plt.rcParams['figure.figsize'] = (7.5, 4)
plt.rcParams['legend.fontsize'] = 14


total_dict = {}
for k, (bt, at, total) in mkcheck_times.items():
    values = buildfs_times.get(k)
    if values is None:
        continue
    _, _, total2 = values
    total_dict[k] = total / total2

from collections import OrderedDict
import operator

t_dict  = OrderedDict()
bt_dict = OrderedDict()
at_dict = OrderedDict()
for k, sp, in sorted(total_dict.items(), key=operator.itemgetter(1), reverse=True):
    bt1, at1, _ = mkcheck_times[k]
    bt2, at2, _ = buildfs_times[k]
    t_dict[k] = sp
    t = bt1 / bt2
    bt_dict[k] = t
    at_dict[k] = at1 / at2


def format_number(x, pos=None):
    if (x < 1):
        return '-' + str(int(1 / float(x))) + 'x'
    return str(int(x)) + 'x'


t_speedups = np.array(list(t_dict.values()))
b_speedups = np.array(sorted(list(bt_dict.values()), reverse=True))
a_speedups = np.array(sorted(list(at_dict.values()), reverse=True))

_, ax = plt.subplots()
plt.semilogy(a_speedups, label="Fault detection time", linewidth=3)
plt.semilogy(
    t_speedups, label="Overall time",
    color='#2C0D49', linestyle='--', linewidth=3
)
plt.semilogy(
    b_speedups, label="Build time",
    color='#796f82', linestyle='-.', linewidth=3
)
ax.yaxis.set_major_formatter(FuncFormatter(format_number))
ax.set_xticklabels([])
ax.legend(loc='upper right')
plt.ylabel('Speedup')
plt.xlabel('Projects')
plt.ylim([0.1, 110000])
plt.savefig(os.path.join(sys.argv[3], 'figure15.pdf'), format='pdf', bbox_inches='tight')

header = ["Phase", "Max", "mean", "Min"]
row1 = [
    "Build",
    "{:.2f}".format(np.max(b_speedups)),
    "{:.2f}".format(np.mean(b_speedups)),
    "{:.2f}".format(np.min(b_speedups))
]
row2 = [
    "Fault detection",
    "{:.2f}".format(np.max(a_speedups)),
    "{:.2f}".format(np.mean(a_speedups)),
    "{:.2f}".format(np.min(a_speedups))
]
row3 = [
    "Overall",
    "{:.2f}".format(np.max(t_speedups)),
    "{:.2f}".format(np.mean(t_speedups)),
    "{:.2f}".format(np.min(t_speedups))
]
header_format = "{:<20}" +  "{:>10}"  + "{:>10}" + "{:>10}"
row_format = "{:<20}" +  "{:>10}"  + "{:>10}" + "{:>10}"
print(header_format.format(*header))
print(row_format.format(*row1))
print(row_format.format(*row2))
print(row_format.format(*row3))
