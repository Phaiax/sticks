#!/usr/bin/python3

import unittest
from enum import Enum, IntEnum


class SIGN(Enum):
    PLUS = 11
    MINUS = 12
    EQUAL = 13

class NUMBER(IntEnum):
    pass

#      c0
#
# c1        c2
#      c8
#      c3
#      c7
# c4        c5
#
#      c6
#
# c7 is the stick that makes a PLUS
# c8 is the stick that makes a EQUAL


display = {
    #   c0  1  2  3  4  5  6  7  8
    0 : [1, 1, 1, 0, 1, 1, 1, 0, 0],
    1 : [0, 0, 1, 0, 0, 1, 0, 0, 0],
    2 : [1, 0, 1, 1, 1, 0, 1, 0, 0],
    3 : [1, 0, 1, 1, 0, 1, 1, 0, 0],
    4 : [0, 1, 1, 1, 0, 1, 0, 0, 0],
    5 : [1, 1, 0, 1, 0, 1, 1, 0, 0],
    6 : [0, 1, 0, 1, 1, 1, 1, 0, 0],
    7 : [1, 0, 1, 0, 0, 1, 0, 0, 0],
    8 : [1, 1, 1, 1, 1, 1, 1, 0, 0],
    9 : [1, 1, 1, 1, 0, 1, 0, 0, 0],
    SIGN.PLUS : [0, 0, 0, 1, 0, 0, 0, 1, 0],
    SIGN.MINUS : [0, 0, 0, 1, 0, 0, 0, 0, 0],
    SIGN.EQUAL : [0, 0, 0, 1, 0, 0, 0, 0, 1],
}

# `#####`   `     `   `     `
#  #   #       #       #####
#  #####     #####     #####
#  #   #       #
#  #####

stickpositions = { # how to print a stick in position c1 or c4
    0: [("+---+"), ("     "), ("     "), ("     "), ("     ")],
    1: [("+    "), ("|    "), ("+    "), ("     "), ("     ")],
    2: [("    +"), ("    |"), ("    +"), ("     "), ("     ")],
    3: [("     "), ("     "), ("+---+"), ("     "), ("     ")],
    4: [("     "), ("     "), ("+    "), ("|    "), ("+    ")],
    5: [("     "), ("     "), ("    +"), ("    |"), ("    +")],
    6: [("     "), ("     "), ("     "), ("     "), ("+---+")],
    7: [("     "), ("  +  "), ("  +  "), ("  +  "), ("     ")],
    8: [("     "), ("====="), ("====="), ("     "), ("     ")],
}

assert(SIGN.PLUS in SIGN)

def num_changes(frm, to):
    """ return (sticks to take, sticks to add) """
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
assert(num_changes(2, SIGN.PLUS) == (4, 1))
assert(num_changes(SIGN.PLUS, SIGN.PLUS) == (0, 0))
assert(num_changes(SIGN.PLUS, SIGN.MINUS) == (1, 0))
assert(num_changes(SIGN.EQUAL, SIGN.PLUS) == (1, 1))
assert(num_changes(2, 5) == (2, 2)) # to change a number from 2 to 5,
                                     # you need to add two and to take two


def parse_equation(str_eqn):
    """ Parses an input string "13+15=22" to
    a equation list [1, 3, PLUS, 1, 5, EQUAL, 2, 2].
    Raises ValueError if illegal input. """
    eqn = []
    for s in str_eqn:
        if s == "+": eqn.append(SIGN.PLUS); continue
        if s == "-": eqn.append(SIGN.MINUS); continue
        if s == "=": eqn.append(SIGN.EQUAL); continue
        i = int(s)
        if i is not None and 0 <= i <= 9:
            eqn.append(i)
        else:
            raise ValueError("Illegal Character")
    return eqn

assert(parse_equation("13+15=22") == [1, 3, SIGN.PLUS, 1, 5, SIGN.EQUAL, 2, 2])
unittest.TestCase().assertRaises(ValueError, parse_equation, "13p15");


def is_num(i):
    return i not in SIGN and 0 <= i <= 9


assert(is_num(2))
assert(is_num(0))
assert(is_num(9))
assert(not is_num(10))
assert(not is_num(SIGN.PLUS))


def is_sign(i):
    return i in SIGN


assert(is_sign(SIGN.PLUS))
assert(is_sign(SIGN.MINUS))
assert(is_sign(SIGN.EQUAL))
assert(not is_sign(9))
assert(not is_sign(12))
assert(not is_sign(int(is_sign(SIGN.PLUS))))


def to_int(digitlist):
    """ Takes a term like [1, 4, 1] and returns 141
    Takes [MINUS, 1, 5, 2] and returns -152 """
    assert(all([not is_sign(c) for c in digitlist[1:]]))
    assert(len(digitlist) >= 1)
    fac = 1
    if is_sign(digitlist[0]):
        assert(len(digitlist) >= 2)
        if digitlist[0] == SIGN.MINUS:
            fac = -1
        digitlist = digitlist[1:]
    return fac * int("".join([str(c) for c in digitlist]))


assert(to_int([1, 2, 4]) == 124)
assert(to_int([SIGN.MINUS, 1, 2, 4]) == -124)
assert(to_int([SIGN.PLUS, 1, 2, 4]) == 124)
assert(to_int([SIGN.PLUS, 1]) == 1)
assert(to_int([SIGN.MINUS, 1]) == -1)


def calc_term(term):
    """ Takes a term like [MINUS, 1, PLUS, 3, 4]
    and returns 33 """
    assert(SIGN.EQUAL not in term)

    numbers = []
    begin = 0
    for i, c in enumerate(term):
        if is_sign(c) and i != 0:
            numbers.append(to_int(term[begin:i]))
            begin = i
    numbers.append(to_int(term[begin:]))
    result = 0
    for n in numbers: result += n
    return result

assert(calc_term(parse_equation("12+17")) == 29)
assert(calc_term(parse_equation("-1+34")) == 33)
assert(calc_term(parse_equation("35-60")) == -25)


def split_eq(eqn):
    index_eq = eqn.index(SIGN.EQUAL)
    return eqn[0:index_eq], eqn[index_eq+1:]


def is_true_equation(eqn):
    """ Takes a valid equation and returns if it is true """
    assert(len(eqn) >= 3)
    assert(SIGN.EQUAL in eqn)
    left, right = split_eq(eqn)
    return calc_term(left) == calc_term(right)


assert( not is_true_equation(parse_equation("35-60=28")))
assert(     is_true_equation(parse_equation("34-15=19")))
assert(     is_true_equation(parse_equation("34=15+19")))
assert(     is_true_equation(parse_equation("34=53-19")))
assert(     is_true_equation(parse_equation("04+15=19")))
assert(     is_true_equation(parse_equation("04-2+15=17")))
assert(     is_true_equation(parse_equation("04+15=17+002")))
assert(     is_true_equation(parse_equation("-04+15=17+002-8")))


def tostring_sign(sign):
    if sign == SIGN.PLUS: return "+"
    if sign == SIGN.MINUS: return "-"
    if sign == SIGN.EQUAL: return "="


def tostring(eqn):
    return "".join([(str(c) if is_num(c) else tostring_sign(c)) for c in eqn])


assert(tostring(parse_equation("04-2+15=17")) == "04-2+15=17")


def add_to_canvas(canvas, obj):
    for canvasline, line in zip(canvas, obj):
        for i, c in enumerate(line):
            if c != " ":
                canvasline[i] = c

def pretty_digit(c):
    """ returns a list canvas[line][char] """
    canvas = [[" "] * 5, [" "] * 5, [" "] * 5, [" "] * 5, [" "] * 5]
    the_sticks = display[c]
    for stick, on in enumerate(the_sticks):
        if on:
            stick_display = stickpositions[stick]
            add_to_canvas(canvas, stick_display)
    return canvas


def merge_digits(prettydigitlist):
    total = ["     "] * 5
    for canvas in prettydigitlist:
        for i, line in enumerate(canvas):
            total[i] += "".join(line) + "  "
    return total


def print_canvas(canvas):
    for line in canvas:
        print(line)


def pretty_eqn(eqn):
    return [pretty_digit(s) for s in eqn]


def print_eqn(eqn):
    print_canvas(merge_digits(pretty_eqn(eqn)))



class Riddle(object):
    """ Each equation is represented by a list of ints and SIGN.?s. """

    def __init__(self, start_equation, max_take,
                 number_of_sticks_must_be_constant=False, max_add=None,
                 signs_and_numbers_can_convert=False):
        self.start_equation = start_equation
        self.max_take = max_take
        self.max_add = max_add if max_add is not None else max_take
        self.signs_and_numbers_can_convert = signs_and_numbers_can_convert
        self.number_of_sticks_must_be_constant = number_of_sticks_must_be_constant
        if self.max_add != self.max_take:
            self.number_of_sticks_must_be_constant = False


    def get_start_equation(self):
        return self.start_equation


    def get_zeroed_equation(self):
        """ return something like 00+00+00 aka [0, 0, PLUS, 0, 0, PLUS, 0, 0] """
        return [0 if is_num(c) else SIGN.PLUS for c in self.start_equation]


    def is_valid_equation(self, eqn):
        number_of_equals = len([1 for c in eqn if c == SIGN.EQUAL])
        if number_of_equals != 1: return False
        left, right = split_eq(eqn)
        if len(left) == 0 or len(right) == 0: return False
        no_two_signs_in_a_row_leftterm = all([not(is_sign(c) and is_sign(left[i+1]))
                                     for i, c in enumerate(left) if i+1 < len(left)])
        no_two_signs_in_a_row_rightterm = all([not(is_sign(c) and is_sign(right[i+1]))
                                     for i, c in enumerate(right) if i+1 < len(right)])
        no_sign_at_ends = is_num(left[len(left)-1]) and is_num(right[len(right)-1])
        all_numbers_still_numbers = all([is_num(c) for c, s in zip(eqn, self.start_equation) if is_num(s)])
        all_signs_still_signs = all([is_sign(c) for c, s in zip(eqn, self.start_equation) if is_sign(s)])
        return number_of_equals == 1 and no_sign_at_ends \
               and no_two_signs_in_a_row_rightterm and no_two_signs_in_a_row_leftterm \
               and (self.signs_and_numbers_can_convert \
                    or (all_numbers_still_numbers and all_signs_still_signs))


    def get_range(self, index):
        if self.signs_and_numbers_can_convert:
            return list(range(0, 10)) + list(SIGN)
        if is_sign(self.start_equation[index]):
            return SIGN
        elif is_num(self.start_equation[index]):
            return range(0, 10)
        assert(False)


    def is_valid_transformation(self, added, taken):
        if self.number_of_sticks_must_be_constant:
            return self.is_valid_step(added, taken)
        else:
            return added <= self.max_add and added == taken


    def is_valid_step(self, added, taken):
        return added <= self.max_add and taken <= self.max_take


r_test = Riddle(parse_equation("35-60=28"), 2)
assert(r_test.get_zeroed_equation() == parse_equation("00+00+00"))

assert(     r_test.is_valid_equation(parse_equation("35-60=28")) )
assert( not r_test.is_valid_equation(parse_equation("35-60+28")) )
r_test2 = Riddle(parse_equation("35--6=28"), 2)
assert( not r_test2.is_valid_equation(parse_equation("35--6=28")) )
assert( not r_test2.is_valid_equation(parse_equation("35-60=28")) )
r_test2 = Riddle(parse_equation("-35-6=28"), 2)
assert( not r_test2.is_valid_equation(parse_equation("-35-6=-8")) )
r_test2 = Riddle(parse_equation("35-628="), 2, True, 2, True)
assert( not r_test2.is_valid_equation(parse_equation("35-628=")) )
assert(     r_test2.is_valid_equation(parse_equation("-3-2=+28")) )

assert(list(r_test.get_range(0)) == [0,1,2,3,4,5,6,7,8,9])
assert(list(r_test.get_range(6)) == [0,1,2,3,4,5,6,7,8,9])
assert(list(r_test.get_range(5)) == [SIGN.PLUS, SIGN.MINUS, SIGN.EQUAL])
assert(list(r_test.get_range(2)) == [SIGN.PLUS, SIGN.MINUS, SIGN.EQUAL])
assert(list(r_test2.get_range(2)) == [0,1,2,3,4,5,6,7,8,9, SIGN.PLUS, SIGN.MINUS, SIGN.EQUAL])

assert( not r_test.is_valid_transformation(2, 1) )
assert(     r_test.is_valid_transformation(2, 2) )
assert( not r_test.is_valid_transformation(3, 3) )
assert(     r_test.is_valid_transformation(0, 0) )
assert(     r_test2.is_valid_transformation(0, 1) )
assert(     r_test2.is_valid_transformation(1, 0) )
assert(     r_test2.is_valid_transformation(2, 2) )


def solve_recursive(equation_class, equation = None, current_ciffer_position = None,
                  total_taken = 0, total_added = 0):

    if current_ciffer_position == None:
        current_ciffer_position = 0
        equation = equation_class.get_start_equation()

    all_solutions = []
    changed_calc = equation.copy()

    for v in equation_class.get_range(current_ciffer_position):
        changed_calc[current_ciffer_position] = v
        sticks_to_take, sticks_to_add = num_changes(
                equation_class.get_start_equation()[current_ciffer_position],
                changed_calc[current_ciffer_position])
        now_added = total_added + sticks_to_add
        now_taken = total_taken + sticks_to_take

        # last recursion level
        if current_ciffer_position == len(equation) - 1:
            if equation_class.is_valid_equation(changed_calc) and \
                equation_class.is_valid_transformation(now_added, now_taken) and \
                is_true_equation(changed_calc):
                    all_solutions.append( (changed_calc.copy(), now_added, now_taken) )

        elif equation_class.is_valid_step(now_added, now_taken):
            new_solutions = solve_recursive(equation_class, changed_calc,
                                          current_ciffer_position + 1, now_taken, now_added)
            all_solutions.extend(new_solutions)

    return all_solutions


assert( (parse_equation("24+36=60"), 2, 2)
        in solve_recursive(Riddle(parse_equation("29-36=50"), 2) ) )


def try_solve_riddle(eqn_str, take_and_add=2, number_of_sticks_must_be_constant=False):
    try:
        eqn = parse_equation(eqn_str) # ValueError
        riddle = Riddle(eqn, take_and_add, number_of_sticks_must_be_constant,
                        signs_and_numbers_can_convert=True)
        #assert(riddle.is_valid_equation(riddle.get_start_equation())) # AssertionError
            # more flexible if we allow every invalid input as start input
        return solve_recursive(riddle), None
    except Exception as e:
        return [], e


assert((parse_equation("23=+23"), 2, 2) in try_solve_riddle("23+=23")[0])


def solve_and_print(eqn_str, take_and_add=2, number_of_sticks_must_be_constant=False):
    print("====================================================================")
    print("Solve: " + eqn_str)
    print_eqn(parse_equation(eqn_str))
    solutions, error = try_solve_riddle(eqn_str, take_and_add, number_of_sticks_must_be_constant)
    if error is None:
        for solution, added, taken in solutions:
            if taken == added:
                print("   {}   ( {} changes )".format(tostring(solution), taken) )
            else:
                print("   {}   ( {} taken, {} added )".format(tostring(solution), taken, added) )
            print_eqn(solution)

solve_and_print("35-60=28")
solve_and_print("35-64=28")
