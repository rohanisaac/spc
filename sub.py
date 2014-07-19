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
            
            
        #self.pr_spacing = spacing
            
            
        # do stuff if subflgs
        # if 1 subfile changed
        # if 8 if peak table should not be used
        # if 128 if subfile modified by arithmetic
        
        #--------------------------
        # decode x,y-data
        #--------------------------
        
        # header + subheader + mumber of data points (int: 4 bytes)
        # ONLY VALID FOR SINGLE SUBFILES !!! need to fix
#        self.DATA_POS = 512 + 32 + (self.PTS*4)
#        self.EXP = ord(self.fexp)
#        self.PTS = int(self.fnpts)
#        
#        # generate x-values (np.arange can't generate the correct amount of elements)
#        self.x_values = np.zeros(self.PTS)
#        for i in range(self.PTS):
#            self.x_values[i] = self.ffirst + (self.SPACING*i)
#            
#        # import the y-data and convert it
#        self.y_int = np.array(struct.unpack("i"*self.PTS,data[self.subhead_siz:]))
#        
#        # conversion string
#        self.y_values = (2**(self.EXP-32))*self.y_int
#        
#        # optionally integerize it
#        self.y_values_int = self.y_values.astype(int)
            
        