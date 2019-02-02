#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Command line utility to convert .SPC files to .TXT

author: Rohan Isaac
"""
from __future__ import division, absolute_import, unicode_literals, print_function
import argparse
import os
import spc


def is_valid_spc_file(filepath):
    """A function used to determine if the given path is an SPC file"""
    return os.path.isfile(filepath) and filepath.lower().endswith('spc')

def get_files_from_path(path):
    """
    A function used to generate a list of SPC files from the given path.
    The function returns a list even for a single file path.
    """
    path = os.path.abspath(path)
    if os.path.isfile(path) and is_valid_spc_file(path):
        return [path]

    elif os.path.isdir(path):
        build_full_path = lambda f:
        all_files = map(build_full_path, os.listdir(path))
        #all_files = [os.path.join(path, f) for f in os.listdir(path)]
        return [filepath for filepath in all_files if is_valid_spc_file(filepath)]

    else:
        return []

def main():
    desc = 'Converts *.spc binary files to text using the spc module'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('filefolder', nargs='+', help='Input *.spc files or directory')
    fformat = parser.add_mutually_exclusive_group()
    fformat.add_argument('-c', '--csv', help='Comma separated output file (.csv) [default]',
                         action='store_true')
    fformat.add_argument('-t', '--txt', help='Tab separated output file (.txt)',
                         action='store_true')
    args = parser.parse_args()

    if args.txt:
        exten = '.txt'
        delim = '\t'
    else:
        # defaults
        exten = '.csv'
        delim = ','

    flist = []

    # add all valid spc files from input file name
    for fn in args.filefolder:
        flist += get_files_from_path(fn)

    if len(flist) == 0:
        print('No valid SPC file(s) found.')

    else:
        # process files
        for fpath in flist:
            foutp = fpath[:-4] + exten
            try:
                print(fpath, end=' ')
                f = spc.File(fpath)
                f.write_file(foutp, delimiter=delim)
                print('Converted')
            except:
                print('Error processing %s' % fpath)

if __name__ == '__main__':
    main()
