#! /usr/bin/env python3

import fileinput


atimes = []
btimes = []
for line in fileinput.input():
    line = line.strip()
    t = tuple(line.split(','))

    if len(t) == 2:
        atimes.append(float(t[0]))
        btimes.append(float(t[1]))
    if len(t) == 1:
        atimes.append(float(t[0]))

def avg(arr):
    return sum(arr) / len(arr)

if len(btimes) > 0:
    print(avg(atimes), avg(btimes))
else:
    print(avg(atimes))
