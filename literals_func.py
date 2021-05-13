################################
# Local dependencies
################################
from literals import Pol, Mon
from lang import write_error_log
import settings
import nums_func


OptionalPol = Pol, None


def find_mon(string: str) -> OptionalPol:
    literal_start = None
    string = string.replace(")", "").replace("(", "")

    if string == "": return None  # It would return one without this

    negative_num = 0
    explicit_positive = 0

    for index, char in enumerate(string):
        try:
            int(char)
        except ValueError:
            write_error_log(
                "ValueError",
                "literals_func.py|find_mon()|for|except",
                settings.settings["debug_mode"]
            )

            if char == "-":
                negative_num = 1

            elif char == "+":
                explicit_positive = 1

            elif char in ".,":
                continue

            else:
                if index == 1:
                    literal_start = index - negative_num - explicit_positive
                else:
                    literal_start = index
                    negative_num = 0
                    explicit_positive = 0
                break

    if literal_start is None: literal_start = len(string)

    if literal_start == 0:
        if negative_num == 0: number = 1.0
        else: number = -1.0

    else: number = nums_func.find_num(string[0:literal_start])

    if number is None: return None

    letters = {}
    last_letter = ""
    temp_number = ""
    ciphers = "0123456789^."  # The "^" character is there just to not be considered in the letters
    allowed_letters = "abcdefghijklmnopqrstuvwxyz"  # To avoid not-operating symbols (@#?...) being considered letters
    literal = string[literal_start + negative_num + explicit_positive:]

    for char in literal:
        if (char not in ciphers) and (char in allowed_letters):
            letters[last_letter] = 1.0 if temp_number == "" else nums_func.find_num(temp_number)

            temp_number = ""
            letters[char] = 1.0
            last_letter = char

        elif char in ciphers:
            temp_number += char if char != "^" else ""

        else:
            return None

    letters[last_letter] = 1.0 if temp_number == "" else nums_func.find_num(temp_number)

    letters[""] = 1.0

    found_monomial = Mon(letters=letters, number=number)

    return Pol([found_monomial])


def str_literal(ltrl):
    if type(ltrl) is Mon:
        ltrl.fix()

        if ltrl.num == 1:
            temp_str = ""

        elif ltrl.num == -1:
            temp_str = "-"

        else:
            temp_str = nums_func.num_to_str(ltrl.num)

        if ltrl.lt[""] != 1:  # I assume that it's not float
            temp_str = f"{nums_func.num_to_str(ltrl.num)}^"
            power = nums_func.num_to_str(ltrl.lt[""])
            if len(power) == 1:
                temp_str += power
            else:
                temp_str += f"({power})"

        for letter in ltrl.lt:
            if letter == "": continue
            temp_str += letter
            if ltrl.lt[letter] != 1:
                if type(ltrl.lt[letter]) is float:
                    temp_str += f"^{nums_func.num_to_str(ltrl.lt[letter])}"
                else:
                    power = nums_func.num_to_str(ltrl.lt[letter])
                    if len(power) == 1:
                        temp_str += f"^{power}"
                    else:
                        temp_str += f"^({power})"

        if temp_str == "":
            temp_str = "1"
        elif temp_str == "-":
            temp_str = "-1"

        return temp_str

    elif type(ltrl) is Pol:
        ltrl.normal().clean()

        temp_str = ""

        for monomial in ltrl.mon:
            if monomial.num >= 0 and temp_str == "":
                temp_str += str_literal(abs(monomial))

            elif monomial.num < 0 and temp_str == "":
                temp_str += str_literal(monomial)

            elif monomial.num >= 0:
                temp_str += " + " + str_literal(monomial)

            else:
                temp_str += " - " + str_literal(abs(monomial))

        return temp_str
