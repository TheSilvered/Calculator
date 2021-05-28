import json
from inspect import currentframe

import lang_attrs

language = lang_attrs.Language


def this_line(name):
    return f"{name}: line {currentframe().f_back.f_lineno}"


def write_error_log(message: str, module: str, print_message: bool = False):
    with open(f"{lang_attrs.log_dir}error.log", "a") as log:
        log.write(f"{module} - {message}\n")

    if print_message: print(message)


def write_info_log(message: str, module: str, print_message: bool = False):
    with open(f"{lang_attrs.log_dir}info.log", "a") as log:
        log.write(f"{module} - {message}\n")

    if print_message: print(message)


def write_debug_log(message: str, module: str, print_message: bool = False):
    with open(f"{lang_attrs.log_dir}debug.log", "a") as log:
        log.write(f"{module} - {message}\n")

    if print_message: print(message)


def write_process_started_log():
    with open(f"settings/process_count.json", "r") as process_j:
        process = json.load(process_j)

    with open(f"{lang_attrs.log_dir}error.log", "a") as log:
        log.write(f"============== Process started {process} ==============\n")

    with open(f"{lang_attrs.log_dir}info.log", "a") as log:
        log.write(f"============== Process started {process} ==============\n")

    with open("calclog/debug.log", "a") as log:
        log.write(f"============== Process started {process} ==============\n")

    process[0] += 1

    with open("settings/process_count.json", "w") as process_j:
        json.dump(process, process_j)


def write_process_ended_log():
    with open(f"{lang_attrs.log_dir}error.log", "a") as log:
        log.write(f"=============== Process ended ===============\n")

    with open(f"{lang_attrs.log_dir}info.log", "a") as log:
        log.write(f"=============== Process ended ===============\n")

    with open(f"{lang_attrs.log_dir}debug.log", "a") as log:
        log.write(f"=============== Process ended ===============\n")


def load_txt(acronym: str, lang_dir: str = "langs", log=True):
    def add_to_attr(obj, attr, st, txt=""):
        new_attr = getattr(getattr(obj, st), attr)
        setattr(getattr(obj, st), attr, new_attr + txt)

    global language

    # Resets all attributes to be empty
    language = lang_attrs.Language

    file = open(f"{lang_dir}/{acronym}.lang", "r")
    main_set = ""
    attr = ""
    prev_invalid_attr = ""
    first_line = False

    for l_no, l in enumerate(file):
        if l[0] == "$":
            main_set = l.replace("$", "").replace("\n", "")

        elif l[0] == "@":
            attr = l.replace("@", "").replace("\n", "")
            first_line = True

        else:
            if l[0] == "&":
                l = l.replace("&", "").replace("\n", "")

            elif l[0:2] == "::":
                continue

            if hasattr(getattr(language, main_set), attr):
                if first_line:
                    setattr(getattr(language, main_set), attr, "")
                add_to_attr(language, attr, main_set, l)
                first_line = False

            elif prev_invalid_attr != attr:
                if log:
                    write_error_log(
                        message=f"Invalid attribute: '@{attr}' at line {l_no}",
                        module =this_line(__name__),
                        print_message=True
                    )

                # Prevents spam in a multiline invalid attribute
                prev_invalid_attr = attr

    file.close()

    if log:
        write_info_log(
            message="Text loaded",
            module =this_line(__name__)
        )

    return language
