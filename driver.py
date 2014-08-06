# -*- coding: utf-8 -*-
"""
@author: Rohan Isaac

Driver function for spc file
"""

# works for f_even_x

import spc

aaaa = spc.File('Data/s_evenx.SPC')
    
aaaa.debug_info()

#print ftest.sub[0].y
#logdat = ftest.log_dict
#logcont = ftest.log_other
#print ftest.log_content

#aaaa.output_txt()

#print ftest.sub.x
#print ftest.sub.y

aaaa.plot()

