# -*- coding: utf-8 -*-
import sys
import random
import argparse
import cdb
from CDB_Reader import CDB_Reader
import os.path
import ConfigParser

def set_arguments(config_file):
    config = ConfigParser.RawConfigParser()
    config.read(config_file)

    global sentence_cdb_dir, event_to_sids_keymap, event_to_count_keymap
    sentence_cdb_dir = config.get('DataBase', 'sid_sentence_cdbdir')
    event_to_sids_keymap = config.get('DataBase', 'event_sid_cdb')
    event_to_count_keymap = config.get('DataBase', 'event_count_cdb')

def sid_to_sentence(sid):
    sid = sid.split(':')[-1]
    sub_dirs = sid.split('-')
    if sub_dirs[0] == "w201103":
        if sub_dirs[1] == "":
            sub_dirs[0] = "w201103.old/%s" % (sub_dirs[2])
            sub_dirs.pop(1)
        else:
            sub_dirs[0] = "w201103/%s" % sub_dirs[1]
        sub_dirs.pop(1)

    which_cdb = "%s/%s/%s/%s.cdb" % (sentence_cdb_dir, sub_dirs[0], "/".join(sub_dirs[1][:3]), sub_dirs[1][:4])
    if not os.path.isfile(which_cdb):
        sys.stderr.write("cdb file not found for %s.\n" % sid)
        return None
    c = cdb.init(which_cdb)
    return c[sid]

def event_to_sentences(ev, n=False, print_sent=False):
    ev_count_cdb = CDB_Reader(event_to_count_keymap)
    ev_sid_cdb = CDB_Reader(event_to_sids_keymap)
    count = ev_count_cdb.get(ev)
    sids = ev_sid_cdb.get(ev)
    if not count or not sids:
        return None
    
    count = int(count)
    sids = sids.split(',')
    if n and n < count:
        sids = random.sample(sids, n)
    
    return_sentences = []
    for sid in sids:
        sent = sid_to_sentence(sid)
        if sent == None:
            continue
        if print_sent:
            print sent
        else:
            return_sentences.append(sent)
    return return_sentences


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', "--event", action="store", dest="event")
    parser.add_argument('-n', "--sample_n", action="store", type=int, default=False, dest="sample_n")
    parser.add_argument('-b', "--html", action="store_true", default=False, dest="html")
    parser.add_argument('--setting_file', action="store", default="./setting.ini", dest="setting_file")
    options = parser.parse_args() 

    set_arguments(options.setting_file) 

    if options.html:
        sentences = event_to_sentences(options.event, n=options.sample_n, print_sent=False)
        if sentences == None:
            print "No sentence found."
        else:
            print "<br>".join(sentences)
    else:
        sentences = event_to_sentences(options.event, n=options.sample_n, print_sent=True)

