#! /usr/bin/env python
"""
Read three csv files and print the results of RQ2 (Table 2)
"""
import sys
import csv
import operator



def read_results(input_file):
    results = {}
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0].startswith('project'):
                continue
            row[0], row[1], row[2], row[3] = (
                row[0], int(row[1]), int(row[2]), int(row[3])
            )
            results[row[0]] = [row[1], row[2], row[3]]
    return results


def find_fixes(make_pre_fixes, gradle_pre_fixes, after_fixes):
    res = []
    for i, (k, v) in enumerate(after_fixes.items()):
        faults = make_pre_fixes.get(k)
        build_system = 'make'
        try:
            if faults is None:
                faults = gradle_pre_fixes[k]
                build_system = 'gradle'
            mn = max(faults[0] - v[0], 0)
            mout = max(faults[1] - v[1], 0)
            ov = max(faults[2] - v[2], 0)
            total = mn + mout + ov
        except:
            print("**Project {}: failed**".format(k))
            mn = 0
            mout = 0
            ov = 0
            total = 0
        res.append([
            k,
            build_system,
            total,
            mn,
            mout,
            ov
        ])
    return res


gradle_pre_file = sys.argv[1]
make_pre_file = sys.argv[2]
after_file = sys.argv[3]
gradle_pre_faults = read_results(gradle_pre_file)
make_pre_faults = read_results(make_pre_file)
after_faults = read_results(after_file)

header = ["Project", "Build System", "Total", "MIN", "MOUT", "OV"]
rows = []
rows.extend(find_fixes(make_pre_faults, gradle_pre_faults, after_faults))
totals = [
    len(rows), "Total",
    sum(row[2] for row in rows),
    sum(row[3] for row in rows),
    sum(row[4] for row in rows),
    sum(row[5] for row in rows)
]
rows = sorted(rows, key=operator.itemgetter(1, 2), reverse=True)
rows.append(totals)
row_format = "{:<40}" +  "{:>20}" + "{:>5}" * 4
print(row_format.format(*header))
for r in rows:
    print(row_format.format(*r))
with open("rq2_out.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(rows)
