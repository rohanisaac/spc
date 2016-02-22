#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gooey import Gooey, GooeyParser

@Gooey(required_cols=1, optional_cols=3, program_name='Convert SPC files', default_size=(610, 530))
def main():
    parser = GooeyParser(description='Convert *.SPC files to text file')
    parser.add_argument('Directory',
                        help='Input directory', widget='DirChooser')
    parser.add_argument('-f', '--format',
                        help='Output format', widget='Dropdown',
                        choices=['txt (tab delimited)', 'csv (comma separated)'], default='csv')
    parser.add_argument('-e', '--header',
                        help='Print header (if exists)', action='store_true',
                        default=True)
    parser.add_argument('-l', '--log',
                        help='Print log data at end of file', action='store_true',
                        default=False)

    args = parser.parse_args()
    print args


if __name__ == '__main__':
    main()
