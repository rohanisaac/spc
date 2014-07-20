# -*- coding: utf-8 -*-
"""
@author: Rohan Isaac

Driver function for spc file
"""

import spc

ftest = spc.File('Data/raman.SPC')
    
ftest.debug_info()

#print ftest.sub[0].y


#logdat = ftest.log_dict
#logcont = ftest.log_other
#print ftest.log_content

#ftest.output_txt()

#print ftest.sub.x
#print ftest.sub.y

ftest.plot()