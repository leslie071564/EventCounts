# -*- coding: utf-8 -*-
import sys
import argparse
import os.path
import ConfigParser

def set_arguments(config_file):
    config = ConfigParser.RawConfigParser()
    config.read(config_file)

    global extract_script, merge_script, clean_script, raw_dir, result_dir, merge_dir, sort_tmp_dir
    extract_script = config.get("Scripts", "extract_script") 
    merge_script = config.get("Scripts", "merge_script") 
    clean_script = config.get("Scripts", "clean_script")
    raw_dir = config.get("Data_Directory", "raw_dir") 
    result_dir = config.get("Data_Directory", "result_dir") 
    merge_dir = config.get("Data_Directory", "merge_dir")
    sort_tmp_dir = config.get("Sorting", "sort_tmp_dir")


def check_existence(folder_stamp, file_stamp):
    check_file = "%s/%s/%s%s.knp.xz" % (raw_dir, '/'.join(folder_stamp), folder_stamp, file_stamp)
    return os.path.isfile(check_file)

def print_event_extract_task(output_file):
    f = open(output_file, 'w')
    for folder_num in range(4905):
        folder_stamp = "%04d" % folder_num
        for file_num in range(100):
            file_stamp = "%02d" % file_num
            if check_existence(folder_stamp, file_stamp):
                cmd = "%s %s %s" % (extract_script, " ".join(list(folder_stamp)), file_stamp)
                f.write(cmd + '\n')
            if folder_num == 4904 and file_num == 24:
                return None

def print_merge_task(output_file):
    f = open(output_file, 'w')
    for folder_num in range(4905):
        folder_stamp = "%04d" % folder_num
        result_prefix = "%s/%s" % (result_dir, folder_stamp)
        merge_prefix = "%s/%s" % (merge_dir, folder_stamp)
        sort_cmd = "LC_ALL=C sort --temporary-directory=%s -k2 %s_*_result.txt > %s_sorted.txt" % (sort_tmp_dir, result_prefix, merge_prefix)
        merge_cmd = "python %s -f %s_sorted.txt -s > %s_result.txt" % (merge_script, merge_prefix, merge_prefix)
        delete_sorted_cmd = "rm -f %s_sorted.txt" % (merge_prefix)
        echo_cmd = "echo finish %s" % folder_stamp
        cmd = "%s && %s && %s && %s" % (sort_cmd, merge_cmd, delete_sorted_cmd, echo_cmd)
        f.write(cmd + '\n')

def print_merge_group_task(output_file):
    f = open(output_file, 'w')
    for folder_group in range(50):
        folder_group_stamp = "%02d" % (folder_group)
        merge_prefix = "%s/%s" % (merge_dir, folder_group_stamp)
        sort_cmd = "LC_ALL sort --temporary-directory=%s -k2 -m %s*_result.txt > %s_sorted.txt" % (sort_tmp_dir, merge_prefix, merge_prefix)
        merge_cmd = "python %s -f %s_sorted.txt -s > %s_result_group.txt" % (merge_script, merge_prefix, merge_prefix)
        clean_cmp = "%s %s_result_group.txt" % (clean_script, merge_prefix)
        delete_sorted_cmd = "rm -f %s_sorted.txt" % (merge_prefix)
        echo_cmd = "echo finish %s" % folder_group_stamp
        cmd = "%s && %s && %s && %s && %s" % (sort_cmd, merge_cmd, clean_cmp, delete_sorted_cmd, echo_cmd)
        f.write(cmd + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', "--event_extract_task_file", action="store", default="", dest="event_extract_task_file")
    parser.add_argument('-m', "--merge_task_file", action="store", default="", dest="merge_task_file")
    parser.add_argument('-g', "--merge_group_task_file", action="store", default="", dest="merge_group_task_file")
    parser.add_argument('--setting_file', action="store", default="./setting.ini", dest="setting_file")
    options = parser.parse_args() 

    set_arguments(options.setting_file) 

    if options.event_extract_task_file:
        print_event_extract_task(options.event_extract_task_file)
    if options.merge_task_file:
        print_merge_task(options.merge_task_file)
    if options.merge_group_task_file:
        print_merge_group_task(options.merge_group_task_file)
