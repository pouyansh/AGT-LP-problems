from scipy.optimize import linprog


def find_mixed_nash_equilibrium(table):
    p1_strategy = []
    p2_strategy = []

    # your code here

    return p1_strategy, p2_strategy


def find_nash_equilibrium(table):
    output = []

    # your code here

    return output


def main(table):
    all_nash_equilibriums = find_nash_equilibrium(table)
    p1_mixed_strategy , p2_mixed_strategy = find_mixed_nash_equilibrium(table)
    return [all_nash_equilibriums, p1_mixed_strategy, p2_mixed_strategy]


# main([[[3, 4], [7, 6], [1, 5]], [[2, 4], [1, 4], [2, 6]]])
