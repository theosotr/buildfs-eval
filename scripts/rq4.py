#! /usr/bin/env python3
# Compute the median and the average times spent on
# analyzing BuildFS programs, and detecting faults for
# both Gradle and Make projects.
import sys
import os


from statistics import median


gradle_performance= {
    'fdt': [],
    'at': []
}
make_performance= {
    'fdt': [],
    'at': []
}

gradle_file = sys.argv[1]
make_file = sys.argv[2]


def populate_data(path, data):
    with open(path) as f:
        for line in f:
            line = line.strip()
            _, _, at, fdt = tuple(line.split(','))
            data['fdt'].append(float(fdt))
            data['at'].append(float(at))


def avg(arr):
    return sum(arr) / len(arr)


populate_data(gradle_file, gradle_performance)
populate_data(make_file, make_performance)

header1 = ["", "Median", "Average"]
header2 = ["Phase", "Gradle", "Make", "Gradle", "Make"]
row1 = [
    "Analysis",
    "{:.2f}".format(median(gradle_performance['at'])),
    "{:.2f}".format(median(make_performance['at'])),
    "{:.2f}".format(avg(gradle_performance['at'])),
    "{:.2f}".format(avg(make_performance['at']))
]
row2 = [
    "Fault detection",
    "{:.2f}".format(median(gradle_performance['fdt'])),
    "{:.2f}".format(median(make_performance['fdt'])),
    "{:.2f}".format(avg(gradle_performance['fdt'])),
    "{:.2f}".format(avg(make_performance['fdt']))
]
header1_format = "{:>20}" +  "{:>15}" + "{:>20}"
header2_format = "{:>20}" +  "{:>10}" * 4
row_format = "{:>20}" +  "{:>10}" * 4
print(header1_format.format(*header1))
print(header2_format.format(*header2))
print(row_format.format(*row1))
print(row_format.format(*row2))
