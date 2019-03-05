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


def mixed_nash_equi_finder_make_support(table, is_first, support):
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
            result = mixed_nash_equi_finder_make_support(table, False, current_support)
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
                state, result = make_probabilities_mixed_nash_equi(table, first_support, second_support)
                if state:
                    result_list = []
                    index = 0
                    for i in range(len(support)):
                        if i in first_support:
                            result_list.append(result[index])
                            index += 1
                        else:
                            result_list.append(0)
                    for i in range(len(current_support)):
                        if i in second_support:
                            result_list.append(result[index])
                            index += 1
                        else:
                            result_list.append(0)

                    output_list.append(result_list)
    return output_list


def check_answer(out, nash_equis, mixed_nash_equis):
    simple_nash = out[0]
    if len(simple_nash) != len(nash_equis):
        return False
    for i in range(len(simple_nash)):
        if not simple_nash[i] in nash_equis:
            return False
    mixed_nash = out[1]
    if len(mixed_nash) != len(mixed_nash_equis):
        return False
    for i in range(len(mixed_nash)):
        if not mixed_nash[i] in mixed_nash_equis:
            return False
    return True


input_table = [[[31, 51], [24, 57], [32, 66], [25, 73]], [[44, 68], [12, 58], [54, 32], [20, 80]],
               [[39, 53], [62, 50], [46, 43], [11, 78]], [[22, 30], [31, 63], [29, 54], [27, 28]]]
output = [[], [[0, 0, 0.5555555555555556, 0.4444444444444444, 0, 0.3404255319148936, 0, 0.6595744680851063]]]

# print(nash_equi_finder(input_table))
# print(mixed_nash_equi_finder_make_support(input_table, True, []))

if check_answer(output, nash_equi_finder(input_table), mixed_nash_equi_finder_make_support(input_table, True, [])):
    print("true")
else:
    print("false")
