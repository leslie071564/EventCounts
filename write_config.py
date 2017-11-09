# -*- coding: utf-8 -*-
import sys
import argparse
PATH_DEAFAULTS = {"raw_dir": "/pear/share/www-uniq/v2006-2015.cf-preparation/knp", "raw_postfix": ".knp.xz",\
             "extract_tmp_dir": "/data/$USER/eventCount_extract_tmp",\
             "extract_dir": "$result_dir/extract_count",\
             "sort_tmp_dir": "/data/$USER/tmp",\
             "event_count_cdb_prefix": "$result_dir/event_count/event_count.cdb",\
             "event_sid_cdb_prefix": "$result_dir/event_sid/event_sid.cdb",\
            }

PATH_OPTS = ["result_dir", "raw_dir", "raw_postfix", "extract_tmp_dir", "extract_dir", "sort_tmp_dir"]
EXTRACT_OPTS = [ "extract_sid", "multi_arg", "only_verb" ]

def export_config_file(options):
    output_fn = open(options.output_fn, 'w')

    for path in PATH_OPTS:
        arg_line = '%s="%s"' % (path, getattr(options, path))
        output_fn.write(arg_line + '\n')

    for opt in EXTRACT_OPTS:
        if getattr(options, opt):
            arg_line = '%s=true' % opt
        else:
            arg_line = '%s=false' % opt

        output_fn.write(arg_line + '\n')

    extract_options = ["--%s" % (opt) for opt in EXTRACT_OPTS if getattr(options, opt)]
    output_fn.write('extract_options="%s"' % (" ".join(extract_options)))

    output_fn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    paths = parser.add_argument_group("paths")
    paths.add_argument("result_dir")
    paths.add_argument("--raw_dir", action="store", default=PATH_DEAFAULTS['raw_dir'], dest="raw_dir")
    paths.add_argument("--raw_postfix", action="store", default=PATH_DEAFAULTS['raw_postfix'], dest="raw_postfix")
    paths.add_argument("--extract_tmp_dir", action="store", default=PATH_DEAFAULTS['extract_tmp_dir'], dest="extract_tmp_dir")
    paths.add_argument("--extract_dir", action="store", default=PATH_DEAFAULTS['extract_dir'], dest="extract_dir")
    paths.add_argument("--sort_tmp_dir", action="store", default=PATH_DEAFAULTS['sort_tmp_dir'], dest="sort_tmp_dir")

    extract_opts = parser.add_argument_group("extract_options")
    extract_opts.add_argument("--extract_sid", action="store_true", dest="extract_sid")
    extract_opts.add_argument("--multi_arg", action="store_true", dest="multi_arg")
    extract_opts.add_argument("--only_verb", action="store_true", dest="only_verb")

    parser.add_argument('-o', "--output_fn", action="store", dest="output_fn")
    options = parser.parse_args() 

    export_config_file(options)
