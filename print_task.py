# -*- coding: utf-8 -*-
import sys
import argparse
import os.path

def check_existence(folder_stamp, file_stamp):
    base_dir = "/pear/share/www-uniq/v2006-2015.cf-preparation/knp"
    check_file = "%s/%s/%s%s.knp.xz" % (base_dir, '/'.join(folder_stamp), folder_stamp, file_stamp)
    return os.path.isfile(check_file)

def print_event_extract_task(output_file):
    f = open(output_file, 'w')
    extract_script = "/home/huang/work/EventCounts/count_events.sh"
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
    merge_script = "/home/huang/work/EventCounts/merge.py"
    result_dir = "/windroot/huang/EventCounts"
    merge_dir = "/windroot/huang/MergeEvent"
    for folder_num in range(4905):
        folder_stamp = "%04d" % folder_num
        result_prefix = "%s/%s" % (result_dir, folder_stamp)
        merge_prefix = "%s/%s" % (merge_dir, folder_stamp)
        #sort_cmd = "sort -k2 --parallel=10 %s_*_result.txt > %s_sorted.txt" % (result_prefix, merge_prefix)
        sort_cmd = "sort -k2 %s_*_result.txt > %s_sorted.txt" % (result_prefix, merge_prefix)
        merge_cmd = "python %s -f %s_sorted.txt -s > %s_result.txt" % (merge_script, merge_prefix, merge_prefix)
        delete_sorted_cmd = "rm -rf %s_sorted.txt" % (merge_prefix)
        echo_cmd = "echo finish %s" % folder_stamp
        cmd = "%s && %s && %s && %s" % (sort_cmd, merge_cmd, delete_sorted_cmd, echo_cmd)
        f.write(cmd + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', "--event_extract_task_file", action="store", default="", dest="event_extract_task_file")
    parser.add_argument('-m', "--merge_task_file", action="store", default="", dest="merge_task_file")
    options = parser.parse_args() 

    if options.event_extract_task_file:
        print_event_extract_task(options.event_extract_task_file)
    if options.merge_task_file:
        print_merge_task(options.merge_task_file)
