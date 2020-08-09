#! /usr/bin/env python
"""
Read CSV file of fixed projects
"""

import sys


if len(sys.argv) != 2:
    print('You must provide the path to csv file of fixed projects')
    exit(1)


row_format = "{:<3}" + "{:<33}" + "{:>2}" + "{:>70}"
with open(sys.argv[1], 'r') as f:
    for (i, line) in enumerate(f):
        line = line.strip()
        project, _, _, build_system, bug_report = tuple(line.split(','))

        if i:
            print(row_format.format(*[i, project, build_system, bug_report]))
        else:
            print(row_format.format(*['#', project, build_system, bug_report]))
