import random
from math import floor

import numpy.random as nprand

from Judge import mixed_nash_equi_finder_make_support, nash_equi_finder

mixed_nash_count = [0 for _ in range(30)]
max_support = [0 for _ in range(14)]
tables = []
count = 0
with open("tests.txt", 'w') as file:
    while count < 6:
        acc = nprand.normal(7, 3, 1)
        acc = floor(acc[0])
        if 12 > acc > 3:
            n = random.randint(2, acc - 2)
            m = acc - n
            table = [[[random.randint(1, 4), random.randint(1, 4)] for _ in range(m)] for _ in range(n)]
            mixeds = mixed_nash_equi_finder_make_support(table, True, [], nash_equi_finder(table))
            # max_s = 0
            # if mixed_nash_count[len(mixeds)] < 2:
            #     for i in range(len(mixeds) - 1):
            #         s = 0
            #         for j in range(len(mixeds[i])):
            #             if mixeds[i][j] > 0:
            #                 s += 1
            #         if max_s < s:
            #             max_s = s
            #     if max_support[max_s] < max_s:
            #         max_support[max_s] += 1
            #         file.write(str(table) + '\n')
            #         count += 1
            #         mixed_nash_count[len(mixeds)] += 1
            # print(len(mixeds), max_s)
            if len(mixeds) > 0:
                file.write(str(table) + '\n')
                count += 1
                print(count, acc, len(mixeds), mixeds, nash_equi_finder(table))
    # while count < 8:
    #     acc = nprand.normal(11, 3, 1)
    #     acc = floor(acc[0])
    #     if 14 > acc > 10:
    #         n = random.randint(2, acc - 2)
    #         m = acc - n
    #         table = [[[random.randint(-20, 20), random.randint(-20, 20)] for _ in range(m)] for _ in range(n)]
    #
    #         mixeds = mixed_nash_equi_finder_make_support(table, True, [], nash_equi_finder(table))
    #         # max_s = 0
    #         # if mixed_nash_count[len(mixeds)] < 4:
    #         #     for i in range(len(mixeds) - 1):
    #         #         s = 0
    #         #         for j in range(len(mixeds[i])):
    #         #             if mixeds[i][j] > 0:
    #         #                 s += 1
    #         #         if max_s < s:
    #         #             max_s = s
    #         #     if max_support[max_s] < max_s + 2:
    #         #         max_support[max_s] += 1
    #         #         file.write(str(table) + '\n')
    #         #         count += 1
    #         #         mixed_nash_count[len(mixeds)] += 1
    #         # print(len(mixeds), max_s)
    #         if len(mixeds) > 0:
    #             file.write(str(table) + '\n')
    #             count += 1
    #             print(count, acc, len(mixeds), mixeds, nash_equi_finder(table))
    while count < 12:
        acc = nprand.normal(11, 3, 1)
        acc = floor(acc[0])
        if 12 > acc > 7:
            n = random.randint(2, acc - 2)
            m = acc - n
            table = [[[random.randint(-200, 200), random.randint(-200, 200)] for _ in range(m)] for _ in range(n)]
            mixeds = mixed_nash_equi_finder_make_support(table, True, [], nash_equi_finder(table))
            min_s = acc
            if len(mixeds) > 0:
                for i in range(len(mixeds)):
                    s = 0
                    for j in range(len(mixeds[i])):
                        if mixeds[i][j] > 0:
                            s += 1
                    if min_s > s:
                        min_s = s
                if min_s >= 5:
                    file.write(str(table) + '\n')
                    count += 1
                    print(count, acc, len(mixeds), mixeds, nash_equi_finder(table))
print(mixed_nash_count)
print(max_support)
