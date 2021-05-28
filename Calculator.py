import new_cmds
import lang
import settings
import expression
from output_string import build_result_string


def main(usr_inp: str) -> str:
    try:
        lang.write_info_log(
            message=f"usr_inp = '{usr_inp}'",
            module =lang.this_line(__name__)
        )

    except UnicodeError:
        lang.write_error_log(
            message="UnicodeError",
            module =lang.this_line(__name__),
            print_message=settings.settings["debug_mode"]
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
        module =lang.this_line(__name__)
    )

    expression_defined = expression.make_expr(usr_inp)
    expression_object = expression.Expression(expression_defined)

    out_nums         = expression_defined[4]
    out_operators    = expression_defined[5]
    out_opening_prth = expression_defined[6]
    out_closing_prth = expression_defined[7]

    result, error_occurred = expression_object.solve()

    if error_occurred != "":
        try:
            return getattr(LANGUAGE.lan, error_occurred)

        except AttributeError:
            return getattr(LANGUAGE.err, error_occurred)

    new_cmds.last_result = result
    return_str = build_result_string(
        out_opening_prth,
        out_closing_prth,
        out_operators,
        out_nums, result
    )

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
                path = "other/info/calc_history/calculations_history.txt"

                with open(path, "a") as ophs:
                    ophs.write(output)

        except (StopIteration, KeyboardInterrupt):
            lang.write_process_ended_log()
            print()
            running = False

        except Exception as exception:
            # raise exception

            lang.write_error_log(
                message=f"Unexpected error:  {exception}",
                module =lang.this_line(__name__),
                print_message=settings.settings["debug_mode"]
            )

            print(LANGUAGE.err.other_error + " '" + str(exception) + "'\n")
            continue

        except:
            lang.write_error_log(
                message="FATAL ERROR",
                module =lang.this_line(__name__),
                print_message=True
            )
