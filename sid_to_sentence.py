# -*- coding: utf-8 -*-
import sys
import random
import argparse
import cdb
import os.path
cdb_base_dir = "/pear/share/www-uniq/v2006-2015.text-cdb"

def get_sentence(sid):
    sid = sid.split(':')[-1]
    sub_dirs = sid.split('-')
    if sub_dirs[0] == "w201103":
        if sub_dirs[1] == "":
            sub_dirs[0] = "w201103.old/%s" % (sub_dirs[2])
            sub_dirs.pop(1)
        else:
            sub_dirs[0] = "w201103/%s" % sub_dirs[1]
        sub_dirs.pop(1)

    which_cdb = "%s/%s/%s/%s.cdb" % (cdb_base_dir, sub_dirs[0], "/".join(sub_dirs[1][:3]), sub_dirs[1][:4])
    if not os.path.isfile(which_cdb):
        sys.stderr.write("cdb file not found for %s.\n" % sid)
        return None
    c = cdb.init(which_cdb)
    return c[sid]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', "--sids", action="store", default="", dest="sids")
    parser.add_argument('-f', "--file", action="store", dest="file")
    parser.add_argument('-t', "--total_n", action="store", type=int, default=0, dest="total_n")
    parser.add_argument('-n', "--sample_n", action="store", type=int, default=0, dest="sample_n")
    options = parser.parse_args() 

    which = []
    if options.total_n and options.sample_n:
        which = random.sample(range(options.total_n), options.sample_n)

    count = 0
    return_sentences = []
    if options.file:
        with open(options.file) as f:
            for line in f:
                if which == [] or count in which:
                    sentence = get_sentence(line.strip())
                    if sentence:
                        return_sentences.append(sentence)
                count += 1

    if options.sids:
        for sid in options.sids.split(','):
            # fix this.
            if sid == '':
                continue
            # fix this.
            if which == [] or count in which:
                sentence = get_sentence(sid)
                if sentence:
                    return_sentences.append(sentence)
            count += 1

    print "<br>".join(return_sentences)
    #print "\n".join(return_sentences)

