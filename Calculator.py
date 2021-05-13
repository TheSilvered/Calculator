################################
# Local dependencies
################################
import new_cmds
import lang
import settings
from nums_func import num_to_str
from literals_func import str_literal
from calc_expression import Expression
from make_expression import make_expr


def build_result_string(open_prth, close_prth, operators, nums, result):
    output_string = ""

    if settings.settings["debug_mode"]:
        print("out_opening_prth", "=", open_prth )
        print("out_closing_prth", "=", close_prth)
        print("out_operators",    "=", operators )
        print("out_nums",         "=", nums      )

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
                output_string = output_string[:-3]  # Removes the last operator and puts a minus instead
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
        module ="Calculator.py|main()|if"
    )

    return output_string


def main(usr_inp: str) -> str:
    try:
        lang.write_info_log(
            f"usr_inp = '{usr_inp}'",
            "Calculator.py|main()|try"
        )

    except UnicodeError:
        lang.write_error_log(
            "UnicodeError",
            "Calculator.py|main()|except",
            settings.settings["debug_mode"]
        )

        return LANGUAGE.err.syntax_error

    if usr_inp == "":
        return LANGUAGE.err.syntax_error

    return_command = new_cmds.exe(usr_inp.lower())
    
    # If it's not a command, the function returns an empty string
    if return_command == "continue":
        return

    usr_inp = usr_inp \
        .replace(" ", "") \
        .replace("{", "(") \
        .replace("[", "(") \
        .replace("}", ")") \
        .replace("]", ")")

    if settings.settings["ignore_prth"]:
        usr_inp = usr_inp \
            .replace("(", "") \
            .replace(")", "")

    lang.write_info_log(
        message=f"fixed usr_inp = '{usr_inp}'",
        module="Calculator.py"
    )

    expression_defined = make_expr(usr_inp)
    expression = Expression(expression_defined)

    out_nums         = expression_defined[4]
    out_operators    = expression_defined[5]
    out_opening_prth = expression_defined[6]
    out_closing_prth = expression_defined[7]

    result, error_occurred = expression.optimized_calculation()

    if error_occurred != "":
        try:
            return getattr(LANGUAGE.lan, error_occurred)

        except AttributeError:
            return getattr(LANGUAGE.err, error_occurred)

    new_cmds.last_result = result

    if not settings.settings["output_string"]:
        if settings.settings["literal"]:
            return_str = str_literal(result) + "\n"
        else:
            return_str = num_to_str(result) + "\n"

    else:
        return_str = build_result_string(out_opening_prth, out_closing_prth, out_operators, out_nums, result)

    return return_str


if __name__ == "__main__":
    lang.write_process_started_log()
    settings.update_settings()

    LANGUAGE = lang.load_txt(settings.settings["lang"])
    print(LANGUAGE.msg.info_msg)

    running = True

    while running:
        try:
            output = main(input(LANGUAGE.inp.expression + "> "))

            if output is not None:
                print(output)

                with open("other/info/calc_history/calculations_history.txt", "a") as ophs:
                    ophs.write(output)

        except (StopIteration, KeyboardInterrupt):
            lang.write_process_ended_log()
            running = False

        except Exception as exception:
            # raise exception
            lang.write_error_log(
                str(exception),
                "Calculator.py|if|while|except",
                settings.settings["debug_mode"]
            )
            
            print(LANGUAGE.err.other_error + " '" + str(exception) + "'\n")
            continue

        except:
            lang.write_error_log(
                "FATAL ERROR",
                "Calculator.py|if|while|except",
                settings.settings["debug_mode"]
            )
