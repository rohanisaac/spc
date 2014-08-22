"""
SubFile class: loads each subfile data segment into object

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
    
    Data
    ----
    x: x-data (optional)
    y: y-data
    y_int: integer y-data if y-data is not floating
    
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
        
        # choose between global stuff and local stuff
        # not very accurate for s_xy
        if self.subnpts > 0: # probably should be > 0 
            pts = self.subnpts
            print "Using local subpoints", pts
        else:
            pts = fnpts
            print "Using global subpoints", pts
            
        # if xvalues exists, y values should be of the same size (need for s_xy)
        if fnpts > 0:
            pts = fnpts
            print "Using global subpoints", pts
            
        yfloat = False
        if self.subexp == 128:
            print "Floating y-values"
            yfloat = True
        
        if self.subexp > 0 and self.subexp < 128:
            exp = self.subexp
            print "Using local exponent", exp
        else:
            exp = fexp
            print "Using global exponent", exp
        
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
            print "Extracted x-data"
            
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
            print "Extracted floating y data"
        else:
            self.y = (2**(exp-32))*y_raw
            print "Extracted integer y-data"
            self.y_int = self.y.astype(int)
        
        #print self.y
            
        # do stuff if subflgs
        # if 1 subfile changed
        # if 8 if peak table should not be used
        # if 128 if subfile modified by arithmetic
               