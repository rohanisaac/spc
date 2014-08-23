# -*- coding: utf-8 -*-
"""
Command line utility to convert .SPC files to .TXT

@author: Rohan Isaac
"""

import sys, os, glob, spc

man = """ USAGE: \n $ python convert %file_name1% %file_name2% \n OR \n \
$ python convert $%dir_name% \n\n EXAMPLE: python convert """

def convert(filename, over):
    of = filename+".txt"
    print "Converting", filename, " to ", of
    if os.path.exists(of):
        if over:
            print "overwriting existing file"
            write(filename,of)
        else:
            print "File already exists. Skipping. If want to overwrite, pass -o"
            
def write(inf, of):
    f = spc.File(inf)
    f.write_file(of)

def main():
    overw = False
    if len(sys.argv) < 2:
        print "No arguments passed"
        print man       
        
    else:
        if "-o" in sys.argv:
            overw = True
            sys.argv.remove("-o")
        
        print "Attempting to convert the following files: "
        for path in sys.argv[1:]:
            print path
            if os.path.isdir(path):
                print "Do stuff if dir"
                for filename in glob.glob(path + "/*.[sS][pP][cC]" ):
                    convert(filename,overw)
            else:
                if os.path.exists(path):
                    convert(path,overw)
                else:
                    print path, " does not exist on disk"

if __name__ == "__main__":
    main()

