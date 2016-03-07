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

    # add all files from input file name
    for fn in args.filefolder:
        ffn = os.path.abspath(fn)
        # or directories
        if os.path.isdir(ffn):
            for f in os.listdir(ffn):
                flist.append(os.path.join(ffn, f))
        else:
            flist.append(ffn)

    # process files
    for fpath in flist:
        if fpath.lower().endswith('spc'):

            foutp = fpath[:-4] + exten
            try:
                print(fpath, end=' ')
                f = spc.File(fpath)
                f.write_file(foutp, delimiter=delim)
                print('Converted')
            except:
                print('Error processing %s' % fpath)
        else:
            print('%s not spc file, skipping' % fpath)

if __name__ == '__main__':
    main()
