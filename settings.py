import json

settings = {
    "debug_mode"   : False,
    "ignore_prth"  : False,
    "us_uk_sys"    : False,
    "output_string": True,
    "accept_all"   : True,
    "literal"      : False,
    "lang"         : "EN"
}

lang_acronyms = {
    "IT": "Italiano",
    "EN": "English",
    "ES": "Espa\u00f1ol",
    "FR": "Fran\u00e7ais"
}

process_count = [0]

def update_settings():
    global settings, lang_acronyms, process_count

    settings = check_json_file(
        path="settings/settings.json",
        filetype=dict,
        check_keys=True,
        backup=settings
        )

    lang_acronyms = check_json_file(
        path="settings/lang_acronyms.json",
        filetype=dict,
        check_keys=True,
        backup=lang_acronyms
        )

    process_count = check_json_file(
        path="settings/process_count.json",
        filetype=list,
        check_len=True,
        backup=process_count
        )


def check_json_file(
    path:str,
    filetype,
    backup,
    check_keys=False,
    check_len=False
    ):

    try:
        with open(path) as j_file:
            new_file = json.load(j_file)

        if type(new_file) is not filetype:
            return backup

        if check_keys:
            for key in new_file:
                if key not in backup:
                    return backup

        if check_len:
            if len(new_file) != len(backup):
                return backup

        return new_file

    except Exception:
        with open(path, "w") as j_file:
            json.dump(backup, j_file)
            
        return backup


settings = check_json_file(
    path="settings/settings.json",
    filetype=dict,
    check_keys=True,
    backup=settings
    )

lang_acronyms = check_json_file(
    path="settings/lang_acronyms.json",
    filetype=dict,
    check_keys=True,
    backup=lang_acronyms
    )

process_count = check_json_file(
    path="settings/process_count.json",
    filetype=list,
    check_len=True,
    backup=process_count
    )
