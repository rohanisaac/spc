# -*- coding: utf-8 -*-
"""
@author: Rohan Isaac

Driver function for spc file
"""

# works for f_even_x
# works for Ft-ir
# works for RAMAN
# works for NMR_SPC

import spc

aaaa = spc.File('Data/NMR_SPC.SPC')
    
aaaa.debug_info()

#print ftest.sub[0].y
#logdat = ftest.log_dict
#logcont = ftest.log_other
#print ftest.log_content

#aaaa.output_txt()

#print ftest.sub.x
#print ftest.sub.y

aaaa.plot()

