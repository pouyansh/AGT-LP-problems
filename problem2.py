from scipy.optimize import linprog


def is_dominant(table, is_row, index):
    if is_row:
        # maximize delta
        c = [0 for _ in range(len(table) - 1)]
        c.append(-1)

        a_ub = []
        b_ub = []

        # p_i >= 0
        for i in range(len(table)):
            if i != index:
                temp_row = [0 for _ in range(len(table) - 1)]
                if i > index:
                    temp_row[i-1] = -1
                else:
                    temp_row[i] = -1
                temp_row.append(0)
                a_ub.append(temp_row)
                b_ub.append(0)

        # delta >= 0
        temp_row = [0 for _ in range(len(table)-1)]
        temp_row.append(-1)
        a_ub.append(temp_row)
        b_ub.append(0)

        # sigma p_i u_ij - delta >= u_(index)j
        for j in range(len(table[0])):
            temp_row = []
            for i in range(len(table)):
                if i != index:
                    temp_row.append(-table[i][j][0])
            temp_row.append(1)
            a_ub.append(temp_row)
            b_ub.append(-table[index][j][0])

        a_eq = []
        b_eq = []

        # sigma p_i = 1
        temp_row = [1 for _ in range(len(table) - 1)]
        temp_row.append(0)
        a_eq.append(temp_row)
        b_eq.append(1)

        res = linprog(c, a_ub, b_ub, a_eq, b_eq)
        if res.success:
            if res.fun != 0:
                print("row deleted: ", index, res.x)
                return True
        return False
    else:
        # maximize delta
        c = [0 for _ in range(len(table[0]) - 1)]
        c.append(-1)

        a_ub = []
        b_ub = []

        # p_i >= 0
        for i in range(len(table[0])):
            if i != index:
                temp_row = [0 for _ in range(len(table[0]) - 1)]
                if i > index:
                    temp_row[i-1] = -1
                else:
                    temp_row[i] = -1
                temp_row.append(0)
                a_ub.append(temp_row)
                b_ub.append(0)

        # delta >= 0
        temp_row = [0 for _ in range(len(table[0]) - 1)]
        temp_row.append(-1)
        a_ub.append(temp_row)
        b_ub.append(0)

        # sigma p_i u_ji - delta >= u_j(index)
        for j in range(len(table)):
            temp_row = []
            for i in range(len(table[0])):
                if i != index:
                    temp_row.append(-table[j][i][1])
            temp_row.append(1)
            a_ub.append(temp_row)
            b_ub.append(-table[j][index][1])

        a_eq = []
        b_eq = []

        # sigma p_i = 1
        temp_row = [1 for _ in range(len(table[0]) - 1)]
        temp_row.append(0)
        a_eq.append(temp_row)
        b_eq.append(1)

        res = linprog(c, a_ub, b_ub, a_eq, b_eq)
        if res.success:
            if res.fun != 0:
                print("column deleted: ", index, res.x)
                return True
        return False


def delete_dominant_strategies(table):
    for i in range(len(table)):
        if is_dominant(table, True, i):
            new_table = []
            for j in range(len(table)):
                if j != i:
                    new_table.append(table[j])
            return delete_dominant_strategies(new_table)
    for i in range(len(table[0])):
        if is_dominant(table, False, i):
            new_table = []
            for j in range(len(table)):
                new_row = []
                for k in range(len(table[0])):
                    if k != i:
                        new_row.append(table[j][k])
                new_table.append(new_row)
            return delete_dominant_strategies(new_table)
    return table


input_table = [[[31, 51], [24, 57], [32, 66], [25, 73]],
               [[44, 68], [12, 58], [54, 32], [20, 80]],
               [[39, 53], [62, 50], [46, 43], [11, 78]],
               [[22, 30], [31, 63], [29, 54], [27, 28]]]
print(delete_dominant_strategies(input_table))
