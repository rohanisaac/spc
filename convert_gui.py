#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GUI verions of convert.py using Gooey

Notes:
Only takes a single directory as input

author: Rohan Isaac
"""
from gooey import Gooey, GooeyParser
import os
import spc


@Gooey(program_name='Convert SPC files')
def main():
    desc = 'Converts *.spc binary files to text using the spc module'
    parser = GooeyParser(description=desc)
    parser.add_argument('filefolder', widget='DirChooser', help='Input directory containing spc file')
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

    # only directory here
    ffn = os.path.abspath(args.filefolder)
    for f in os.listdir(ffn):
        flist.append(os.path.join(ffn, f))

    # process files
    for fpath in flist:
        if fpath.lower().endswith('spc'):

            foutp = fpath[:-4] + exten
            try:
                print fpath,
                f = spc.File(fpath)
                f.write_file(foutp, delimiter=delim)
                print 'Converted'
            except:
                print 'Error processing %s' % fpath
        else:
            print '%s not spc file, skipping' % fpath

if __name__ == '__main__':
    main()
