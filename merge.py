# -*- coding: utf-8 -*-
import sys
import os.path
import argparse

def merge_count_file(file_loc, threshold=0):
    with open(file_loc, 'r') as FILE:
        now_ev = None
        now_count = 0
        for line in FILE:
            line_count, line_ev = line.strip().split(' ')
            line_count = int(line_count)
            if not now_ev:
                now_ev = line_ev
            if now_ev == line_ev:
                now_count += line_count
            else:
                if now_count >= threshold:
                    print "%s %s" % (now_count, now_ev)
                now_ev = line_ev
                now_count = line_count
        if now_count >= threshold:
            print "%s %s" % (now_count, now_ev)

def merge_sid_file(file_loc, threshold=0):
    with open(file_loc, 'r') as FILE:
        now_ev = None
        now_count = 0
        now_sids = ""
        for line in FILE:
            line_count, line_ev, line_sids = line.strip().split(' ')
            line_count = int(line_count)
            #if not now_ev:
               # now_ev = line_ev
                #now_count = line_count
               # now_sids = line_sids
            if now_ev == line_ev:
                now_count += line_count
                now_sids += (',' + line_sids)
            else:
                if now_count >= threshold:
                    print "%s %s %s" % (now_count, now_ev, now_sids)
                now_ev = line_ev
                now_count = line_count
                now_sids = line_sids
        if now_count >= threshold:
            print "%s %s %s" % (now_count, now_ev, now_sids)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', "--threshold", action="store", type=int, default=0, dest="threshold")
    parser.add_argument('-f', "--file_loc", action="store", default="", dest="file_loc")
    parser.add_argument('-c', "--count", action="store_true", default=False, dest="count")
    parser.add_argument('-s', "--sid", action="store_true", default=False, dest="sid")
    options = parser.parse_args() 

    if not os.path.isfile(options.file_loc):
        sys.stderr.write("file %s not exist.\n" % options.file_loc)
        sys.exit()

    if options.count:
        merge_count_file(options.file_loc, threshold=options.threshold)
    elif options.sid:
        merge_sid_file(options.file_loc, threshold=options.threshold)
    else:
        sys.stderr.write("please specify file type: --count or --sid\n")
        sys.exit()
