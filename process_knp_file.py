# -*- coding: utf-8 -*-
import sys
import re
import operator
import argparse
import os.path
from itertools import combinations, product

import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stderr = codecs.getwriter('utf-8')(sys.stderr)

from pyknp import KNP
knp = KNP()

MainCases = [u"ガ", u"ヲ", u"ニ", u"デ"]
AllCases = MainCases + [u"ト", u"カラ", u"ヨリ", u"ヘ", u"マデ", u"未"]

def print_events(options):
    if not os.path.isfile(options.knp_file):
        sys.stderr.write("input file not exists: %s\n" % options.knp_file)
        return False

    TO_FILE = open(options.event_file, 'wb')

    data = ""
    now_sid = ""
    for line in iter(open(options.knp_file, 'r').readline, ""):
        data += line
        if options.extract_sid and line.startswith("# S-ID:"):
            now_sid = line.split()[1]

        if line.strip() == "EOS":
            try:
                result = knp.result(data.decode('utf-8'))
                events_of_sent = process_sent(result, multi_arg=options.multi_arg, only_verb=options.only_verb, only_main_cases=options.only_main_cases)
                if now_sid:
                    events_of_sent = ["1 %s %s" % (x, now_sid) for x in events_of_sent]
                for ev in events_of_sent:
                    TO_FILE.write(ev.encode('utf-8') + '\n')
            except :
                data = ""
            data = ""

def get_sent_structure(result, only_verb=False, only_main_cases=False):
    preds = {}
    for tag_id, tag in enumerate(result.tag_list()):
        dep_cases = re.findall(ur"<係:(.*?)格>", tag.fstring)
        # throw away arg with multiple cases.
        if len(dep_cases) != 1:
            continue

        case = dep_cases[0]
        if only_main_cases and case not in MainCases:
            continue
        elif case not in AllCases:
            continue

        pred = result.tag_list()[tag.parent_id]
        if only_verb and u"<用言:動>" not in pred.fstring:
            continue

        prev_tag = result.tag_list()[tag_id - 1] if tag_id else None
        arg = get_noun_rep(tag, prev_tag)
        if arg:
            if u"<用言代表表記:" not in pred.fstring:
                continue
            pred_str = re.search(ur"<用言代表表記:(.*?)>", pred.fstring)
            pred_str = pred_str.group(1)
            event_rep = "%s-%s-%s" % (arg, case, pred_str)
            if pred_str not in preds.keys():
                preds[pred_str] = {}
            preds[pred_str][case] = event_rep
    return preds

def process_sent(result, multi_arg=False, only_verb=False, only_main_cases=False):
    struc = get_sent_structure(result, only_verb=only_verb, only_main_cases=only_main_cases)
    ALL_EVENTS = []
    for pred_str, pred_struc in struc.iteritems():
        ALL_EVENTS += pred_struc.values()
        if not multi_arg or len(pred_struc) == 1:
            continue
        for i, j in combinations(sorted(pred_struc.keys()), 2):
            ALL_EVENTS.append( "%s##%s" % (pred_struc[i], pred_struc[j]) )
        if len(pred_struc) == 2:
            continue
        for i, j, k in combinations(sorted(pred_struc.keys()), 3):
            ALL_EVENTS.append( "%s##%s##%s" % (pred_struc[i], pred_struc[j], pred_struc[k]) )
        if len(pred_struc) == 3:
            continue
        for i, j, k, l in combinations(sorted(pred_struc.keys()), 4):
            ALL_EVENTS.append( "%s##%s##%s##%s" % (pred_struc[i], pred_struc[j], pred_struc[k], pred_struc[l]) )
    return ALL_EVENTS

def get_noun_rep(this_tag, prev_tag):
    # 正規化代表表記? 
    this_repname = this_tag.repname.split('+')
    if not this_repname:
        return None

    flag = False
    if len(this_repname) == 1 and len(this_repname[0].split('/')[0]) == 1:
        flag = True

    if prev_tag: 
        prev_mrph = prev_tag.mrph_list()[-1]
    else:
        prev_mrph = None
    for mrph in this_tag.mrph_list():
        if mrph.repname not in this_repname:
            prev_mrph = mrph
            continue
        mrph_index = this_repname.index(mrph.repname)
        if mrph.hinsi == u"特殊":
            return None
        this_repname[mrph_index] = replace_by_category(mrph)
        if flag:
            if u"<複合←>" in mrph.fstring or mrph.hinsi == u"接尾辞":
                prev_mrph_rep = replace_by_category(prev_mrph)
                if not prev_mrph_rep:
                    return None
                this_repname.insert(0, prev_mrph_rep)
                break
    return "+".join(this_repname)

def replace_by_category(mrph):
    if not mrph:
        return None
    if mrph.bunrui in [u"数詞", u"人名", u"地名"]:
        return "[%s]" % mrph.bunrui
    return mrph.repname

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', "--knp_file", action="store", dest="knp_file")
    parser.add_argument('-o', "--event_file", action="store", dest="event_file")

    parser.add_argument("--extract_sid", action="store_true", dest="extract_sid")
    parser.add_argument("--multi_arg", action="store_true", dest="multi_arg")
    parser.add_argument("--only_verb", action="store_true", dest="only_verb")
    parser.add_argument("--only_main_cases", action="store_true", dest="only_main_cases")

    parser.add_argument('-d', "--debug", action="store", type=int, default=False, dest="if_debug")
    options = parser.parse_args() 
    
    # testing.
    print_events(options)
    sys.exit()

