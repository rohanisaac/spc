# -*- coding: utf-8 -*-
"""
Command line utility to convert .SPC files to .TXT

@author: Rohan Isaac
"""

import sys, os, glob, spc

man = """ USAGE: \n $ python convert %file_name1% %file_name2% \n OR \n \
$ python convert $%dir_name% \n\n EXAMPLE: python convert """

def convert(filename):
    print "Converting", filename
    f = spc.File(filename)
    f.write_file(filename+".txt")

def main():
    if len(sys.argv) < 2:
        print "No arguments passed"
        print man
        
    else:
        print "Converting the following files: "
        for path in sys.argv[1:]:
            print path
            if os.path.isdir(path):
                print "Do stuff if dir"
                for filename in glob.glob(path + "/*.[sS][pP][cC]" ):
                    convert(filename)
            else:
                convert(filename)

if __name__ == "__main__":
    main()

