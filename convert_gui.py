#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gooey import Gooey, GooeyParser

@Gooey
def main():
    parser = GooeyParser(description='Convert SPC to text files')
    parser.add_argument('Filename', widget='FileChooser')
    #parser.add_argument('Fileformat', widget='RadioGroup')
    args = parser.parse_args()

    for i in range(100):
        print "Hello"

if __name__ == '__main__':
    main()
