# -*- coding: utf-8 -*-
"""
@author: Rohan Isaac

Driver function for spc file
"""

# works for s_evenx
# works for Ft-ir
# works for RAMAN
# works for NMR_SPC
# works for NMR_FID
# works for nir

import spc

aaaa = spc.File('Data/nir.SPC')
    
aaaa.debug_info()

#print ftest.sub[0].y
#logdat = ftest.log_dict
#logcont = ftest.log_other
#print ftest.log_content

#aaaa.output_txt()

#print ftest.sub.x
#print ftest.sub.y

aaaa.plot()


