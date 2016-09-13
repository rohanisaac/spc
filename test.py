#!/usr/bin/env python
from __future__ import absolute_import, unicode_literals, print_function, division
import os
import spc

tfile = 0
tpass = 0

dpath = os.path.join(os.path.dirname(__file__), 'test_data')
mfile = []
rfile = []
lfile = []
for i in os.listdir(dpath):
    if i[-3:].lower() == 'spc':
        tfile += 1
        print(i)
        f1 = spc.File(os.path.join(dpath, i))
        outfile = os.path.join(dpath, 'txt2', i + '.txt')
        with open(outfile, 'r') as fin:
            dat = fin.read()
            if f1.data_txt() == dat:
                print("Pass\n------")
                tpass += 1
            else:
                print("Fail\n------")
                mfile.append(i)
print("Passed %i of %i tests. " % (tpass, tfile))
print("Did not match ref file: ", mfile)
print("Did not have ref file: ", rfile)
print("Did not load file: ", lfile)
