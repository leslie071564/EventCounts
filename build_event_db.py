# -*- coding: utf-8 -*-
import sys
from CDB_Writer import CDB_Writer
import argparse
import codecs

def write_event_sid_db(input_file, db_file):
    if db_file.endswith('.keymap'):
        db_file = db_file.split('.keymap')[0]
    DEFAULTLFS = 2.5 * 1024 * 1024 * 1024
    keymap_file = db_file.split('/')[-1] + '.keymap'
    limit_file_size = DEFAULTLFS 
    fetch = 100
    encoding_in = 'utf8'
    encoding_out = 'utf8'
    
    maker = CDB_Writer(db_file, keymap_file, limit_file_size, fetch, encoding_out)
    with open(input_file, 'r') as f:
        for l in f:
            count, ev, sids = l.strip().split(' ')
            try:
                maker.add(ev.decode(encoding_in), sids)
            except OverflowError:
                sids = sids.split(',')
                num = len(sids) / 500000
                print ev, num
                maker.add(ev.decode(encoding_in), str(num))
                for n in xrange(num):
                    maker.add("%s%s" % (ev.decode(encoding_in), n), ','.join(sids[n*500000:min((n+1)*500000, len(sids))]))

    del maker


def write_event_count_db(input_file, db_file):
    if db_file.endswith('.keymap'):
        db_file = db_file.split('.keymap')[0]
    DEFAULTLFS = 2.5 * 1024 * 1024 * 1024
    keymap_file = db_file.split('/')[-1] + '.keymap'
    limit_file_size = DEFAULTLFS
    fetch = 10000
    encoding_in = 'utf8'
    encoding_out = 'utf8'

    maker = CDB_Writer(db_file, keymap_file, limit_file_size, fetch, encoding_out)
    with open(input_file, 'r') as f:
        for l in f:
            count, ev = l.strip().split(' ')
            maker.add(ev.decode(encoding_in), count)

    del maker


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--build_event_sid_db", action="store_true", default="", dest="build_event_sid_db")
    parser.add_argument("--build_event_count_db", action="store_true", default="", dest="build_event_count_db")

    parser.add_argument('-i', "--input_file", action="store", default="", dest="input_file")
    parser.add_argument('-o', "--cdb_prefix", action="store", default="", dest="cdb_prefix")
    options = parser.parse_args() 

    if options.build_event_sid_db:
        write_event_sid_db(options.input_file, options.cdb_prefix)

    elif options.build_event_count_db:
        write_event_count_db(options.input_file, options.cdb_prefix)
