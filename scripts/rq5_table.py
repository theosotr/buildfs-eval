#! /usr/bin/env python3
# Give as input the directory with the traces, it must contains two directories
# make-projects and gradle-projects
# Print table 3 and create buildfs.times and mkcheck.times
import sys
import os
import csv
from statistics import median


def avg(l):
    return sum(l) / len(l)


# Print Table 3 and write buildfs.times and mkcheck.times
buildfs_times = {
    'bt': [],
    'fdt': [],
    'total': []
}

mkcheck_times = {
    'bt': [],
    'fdt': [],
    'total': []
}

mkcheck_projects = set()

def populate_data(path, data, mkcheck=False):
    with open(path) as f:
        for line in f:
            line = line.strip()
            if mkcheck:
                p, bt, ft, rt = tuple(line.split(','))
                data['bt'].append(float(bt))
                data['fdt'].append(float(ft) + float(rt))
                data['total'].append(float(bt) + float(ft) + float(rt))
                mkcheck_projects.add(p)
            else:
                p, bt, _, ft = tuple(line.split(','))
                # remove BuildFS entries where we do not have results for mkcheck.
                if p not in mkcheck_projects:
                    continue
                data['bt'].append(float(bt))
                data['fdt'].append(float(ft))
                data['total'].append(float(bt) + float(ft))


populate_data(sys.argv[2], mkcheck_times, mkcheck=True)
populate_data(sys.argv[1], buildfs_times)


header1 = ["", "Median", "Average"]
header2 = ["Phase", "BuildFS", "mkcheck", "BuildFS", "mkcheck"]
row1 = [
    "Build",
    "{:.2f}".format(median(buildfs_times['bt'])),
    "{:.2f}".format(median(mkcheck_times['bt'])),
    "{:.2f}".format(avg(buildfs_times['bt'])),
    "{:.2f}".format(avg(mkcheck_times['bt']))
]
row2 = [
    "Fault detection",
    "{:.2f}".format(median(buildfs_times['fdt'])),
    "{:.2f}".format(median(mkcheck_times['fdt'])),
    "{:.2f}".format(avg(buildfs_times['fdt'])),
    "{:.2f}".format(avg(mkcheck_times['fdt']))
]
row3 = [
    "Overall",
    "{:.2f}".format(median(buildfs_times['total'])),
    "{:.2f}".format(median(mkcheck_times['total'])),
    "{:.2f}".format(avg(buildfs_times['total'])),
    "{:.2f}".format(avg(mkcheck_times['total']))
]
header1_format = "{:>20}" +  "{:>15}" + "{:>20}"
header2_format = "{:>20}" +  "{:>10}" * 4
row_format = "{:>20}" +  "{:>10}" * 4
print(header1_format.format(*header1))
print(header2_format.format(*header2))
print(row_format.format(*row1))
print(row_format.format(*row2))
print(row_format.format(*row3))
