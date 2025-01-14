import pyperclip

import json
import os

import lang
import settings
import nums_func
import cmds_parser

LANGUAGE = lang.language
LOCAL_DIR = os.path.abspath(".")
last_result = None


class InvalidDataFileError(Exception):
    """
    Exception raised when trying to open a .calc file and it's not valid or of
    the expected type
    """
    pass


class ReservedNameError(Exception):
    """
    Exception raised when trying to save a file with a windows reserved name
    such as CON, PRN, AUX, ...
    """
    pass


def exe(usr_inp: str):
    COMMAND_KEYS = "_#"

    FUNCTION_MAPPINGS = {
        "_help": {"func": bs_help              , "args": True },
        "_info": {"func": bs_info              , "args": False},
        "_advn": {"func": bs_advanced          , "args": False},
        "_exmp": {"func": bs_example           , "args": False},
        "_vshs": {"func": bs_vs_history        , "args": True },
        "_sets": {"func": bs_settings          , "args": True },
        "_lang": {"func": bs_language          , "args": True },
        "_stop": {"func": bs_stop              , "args": False},
        "_memr": {"func": bs_memory            , "args": True },
        "_ltrl": {"func": bs_literal           , "args": False},
        "_ophs": {"func": bs_operations_history, "args": True },
        "#gthb": {"func": bs_github_link       , "args": False},
        "#code": {"func": bs_github_link       , "args": False},
        "#ltrl": {"func": bs_literal           , "args": False},
        "#exit": {"func": ad_exit              , "args": False},
        "#inst": {"func": ad_exit              , "args": False},
        "#dbug": {"func": ad_debug             , "args": False},
        "#prth": {"func": ad_ignore_prth       , "args": False},
        "#path": {"func": ad_path              , "args": False},
        "#prcs": {"func": ad_process           , "args": False}
    }

    try:
        command = cmds_parser.parse(
            cmd_string=usr_inp,
            key=COMMAND_KEYS,
            mapping=FUNCTION_MAPPINGS,
            float_func=nums_func.find_num,
            float_func_args=False
        )

        if command is None: return ""

        if settings.settings["debug_mode"]:
            print(f"command.name = {command.name}")
            print(f"command.args = {command.args}")
            print(f"command.acc_args = {command.acc_args}")

        command.exe()

        # Saves the settings whether or not there were any changes
        with open("settings/settings.json", "w") as j_settings:
            json.dump(settings.settings, j_settings)

        settings.update_settings()

    except (
        KeyError,
        OSError,
        TypeError,
        InvalidDataFileError,
        cmds_parser.InvalidCommandError

    ) as e:
        lang.write_error_log(
            message=f"KeyError, OSError, TypeError, InvalidCommandError: {e}",
            module =lang.this_line(__name__),
            print_message=settings.settings["debug_mode"]
        )

        print(LANGUAGE.err.invalid_command)

    except InvalidDataFileError:
        lang.write_error_log(
            message="InvalidDataFileError",
            module =lang.this_line(__name__),
            print_message=settings.settings["debug_mode"]
        )

        print(LANGUAGE.err.invalid_data)

    except FileNotFoundError:
        lang.write_error_log(
            message="FileNotFoundError",
            module =lang.this_line(__name__),
            print_message=settings.settings["debug_mode"]
        )

        print(LANGUAGE.err.file_not_found)

    except PermissionError:
        lang.write_error_log(
            message="PermissionError",
            module =lang.this_line(__name__),
            print_message=settings.settings["debug_mode"]
        )

        print(LANGUAGE.err.permission_error)

    except UnicodeError:
        lang.write_error_log(
            message="UnicodeError",
            module =lang.this_line(__name__),
            print_message=settings.settings["debug_mode"]
        )

        print(LANGUAGE.err.file_not_found)

    except ReservedNameError:
        lang.write_error_log(
            message="ReservedNameError",
            module =lang.this_line(__name__),
            print_message=settings.settings["debug_mode"]
        )

        print(LANGUAGE.err.name_error)

    return "continue"

#-------------------------------------------------------------------------------
def get_answer(message:str):
    answer = input(f"\n{message}> ")
    if answer.lower() == "y": return True
    elif answer.lower() == "n": return False
    else: return None

#-------------------------------------------------------------------------------
def switch_settings(dict_key: str):
    settings.settings[dict_key] = not settings.settings[dict_key]

    set_to = str(settings.settings[dict_key]).lower()

    parameter_changed = getattr(LANGUAGE.out, dict_key)
    is_now = LANGUAGE.out.switch
    true_or_false = getattr(LANGUAGE.lan, set_to)

    print(f"'{parameter_changed}' {is_now} {true_or_false}\n")

#-------------------------------------------------------------------------------
def set_path(args):
    if len(args) == 1:
        file_path = input(f"\n{LANGUAGE.inp.open_path}> ")

    elif len(args) == 2:
        file_path = args[1]

    else:
        raise cmds_parser.InvalidCommandError

    if len(file_path) <= 5 or file_path[-5:] != ".calc":
        name = input(f"\n{LANGUAGE.inp.file_name}> ")

        if len(name) <= 5 or name[-5:] != ".calc":
            name += ".calc"

        file_path = os.path.join(file_path, name)

    file_path = file_path.replace("/", "\\")

    lang.write_info_log(
        message=f"Save file path: {file_path}",
        module =lang.this_line(__name__)
    )

#-------------------------------------------------------------------------------
def bs_help(args):
    # If there is no command specified
    if not args:
        print(LANGUAGE.msg.help_msg)

    elif len(args) == 1:
        attr = args[0].replace("_", "bs_").replace("#", "ad_")

        if hasattr(LANGUAGE.cmd, attr):
            print(getattr(LANGUAGE.cmd, attr))

        else:
            print(f"{LANGUAGE.err.no_such_cmd} '{args[0]}'\n")

    else:
        print(f"{LANGUAGE.err.invalid_arg} '{args[1]}'\n")

#-------------------------------------------------------------------------------
def bs_info():
    print(LANGUAGE.msg.info_msg)

#-------------------------------------------------------------------------------
def bs_advanced():
    print(LANGUAGE.msg.advanced_help)

#-------------------------------------------------------------------------------
def bs_example():
    print(LANGUAGE.msg.example)

#-------------------------------------------------------------------------------
def bs_vs_history(args):
    NEWS_KEYWORDS = ["last", "latest", "news", "potato"]
    VS_PATH = "other/installer/VERSION_HISTORY.txt"

    def show_all():
        print()
        with open(VS_PATH, "r") as version_history_file:
            for line in version_history_file:
                print(line.replace("\n", ""))
        print()


    def show_news():
        with open(VS_PATH, "r") as version_history_file:
            for line_count, line in enumerate(version_history_file):
                if line_count == 3:
                    # The last version is always in this position in the file
                    last_version = line[8:15]
                    break

        show_version(last_version)


    def show_version(version: str):
        try:
            with open(f"other/info/versions/{version}.txt") as version_file:
                for line in version_file:
                    print(line.replace("\n", ""))
                print()

        except FileNotFoundError:
            print(LANGUAGE.err.invalid_version)


    if not args:
        show_all()

    elif args == ["path"]:
        path = os.path.join(LOCAL_DIR, VS_PATH)

        print(path, "\n")
        pyperclip.copy(path)

    elif len(args) == 1 and args[0].lower() in NEWS_KEYWORDS:
        show_news()

    elif len(args) == 1:
        show_version(args[0])

    else:
        print(f"{LANGUAGE.err.invalid_arg} '{args[1]}'\n")

#-------------------------------------------------------------------------------
def bs_settings(args):
    def show():
        def make_str(st: str, gt_from="settings"):
            setting = settings.settings[st]

            if gt_from == "settings": 
                set_status = getattr(LANGUAGE.lan, str(setting).lower())
            elif gt_from == "lang_acronyms":
                set_status = settings.lang_acronyms[setting]
            else:
                set_status = ""

            string = ""
            string += f"{getattr(LANGUAGE.out, st)}: "
            string += set_status


            return string

        print()

        print(make_str("debug_mode"))
        print(make_str("ignore_prth"))
        print(make_str("output_string"))
        print(make_str("literal"))
        print()

        print(make_str("us_uk_sys"))
        print(make_str("accept_all"))
        print()

        print(make_str("lang", "lang_acronyms"))
        print()


    def reset():
        answer = get_answer(LANGUAGE.inp.settings_res)
        lang.write_info_log(
            message=f"Answer: {answer}",
            module =lang.this_line(__name__)
        )

        if answer is None:
            print(LANGUAGE.err.invalid_answer)

        if answer:
            settings.settings["debug_mode"]    = False
            settings.settings["us_uk_sys"]     = False
            settings.settings["ignore_prth"]   = False
            settings.settings["output_string"] = True
            settings.settings["accept_all"]    = True
            settings.settings["literal"]       = False
            print(LANGUAGE.msg.settings_res)

        else:
            print(LANGUAGE.out.operation_cancelled)

    def open_settings_file(file_info):
        if len(file_info) == 1:
            file_path = input(f"\n{LANGUAGE.inp.open_path}> ")

        elif len(file_info) == 2:
            file_path = file_info[1]

        else:
            print(f"{LANGUAGE.err.invalid_arg} '{file_info[3]}'\n")
            return

        file_path = file_path.replace("/", "\\")

        lang.write_info_log(
            message=f"Open file path: {file_path}",
            module =lang.this_line(__name__)
        )

        if len(file_path) <= 5 or file_path[-5:] != ".calc":
            fname = input(f"\n{LANGUAGE.inp.file_name}> ")

            if len(name) <= 5 or name[-5:] != ".calc":
                name += ".calc"

            file_path = os.path.join(file_path, name)

        lang.write_info_log(
            message=f"Open file name: {file_path}",
            module =lang.this_line(__name__)
        )

        with open(file_path, "r") as sets_file:
            try:
                sets_dict = json.load(sets_file)

                if sets_dict["type"] == "sets":
                    new_sets = sets_dict["data"]

                else: raise InvalidDataFileError


            except KeyError: raise InvalidDataFileError

        # Prevents invalid settings from being inserted
        for key in new_sets:
            if not key in settings.settings:
                raise InvalidDataFileError

            if type(new_sets[key]) is not type(settings.settings[key]):
                raise InvalidDataFileError

        with open("settings/settings.json", "w") as json_settings:
            json.dump(new_sets, json_settings)

        settings.update_settings()
        bs_language(["reload"])

        print(f"'{file_path}' {LANGUAGE.msg.file_opened}\n")


    def save_settings_file(file_info):

        if len(file_info) == 1:
            file_path = input(f"\n{LANGUAGE.inp.open_path}> ")

        elif len(file_info) == 2:
            file_path = file_info[1]

        else:
            print(f"{LANGUAGE.err.invalid_arg} '{file_info[2]}'\n")
            return

        file_path = file_path.replace("/", "\\")

        if len(file_path) <= 5 or file_path[-5:] != ".calc":
            name = input(f"\n{LANGUAGE.inp.file_name}> ")

            if len(name) <= 5 or name[-5:] != ".calc":
                name += ".calc"

            file_path = os.path.join(file_path, name)

        file_path = file_path.replace("/", "\\")

        lang.write_info_log(
            message=f"Save file path: {file_path}",
            module =lang.this_line(__name__)
        )

        last_slash = 0
        for i, char in enumerate(file_path):
            if char == "\\" or char == "/":
                last_slash = i + 1

        file_name = file_path[last_slash:-5].lower()  # The -5 removes .calc
        RESERVED_FILE_NAMES = [
            "con",  "prn",  "aux",  "nul",  "com1", "com2", "com3", "com4",
            "com5", "com6", "com7", "com7", "com8", "com9", "com0", "lpt1", 
            "lpt2", "lpt3", "lpt4", "lpt5", "lpt6", "lpt7", "lpt8", "lpt9",
            "lpt0"
        ]

        if file_name in RESERVED_FILE_NAMES:
            raise ReservedNameError

        sets_to_save = {"type": "sets", "data": settings.settings}

        with open(file_path, "w") as sets_file:
            json.dump(sets_to_save, sets_file)

        settings.update_settings()
        bs_language(["reload"])

        print(f"{LANGUAGE.msg.file_saved} {file_path}\n")


    if not args:
        show()

    elif args == ["expr"]:
        switch_settings("output_string")

    elif args == ["acal"]:
        switch_settings("accept_all")

    elif args == ["swap"]:
        switch_settings("us_uk_sys")

    elif args == ["reset"]:
        reset()

    elif len(args) >= 1 and args[0] == "open":
        open_settings_file(args)

    elif len(args) >= 1 and args[0] == "save":
        save_settings_file(args)

    else:
        print(f"{LANGUAGE.err.invalid_arg} '{args[0]}'\n")

#-------------------------------------------------------------------------------

def bs_language(args):
    def reload_lang():
        lang.load_txt(settings.settings["lang"])

        print(LANGUAGE.msg.lang_loaded)


    def add_language(lang_info):
        if len(lang_info) != 3:
            print("Not enough arguments")
            return

        lang_acronym = lang_info[1].upper
        lang_name = lang_info[2]

        lang.write_info_log(
            message=f"acronym = {lang_acronym}",
            module =lang.this_line(__name__)
        )

        lang.write_info_log(
            message=f"lang_name = {lang_name}",
            module =lang.this_line(__name__)
        )

        # To make sure the file exists
        with open(f"langs/{lang_acronym}.lang"):
            pass

        settings.lang_acronyms[lang_acronym] = lang_name
        with open("settings/lang_acronyms.json", "w") as j_acronym_lang:
            json.dump(settings.lang_acronyms, j_acronym_lang)

    language = ""

    if not args:
        # Prints out the list of available languages
        print(LANGUAGE.msg.available_languages)
        for acronym in settings.lang_acronyms:
            print(f"{acronym} -> {settings.lang_acronyms[acronym]}")

        language = input(f"\n{LANGUAGE.inp.lang_acronym}> ").upper()

    elif args == ["reload"]:
        reload_lang()
        return

    elif len(args) >= 1:
        if args[0] == "add": add_language(args)

        elif len(args) == 1: language = args[0].upper()

        else: raise cmds_parser.InvalidCommandError

    else: raise cmds_parser.InvalidCommandError

    lang.write_info_log(
        message=f"Acronym: {language}",
        module =lang.this_line(__name__)
    )


    if language in settings.lang_acronyms:
        settings.settings["lang"] = language
        lang.load_txt(language)
        print(
            f"'{LANGUAGE.out.lang}' "
            f"{LANGUAGE.out.switch} "
            f"{settings.lang_acronyms[language]}\n"
        )

    else: print(LANGUAGE.err.no_such_lang)

#-------------------------------------------------------------------------------

def bs_stop():
    answer = get_answer(LANGUAGE.inp.stop)

    lang.write_info_log(
        message=f"Answer: {answer}",
        module =lang.this_line(__name__)
    )

    if answer is None:
        print(LANGUAGE.err.invalid_answer)

    if answer:
        raise StopIteration
        
    else:
        print(LANGUAGE.out.operation_cancelled)

#-------------------------------------------------------------------------------

def bs_memory(args):


    def show_memory():
        if nums_func.memory == {}: print(LANGUAGE.msg.empty_mem)
        else:
            print()
            for key in nums_func.memory:
                try:
                    value = nums_func.num_to_str(nums_func.memory[key])
                    print(f"{key} = {value}")

                except OverflowError:
                    lang.write_error_log(
                        message="OverflowError",
                        module =lang.this_line(__name__),
                        print_message=settings.settings["debug_mode"]
                    )

                    print(f"{key} = {LANGUAGE.lan.infinity}")
            print()


    def add_memory(num_to_add_info):
        if len(num_to_add_info) == 1:
            add_mem = input(f"\n{LANGUAGE.inp.add_mem}> ")

            lang.write_info_log(
                message=f"Input: {add_mem}",
                module =lang.this_line(__name__)
            )

            name_value = add_mem.split()
            mem_cell_name = name_value[0]
            if len(name_value) > 1:
                mem_cell_value = nums_func.find_num(name_value[1])

            else:
                mem_cell_value = last_result

            if mem_cell_value is None and last_result is not None:
                print(f"{LANGUAGE.err.invalid_arg} '{name_value[1]}'\n")
                return

            elif mem_cell_value is None and last_result is None:
                raise cmds_parser.InvalidCommandError

        elif 2 <= len(num_to_add_info) <= 3:
            mem_cell_name = num_to_add_info[1]

            if len(num_to_add_info) == 2:
                mem_cell_value = last_result

            else:
                # The value is already a float
                mem_cell_value = num_to_add_info[2]

            if type(mem_cell_name) is float:
                print(f"{LANGUAGE.err.invalid_arg} '{num_to_add_info[1]}'\n")
                return

            elif type(mem_cell_value) is not float:
                print(f"{LANGUAGE.err.invalid_arg} '{num_to_add_info[2]}'\n")
                return

        else:
            print(f"{LANGUAGE.err.invalid_arg} '{num_to_add_info[3]}'\n")
            return

        lang.write_info_log(
            message=f"Name: {mem_cell_name}",
            module =lang.this_line(__name__)
        )

        lang.write_info_log(
            message=f"Value: {mem_cell_value}",
            module =lang.this_line(__name__)
        )

        if nums_func.find_num(mem_cell_name, False) is not None:
            print(LANGUAGE.err.no_num_name)
            return

        nums_func.memory[mem_cell_name] = mem_cell_value

        str_value = nums_func.num_to_str(mem_cell_value)

        print(f"'{mem_cell_name} = {str_value}' {LANGUAGE.msg.added_to_mem}\n")


    def del_memory(num_to_del_info):
        if len(num_to_del_info) == 1:
            mem_cell_name = input(f"\n{LANGUAGE.inp.del_mem}> ")

        elif len(num_to_del_info) == 2:
            mem_cell_name = num_to_del_info[1]

        else:
            print(f"{LANGUAGE.err.invalid_arg} '{num_to_del_info[2]}'\n")
            return

        lang.write_info_log(
            message=f"Cell: {mem_cell_name}",
            module =lang.this_line(__name__)
        )

        try:
            del nums_func.memory[mem_cell_name]
            print(f"'{mem_cell_name}' {LANGUAGE.msg.deleted_from_mem}\n")

        except KeyError:
            lang.write_error_log(
                message="KeyError",
                module =lang.this_line(__name__),
                print_message=settings.settings["debug_mode"]
            )

            print(LANGUAGE.err.no_mem_cell)


    def clear_memory():
        answer = get_answer(LANGUAGE.inp.mem_res)
        lang.write_info_log(
            message=f"Answer: {answer}",
            module =lang.this_line(__name__)
        )

        if answer is None:
            print(LANGUAGE.err.invalid_answer)

        if answer:
            nums_func.memory = {}
            print(LANGUAGE.msg.mem_res)

        else:
            print(LANGUAGE.out.operation_cancelled)


    def open_memory_file(file_info):
        overwrite = False

        if len(file_info) == 1:
            file_path = input(f"\n{LANGUAGE.inp.open_path}> ")

        elif len(file_info) == 2:
            file_path = file_info[1]

        elif len(file_info) == 3:
            file_path = file_info[1]

            if type(file_info[2]) is not bool:
                print(f"{LANGUAGE.err.invalid_arg} '{file_info[2]}'\n")
                return

        else:
            print(f"{LANGUAGE.err.invalid_arg} '{file_info[3]}'\n")
            return

        file_path = file_path.replace("/", "\\")

        lang.write_info_log(
            message=f"Open file path: {file_path}",
            module =lang.this_line(__name__)
        )

        if (len(file_path) <= 5 or file_path[-5:] != ".calc") or \
           (len(file_path) <= 4 or file_path[-4:] != ".mem"):
            name = input(f"\n{LANGUAGE.inp.file_name}> ")

            if (len(name) <= 5 or name[-5:] != ".calc") or \
               (len(name) <= 4 or name[-5:] != ".mem"):
                name += ".calc"

            file_path = os.path.join(file_path, name)

        lang.write_info_log(
            message=f"overwrite = {overwrite}",
            module =lang.this_line(__name__)
        )

        if len(file_path) >= 5 and file_path[-5:] == ".calc":
            is_old_mem = False

        elif len(file_path) >= 4 and file_path[-4:] == ".mem":
            is_old_mem = True

        lang.write_info_log(
            message=f"Open file name: {file_path}",
            module =lang.this_line(__name__)
        )

        with open(file_path, "r") as mem_file:
            if is_old_mem:
                new_mem = json.load(mem_file)
            else:
                try:
                    mem_dict = json.load(mem_file)

                    if mem_dict["type"] == "memr":
                        new_mem = mem_dict["data"]

                    else:
                        raise InvalidDataFileError

                except KeyError:
                    raise InvalidDataFileError

        if overwrite:
            lang.memory = new_mem

        else:
            for key in new_mem:
                nums_func.memory[key] = new_mem[key]

        print(f"'{file_path}' {LANGUAGE.msg.file_opened}\n")


    def save_memory_file(file_info):
        if len(file_info) == 1:
            file_path = input(f"\n{LANGUAGE.inp.open_path}> ")

        elif len(file_info) == 2:
            file_path = file_info[1]

        else:
            print(f"{LANGUAGE.err.invalid_arg} '{file_info[2]}'\n")
            return

        file_path = file_path.replace("/", "\\")

        if len(file_path) <= 5 or file_path[-5:] != ".calc":
            name = input(f"\n{LANGUAGE.inp.file_name}> ")

            if len(name) <= 5 or name[-5:] != ".calc":
                name += ".calc"

            file_path = os.path.join(file_path, name)

        file_path = file_path.replace("/", "\\")

        lang.write_info_log(
            message=f"Save file path: {file_path}",
            module =lang.this_line(__name__)
        )

        last_slash = 0
        for i, char in enumerate(file_path):
            if char == "\\" or char == "/":
                last_slash = i + 1

        file_name = file_path[last_slash:-5].lower()  # The -5 removes .calc
        RESERVED_FILE_NAMES = [
            "con",  "prn",  "aux",  "nul",  "com1", "com2", "com3", "com4",
            "com5", "com6", "com7", "com7", "com8", "com9", "com0", "lpt1", 
            "lpt2", "lpt3", "lpt4", "lpt5", "lpt6", "lpt7", "lpt8", "lpt9",
            "lpt0"
        ]

        if file_name in RESERVED_FILE_NAMES:
            raise ReservedNameError

        mem_to_save = {"type": "memr", "data": nums_func.memory}

        with open(file_path, "w") as mem_file:
            json.dump(mem_to_save, mem_file)

        print(f"{LANGUAGE.msg.file_saved} {file_path}\n")


    if settings.settings["literal"]:
            print(LANGUAGE.err.inaccessible_mem)
            return

    if not args: show_memory()

    elif len(args) >= 1 and args[0] == "add": add_memory(args)

    elif len(args) >= 1 and args[0] == "del": del_memory(args)

    elif len(args) >= 1 and args[0] == "clear": clear_memory()

    elif len(args) >= 1 and args[0] == "open": open_memory_file(args)

    elif len(args) >= 1 and args[0] == "save": save_memory_file(args)

#-------------------------------------------------------------------------------

def bs_literal():
    switch_settings("literal")

#-------------------------------------------------------------------------------

def ad_exit():
    raise StopIteration

#-------------------------------------------------------------------------------

def ad_debug():
    switch_settings("debug_mode")

#-------------------------------------------------------------------------------

def ad_ignore_prth():
    switch_settings("ignore_prth")

#-------------------------------------------------------------------------------

def ad_path():
    print(LOCAL_DIR, "\n")
    pyperclip.copy(LOCAL_DIR)

#-------------------------------------------------------------------------------

def ad_process():
    with open("settings/process_count.json") as j_process:
        process = json.load(j_process)
    print(process[0])
    print()

#-------------------------------------------------------------------------------

def bs_operations_history(args):
    CALC_HISTORY_PATH = "other/info/calc_history/calculations_history.txt"

    def show():
        with open(CALC_HISTORY_PATH, "r") as calc_hs:
            is_empty = True

            for line in calc_hs:
                is_empty = False
                print(line.replace("\n", ""))

            if is_empty:
                print(LANGUAGE.msg.empty_ophs)
            else:
                print()
        return


    def clear():
        answer = get_answer(LANGUAGE.inp.ophs_res)

        if answer is None:
            print(LANGUAGE.err.invalid_answer)

        elif answer:
            with open(CALC_HISTORY_PATH, "w"):
                pass

            print(LANGUAGE.msg.ophs_res)

        else:
            print(LANGUAGE.out.operation_cancelled)


    if not args: show()

    if args == ["clear"]: clear()

    else: print(f"{LANGUAGE.err.invalid_arg} '{args[1]}'\n")


def bs_github_link():
    link = "https://github.com/TheSilvered/Calculator3"
    pyperclip.copy(link)
    print(link)
    print()
