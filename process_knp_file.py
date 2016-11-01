# -*- coding: utf-8 -*-
import sys
import re
import operator
import os.path
import argparse
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stderr = codecs.getwriter('utf-8')(sys.stderr)
from pyknp import KNP
knp = KNP()


def print_events(knp_file, to_file, if_debug=False, print_sid=False):
    if not os.path.isfile(knp_file):
        return False
    TO_FILE = open(to_file, 'wb')

    data = ""
    sent_count = 0
    now_sid = ""
    for line in iter(open(knp_file, 'r').readline, ""):
        data += line
        if print_sid and line.startswith("# S-ID:"):
            now_sid = line.split()[1]

        if line.strip() == "EOS":
            try:
                result = knp.result(data.decode('utf-8'))
                events_of_sent = process_sent(result, if_debug=bool(if_debug))
                if now_sid:
                    events_of_sent = ["1 %s %s" % (x, now_sid) for x in events_of_sent]
                for ev in events_of_sent:
                    TO_FILE.write(ev.encode('utf-8') + '\n')
            except :
                pass
            ### print progessing percentage of current file:
            sent_count += 1
            if if_debug and sent_count == if_debug:
                break
            ###
            data = ""


def process_sent(result, if_debug=False):
    ALL_EVENTS = []
    for tag_id, tag in enumerate(result.tag_list()):
        dep_cases = re.findall(ur"<係:(.*?)格>", tag.fstring)
        # no such case of multiple cases?
        # throw away arg with multiple cases.
        if len(dep_cases) != 1:
            continue
        case = dep_cases[0]
        if case not in [u"ガ", u"ヲ", u"ニ"]:
            continue
        pred = result.tag_list()[tag.parent_id]
        # check if OK.
        if u"<用言:動>" not in pred.fstring:
            continue
        # check if OK.
        prev_tag = result.tag_list()[tag_id - 1] if tag_id else None
        arg = get_noun_rep(tag, prev_tag)
        if arg:
            pred_str = re.search(ur"<用言代表表記:(.*?)>", pred.fstring).group(1)
            event_rep = "%s-%s-%s" % (arg, case, pred_str)
            ALL_EVENTS.append(event_rep)
    if if_debug and ALL_EVENTS:
        sys.stderr.write(print_original_sentence(result) + '\n')
        sys.stderr.write(" ".join(ALL_EVENTS) + '\n')
    return ALL_EVENTS

def print_original_sentence(result, delimiter=""):
    return delimiter.join([x.midasi for x in result.mrph_list()])
    pass

def get_noun_rep(this_tag, prev_tag):
    # 正規化代表表記? 
    this_repname = this_tag.repname.split('+')
    if not this_repname:
        return None
    if len(this_repname) == 1 and len(this_repname[0].split('/')[0]) == 1:
        flag = True
    else:
        flag = False
    
    prev_mrph = prev_tag.mrph_list()[-1]
    for mrph in this_tag.mrph_list():
        if mrph.repname not in this_repname:
            prev_mrph = mrph
            continue
        mrph_index = this_repname.index(mrph.repname)
        if mrph.hinsi == u"特殊":
            return None
        this_repname[mrph_index] = replace_by_category(mrph)
        if flag:
            if u"<複合←>" in mrph.fstring or this_mrph.hinsi == u"接尾辞":
                this_repname.insert(0, replace_by_category(prev_mrph))
                break
    return "+".join(this_repname)

def replace_by_category(mrph):
    if mrph.bunrui in [u"数詞", u"人名", u"地名"]:
        return "[%s]" % mrph.bunrui
    return mrph.repname

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', "--debug", action="store", type=int, default=False, dest="if_debug")
    parser.add_argument('-i', "--knp_file", action="store", dest="knp_file")
    parser.add_argument('-o', "--event_file", action="store", dest="event_file")
    parser.add_argument('-s', "--print_sid", action="store_true", default=False, dest="print_sid")
    options = parser.parse_args() 
    
    # testing.
    print_events(options.knp_file, options.event_file, if_debug=options.if_debug, print_sid=options.print_sid)
    sys.exit()

