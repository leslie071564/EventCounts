# -*- coding: utf-8 -*-
import sys
import random
import argparse
import cdb
from CDB_Reader import CDB_Reader
import os.path
import ConfigParser
###
existed_db_setting = "/windroot/huang/EventCounts_20161030/setting.ini"
###

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

def events_to_sentences(evs, n=False, print_sent=False):
    ev_count_cdb = CDB_Reader(event_to_count_keymap)
    ev_sid_cdb = CDB_Reader(event_to_sids_keymap)

    evs = evs.split("##")
    all_sids = set()
    for ev in evs:
        ev_count = ev_count_cdb.get(ev)
        ev_sids = ev_sid_cdb.get(ev)
        if not ev_count or not ev_sids:
            return None
        ev_sids = ev_sids.split(',')
        if all_sids == set():
            all_sids = set(ev_sids)
        else:
            all_sids = all_sids & set(ev_sids) 
    count = len(all_sids)
    sys.stderr.write("%s\n" % count)

    if n and n < count:
        sids = random.sample(all_sids, n)
    else:
        sids = all_sids
    
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
    parser.add_argument('--setting_file', action="store", default=existed_db_setting, dest="setting_file")
    options = parser.parse_args() 

    set_arguments(options.setting_file) 

    if options.html:
        sentences = events_to_sentences(options.event, n=options.sample_n, print_sent=False)
        if sentences == None:
            print "No sentence found."
        else:
            print "<br>".join(sentences)
    else:
        sentences = events_to_sentences(options.event, n=options.sample_n, print_sent=True)

