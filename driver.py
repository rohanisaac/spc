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
ftest = spc.File('Data/HENE25.SPC')
    
# if needed look at the debug info
# need to improve debug info
ftest.debug_info()

# can access the raw x and y dat
print ftest.sub[0].y

# or the log data as a dictionay
print ftest.log_dict
# stuff that couldn't be processed into a dictionary
print ftest.log_other 

# output the data to a text file
#ftest.output_txt()

# plot the data using matplotlib
ftest.plot()

print ftest.data_txt()

