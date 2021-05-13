################################
# Local dependencies
################################
import lang
import settings as sets

LANGUAGE = lang.language
OptionalFloat = float, None
memory = {}


# Finds the number ignoring commas and points based on certain criteria
def find_num(string: str, use_mem=True) -> OptionalFloat:
    ignore_char_list = ["(", ")"]
    char_quantity = {"points": 0, "commas": 0}
    char_last_pos = {"points": 0, "commas": 0}

    if sets.settings["accept_all"]:
        for index, char in enumerate(string):
            if char == ".":
                char_quantity["points"] += 1
                char_last_pos["points"] = index

            elif char == ",":
                char_quantity["commas"] += 1
                char_last_pos["commas"] = index

        if char_quantity["points"] > 1:
            ignore_char_list += "."

        if char_quantity["commas"] > 1:
            ignore_char_list += ","

        if ignore_char_list == ["(", ")"]:
            ignore_char_list += "." if char_last_pos["points"] < char_last_pos["commas"] else ","

    elif sets.settings["us_uk_sys"]:
        ignore_char_list = ["(", ")", ","]
    else:
        ignore_char_list = ["(", ")", "."]

    string_number = ""

    for index, char in enumerate(string):
        if char not in ignore_char_list:
            string_number += "." if char == "," else char
    try:
        return float(string_number)
    except ValueError:
        lang.write_error_log(
            "ValueError",
            "nums_func.py|find_num()|except",
            sets.settings["debug_mode"]
        )

        try:
            if use_mem:
                return memory[string_number]
            else:
                raise KeyError

        except KeyError:
            lang.write_error_log(
                "KeyError",
                "nums_func.py|find_num()|except|except",
                sets.settings["debug_mode"]
            )

            return None


def fix(number) -> OptionalFloat:
    if type(number) is complex: raise TypeError

    if type(number) is not float: return number

    # If the decimal part is longer than 10 digits is worth to try and fix it, else there's probably no error
    if len(str(number)) - len(str(int(number))) < 10:
        return number


    string = str(number)
    point_arrived = False

    cons_nines = 0
    max_cons_nines = 0
    nines_start = None

    cons_zeros = 0
    max_cons_zeros = 0
    zeros_start = None

    for char in range(len(string)):

        if string[char] == ".":
            point_arrived = True
            continue

        if point_arrived:
            if string[char] == "0" and string[char - 1] == "0":
                if cons_zeros == 0:
                    zeros_start = char - 1
                cons_zeros += 1

            elif string[char] == "9" and string[char - 1] == "9":
                if cons_nines == 0:
                    nines_start = char - 2 if string[char - 2] == "." else char - 1
                cons_nines += 1

            else:
                if cons_zeros > max_cons_zeros:
                    max_cons_zeros = cons_zeros

                if cons_nines > max_cons_nines:
                    max_cons_nines = cons_nines

                cons_zeros = 0
                cons_nines = 0

    if cons_zeros > max_cons_zeros:
        max_cons_zeros = cons_zeros

    if cons_nines > max_cons_nines:
        max_cons_nines = cons_nines

    if max_cons_zeros >= 3 or max_cons_nines >= 3:
        fixed_number = ""
        if nines_start is not None:
            for char in range(0, nines_start - 1):
                fixed_number += string[char]
            try:
                if string[nines_start] == ".":
                    raise ValueError
                fixed_number += str(int(string[nines_start - 1]) + 1)

            except ValueError:
                lang.write_error_log(
                    "ValueError",
                    "nums_func.py|fix()|if|if|except",
                    sets.settings["debug_mode"]
                )

                fixed_number = str(int(string[:nines_start]) + 1)

        elif zeros_start is not None:
            for char in range(0, zeros_start - 1):
                fixed_number += string[char]
            fixed_number += string[zeros_start - 1]

        try:
            return float(fixed_number)
        except ValueError:
            lang.write_error_log(
                "ValueError",
                "nums_func.py|fix()|if|except",
                sets.settings["debug_mode"]
            )

            return number
    else:
        return number


def num_to_str(number: float) -> str:
    try:
        number = fix(number)
        if type(number) is not float: return str(number)

    except OverflowError:
        lang.write_error_log(
            "OverflowError",
            "nums_func.py|num_to_str()|except",
            sets.settings["debug_mode"]
        )

        return LANGUAGE.lan.infinity

    except TypeError:
        lang.write_error_log(
            "TypeError",
            "nums_func.py|num_to_str()|except",
            sets.settings["debug_mode"]
        )

        if type(number) is complex:
            x_axis = num_to_str(number.real)
            y_axis = num_to_str(number.imag)

        else:
            x_axis = num_to_str(number.first_mon().num.real)
            y_axis = num_to_str(number.first_mon().num.imag)

        return f"X: {x_axis}, Y: {y_axis}"

    take_number = ""
    string_number = ""

    if abs(number) >= 100_000_000_000:
        exp = 0
        while len(str(abs(int(number)))) > 1:
            number /= 10
            exp += 1

        number = fix(number)
        if int(number) == number:
            string_number = str(int(number)) + "e" + str(exp)
        else:
            string_number = num_to_str(number) + "e" + str(exp)

    elif number <= -1000 or number >= 1000:
        is_negative = True if number < 0 else False
        abs_number = str(abs(int(number)))

        for i in range(len(abs_number) % 3):
            take_number += abs_number[i]

        for i in range(len(abs_number) % 3, len(abs_number)):
            if len(string_number) % 3 == 0 and i != 0:
                take_number += "," if sets.settings["us_uk_sys"] else "."
            take_number += str(abs_number)[i]
            string_number += str(abs_number)[i]

        if number > int(number):
            for i in range(len(str(int(number))), len(str(number))):
                if str(number)[i] == ".":
                    take_number += "." if sets.settings["us_uk_sys"] else ","
                else:
                    take_number += str(number)[i]

        string_number = "-" + take_number if is_negative else take_number

    else:
        if number > int(number):
            for char in str(number):
                if char == ".":
                    take_number += "." if sets.settings["us_uk_sys"] else ","
                else:
                    take_number += char
            string_number = take_number
        else:
            string_number = str(int(number))

    return string_number
