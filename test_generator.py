import random
from math import floor

import numpy.random as nprand

from Judge import mixed_nash_equi_finder_make_support

mixed_nash_count = [0 for _ in range(2250)]
max_support = [0 for _ in range(14)]
tables = []
count = 0
with open("tests.txt", 'w') as file:
    while count < 10:
        acc = nprand.normal(7, 3, 1)
        acc = floor(acc[0])
        if 14 > acc > 3:
            n = random.randint(2, acc - 2)
            m = acc - n
            table = [[[random.randint(1, 4), random.randint(1, 4)] for _ in range(m)] for _ in range(n)]
            mixeds = mixed_nash_equi_finder_make_support(table, True, [])
            max_s = 0
            if mixed_nash_count[len(mixeds)] < 2:
                for i in range(len(mixeds) - 1):
                    s = 0
                    for j in range(len(mixeds[i])):
                        if mixeds[i][j] > 0:
                            s += 1
                    if max_s < s:
                        max_s = s
                if max_support[max_s] < max_s:
                    max_support[max_s] += 1
                    file.write(str(table) + '\n')
                    count += 1
                    mixed_nash_count[len(mixeds)] += 1
            print(len(mixeds), max_s)
    while count < 20:
        acc = nprand.normal(11, 3, 1)
        acc = floor(acc[0])
        if 14 > acc > 10:
            n = random.randint(2, acc - 2)
            m = acc - n
            table = [[[random.randint(1, 4), random.randint(1, 4)] for _ in range(m)] for _ in range(n)]
            mixeds = mixed_nash_equi_finder_make_support(table, True, [])
            max_s = 0
            if mixed_nash_count[len(mixeds)] < 4:
                for i in range(len(mixeds) - 1):
                    s = 0
                    for j in range(len(mixeds[i])):
                        if mixeds[i][j] > 0:
                            s += 1
                    if max_s < s:
                        max_s = s
                if max_support[max_s] < max_s + 2:
                    max_support[max_s] += 1
                    file.write(str(table) + '\n')
                    count += 1
                    mixed_nash_count[len(mixeds)] += 1
            print(len(mixeds), max_s)
    while count < 25:
        acc = nprand.normal(9, 3, 1)
        acc = floor(acc[0])
        if 14 > acc > 3:
            n = random.randint(2, acc - 2)
            m = acc - n
            table = [[[random.randint(-20, 20), random.randint(-20, 20)] for _ in range(m)] for _ in range(n)]
            mixeds = mixed_nash_equi_finder_make_support(table, True, [])
            max_s = 0
            if mixed_nash_count[len(mixeds)] < 6:
                for i in range(len(mixeds) - 1):
                    s = 0
                    for j in range(len(mixeds[i])):
                        if mixeds[i][j] > 0:
                            s += 1
                    if max_s < s:
                        max_s = s
                if max_support[max_s] < max_s + 3:
                    max_support[max_s] += 1
                    file.write(str(table) + '\n')
                    count += 1
                    mixed_nash_count[len(mixeds)] += 1
            print(len(mixeds), max_s)
print(mixed_nash_count)
print(max_support)
