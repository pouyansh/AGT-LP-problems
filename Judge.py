from scipy.optimize import linprog


def check_if_nash(table, i, j):
    for k in range(len(table)):
        if table[k][j][0] > table[i][j][0]:
            return False
    for k in range(len(table[i])):
        if table[i][k][1] > table[i][j][1]:
            return False
    return True


def nash_equi_finder(table):
    output_list = []
    for i in range(len(table)):
        for j in range(len(table[i])):
            if check_if_nash(table, i, j):
                output_list.append([i, j])
    return output_list


def check_if_mixed_nash(table, result, first_support, second_support):
    first_persons_utility = 0
    for i in range(len(second_support)):
        first_persons_utility += result[len(first_support) + i] * table[first_support[0]][second_support[i]][0]
    for i in range(len(table)):
        temp_utility = 0
        for j in range(len(second_support)):
            temp_utility += result[len(first_support) + j] * table[i][second_support[j]][0]
        if first_persons_utility < temp_utility:
            return False

    second_persons_utility = 0
    for i in range(len(first_support)):
        second_persons_utility += result[i] * table[first_support[i]][second_support[0]][1]
    for i in range(len(table[0])):
        temp_utility = 0
        for j in range(len(first_support)):
            temp_utility += result[j] * table[first_support[j]][i][1]
        if second_persons_utility < temp_utility:
            return False

    return True


def make_probabilities_mixed_nash_equi(table, first_support, second_support):
    c = [0 for _ in range(len(first_support) + len(second_support))]
    c.append(-1)
    a_ub = []
    b_ub = []

    # p_i - delta >= 0 , q_i - delta >= 0
    for i in range(len(first_support) + len(second_support)):
        temp_list = [0 for _ in range(len(first_support) + len(second_support) + 1)]
        temp_list[i] = -1
        temp_list[len(temp_list) - 1] = 1
        a_ub.append(temp_list)
        b_ub.append(0)

    # delta >= 0
    temp_list = [0 for _ in range(len(first_support) + len(second_support))]
    temp_list.append(-1)
    a_ub.append(temp_list)
    b_ub.append(0)

    a_eq = []
    b_eq = []

    # sigma p_i = 1 and sigma q_i = 1
    temp_list = [0 for _ in range(len(first_support))]
    for i in range(len(second_support)):
        temp_list.append(1)
    temp_list.append(0)
    a_eq.append(temp_list)
    b_eq.append(1)
    temp_list = [1 for _ in range(len(first_support))]
    for i in range(len(second_support)):
        temp_list.append(0)
    temp_list.append(0)
    a_eq.append(temp_list)
    b_eq.append(1)

    # set restricts for q_is in order to make it possible for the first person to plat mixed
    for i in range(1, len(first_support)):
        temp_list = [0 for _ in range(len(first_support))]
        for j in range(len(second_support)):
            temp_list.append(
                table[first_support[i]][second_support[j]][0] - table[first_support[0]][second_support[j]][0])
        temp_list.append(0)
        a_eq.append(temp_list)
        b_eq.append(0)

    # set restricts for p_is in order to make it possible for the second person to plat mixed
    for i in range(1, len(second_support)):
        temp_list = []
        for j in range(len(first_support)):
            temp_list.append(
                table[first_support[j]][second_support[i]][1] - table[first_support[j]][second_support[0]][1])
        for j in range(len(second_support)):
            temp_list.append(0)
        temp_list.append(0)
        a_eq.append(temp_list)
        b_eq.append(0)

    if not a_ub == [] and not a_eq == []:
        res = linprog(c=c, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq)
    elif not a_ub == []:
        res = linprog(c=c, A_ub=a_ub, b_ub=b_ub)
    if res.success:
        if res.x[len(res.x) - 1] > 0:
            if check_if_mixed_nash(table, res.x, first_support, second_support):
                return True, res.x
    return False, []


def mixed_nash_equi_finder_make_support(table, is_first, support, nash_equis):
    output_list = []
    if is_first:
        current_support = [0 for _ in range(len(table))]
        temporary_variable = 1
        while temporary_variable < 2 ** len(table):
            temporary_variable += 1
            if current_support[0] == 0:
                current_support[0] = 1
            else:
                index = 0
                while current_support[index] == 1:
                    current_support[index] = 0
                    index += 1
                current_support[index] = 1
            result = mixed_nash_equi_finder_make_support(table, False, current_support, nash_equis)
            if result:
                for i in range(len(result)):
                    output_list.append(result[i])
    else:
        current_support = [0 for _ in range(len(table[0]))]
        temporary_variable = 1
        while temporary_variable < 2 ** len(table[0]):
            temporary_variable += 1
            if current_support[0] == 0:
                current_support[0] = 1
            else:
                index = 0
                while current_support[index] == 1:
                    current_support[index] = 0
                    index += 1
                current_support[index] = 1
            first_support = []
            for i in range(len(support)):
                if support[i] == 1:
                    first_support.append(i)
            second_support = []
            for i in range(len(current_support)):
                if current_support[i] == 1:
                    second_support.append(i)
            if len(first_support) > 1 or len(second_support) > 1:
                check = True
                for k in range(len(nash_equis)):
                    if nash_equis[k][0] in first_support:
                        if nash_equis[k][1] in second_support:
                            check = False
                if check:
                    # print(first_support, second_support, nash_equis)
                    state, result = make_probabilities_mixed_nash_equi(table, first_support, second_support)
                    if state:
                        result_list = []
                        index = 0
                        for i in range(len(support)):
                            if i in first_support:
                                result_list.append(round(result[index], 3))
                                index += 1
                            else:
                                result_list.append(0)
                        for i in range(len(current_support)):
                            if i in second_support:
                                result_list.append(round(result[index], 3))
                                index += 1
                            else:
                                result_list.append(0)

                        output_list.append(result_list)
    return output_list


def check_if_mixed_nash_equilibrium(table, mixed_strategy):
    # check if each element in support has the same utility
    p1_first_actions_utility = 0
    p1_first_actions_index = 0
    while mixed_strategy[p1_first_actions_index] == 0.0:
        p1_first_actions_index += 1
    for i in range(len(table[0])):
        p1_first_actions_utility += mixed_strategy[len(table) + i] * table[p1_first_actions_index][i][0]
    for j in range(p1_first_actions_index + 1, len(table)):
        if mixed_strategy[j] > 0:
            temp_utility = 0
            for i in range(len(table[0])):
                temp_utility += mixed_strategy[len(table) + i] * table[j][i][0]
            if abs(p1_first_actions_utility - temp_utility) > 1e-2:
                return False
    p2_first_actions_utility = 0
    p2_first_actions_index = len(table)
    while mixed_strategy[p2_first_actions_index] == 0.0:
        p2_first_actions_index += 1
    for i in range(len(table)):
        p2_first_actions_utility += mixed_strategy[i] * table[i][p2_first_actions_index - len(table)][1]
    for j in range(p2_first_actions_index + 1, len(table) + len(table[0])):
        if mixed_strategy[j] > 0:
            temp_utility = 0
            for i in range(len(table)):
                temp_utility += mixed_strategy[i] * table[i][j - len(table)][1]
            if abs(p2_first_actions_utility - temp_utility) > 1e-2:
                return False

    # print(p1_first_actions_index, p1_first_actions_utility, p2_first_actions_index, p2_first_actions_utility)
    # check if there is no strategy for each of them with higher utility
    # for p1
    c = []
    for i in range(len(table)):
        c_i = 0
        for j in range(len(table[0])):
            c_i += mixed_strategy[len(table) + j] * table[i][j][0]
        c.append(c_i)

    a_eq = []
    b_eq = []

    # sigma p_i = 1
    temp_row = [1 for _ in range(len(table))]
    a_eq.append(temp_row)
    b_eq.append(1)

    a_ub = []
    b_ub = []

    # p_i >= 0
    for i in range(len(table)):
        temp_row = [0 for _ in range(len(table))]
        temp_row[i] = -1
        a_ub.append(temp_row)
        b_ub.append(0)

    result = linprog(c, a_ub, b_ub, a_eq, b_eq)
    if not result.success:
        return False
    if result.fun > p1_first_actions_utility:
        return False

    # for p2
    c = []
    for i in range(len(table[0])):
        c_i = 0
        for j in range(len(table)):
            c_i += mixed_strategy[j] * table[j][i][1]
        c.append(c_i)

    a_eq = []
    b_eq = []

    # sigma q_i = 1
    temp_row = [1 for _ in range(len(table[0]))]
    a_eq.append(temp_row)
    b_eq.append(1)

    a_ub = []
    b_ub = []

    # q_i >= 0
    for i in range(len(table[0])):
        temp_row = [0 for _ in range(len(table[0]))]
        temp_row[i] = -1
        a_ub.append(temp_row)
        b_ub.append(0)

    result = linprog(c, a_ub, b_ub, a_eq, b_eq)
    if not result.success:
        return False
    if result.fun > p2_first_actions_utility:
        return False
    return True


def check_answer(table, out):
    nash_equis = nash_equi_finder(table)
    simple_nash = out[0]
    if len(simple_nash) != len(nash_equis):
        return False
    for i in range(len(simple_nash)):
        if not simple_nash[i] in nash_equis:
            return False
    mixed_nash = out[1]
    for i in range(len(out[2])):
        mixed_nash.append(out[2][i])
    if not check_if_mixed_nash_equilibrium(table, mixed_nash):
        return False
    for i in range(len(nash_equis)):
        if out[1][nash_equis[i][0]] > 0 and out[2][nash_equis[i][1]] > 0:
            return False
    return True


def create_test_format():
    with open("tests.txt", 'r') as f:
        line = f.readline()
        cnt = 1
        while line:
            print("\tdef test", cnt, "(self): \n",
                  "\t\ttime_limit = 30 \n",
                  "\t\tstart_time = time.time() \n ",
                  "\t\tinp = ", line,
                  "\n\t\tresult = main(inp)",
                  "\t\tself.assertEqual(check_answer(inp, result), True) \n",

                  "\t\tpassed_time = time.time() - start_time \n",
                  "\t\tself.assertLess(passed_time, time_limit)")
            line = f.readline()
            cnt += 1


# class TestMethods(unittest.TestCase):
#
#     def __init__(self, *args, **kwargs):
#         super(TestMethods, self).__init__(*args, **kwargs)
#
#     def test1(self):
#         time_limit = 30
#         start_time = time.time()
#         inp = [[[1, 1], [3, 2], [4, 3], [2, 1], [1, 1], [3, 1], [3, 4], [2, 2]],
#                [[3, 4], [4, 3], [4, 3], [3, 4], [3, 1], [2, 4], [2, 2], [3, 2]],
#                [[1, 2], [1, 1], [4, 4], [2, 2], [4, 1], [4, 3], [2, 3], [2, 4]],
#                [[1, 1], [3, 4], [1, 1], [1, 1], [3, 2], [2, 4], [3, 2], [2, 4]]]
#
#         result = main(inp)
#         self.assertEqual(check_answer(inp, result), True)
#         passed_time = time.time() - start_time
#         self.assertLess(passed_time, time_limit)
#
#     def test2(self):
#         time_limit = 30
#         start_time = time.time()
#         inp = [[[2, 2], [1, 4]], [[3, 2], [2, 4]], [[1, 3], [4, 2]]]
#
#         result = main(inp)
#         self.assertEqual(check_answer(inp, result), True)
#         passed_time = time.time() - start_time
#         self.assertLess(passed_time, time_limit)
#
#     def test3(self):
#         time_limit = 30
#         start_time = time.time()
#         inp = [[[2, 2], [4, 1], [2, 2], [3, 3]], [[2, 2], [2, 3], [2, 3], [3, 1]], [[3, 2], [3, 1], [4, 1], [2, 3]],
#                [[4, 1], [3, 1], [2, 3], [1, 1]], [[3, 4], [1, 4], [1, 3], [3, 4]]]
#
#         result = main(inp)
#         self.assertEqual(check_answer(inp, result), True)
#         passed_time = time.time() - start_time
#         self.assertLess(passed_time, time_limit)
#
#     def test4(self):
#         time_limit = 30
#         start_time = time.time()
#         inp = [[[1, 4], [2, 2], [1, 2], [3, 1]], [[1, 2], [3, 3], [3, 3], [1, 2]], [[1, 1], [4, 1], [1, 2], [2, 2]],
#                [[1, 2], [1, 1], [3, 3], [1, 2]], [[1, 3], [1, 4], [2, 2], [2, 2]]]
#
#         result = main(inp)
#         self.assertEqual(check_answer(inp, result), True)
#         passed_time = time.time() - start_time
#         self.assertLess(passed_time, time_limit)
#
#     def test5(self):
#         time_limit = 30
#         start_time = time.time()
#         inp = [[[4, 1], [2, 4]], [[4, 2], [2, 2]], [[2, 1], [1, 4]], [[1, 2], [3, 1]]]
#
#         result = main(inp)
#         self.assertEqual(check_answer(inp, result), True)
#         passed_time = time.time() - start_time
#         self.assertLess(passed_time, time_limit)
#
#     def test6(self):
#         time_limit = 30
#         start_time = time.time()
#         inp = [[[2, 1], [3, 1], [2, 1], [2, 3], [1, 3]], [[3, 2], [3, 2], [1, 4], [4, 1], [2, 3]],
#                [[1, 2], [3, 1], [3, 1], [2, 4], [2, 3]]]
#
#         result = main(inp)
#         self.assertEqual(check_answer(inp, result), True)
#         passed_time = time.time() - start_time
#         self.assertLess(passed_time, time_limit)
#
#     def test7(self):
#         time_limit = 30
#         start_time = time.time()
#         inp = [[[134, -9], [-160, -192], [33, 5], [185, -52], [-164, 162]],
#                [[-24, -87], [149, 16], [-193, -149], [-11, 133], [-34, 83]],
#                [[179, -40], [-135, 99], [-128, 148], [-124, -104], [-197, 78]],
#                [[25, -33], [-151, 113], [-177, -113], [-138, -152], [197, -173]],
#                [[-121, -59], [-161, -21], [55, -176], [160, -74], [185, 136]],
#                [[1, 187], [58, 10], [177, 82], [-162, -148], [34, 44]]]
#
#         result = main(inp)
#         self.assertEqual(check_answer(inp, result), True)
#         passed_time = time.time() - start_time
#         self.assertLess(passed_time, time_limit)
#
#     def test8(self):
#         time_limit = 30
#         start_time = time.time()
#         inp = [[[188, 109], [-173, -43], [-56, 43], [-28, 67], [-164, -61], [-126, 11], [151, 24]],
#                [[7, 194], [169, -3], [-42, 163], [49, -178], [61, -121], [20, 93], [-192, -109]],
#                [[157, -183], [92, -171], [-58, -103], [-27, 6], [34, -146], [170, 167], [-174, 117]],
#                [[-197, -140], [45, 171], [67, -132], [131, 80], [116, -5], [189, 40], [172, 132]],
#                [[-91, -26], [-74, 177], [179, -165], [-67, 109], [91, -154], [164, 187], [-180, 106]]]
#
#         result = main(inp)
#         self.assertEqual(check_answer(inp, result), True)
#         passed_time = time.time() - start_time
#         self.assertLess(passed_time, time_limit)
#
#     def test9(self):
#         time_limit = 30
#         start_time = time.time()
#         inp = [[[-108, 40], [14, 115], [-20, -82], [-94, -152], [-93, -169]],
#                [[68, 6], [50, -63], [103, 173], [-78, 192], [-99, -118]],
#                [[153, -160], [-74, 100], [-165, 84], [42, 129], [-110, -5]],
#                [[40, 49], [-189, 75], [164, -78], [-109, 177], [-98, -200]],
#                [[-171, -37], [37, -129], [-11, 47], [-139, 128], [-29, 95]],
#                [[48, 172], [-195, 42], [106, 112], [50, -88], [107, -177]],
#                [[68, 42], [-34, -10], [23, 147], [147, -14], [-168, -72]],
#                [[68, 157], [63, -130], [-19, -65], [86, -76], [121, 33]]]
#
#         result = main(inp)
#         self.assertEqual(check_answer(inp, result), True)
#         passed_time = time.time() - start_time
#         self.assertLess(passed_time, time_limit)
#
#     def test10(self):
#         time_limit = 30
#         start_time = time.time()
#         inp = [[[179, -37], [190, 39], [116, 3], [-136, 74]], [[109, -188], [137, -24], [-177, -46], [173, -84]],
#                [[108, 188], [143, -130], [-138, 55], [-193, 96]], [[-163, 152], [-160, -126], [-87, 121], [12, 104]],
#                [[-182, 174], [139, -123], [142, 72], [-27, 55]], [[118, 71], [94, 76], [22, -129], [113, 192]],
#                [[-37, -15], [130, -37], [60, 117], [190, 81]], [[58, 140], [167, -179], [-49, -110], [-35, 115]]]
#
#         result = main(inp)
#         self.assertEqual(check_answer(inp, result), True)
#         passed_time = time.time() - start_time
#         self.assertLess(passed_time, time_limit)
#
#     def test11(self):
#         time_limit = 30
#         start_time = time.time()
#         inp = [[[-113, 20], [59, 117], [56, 125], [-187, 174], [22, -59]],
#                [[-122, 96], [100, -162], [4, 197], [138, -143], [23, -68]],
#                [[-127, -130], [-49, -89], [117, 80], [196, 151], [-49, 156]],
#                [[-34, 123], [-61, -96], [-91, 112], [-37, 76], [-64, 74]],
#                [[-38, -19], [-197, 144], [-101, 121], [-13, 185], [172, -53]],
#                [[86, -158], [86, -182], [-115, -157], [167, 184], [-188, -56]]]
#
#         result = main(inp)
#         self.assertEqual(check_answer(inp, result), True)
#         passed_time = time.time() - start_time
#         self.assertLess(passed_time, time_limit)
#
#     def test12(self):
#         time_limit = 30
#         start_time = time.time()
#         inp = [[[130, -98], [-39, 141], [-187, -101], [-62, 42], [112, -37]],
#                [[-40, -11], [-172, -64], [-39, -17], [-187, -176], [103, 163]],
#                [[-77, -59], [-89, -16], [-85, -118], [72, 19], [61, 138]],
#                [[42, 62], [129, -66], [-49, 61], [-94, 150], [-89, 172]],
#                [[144, 169], [-78, -70], [-118, 154], [-130, 93], [-176, -161]],
#                [[115, -69], [-35, 196], [71, 200], [158, 17], [90, 63]]]
#
#         result = main(inp)
#         print(check_answer(inp, result))
#         self.assertEqual(check_answer(inp, result), True)
#         passed_time = time.time() - start_time
#         print(passed_time)
#         self.assertLess(passed_time, time_limit)

# print(nash_equi_finder(input_table))
# print([nash_equi_finder(input_table),
#        mixed_nash_equi_finder_make_support(input_table, True, [], nash_equi_finder(input_table))])

# create_test_format()

# if check_answer(input_table, output, nash_equi_finder(input_table)):
#     print("true")
# else:
#     print("false")
