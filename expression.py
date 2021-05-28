from copy import copy

import lang
import literals
import settings
from literals_func import find_mon
from nums_func import find_num


class Expression:
    """Solves an expression defined by thr make_expr() function defined below"""

    def __init__(self, expression):
        self._nums = expression[0]
        self._ops = expression[1]
        self._o_prth = expression[2]
        self._c_prth = expression[3]

    def solve(self):
        if None in self._nums:
            return None, "syntax_error"

        operations = ["R", "^", "*/%", "+-"]
        error_occurred = ""

        lang.write_info_log(
            message=f"============== Expression Calculation ==============\n",
            module =lang.this_line(__name__),
            print_message=settings.settings["debug_mode"]
        )

        for prth_pos in range(len(self._c_prth)):
            total_calcs = 0
            not_calc_nums = []
            o_prth = self._o_prth[prth_pos]
            c_prth = self._c_prth[prth_pos]

            for i in range(o_prth):
                not_calc_nums.append(self._nums[i])

            calc_nums = self._nums[o_prth:c_prth + 1].copy()

            for operation in operations:
                calcs = 0
                for i in range(c_prth - o_prth - total_calcs):
                    num_1 = calc_nums[i     - calcs]
                    num_2 = calc_nums[i + 1 - calcs]
                    op = self._ops[i + o_prth - calcs]

                    try:
                        if op not in operation: continue

                        elif num_1 == num_2 == 0 and op == "^":
                            raise ZeroDivisionError

                        elif op == "+": calc_nums[i-calcs] = num_1+ num_2

                        elif op == "-": calc_nums[i-calcs] = num_1- num_2

                        elif op == "*": calc_nums[i-calcs] = num_1* num_2

                        elif op == "/": calc_nums[i-calcs] = num_1/ num_2

                        elif op == "%": calc_nums[i-calcs] = num_1% num_2

                        elif op == "^": calc_nums[i-calcs] = num_1**num_2

                        elif op == "R":
                            if type(num_1) is literals.Pol:
                                calc_nums[i-calcs] = num_2.root(num_1)

                            else:
                                calc_nums[i-calcs] = num_2 ** (1 / num_1)

                        lang.write_info_log(
                            message=f"calc {num_1}, {num_2} -> '{op}'",
                            module =lang.this_line(__name__),
                            print_message=settings.settings["debug_mode"]
                        )

                        lang.write_info_log(
                            message=f"result {calc_nums[i - calcs]}\n",
                            module =lang.this_line(__name__),
                            print_message=settings.settings["debug_mode"]
                        )

                        del calc_nums[i + 1 - calcs]
                        del self._ops[i + o_prth - calcs]
                        total_calcs += 1
                        calcs += 1

                    except OverflowError:
                        error_occurred = "infinity"

                        lang.write_error_log(
                            message="OverflowError",
                            module =lang.this_line(__name__),
                            print_message=settings.settings["debug_mode"]
                        )

                        break

                    except ZeroDivisionError:
                        if num_1 == 0:
                            error_occurred = "undetermined"
                        else:
                            error_occurred = "impossible"

                        lang.write_error_log(
                            message="ZeroDivisionError",
                            module =lang.this_line(__name__),
                            print_message=settings.settings["debug_mode"]
                        )

                        break

                    except literals.ImpossibleDivError:
                        error_occurred = "impossible_div_error"

                        lang.write_error_log(
                            message="ImpossibleDivError",
                            module =lang.this_line(__name__),
                            print_message=settings.settings["debug_mode"]
                        )

                        break

                    except literals.NonIntPowError:
                        error_occurred = "non_int_pow_error"

                        lang.write_error_log(
                            message="NonIntPowError",
                            module =lang.this_line(__name__),
                            print_message=settings.settings["debug_mode"]
                        )

                        break

                    except literals.NonIntRootError:
                        error_occurred = "non_int_root_error"

                        lang.write_error_log(
                            message="non_int_root_error",
                            module =lang.this_line(__name__),
                            print_message=settings.settings["debug_mode"]
                        )

                        break

            not_calc_nums += calc_nums

            for i in range(c_prth + 1, len(self._ops) + 1 + total_calcs):
                not_calc_nums.append(self._nums[i])

            for i in range(len(self._c_prth)):
                self._c_prth[i] -= total_calcs

                if self._o_prth[i] >= c_prth:
                    self._o_prth[i] -= total_calcs

            self._nums = not_calc_nums.copy()

        result = self._nums[0]

        return result, error_occurred


################################
# Defines the parenthesis, the operators and the numbers of an expression
################################
def make_expr(usr_inp):
    # To manage operators and numbers
    op_types = "+-*X/:%^R"
    op_match = {
        "+": "+",
        "-": "-",
        "*": "*",
        "X": "*",
        "/": "/",
        ":": "/",
        "%": "%",
        "^": "^",
        "R": "R"
    }

    ops = []
    ops_pos = []  # Based on their position on the string
    nums = []

    # The original nums and operators lists will be changed,
    # these are used for the output
    out_ops = []

    # To manage the parenthesis
    temp_o_prth = []  # Prth stands for "parenthesis"
    c_prth = []  # The position of the parenthesis based on the operators
    o_prth = []

    # Finds the position of the operators and of the parenthesis,
    # which is based on the operators
    for i, char in enumerate(usr_inp):
        if char == "(":
            # If there is a number or a closing parenthesis before,
            # there is a multiplication
            if i != 0 and not i-1 in ops_pos and usr_inp[i-1] != "(":
                ops_pos.append(i)
                ops.append("*")
                out_ops.append("*")
            temp_o_prth.append(len(ops))

        elif char == ")":
            if len(temp_o_prth) == 0:
                nums.append(None)
                break

            c_prth.append(len(ops))
            o_prth.append(temp_o_prth.pop())

        elif char in op_types and usr_inp[i-1] != "(" and i != 0:
            if char != "^" or usr_inp[i-1] in "0123456789)":
                operator = op_match[char]
                ops_pos.append(i)
                ops.append(operator)
                out_ops.append(operator)

            # To allow N^-N and NR-N to be valid
            if len(ops_pos) > 1 and ops_pos[-2] == i - 1:
                if ops[-2] in "^R":
                    ops.pop()
                    ops_pos.pop()
                    out_ops.pop()

        # If there is a closing parenthesis before but no operators,
        # there is a multiplication
        elif i != 0 and usr_inp[i-1] == ")":
            ops_pos.append(i)
            ops.append("*")
            out_ops.append("*")

    # If some opening or closing parenthesis are missing
    if len(o_prth) != len(c_prth) or len(temp_o_prth) != 0:
        nums.append(None)

    # Creates some fake parenthesis of the whole equation
    # It's here because could be redundant
    o_prth.append(0)
    c_prth.append(len(ops))

    # Removes any redundant parenthesis
    # There is always going to be a pair of parenthesis
    # surrounding the expression

    # -1 is never going to be on the list, so the first time it won't be True
    previous_prth = -1
    for i in range(len(c_prth) - 1, -1, -1):  # The order in reverse
        if previous_prth == c_prth[i] and o_prth[i] == o_prth[i+1]:
            del o_prth[i]
            del c_prth[i]

        previous_prth = c_prth[i]


    last_pos = -1

    if settings.settings["literal"]:
        for pos in ops_pos:
            nums.append(find_mon(usr_inp[last_pos + 1:pos]))
            last_pos = pos

        nums.append(find_mon(usr_inp[last_pos + 1:]))

    else:
        for pos in ops_pos:
            nums.append(find_num(usr_inp[last_pos + 1:pos]))
            last_pos = pos

        nums.append(find_num(usr_inp[last_pos + 1:]))

    out_o_prth = copy(o_prth)
    out_o_prth.remove(0)
    out_c_prth = copy(c_prth)
    out_c_prth.remove(len(ops))
    out_nums = copy(nums)

    lang.write_info_log(
        message=f"============== Expression Output ==============\n",
        module =lang.this_line(__name__),
        print_message=settings.settings["debug_mode"]
    )

    lang.write_debug_log(
        message=f"{usr_inp=}",
        module =lang.this_line(__name__),
        print_message=settings.settings["debug_mode"]
    )

    lang.write_debug_log(
        message=f"{ops=}",
        module =lang.this_line(__name__),
        print_message=settings.settings["debug_mode"]
    )

    lang.write_debug_log(
        message=f"{ops_pos=}",
        module =lang.this_line(__name__),
        print_message=settings.settings["debug_mode"]
    )

    lang.write_debug_log(
        message=f"{o_prth=}",
        module =lang.this_line(__name__),
        print_message=settings.settings["debug_mode"]
    )

    lang.write_debug_log(
        message=f"{c_prth=}",
        module =lang.this_line(__name__),
        print_message=settings.settings["debug_mode"]
    )

    lang.write_debug_log(
        message=f"{nums=}",
        module =lang.this_line(__name__),
        print_message=settings.settings["debug_mode"]
    )

    if settings.settings["debug_mode"]:
        print()

    return     nums,     ops,     o_prth,     c_prth,\
           out_nums, out_ops, out_o_prth, out_c_prth
