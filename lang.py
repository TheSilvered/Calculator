################################
# Local dependencies
################################
import lang_attrs

################################
# External modules
################################
import json



language = lang_attrs.Language


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
    with open(f"settings/process_count.json") as process_j:
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


def load_txt(acronym: str):
    def add_to_attr(obj, attr, st, txt=""):
        new_attr = getattr(getattr(obj, st), attr)
        setattr(getattr(obj, st), attr, new_attr + txt)

    global language

    language = lang_attrs.Language

    file = open(f"langs/{acronym}.lang", "r")
    main_set = ""
    attribute = ""
    previous_invalid_attribute = ""
    first_line = False

    for line_count, line in enumerate(file):
        if line[0] == "$":
            main_set = line.replace("$", "").replace("\n", "")

        elif line[0] == "@":
            attribute = line.replace("@", "").replace("\n", "")
            first_line = True

        else:
            if line[0] == "&":
                line = line.replace("&", "").replace("\n", "")

            elif line[0:2] == "::":
                continue

            if hasattr(getattr(language, main_set), attribute):
                if first_line: setattr(getattr(language, main_set), attribute, "")
                add_to_attr(language, attribute, main_set, line)
                first_line = False

            elif previous_invalid_attribute != attribute:
                write_error_log(
                    f"Invalid attribute: '@{attribute}' at line {line_count}",
                    "lang.py|load_txt()|for|else|elif",
                    True
                )
                previous_invalid_attribute = attribute  # Prevents spam in a multiline invalid attribute

    file.close()

    write_info_log("Text loaded", "lang.py|load_txt()")

    return language
