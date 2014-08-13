# -*- coding: utf-8 -*-
"""
@author: Rohan Isaac

Driver function for spc file
"""

# Does not work for the following
# m_ordz
# m_xyxy
# ms

# works with s_xy with hack, need to fix

# load the library
import spc

# create an object by sending the path to file
aaaa = spc.File('Data/s_xy.SPC')
    
# if needed look at the debug info
# need to improve debug info
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


