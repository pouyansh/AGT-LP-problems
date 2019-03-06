import random
from math import floor

import numpy.random as nprand

from Judge import mixed_nash_equi_finder_make_support

mixed_nash_count = [0 for _ in range(2250)]
tables = []
count = 0
with open("tests.txt", 'w') as file:
    while count < 15:
        acc = nprand.normal(7, 3, 1)
        acc = floor(acc[0])
        if 14 > acc > 3:
            n = random.randint(2, acc - 2)
            m = acc - n
            table = [[[random.randint(1, 5), random.randint(1, 5)] for _ in range(m)] for _ in range(n)]
            mixeds = mixed_nash_equi_finder_make_support(table, True, [])
            if mixed_nash_count[len(mixeds)] < 2:
                tables.append(table)
                file.write(str(table) + '\n')
                count += 1
                mixed_nash_count[len(mixeds)] += 1
            print(len(mixeds), table)
    while count < 20:
        acc = nprand.normal(11, 3, 1)
        acc = floor(acc[0])
        if 14 > acc > 10:
            n = random.randint(2, acc - 2)
            m = acc - n
            table = [[[random.randint(1, 4), random.randint(1, 4)] for _ in range(m)] for _ in range(n)]
            mixeds = mixed_nash_equi_finder_make_support(table, True, [])
            if mixed_nash_count[len(mixeds)] < 4:
                tables.append(table)
                file.write(str(table) + '\n')
                count += 1
                mixed_nash_count[len(mixeds)] += 1
            print(len(mixeds), table)
    while count < 25:
        acc = nprand.normal(9, 3, 1)
        acc = floor(acc[0])
        if 14 > acc > 3:
            n = random.randint(2, acc - 2)
            m = acc - n
            table = [[[random.randint(-20, 20), random.randint(-20, 20)] for _ in range(m)] for _ in range(n)]
            mixeds = mixed_nash_equi_finder_make_support(table, True, [])
            if mixed_nash_count[len(mixeds)] < 6:
                tables.append(table)
                file.write(str(table) + '\n')
                count += 1
                mixed_nash_count[len(mixeds)] += 1
            print(len(mixeds), table)
print(mixed_nash_count)
print(tables)