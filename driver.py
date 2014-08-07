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

# load the library
import spc

# create an object by sending the path to file
aaaa = spc.File('Data/m_evenz.SPC')
    
# if needed look at the debug info
aaaa.debug_info()

# can access the raw x and y dat
#print ftest.sub[0].y

# or the log data as a dictionay
#logdat = ftest.log_dict
# stuff that couldn't be processed into a dictionary
#logcont = ftest.log_other 

# output the data to a text file
#aaaa.output_txt()

# plot the data using matplotlib

aaaa.plot()


