# -*- coding:utf-8 -*-
#
# 2019/12/17 Optimize IO and mem.
# @auth:zeyu.yang@datavisor.com

import sys
import os
import argparse
import gzip
import json
import time
import logging


# event_type_field = 'eventtype'
event_type_field = 'EVENT_TYPE_NAME'
# counters
file_count = 0
v_error_count = 0
# log
mlogger = logging.getLogger()


def init_logger():
    # mlogger = logging.getLogger()
    logfile = './raw_data_counter.log'
    mlogger.setLevel(logging.INFO)

    fh = logging.FileHandler(logfile, mode='a')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    formatter = logging.Formatter("%(asctime)s  [%(levelname)s] %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    mlogger.addHandler(fh)
    mlogger.addHandler(ch)


def read_gz_file(path):
    if os.path.exists(path):
        with gzip.open(path, 'r') as pf:
            for line in pf:
                yield line
    else:
        mlogger.error('the path [{}] is not exist!'.format(path))


def write_result_to_csv(events):
    if events:
        output = open('counters.csv', 'w+')
        for e_type, counters in events.items():
            for field, cnt in counters.items():
                if not e_type:
                    e_type = ""
                s = e_type+','+field+','+str(cnt)
                output.write(s+'\n')

        mlogger.info(
            'Total %d files finished, output in counters.csv' % file_count)
    else:
        mlogger.warning("No eligible data")

if __name__ == '__main__':
    init_logger()

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', default='input')
    parser.add_argument('--output_dir', default='output')

    parser.add_argument('--file_type', default='.gz')
    parser.add_argument('--target_str', default='')
    parser.add_argument('--file_prefix', default='rawlog.')
    ns = parser.parse_args()

    mlogger.debug("input_dir: %s" % ns.input_dir)

    events = {}

    mlogger.info('Start')
    for root, subdirs, files in os.walk(ns.input_dir):
        for file in files:
            if '.' not in file:
                continue
            if file.startswith(ns.file_prefix) & file.endswith(ns.file_type):
                lines = read_gz_file(os.path.join(root, file))
                if getattr(lines, '__iter__', None):
                    for line in lines:
                        try:
                            mp = json.loads(line.strip())
                            e_type = mp.get(event_type_field)
                            if not e_type:
                                mlogger.debug(
                                    "field {} is none.".format(event_type_field))
                                mlogger.debug(line)
                            if e_type not in events:
                                events[e_type] = {}
                            for k in mp:
                                events[e_type][k] = events[e_type].get(
                                    k, 0) + 1
                        except ValueError:
                            v_error_count += 1
                            mlogger.debug("ValueError %d" % v_error_count)
                            continue

                file_count += 1
                if file_count % 100 == 0:
                    mlogger.info("%d files finished." % (file_count))

    write_result_to_csv(events)
    mlogger.info('Finished.')
