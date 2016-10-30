# -*- coding: utf-8 -*-
import sys
from CDB_Writer import CDB_Writer
import argparse
import codecs

def write_event_sid_db(input_file, db_file):
    DEFAULTLFS = 2.5 * 1024 * 1024 * 1024
    keymap_file = db_file.split('/')[-1] + '.keymap'
    limit_file_size = DEFAULTLFS 
    fetch = 100
    encoding_in = 'utf8'
    encoding_out = 'utf8'
    
    maker = CDB_Writer(db_file, keymap_file, limit_file_size, fetch, encoding_out)
    with open(input_file, 'r') as f:
        #for l in iter(f.readline, ''):
        for l in f:
            count, ev, sids = l.strip().split(' ')
            maker.add(ev.decode(encoding_in), sids)

    del maker


def write_event_count_db(input_file, db_file):
    DEFAULTLFS = 2.5 * 1024 * 1024 * 1024
    keymap_file = db_file.split('/')[-1] + '.keymap'
    limit_file_size = DEFAULTLFS
    fetch = 10000
    encoding_in = 'utf8'
    encoding_out = 'utf8'

    maker = CDB_Writer(db_file, keymap_file, limit_file_size, fetch, encoding_out)
    with open(input_file, 'r') as f:
        for l in f:
            count, ev, sids = l.strip().split(' ')
            maker.add(ev.decode(encoding_in), count)

    del maker


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', "--input_file", action="store", default="", dest="input_file")
    parser.add_argument('-s', "--event_sid", action="store", default="", dest="event_sid")
    parser.add_argument('-c', "--event_count", action="store", default="", dest="event_count")
    options = parser.parse_args() 

    if options.event_sid:
        write_event_sid_db(options.input_file, options.event_sid)
    if options.event_count:
        write_event_count_db(options.input_file, options.event_count)
