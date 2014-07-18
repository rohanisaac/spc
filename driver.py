# -*- coding: utf-8 -*-
"""
@author: Rohan Isaac

Driver function for spc file
"""

import spc

ftest = spc.File('Data/S_EVENX.SPC')
print ftest.x_values
print dir(ftest)
print ftest.metadict