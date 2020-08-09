#! /usr/bin/env python
"""
Read two csv files and print the results of RQ1
"""
import sys
import csv


def init_results():
    return {'total_projects': 0, 'total_projects_faults': 0,
            'total_projects_min': 0, 'total_projects_mout': 0,
            'total_projects_ov': 0, 'total_min': 0, 'total_mout': 0,
            'total_ov': 0
            }

def read_results(input_file, results):
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0].startswith('project'):
                continue
            row[1], row[2], row[3] = (int(row[1]), int(row[2]), int(row[3]))
            results['total_projects'] += 1
            if row[1] > 0 or row[2] > 0 or row[3] > 0:
                results['total_projects_faults'] += 1
            if row[1] > 0:
                results['total_projects_min'] += 1
            if row[2] > 0:
                results['total_projects_mout'] += 1
            if row[3] > 0:
                results['total_projects_ov'] += 1
            results['total_min'] += row[1]
            results['total_mout'] += row[2]
            results['total_ov'] += row[3]
    return results

gradle_file = sys.argv[1]
make_file = sys.argv[2]
make = init_results()
gradle = init_results()
make = read_results(make_file, make)
gradle = read_results(gradle_file, gradle)

header = ["Build System", "Projects", "MIN", "MOUT", "OV"]
make_row = [
    "make",
    "{}/{}".format(make['total_projects_faults'], make['total_projects']),
    make['total_projects_min'],
    make['total_projects_mout'],
    make['total_projects_ov']
]
gradle_row = [
    "gradle",
    "{}/{}".format(gradle['total_projects_faults'], gradle['total_projects']),
    gradle['total_projects_min'],
    gradle['total_projects_mout'],
    gradle['total_projects_ov']
]
row_format ="{:>15}" * 5
print(row_format.format(*header))
print(row_format.format(*gradle_row))
print(row_format.format(*make_row))
print("")
gradle_message = ("Gradle: {} related to incremental builds ({} MIN, {} MOUT) "
                  "and {} related to parallel builds (OV)").format(
    gradle['total_min'] + gradle['total_mout'],
    gradle['total_min'], gradle['total_mout'], gradle['total_ov']
)
make_message = "Make: {} MIN and {} OV".format(
    make['total_min'], make['total_ov']
)
print(gradle_message)
print(make_message)
