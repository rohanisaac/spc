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
    
    def __init__(self, data, fnpts, fexp, txyxy):
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
            
        y_dat_pos = self.subhead_siz
            
        #--------------------------
        # if x_data present
        #--------------------------
            
        if txyxy:
            x_str = 'i'*fnpts
            x_dat_pos = y_dat_pos
            x_dat_end = x_dat_pos + (4*fnpts)
            x_raw = np.array(struct.unpack(x_str, data[x_dat_pos:x_dat_end]))
            self.x = (2**(fexp-32))*x_raw
            
            y_dat_pos = x_dat_end
        
        #--------------------------
        # extract y_data
        #--------------------------
            
        y_dat_str = 'i'*fnpts
        y_dat_end = y_dat_pos + (4*fnpts)
        y_raw = np.array(struct.unpack(y_dat_str, data[y_dat_pos:y_dat_end]))
        
        self.y = (2**(fexp-32))*y_raw
        self.y = self.y.astype(int)
            
        # do stuff if subflgs
        # if 1 subfile changed
        # if 8 if peak table should not be used
        # if 128 if subfile modified by arithmetic
               