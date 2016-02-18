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


def num_changes_(frm, to):
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


assert(num_changes_(3, 8) == (0, 2))
assert(num_changes_(3, 2) == (1, 1))
assert(num_changes_(6, 6) == (0, 0))
assert(num_changes_(2, 5) == (2, 2)) # to change a number from 2 to 5, 
                                     # you need to add two and to take two


class RiddleType1(object):
    """ Each equation is represented by a list of ints.
    This equation type uses special digits to determine if
    it should use plus or minus or equal as sign. 
    10: plus
    11: minus
    12: equal sign
    The signs are appended to the digis
    ab $ cd @ ef   is saved as abcdef$@ """

    PLUS = 10
    MINUS = 11
    EQUAL = 12

    def __init__(self, start_equation):
        assert(len(start_equation) == 8)
        self.start_equation = start_equation

    def get_start_equation(self):
        return self.start_equation

    def get_zeroed_equation(self):
        # 00 + 00 + 00
        return [0] * 6 + [self.PLUS, self.PLUS]

    def is_valid_equation(self, e):
        one_equal_sign = (e[6] == self.EQUAL and e[7] != self.EQUAL) or \
                         (e[6] != self.EQUAL and e[7] == self.EQUAL)
        all_numbers_in_range = all([0 <= c <= 9 for c in e[0:6]])
        all_signs_in_range = all([self.PLUS <= c <= self.EQUAL for c in e[6:8]])
        return one_equal_sign and all_numbers_in_range and all_signs_in_range

    def is_true_equation(self, e):
        if e[6] == self.PLUS and e[7] == self.EQUAL: return self.ab_plus_cd_is_ef(*e[0:6])
        if e[6] == self.MINUS and e[7] == self.EQUAL: return self.ab_minus_cd_is_ef(*e[0:6])
        if e[6] == self.EQUAL and e[7] == self.PLUS: return self.ab_is_cd_plus_ef(*e[0:6])
        if e[6] == self.EQUAL and e[7] == self.MINUS: return self.ab_is_cd_minus_ef(*e[0:6])

    def ab_minus_cd_is_ef(self, a,b,c,d,e,f):
        return (a*10 + b) - (c*10 + d) == (e*10 + f)

    def ab_plus_cd_is_ef(self, a,b,c,d,e,f):
        return (a*10 + b) + (c*10 + d) == (e*10 + f)

    def ab_is_cd_plus_ef(self, a,b,c,d,e,f):
        return (a*10 + b) == (c*10 + d) + (e*10 + f)

    def ab_is_cd_minus_ef(self, a,b,c,d,e,f):
        return (a*10 + b) == (c*10 + d) - (e*10 + f)

    def num_changes(self, frm, to):
        if 0 <= frm <= 9 and 0 <= to <= 9:
            return num_changes_(frm, to)
        if self.PLUS <= frm <= self.EQUAL and self.PLUS <= to <= self.EQUAL:
            if frm == self.PLUS and to == self.MINUS:
                return (1, 0)
            if frm == self.PLUS and to == self.EQUAL:
                return (1, 1)
            if frm == self.MINUS and to == self.PLUS:
                return (0, 1)
            if frm == self.MINUS and to == self.EQUAL:
                return (0, 1)
            if frm == self.EQUAL and to == self.MINUS:
                return (1, 0)
            if frm == self.EQUAL and to == self.PLUS:
                return (1, 1)
            if frm == to:
                return (0, 0)
        assert(False)

    def tostring_sign(self, sign):
        if sign == self.PLUS: return "+"
        if sign == self.MINUS: return "-"
        if sign == self.EQUAL: return "="

    def tostring(self, equation):
        str_equation = equation.copy()[0:6]
        str_equation.insert(2, self.tostring_sign(equation[6]))
        str_equation.insert(5, self.tostring_sign(equation[7]))
        return "{}{} {} {}{} {} {}{}".format(*str_equation)

    def get_range(self, current_ciffer_position):
        if 0 <= current_ciffer_position <= 5:
            return range(0, 10)
        if 6 <= current_ciffer_position <= 7:
            return range(self.PLUS, self.EQUAL + 1)
        assert(False)

    def is_valid_transformation(self, total_added, total_taken):
        return total_added <= 2 and total_added == total_taken

    def is_valid_step(self, total_added, total_taken):
        return total_added <= 2 and total_taken <= 2


r_test = RiddleType1([3, 5, 6, 0, 2, 8, RiddleType1.MINUS, RiddleType1.EQUAL])
assert( not r_test.is_true_equation(r_test.get_start_equation()))
assert(     r_test.ab_minus_cd_is_ef(3,4, 1,5, 1,9)) # 34 - 15 = 19?
assert(     r_test.is_true_equation([3,4, 1,5, 1,9, RiddleType1.MINUS, RiddleType1.EQUAL])) # 34 - 15 = 19?
assert(     r_test.is_true_equation([3,4, 1,5, 1,9, RiddleType1.EQUAL, RiddleType1.PLUS])) # 34 = 15 + 19?
assert(     r_test.is_true_equation([3,4, 5,3, 1,9, RiddleType1.EQUAL, RiddleType1.MINUS])) # 34 = 53 - 19?
assert(     r_test.is_true_equation([0,4, 1,5, 1,9, RiddleType1.PLUS, RiddleType1.EQUAL])) # 04 + 15 = 19?

assert(list(r_test.get_range(0)) == [0,1,2,3,4,5,6,7,8,9])
assert(list(r_test.get_range(5)) == [0,1,2,3,4,5,6,7,8,9])
assert(list(r_test.get_range(6)) == [r_test.PLUS, r_test.MINUS, r_test.EQUAL])
assert(list(r_test.get_range(7)) == [r_test.PLUS, r_test.MINUS, r_test.EQUAL])

def recursive_try(equation_class, equation = None, current_ciffer_position = None,
                  total_taken = 0, total_added = 0):

    if current_ciffer_position == None:
        current_ciffer_position = 0
        equation = equation_class.get_start_equation()

    all_solutions = []
    changed_calc = equation.copy()

    for v in equation_class.get_range(current_ciffer_position):
        changed_calc[current_ciffer_position] = v
        sticks_to_take, sticks_to_add = equation_class.num_changes(
                equation_class.get_start_equation()[current_ciffer_position],
                changed_calc[current_ciffer_position])
        now_added = total_added + sticks_to_add
        now_taken = total_taken + sticks_to_take

        # last recursion level
        if current_ciffer_position == len(equation) - 1:
            if equation_class.is_valid_equation(changed_calc) and \
                equation_class.is_valid_transformation(now_added, now_taken) and \
                equation_class.is_true_equation(changed_calc):
                    all_solutions.append( (changed_calc.copy(), now_added, now_taken) )

        elif equation_class.is_valid_step(now_added, now_taken):
            new_solutions = recursive_try(equation_class, changed_calc, 
                                          current_ciffer_position + 1, now_taken, now_added)
            all_solutions.extend(new_solutions)

    return all_solutions


assert( ([2,4, 3,6, 6,0, RiddleType1.PLUS, RiddleType1.EQUAL], 2, 2) 
        in recursive_try(RiddleType1([2,9, 3,6, 5,0, RiddleType1.MINUS, RiddleType1.EQUAL ]) ) )

r1 = RiddleType1([3,5, 6,0, 2,8, RiddleType1.MINUS, RiddleType1.EQUAL])
print("solve " + r1.tostring(r1.get_start_equation()))
for solution, added, taken in recursive_try(r1):
    assert(taken == added)
    print("   {}   ( {} changes )".format(r1.tostring(solution), taken) )
