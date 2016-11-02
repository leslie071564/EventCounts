# -*- coding: utf-8 -*-
import sys
from CDB_Writer import CDB_Writer
import argparse

def write_argkey_db(all_key, output_db):
    DEFAULTLFS = 2.5 * 1024 * 1024 * 1024
    keymap_file = output_db.split('/')[-1] + '.keymap'
    limit_file_size = DEFAULTLFS 
    fetch = 10000
    encoding_in = 'utf8'
    encoding_out = 'utf8'
    maker = CDB_Writer(output_db, keymap_file, limit_file_size, fetch, encoding_out)

    with open(all_key, 'r') as f:
        now_arg = None
        now_preds = []
        for line in f:
            arg, case, pred = line.strip().split('-')
            arg = "%s-%s" % (arg, case)
            if now_arg == arg:
                now_preds.append(pred)
            else:
                if now_arg:
                    pass
                    maker.add(now_arg.decode(encoding_in), " ".join(now_preds))
                    #print "%s:%s" % (now_arg, " ".join(now_preds))
                now_arg = arg
                now_preds = [ pred ]
        # last instance.
        maker.add(now_arg.decode(encoding_in), " ".join(now_preds))
        #print "%s:%s" % (now_arg.decode(encoding_in), " ".join(now_preds))

    del maker

def write_predkey_db(all_key, output_db):
    DEFAULTLFS = 2.5 * 1024 * 1024 * 1024
    keymap_file = output_db.split('/')[-1] + '.keymap'
    limit_file_size = DEFAULTLFS 
    fetch = 10000
    encoding_in = 'utf8'
    encoding_out = 'utf8'
    maker = CDB_Writer(output_db, keymap_file, limit_file_size, fetch, encoding_out)

    with open(all_key, 'r') as f:
        now_pred = None
        now_args = []
        for line in f:
            line = line.strip()
            arg, case, pred = line.split('-')
            pred = "%s-%s" % (case, pred)
            if now_pred == pred:
                now_args.append(arg)
            else:
                if now_pred:
                    #print "%s:%s" % (now_pred, " ".join(now_args))
                    maker.add(now_pred.decode(encoding_in), " ".join(now_args))
                now_pred = pred
                now_args = [ arg ]
        # last instance.
        maker.add(now_pred.decode(encoding_in), " ".join(now_args))
        #print "%s:%s" % (now_pred, " ".join(now_args))

    del maker

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', "--sort_by_arg", action="store", default="", dest="sort_by_arg")
    parser.add_argument('-p', "--sort_by_pred", action="store", default="", dest="sort_by_pred")
    parser.add_argument('-i', "--input_file", action="store", default="", dest="input_file")
    options = parser.parse_args() 

    if options.sort_by_arg and options.sort_by_pred:
        sys.stderr.write("Use -a/--sort_by_arg if input file is sorted by argument\n")
        sys.stderr.write("\tor\nUse -p/--sort_by_pred if input file is sorted by predicate.\n")
        sys.exit()

    if options.sort_by_arg:
        write_argkey_db(options.input_file, options.sort_by_arg)
    elif options.sort_by_pred:
        write_predkey_db(options.input_file, options.sort_by_pred)
