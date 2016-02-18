#!/usr/bin/python3

#    c0
# c1    c2
#    c3
# c4    c5
#    c6


display = {
    #   c0  1  2  3  4  5  6
    0 : [1, 1, 1, 0, 1, 1, 1],
    1 : [0, 0, 1, 0, 0, 1, 0],
    2 : [1, 0, 1, 1, 1, 0, 1],
    3 : [1, 0, 1, 1, 0, 1, 1],
    4 : [0, 1, 1, 1, 0, 1, 0],
    5 : [1, 1, 0, 1, 0, 1, 1],
    6 : [0, 1, 0, 1, 1, 1, 1],
    7 : [1, 0, 1, 0, 0, 1, 0],
    8 : [1, 1, 1, 1, 1, 1, 1],
    9 : [1, 1, 1, 1, 0, 1, 0],
}


def num_changes(frm, to):
    """ return (sticks to take, sticks to add) """
    assert(0 <= frm and frm <= 9)
    assert(0 <= to  and to  <= 9)
    sticks_to_add = 0
    sticks_to_take = 0
    for c_frm, c_to in zip(display[frm], display[to]):
        if c_frm and not c_to:
            sticks_to_take += 1
        if c_to and not c_frm:
            sticks_to_add += 1
    return sticks_to_take, sticks_to_add


assert(num_changes(3, 8) == (0, 2))
assert(num_changes(3, 2) == (1, 1))
assert(num_changes(6, 6) == (0, 0))
assert(num_changes(2, 5) == (2, 2)) # to change a number from 2 to 5, you need to add two and to take two

start_calc = [3, 5, 6, 0, 2, 8]

def ab_minus_cd_is_ef(a,b,c,d,e,f):
    return (a*10 + b) - (c*10 + d) == (e*10 + f)

assert( not ab_minus_cd_is_ef(*start_calc))
assert(     ab_minus_cd_is_ef(3, 4, 1, 5, 1, 9)) # 34 - 15 = 19?

def ab_plus_cd_is_ef(a,b,c,d,e,f):
    return (a*10 + b) + (c*10 + d) == (e*10 + f)

assert( not ab_plus_cd_is_ef(3, 4, 1, 5, 1, 9)) # 34 + 15 != 19?
assert(     ab_plus_cd_is_ef(3, 4, 1, 5, 4, 9)) # 34 + 15  = 49?

def tostring_plus(calculation):
    return "{}{} + {}{} = {}{}".format(*calculation)

def tostring_minus(calculation):
    return "{}{} - {}{} = {}{}".format(*calculation)

def tostring(calculation, sign):
    if sign == "+": return tostring_plus(calculation)
    if sign == "-": return tostring_minus(calculation)

def recursive_try(start_calc, calculation = None, current_ciffer_position = None, total_taken = 0, total_added = 0):

    if current_ciffer_position == None:
        current_ciffer_position = 0
        calculation = [0] * len(start_calc)

    all_solutions = []
    changed_calc = calculation.copy()

    for v in range(0, 10):
        changed_calc[current_ciffer_position] = v
        sticks_to_take, sticks_to_add = num_changes(start_calc[current_ciffer_position],
                                                    changed_calc[current_ciffer_position])
        now_added = total_added + sticks_to_add
        now_taken = total_taken + sticks_to_take

        if current_ciffer_position == len(calculation) - 1: # last recursion level
            if now_added <= 2 and now_added == now_taken and ab_minus_cd_is_ef(*changed_calc):
                all_solutions.append((changed_calc.copy(), "-"))
            if now_added <= 1 and now_added + 1 == now_taken and ab_plus_cd_is_ef(*changed_calc):
                all_solutions.append((changed_calc.copy(), "+"))
            continue

        if now_taken <= 2 and now_added <= 2:
            new_solutions = recursive_try(start_calc, changed_calc, current_ciffer_position + 1, now_taken, now_added)
            all_solutions.extend(new_solutions)

    return all_solutions


assert( ([2, 4, 3, 6, 6, 0], "+") in recursive_try([2, 9, 3, 6, 5, 0]) )

print("solve 35-60=28")
for solution in recursive_try([3, 5, 6, 0, 2, 8]):
    print("   ", tostring(*solution))
