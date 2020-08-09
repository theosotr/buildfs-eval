#! /usr/bin/env python3

import fileinput

import numpy as np


slowdowns = []
for line in fileinput.input():
    line = line.strip()
    _, base, buildfs = tuple(line.split(','))
    if not float(base):
        base = 1
    else:
        slowdowns.append(float(buildfs) / float(base))


print(str(round(np.percentile(slowdowns, 90), 2)) + "X")
