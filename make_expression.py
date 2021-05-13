################################
# Local dependencies
################################
import lang
import settings as sets
from literals_func import find_mon
from nums_func import find_num

################################
# External modules
################################
from copy import copy

################################
# Defines the parenthesis, the operators and the numbers of an expression
################################
def make_expr(usr_inp):
    # To manage operators and numbers
    operator_types = "+-*X/:%^R"
    operators = []
    operators_pos = []  # Based on their position on the string
    nums = []

    # The original nums and operators lists will be changed, these are used for the output
    out_operators = []

    # To manage the parenthesis
    temporary_opening_prth = []  # Prth stands for "parenthesis"
    closing_prth = []  # The position of the parenthesis based on the operators
    opening_prth = []

    # Finds the position of the operators and of the parenthesis, which is based on the operators
    for i, char in enumerate(usr_inp):
        if char == "(":
            # If there is a number or a closing parenthesis before, there is a multiplication
            if i != 0 and not i - 1 in operators_pos and usr_inp[i - 1] != "(":
                operators_pos.append(i)
                operators.append("*")
                out_operators.append("*")
            temporary_opening_prth.append(len(operators))

        elif char == ")":
            if len(temporary_opening_prth) == 0:
                nums.append(None)
                break

            closing_prth.append(len(operators))
            opening_prth.append(temporary_opening_prth.pop())

        elif char in operator_types and usr_inp[i - 1] != "(" and i != 0:
            if char != "^" or usr_inp[i - 1] in "0123456789)":
                operator = "/" if char == ":" else "*" if char == "X" else char
                operators_pos.append(i)
                operators.append(operator)
                out_operators.append(operator)

            if len(operators_pos) > 1 and operators_pos[-2] == i - 1:  # To allow N^-N and NR-N to be valid
                if operators[-2] in "^R":
                    operators.pop()
                    operators_pos.pop()
                    out_operators.pop()

        # If there is a closing parenthesis before but no operators, there is a multiplication
        elif i != 0 and usr_inp[i - 1] == ")":
            operators_pos.append(i)
            operators.append("*")
            out_operators.append("*")

    # If some opening or closing parenthesis are missing
    if len(opening_prth) != len(closing_prth) or len(temporary_opening_prth) != 0:
        nums.append(None)

    # Creates some fake parenthesis of the whole equation
    # It's here because could be redundant
    opening_prth.append(0)
    closing_prth.append(len(operators))

    # Removes any redundant parenthesis
    # There is always going to be a pair of parenthesis surrounding the expression
    previous_prth = -1  # -1 is never going to be on the list, so the first time it won't be True
    for i in range(len(closing_prth) - 1, -1, -1):  # The order in reverse
        if previous_prth == closing_prth[i] and opening_prth[i] == opening_prth[i + 1]:
            del opening_prth[i]
            del closing_prth[i]

        previous_prth = closing_prth[i]


    last_pos = -1

    if sets.settings["literal"]:
        for position in operators_pos:
            nums.append(find_mon(usr_inp[last_pos + 1:position]))
            last_pos = position

        nums.append(find_mon(usr_inp[last_pos + 1:]))  # Appends the last number

    else:
        for position in operators_pos:
            nums.append(find_num(usr_inp[last_pos + 1:position]))
            last_pos = position

        nums.append(find_num(usr_inp[last_pos + 1:]))  # Appends the last number

    out_opening_prth = copy(opening_prth)
    out_opening_prth.remove(0)
    out_closing_prth = copy(closing_prth)
    out_closing_prth.remove(len(operators))
    out_nums = copy(nums)

    lang.write_debug_log(
        f"clear_input = {usr_inp}",
        "make_expression.py|make_expr()",
        sets.settings["debug_mode"]
    )

    lang.write_debug_log(
        f"operators = {operators}",
        "make_expression.py|make_expr()",
        sets.settings["debug_mode"]
    )

    lang.write_debug_log(
        f"operators_pos = {operators_pos}",
        "make_expression.py|make_expr()",
        sets.settings["debug_mode"]
    )

    lang.write_debug_log(
        f"opening_prth = {opening_prth}",
        "make_expression.py|make_expr()",
        sets.settings["debug_mode"]
    )

    lang.write_debug_log(
        f"closing_prth = {closing_prth}",
        "make_expression.py|make_expr()",
        sets.settings["debug_mode"]
    )

    lang.write_debug_log(
        f"nums = {nums}",
        "make_expression.py|make_expr()",
        sets.settings["debug_mode"]
    )

    return     nums,     operators,     opening_prth,     closing_prth,\
           out_nums, out_operators, out_opening_prth, out_closing_prth
