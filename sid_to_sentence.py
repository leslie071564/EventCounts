# -*- coding: utf-8 -*-
import sys
import argparse
import cdb
import os.path
cdb_base_dir = "/pear/share/www-uniq/v2006-2015.text-cdb"

def get_sentence(sid):
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
    parser.add_argument('-s', "--sid", action="store", dest="sid")
    options = parser.parse_args() 

    print get_sentence(options.sid)

