# -*- coding: utf-8 -*-
import sys
import argparse
import os.path
from glob import glob
import os
import fnmatch

def check_existence(folder_stamp, file_stamp):
    check_file = "%s/%s/%s%s.knp.xz" % (raw_dir, '/'.join(folder_stamp), folder_stamp, file_stamp)
    return os.path.isfile(check_file)

def get_config(setting_fn):
    lines = [line.rstrip().replace('"', '') for line in open(setting_fn, 'r').readlines()]
    settings = dict(line.split('=') for line in lines)
    return settings

def print_event_extract_task(config_fn, output_fn):
    settings = get_config(config_fn)
    raw_dir = settings['raw_dir']
    
    extract_script = "./count_events.sh"
    output_file = open(output_fn, 'w')
    for root, dirnames, filenames in os.walk("%s" % raw_dir):
        if filenames == []:
            continue
        for fn_base in filenames:
            fn_base = fn_base.split('.')[0]
            relpath = os.path.relpath(root, raw_dir)
            if relpath != '.':
                file_stamp = "%s/%s" % (relpath, fn_base)
            else:
                file_stamp = fn_base

            cmd = "%s %s %s" % (extract_script, file_stamp, config_fn)
            output_file.write(cmd + '\n')

def print_merge_task(config_fn, output_fn):
    settings = get_config(config_fn)
    result_dir = settings['result_dir']
    extract_dir = settings['extract_dir'].replace('$result_dir', result_dir)
    merge_tmp_dir, sort_tmp_dir = settings['extract_tmp_dir'], settings['sort_tmp_dir']
    with_sid = "--extract_sid" in settings['extract_options']

    output_file = open(output_fn, 'w')
    for root, dirnames, filenames in os.walk("%s" % extract_dir, topdown=False):
        rel_path = os.path.relpath(root, extract_dir)

        if filenames == []:
            continue

        if rel_path == ".":
            concat_fn = "%s/all_concat" % merge_tmp_dir
            merged_file = "%s/all_events.txt" % result_dir
        else:
            concat_fn = "%s/%s_concat" % (merge_tmp_dir, rel_path.replace('/', ''))
            merge_dir = os.path.dirname("%s/%s" % (extract_dir, rel_path))
            merged_file = "%s/%s_merged" % (merge_dir, rel_path.replace('/', ''))

        cat_cmd = "cat %s/* > %s" % (root, concat_fn)
        sort_cmd = "LC_ALL=C sort --temporary-directory=%s -k2,2 %s -o %s" % (sort_tmp_dir, concat_fn, concat_fn)
        if with_sid:
            merge_cmd = "python ./merge.py -f %s -t 2 -s > %s" % (concat_fn, merged_file)
        else:
            merge_cmd = "python ./merge.py -f %s -t 2 -c > %s" % (concat_fn, merged_file)
        rm_cmd = "rm -rf %s" % (root)
        cmd = " && ".join([cat_cmd, sort_cmd, merge_cmd, rm_cmd])
        output_file.write(cmd + '\n')
        #print cmd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', "--event_extract_task", action="store_true", dest="event_extract_task")
    parser.add_argument('-m', "--merge_task", action="store_true", dest="merge_task")

    parser.add_argument('--config_fn', action="store", default="./config.sh", dest="config_fn")
    parser.add_argument('--task_fn', action="store", default="./tmp", dest="task_fn")

    options = parser.parse_args() 

    if options.event_extract_task:
        print_event_extract_task(options.config_fn, options.task_fn)

    if options.merge_task:
        print_merge_task(options.config_fn, options.task_fn)
