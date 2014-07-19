"""
SubFile class

@author: Rohan Isaac
"""

from __future__ import division
import struct
import numpy as np

class subFile:
    """ 
    Processes each subfile passed to it, extracts header information and data
    information and places them in data members
    """
    subhead_str = "<cchfffiif4s"
    subhead_siz = 32
    
    def __init__(self, data, fnpts, fexp):
        #--------------------------
        # decode subheader
        #--------------------------
        
        subflgs, \
            subexp, \
            subindx, \
            subtime, \
            subnext, \
            subnois, \
            subnpts, \
            subscan, \
            subwlevel, \
            subresv \
            = struct.unpack(self.subhead_str, data[:self.subhead_siz])
            
        #--------------------------
        # extract y_data
        #--------------------------
            
        y_dat_str = 'i'*fnpts
        y_raw = np.array(struct.unpack(y_dat_str, data[32:]))
        
        self.y = (2**(fexp-32))*y_raw
        self.y = self.y.astype(int)
            
        # do stuff if subflgs
        # if 1 subfile changed
        # if 8 if peak table should not be used
        # if 128 if subfile modified by arithmetic
               