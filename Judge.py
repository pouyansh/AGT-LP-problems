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


def check_if_mixed_nash_equi(table, first_support, second_support):
    c = [0 for _ in range(len(first_support) + len(second_support))]
    c.append(-1)
    A_ub = []
    b_ub = []

    # p_i - delta >= 0 , q_i - delta >= 0
    for i in range(len(first_support) + len(second_support)):
        temp_list = [0 for _ in range(len(first_support) + len(second_support) + 1)]
        temp_list[i] = 1
        temp_list[len(temp_list)-1] = -1
        A_ub.append(temp_list)
        b_ub.append(0)

    # delta >= 0
    temp_list = [0 for _ in range(len(first_support) + len(second_support))]
    temp_list.append(1)
    A_ub.append(temp_list)
    b_ub.append(0)

    A_eq = []
    b_eq = []

    # sigma p_i = 1 and sigma q_i = 0
    temp_list = [0 for _ in range(len(first_support))]
    for i in range(len(second_support)):
        temp_list.append(1)
    temp_list.append(0)
    A_eq.append(temp_list)
    b_eq.append(1)
    temp_list = [1 for _ in range(len(first_support))]
    for i in range(len(second_support)):
        temp_list.append(0)
    temp_list.append(0)
    A_eq.append(temp_list)
    b_eq.append(1)

    # set restricts for q_is in order to make it possible for the first person to plat mixed
    for i in range(1, len(first_support)):
        temp_list = [0 for _ in range(len(first_support))]
        for j in range(len(second_support)):
            temp_list.append(
                table[first_support[i]][second_support[j]][0] - table[first_support[0]][second_support[j]][0])
        temp_list.append(0)
        A_eq.append(temp_list)
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
        A_eq.append(temp_list)
        b_eq.append(0)

    print(first_support, second_support, A_ub, b_ub, A_eq, b_eq)
    if not A_ub == [] and not A_eq == []:
        res = linprog(c=c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq)
    elif not A_ub == []:
        res = linprog(c=c, A_ub=A_ub, b_ub=b_ub)
    print(res.x)


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
            output_list.append(mixed_nash_equi_finder_make_support(table, False, current_support))
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
            check_if_mixed_nash_equi(table, first_support, second_support)


input_table = [[[3, 4], [2, 3], [3, 7]], [[4, 2], [5, 2], [5, 3]], [[6, 2], [4, 1], [2, 7]]]
output = [[[3, 1]], [[0.5, 0, 0.5, 0.75, 0.25, 0]]]

print(nash_equi_finder(input_table))
mixed_nash_equi_finder_make_support(input_table, True, [])
