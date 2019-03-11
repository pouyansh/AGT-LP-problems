import time
import unittest
from source import main
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


class TestMethods(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMethods, self).__init__(*args, **kwargs)

    def test1(self):
        time_limit = 30
        start_time = time.time()
        inp = [[[1, 3], [1, 4], [2, 1]], [[2, 2], [2, 1], [3, 4]], [[2, 2], [4, 3], [1, 4]],
               [[1, 3], [1, 4], [4, 3]]]

        result = main(inp)
        self.assertEqual(check_answer(inp, result), True)
        passed_time = time.time() - start_time
        self.assertLess(passed_time, time_limit)

    def test2(self):
        time_limit = 30
        start_time = time.time()
        inp = [[[2, 4], [1, 3], [4, 3], [2, 1], [2, 4], [2, 3]], [[1, 3], [3, 1], [2, 1], [2, 2], [2, 4], [2, 2]],
               [[3, 2], [3, 3], [1, 4], [1, 4], [2, 2], [3, 1]]]

        result = main(inp)
        self.assertEqual(check_answer(inp, result), True)
        passed_time = time.time() - start_time
        self.assertLess(passed_time, time_limit)

    def test3(self):
        time_limit = 30
        start_time = time.time()
        inp = [[[4, 3], [3, 2], [3, 1], [4, 1], [1, 3]], [[4, 1], [4, 4], [1, 3], [4, 2], [3, 3]],
               [[2, 2], [2, 4], [3, 1], [4, 1], [3, 4]], [[2, 4], [2, 3], [1, 4], [4, 2], [2, 2]],
               [[3, 4], [4, 1], [1, 3], [3, 3], [2, 2]], [[2, 1], [3, 1], [1, 2], [1, 1], [4, 1]]]

        result = main(inp)
        self.assertEqual(check_answer(inp, result), True)
        passed_time = time.time() - start_time
        self.assertLess(passed_time, time_limit)

    def test4(self):
        time_limit = 30
        start_time = time.time()
        inp = [[[1, 2], [2, 1], [1, 1], [3, 3], [2, 4], [2, 1]], [[1, 3], [4, 2], [1, 4], [2, 2], [2, 1], [2, 2]]]

        result = main(inp)
        self.assertEqual(check_answer(inp, result), True)
        passed_time = time.time() - start_time
        self.assertLess(passed_time, time_limit)

    def test5(self):
        time_limit = 30
        start_time = time.time()
        inp = [[[4, 3], [3, 4], [1, 2], [2, 2], [1, 1]], [[2, 4], [1, 4], [3, 4], [1, 3], [4, 3]],
               [[4, 3], [4, 1], [1, 2], [2, 4], [3, 3]]]

        result = main(inp)
        self.assertEqual(check_answer(inp, result), True)
        passed_time = time.time() - start_time
        self.assertLess(passed_time, time_limit)

    def test6(self):
        time_limit = 30
        start_time = time.time()
        inp = [[[4, 1], [1, 1], [1, 2]], [[3, 1], [4, 2], [1, 3]], [[3, 1], [1, 2], [3, 1]]]

        result = main(inp)
        self.assertEqual(check_answer(inp, result), True)
        passed_time = time.time() - start_time
        self.assertLess(passed_time, time_limit)

    def test7(self):
        time_limit = 30
        start_time = time.time()
        inp = [[[285, 179], [340, 400], [332, 322], [126, 2], [321, 145], [233, 81]],
               [[380, 66], [21, 16], [338, 110], [195, 254], [231, 64], [78, 301]],
               [[154, 323], [274, 274], [367, 246], [314, 205], [328, 75], [215, 64]],
               [[117, 50], [120, 363], [382, 260], [378, 53], [346, 189], [35, 243]],
               [[382, 365], [219, 202], [218, 49], [366, 369], [274, 340], [174, 29]]]

        result = main(inp)
        self.assertEqual(check_answer(inp, result), True)
        passed_time = time.time() - start_time
        self.assertLess(passed_time, time_limit)

    def test8(self):
        time_limit = 30
        start_time = time.time()
        inp = [[[144, 379], [131, 221], [333, 79], [122, 296], [149, 258]],
               [[137, 137], [221, 103], [43, 229], [35, 191], [305, 23]],
               [[42, 322], [183, 392], [54, 289], [183, 237], [304, 132]],
               [[115, 28], [233, 150], [177, 267], [115, 283], [318, 185]],
               [[170, 218], [367, 244], [75, 313], [60, 167], [254, 280]]]

        result = main(inp)
        self.assertEqual(check_answer(inp, result), True)
        passed_time = time.time() - start_time
        self.assertLess(passed_time, time_limit)

    def test9(self):
        time_limit = 30
        start_time = time.time()
        inp = [[[230, 73], [148, 261], [385, 305], [371, 40]], [[80, 215], [306, 103], [84, 257], [12, 134]],
               [[341, 293], [71, 237], [271, 138], [182, 332]], [[7, 271], [292, 179], [109, 14], [124, 398]],
               [[257, 344], [258, 299], [245, 159], [225, 308]], [[8, 380], [192, 248], [259, 394], [225, 382]],
               [[251, 79], [67, 60], [49, 198], [32, 377]]]

        result = main(inp)
        self.assertEqual(check_answer(inp, result), True)
        passed_time = time.time() - start_time
        self.assertLess(passed_time, time_limit)

    def test10(self):
        time_limit = 30
        start_time = time.time()
        inp = [[[294, 364], [25, 197], [48, 313], [186, 89], [376, 21], [229, 167], [211, 207], [171, 206]],
               [[103, 156], [192, 393], [238, 33], [160, 383], [116, 351], [266, 162], [225, 312], [251, 293]],
               [[214, 382], [266, 230], [166, 315], [300, 350], [254, 108], [79, 74], [31, 339], [239, 271]]]

        result = main(inp)
        self.assertEqual(check_answer(inp, result), True)
        passed_time = time.time() - start_time
        self.assertLess(passed_time, time_limit)

    def test11(self):
        time_limit = 30
        start_time = time.time()
        inp = [[[362, 239], [7, 383], [174, 159], [301, 296]], [[358, 209], [378, 4], [340, 226], [266, 131]],
               [[130, 306], [226, 152], [58, 297], [339, 127]], [[336, 108], [382, 327], [103, 89], [109, 164]],
               [[395, 257], [109, 185], [384, 353], [61, 9]]]

        result = main(inp)
        self.assertEqual(check_answer(inp, result), True)
        passed_time = time.time() - start_time
        self.assertLess(passed_time, time_limit)

    def test12(self):
        time_limit = 30
        start_time = time.time()
        inp = [[[376, 9], [32, 0], [20, 217], [251, 18]], [[245, 286], [353, 219], [159, 27], [320, 119]],
               [[327, 238], [293, 316], [4, 99], [38, 97]], [[248, 209], [261, 40], [25, 2], [97, 60]]]

        result = main(inp)
        self.assertEqual(check_answer(inp, result), True)
        passed_time = time.time() - start_time
        self.assertLess(passed_time, time_limit)

    def test13(self):
        time_limit = 30
        start_time = time.time()
        inp = [[[376, 9], [32, 0], [20, 217], [251, 18]], [[245, 286], [353, 219], [159, 27], [320, 119]],
               [[327, 238], [293, 316], [4, 99], [38, 97]], [[248, 209], [261, 40], [25, 2], [97, 60]]]

        result = main(inp)
        self.assertEqual(check_answer(inp, result), True)
        passed_time = time.time() - start_time
        self.assertLess(passed_time, time_limit)
