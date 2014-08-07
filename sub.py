"""
SubFile class

@author: Rohan Isaac
"""

from __future__ import division
import struct
import numpy as np

from global_fun import read_subheader

class subFile:
    """ 
    Processes each subfile passed to it, extracts header information and data
    information and places them in data members
    """
    
    def __init__(self, data, fnpts, fexp, txyxy):
        
        # extract subheader info
        self.subflgs, \
            self.subexp, \
            self.subindx, \
            self.subtime, \
            self.subnext, \
            self.subnois, \
            self.subnpts, \
            self.subscan, \
            self.subwlevel, \
            self.subresv \
            = read_subheader(data[:32])
        
        #print read_subheader(data[:32])
        y_dat_pos = 32
            
        print "Global pts", fnpts
        print "Individual pts", self.subnpts
        
        # choose between global stuff and local stuff
        if self.subnpts > 0:
            pts = self.subnpts
        else:
            pts = fnpts
            
        yfloat = False
        if self.subexp == 128:
            print "Floating y-values"
            yfloat = True
        
        if self.subexp > 0 and self.subexp < 128:
            exp = self.subexp
        else:
            exp = fexp
            
        #print "exponent is ", exp, "or", fexp
        
        #--------------------------
        # if x_data present
        #--------------------------
            
        if txyxy:
            x_str = 'i'*pts
            
            #print "Len of str", struct.calcsize(x_str)
            x_dat_pos = y_dat_pos
            x_dat_end = x_dat_pos + (4*pts)
            x_raw = np.array(struct.unpack(x_str, data[x_dat_pos:x_dat_end]))
            self.x = (2**(exp-32))*x_raw
            
            y_dat_pos = x_dat_end
        
        #--------------------------
        # extract y_data
        #--------------------------
            
        if yfloat:
            y_dat_str = 'f'*pts
        else:
            y_dat_str = 'i'*pts
        y_dat_end = y_dat_pos + (4*pts)
        y_raw = np.array(struct.unpack(y_dat_str, data[y_dat_pos:y_dat_end]))
        
        #print "y_data from ", y_dat_pos, " to ", y_dat_end
        
        if yfloat:
            self.y = y_raw
        else:
            self.y = (2**(exp-32))*y_raw
        #print self.y
        
        self.y_int = self.y.astype(int)
            
        # do stuff if subflgs
        # if 1 subfile changed
        # if 8 if peak table should not be used
        # if 128 if subfile modified by arithmetic
               