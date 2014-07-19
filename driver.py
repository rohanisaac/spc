# -*- coding: utf-8 -*-
"""
@author: Rohan Isaac

Driver function for spc file
"""

import spc

ftest = spc.File('Data/HENE25.SPC')
#print ftest.x_values
for i in dir(ftest):
    print i
#print ftest.metadict
    
print ftest.dat.y
print ftest.x

print len(ftest.dat.y)

print len(ftest.x)

print ftest.log_dict