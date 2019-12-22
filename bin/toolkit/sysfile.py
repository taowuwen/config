#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, glob
from binaryornot.check import is_binary
import argparse
from utils import *
import re
import multiprocessing
import queue



class FileFind:
    '''
    we have follow setting ups

    1. arguments
        a. follow symbol links
        b. exception lists
        c. file lists
        d. exception binary
        e. Process numbers in Pool or thread numbers in pool
        f. ignorecase search
    '''

    def __init__(self, basedir = './', exception_list = [], follow_symbol = False):
        self.basedir = basedir
        self.follow_symbol_link = follow_symbol
        self.exceptions = exception_list


    def walk(self, cb = None):

        if not cb:
            return None

        return self.scan_dir(self.basedir, cb)

    def scan_dir(self, basedir, cb):

        for fl in glob.glob(f'{basedir}/*'):

            if os.path.basename(fl) in self.exceptions:
                continue

            if not self.follow_symbol_link and os.path.islink(fl):
                continue

            try:
                if os.path.isdir(fl):
                    cb(fl, 1)
                    self.scan_dir(fl, cb)
                else:
                    cb(fl, 0)

            except Exception as e:
                print(e)
                raise

def prepare_parser_commmon():

    parser = argparse.ArgumentParser("toolkit({0}) helper by taowuwen@gmail.com 20191221.".format(sys.argv[0]))
    
    # version 
    parser.add_argument('-v', action='version', version='%(prog)s Version 1.0')

    # exception lists
    parser.add_argument('-e', '--exception', default="", help='exception lists, files or dictionary in this list will not be scanned', type=str)

    # follow symbol links
    parser.add_argument('-f', '--follow-symbol', action="store_true", default=False, help='follow symbol links')

    # ignorecase
    parser.add_argument('-i', '--ignorecase', action="store_true", default=False, help='ignorecase')

    return parser


def parser_arguments(parser):
    parser.add_argument('file_list', metavar='key', type=str, nargs='+', help='give one or more files')
    args = parser.parse_args()

    args.exception_list = args.exception.split(',')

    return args

def find_file(args, is_dir = 0):

    if args.ignorecase:
        file_list = [fl.lower() for fl in args.file_list]
    else:
        file_list = args.file_list

    def find_file_cb(fl, isdir):

        if is_dir is not isdir:
            return 0

        filename = os.path.basename(fl)
        key = filename

        if args.ignorecase:
            key = filename.lower()

        if key in file_list:
            print(paint_substr(Color.green, fl, filename))

    ff = FileFind(exception_list = args.exception_list, follow_symbol = args.follow_symbol)
    ff.walk(find_file_cb)


def main_default(parser):
    parser_arguments(parser)
    parser.print_help()

def main_ffile(parser):
    return find_file(parser_arguments(parser), 0)

def main_fdir(parser):
    return find_file(parser_arguments(parser), 1)

def fstring_prepare_arguments(parser):
    # binary files
    parser.add_argument('-b', '--enable-binary' ,action='store_true', default=False,  help='enable search in binary files')

    # subprocess number
    parser.add_argument('-p', '--process-num', default=multiprocessing.cpu_count(), type=int, help='process number to process search, default 2')


def find_string_child_main(msg_queue, msg_queue_out, str_list=[], enable_binary = False, ignorecase=False):

    paintor = paint_substr_ignorecase if ignorecase else paint_substr

    while True:
        fl = msg_queue.get()
        
        if fl == "command:bye-bye!!!":
            break

        if not enable_binary and is_binary(fl):
            continue

        with open(fl, 'rb') as fp:

            ln_num = 0

            for ln_bytes in fp:

                try:
                    ln = decode_str(ln_bytes).rstrip()
                    ln_match = ln.lower() if ignorecase else ln
                except DecodeFailed:
                    ln_num += 1
                    continue
                else:
                    ln_num += 1
                        
                    for key in str_list: # here we have one bug, we can't match multi key in one line
                        if key in ln_match:
                            # line num + filename \t painted line
                            msg_queue_out.put(f'{Color.green}{ln_num}\t{Color.yellow}|{fl}|\t{Color.normal} {paintor(Color.red, ln, key)}')
                            break

    msg_queue_out.put('child:bye-bye!!!')
    sys.exit(0)


def find_string(args):
    '''
    1. [parent] ---put(filename) --->  [ msgqueue ] <---get---- [ child ]
    2. [ child] ---put(msg) ---------> [ result   ] <---get---- [ parent]
    or 
    2.1 [ child] ---put(msg) ---------> [ result  ] <---get-- [ output child do print out]
    3. [parent wait for all the child exit status ]
    '''
    msg_queue = multiprocessing.Queue(1024)
    msg_queue_out = multiprocessing.Queue(1024)
    proc_list = []

    def find_string_cb(fl, isdir):

        if isdir:
            return 0

        msg_queue.put(fl)

    if args.process_num <= 0:
        args.process_num = multiprocessing.cpu_count()

    if args.ignorecase:
        str_list = [fl.lower() for fl in args.file_list]
    else:
        str_list = args.file_list

    for x in range(args.process_num):
        p = multiprocessing.Process(target = find_string_child_main, args=(msg_queue, msg_queue_out, str_list, args.enable_binary, args.ignorecase))
        p.start()
        proc_list.append(p)

    ff = FileFind(exception_list = args.exception_list, follow_symbol = args.follow_symbol)
    ff.walk(find_string_cb)

    for p in proc_list:
        msg_queue.put('command:bye-bye!!!')

    recevied_bye = 0

    while True:
        res = msg_queue_out.get()

        if res == 'child:bye-bye!!!':
            recevied_bye += 1
            if recevied_bye == args.process_num:
                break
            continue

        print(res)

    for p in proc_list:
        p.join()

    return 0

def main_fstring(parser):
    fstring_prepare_arguments(parser)
    return find_string(parser_arguments(parser))

if __name__ == '__main__':

    main = {
        "ffile":    main_ffile,
        "fdir":     main_fdir,
        "fstring":  main_fstring,
    }.get(os.path.basename(sys.argv[0]), main_default)

    sys.exit(not main(prepare_parser_commmon()))
