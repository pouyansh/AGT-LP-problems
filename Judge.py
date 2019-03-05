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


input_table = [[[3, 4], [2, 3], [3, 7]], [[4, 2], [5, 2], [5, 3]], [[6, 2], [4, 1], [2, 7]]]
output = [[[3, 1]], [[0.5, 0, 0.5, 0.75, 0.25, 0]]]

print(nash_equi_finder(input_table))
