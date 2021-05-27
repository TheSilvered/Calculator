class Language:


    class Msg:
        info_msg            = ""
        help_msg            = ""
        advanced_help       = ""
        example             = ""
        available_languages = ""
        added_to_mem        = ""
        deleted_from_mem    = ""
        empty_mem           = ""
        settings_res        = ""
        mem_res             = ""
        lang_loaded         = ""
        file_saved          = ""
        file_opened         = ""
        empty_ophs          = ""
        ophs_res            = ""


    class Err:
        syntax_error         = ""
        non_int_root_error   = ""
        file_not_found       = ""
        invalid_command      = ""
        invalid_arg          = ""
        permission_error     = ""
        no_num_name          = ""
        no_mem_cell          = ""
        invalid_answer       = ""
        no_such_cmd          = ""
        no_such_lang         = ""
        impossible_div_error = ""
        non_int_pow_error    = ""
        name_error           = ""
        inaccessible_mem     = ""
        other_error          = ""
        invalid_version      = ""
        invalid_data         = ""


    class Inp:
        expression   = ""
        stop         = ""
        lang_acronym = ""
        add_mem      = ""
        del_mem      = ""
        mem_res      = ""
        settings_res = ""
        save_path    = ""
        open_path    = ""
        file_name    = ""
        ophs_res     = ""


    class Out:
        debug_mode          = ""
        ignore_prth         = ""
        us_uk_sys           = ""
        output_string       = ""
        accept_all          = ""
        lang                = ""
        switch              = ""
        literal             = ""
        operation_cancelled = ""


    class Lan:
        infinity     = ""
        true         = ""
        false        = ""
        undetermined = ""
        impossible   = ""


    class Cmd:
        bs_advn = ""
        bs_exmp = ""
        bs_help = ""
        bs_info = ""
        bs_lang = ""
        bs_stop = ""
        bs_vshs = ""
        bs_ltrl = ""
        bs_memr = ""
        bs_sets = ""
        bs_ophs = ""
        ad_dbug = ""
        ad_exit = ""
        ad_prth = ""
        ad_path = ""
        ad_gthb = ""

    msg = Msg
    err = Err
    inp = Inp
    out = Out
    lan = Lan
    cmd = Cmd


log_dir = "calclog/"
