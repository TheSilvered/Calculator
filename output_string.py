import settings
import lang
from literals_func import str_literal
from nums_func import num_to_str

def build_result_string(open_prth, close_prth, operators, nums, result):
    output_string = ""

    lang.write_info_log(
        message=f"============== Output String ==============\n",
        module =lang.this_line(__name__),
        print_message=settings.settings["debug_mode"]
    )

    lang.write_info_log(
        message=f"{open_prth=}",
        module =lang.this_line(__name__),
        print_message=settings.settings["debug_mode"]
    )

    lang.write_info_log(
        message=f"{close_prth=}",
        module =lang.this_line(__name__),
        print_message=settings.settings["debug_mode"]
    )

    lang.write_info_log(
        message=f"{operators=}",
        module =lang.this_line(__name__),
        print_message=settings.settings["debug_mode"]
    )

    lang.write_info_log(
        message=f"{nums=}",
        module =lang.this_line(__name__),
        print_message=settings.settings["debug_mode"]
    )

    # Adds any opening parenthesis that are before everything
    output_string += "(" * open_prth.count(0)

    if settings.settings["literal"]:
        output_string += str_literal(nums[0])
    else:
        output_string += num_to_str(nums[0])

    for i, operator in enumerate(operators):
        output_string += ")" * close_prth.count(i)
        output_string += f" {operator} " if operator != "R" else "R "
        output_string += "(" * open_prth.count(i + 1)

        if not settings.settings["literal"]:
            output_string += num_to_str(nums[i + 1])

        else:
            pol_string = str_literal(nums[i + 1])
            if pol_string[0] == "-" and output_string[-2:] in ["+ ", "- "]:
                # Removes the last operator and puts a minus instead
                output_string = output_string[:-3]
                output_string += " - " + pol_string[1:]
            else:
                output_string += pol_string

    output_string += ")" * close_prth.count(len(operators))
    output_string += " = "

    if settings.settings["literal"]:
        output_string += str_literal(result) + "\n"
    else:
        output_string += num_to_str(result) + "\n"

    lang.write_info_log(
        message=output_string,
        module =lang.this_line(__name__)
    )

    return output_string
