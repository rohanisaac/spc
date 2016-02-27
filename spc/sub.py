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

        # header is 32 bytes
        y_dat_pos = 32

        if txyxy:
            # only reason to use subnpts if x data is here
            pts = self.subnpts
        else:
            pts = fnpts

        # Choosing exponent
        # -----------------
        if -128 < self.subexp < 128:
            # if subfile has reasonable exponent, use it
            exp = self.subexp
        elif -128 < fexp < 128:
            # if global exponent is reasonable, use it
            exp = fexp
        else:
            # all else fails, set exp 0
            exp = 0

        # --------------------------
        # if x_data present
        # --------------------------
        if txyxy:
            x_str = '<' + 'i' * pts
            x_dat_pos = y_dat_pos
            x_dat_end = x_dat_pos + (4 * pts)

            x_raw = np.array(struct.unpack(x_str, data[x_dat_pos:x_dat_end]))
            self.x = (2**(exp - 32)) * x_raw

            y_dat_pos = x_dat_end

        # --------------------------
        # extract y_data
        # --------------------------
        y_dat_str = '<'
        if self.subexp == 128:
            # Floating y-values
            y_dat_str += 'f' * pts
            y_dat_end = y_dat_pos + (4 * pts)
            y_raw = np.array(struct.unpack(y_dat_str, data[y_dat_pos:y_dat_end]))
            self.y = y_raw
        else:
            # integer format
            lydata = len(data) - y_dat_pos
            if int(lydata / pts) == 4:
                # 32 bit, using size of subheader to figure out data type
                y_dat_str += 'i' * pts
                y_dat_end = y_dat_pos + (4 * pts)
                y_raw = np.array(struct.unpack(y_dat_str, data[y_dat_pos:y_dat_end]))
                self.y = (2**(exp - 32)) * y_raw
            else:
                # 16 bit
                y_dat_str += 'h' * pts  # short
                y_dat_end = y_dat_pos + (2 * pts)
                y_raw = np.array(struct.unpack(y_dat_str, data[y_dat_pos:y_dat_end]))
                self.y = (2**(exp - 32)) * y_raw


class subFileOld:
    """
    Processes each subfile passed to it, extracts header information and data
    information and places them in data members. Used for the old format where
    the y-values are stored in an odd way

    Data
    ----
    x: x-data (optional)
    y: y-data

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

        # print read_subheader(data[:32])
        y_dat_pos = 32

        # choose between global stuff and local stuff
        # not very accurate for s_xy
        if self.subnpts > 0:  # probably should be > 0
            pts = self.subnpts
            #print "Using local subpoints", pts
        else:
            pts = fnpts
            #print "Using global subpoints", pts

        # if xvalues exists, y values should be the same size (need for s_xy)
        if fnpts > 0:
            pts = fnpts
            #print "Using global subpoints", pts

        yfloat = False
        if self.subexp == 128:
            #print "Floating y-values"
            yfloat = True

        if self.subexp > 0 and self.subexp < 128:
            exp = self.subexp
            #print "Using local exponent", exp
        else:
            exp = fexp
            #print "Using global exponent", exp

        # --------------------------
        # if x_data present
        # --------------------------

        if txyxy:
            x_str = 'i' * pts
            # print "Len of str", struct.calcsize(x_str)
            x_dat_pos = y_dat_pos
            x_dat_end = x_dat_pos + (4 * pts)

            x_raw = np.array(struct.unpack(x_str, data[x_dat_pos:x_dat_end]))
            self.x = (2**(exp - 32)) * x_raw
            #print "Extracted x-data"

            y_dat_pos = x_dat_end

        # --------------------------
        # extract y_data
        # --------------------------

        # for old format, extract the entire array out as 1 bit unsigned
        # integers, swap 1st and 2nd byte, as well as 3rd and 4th byte to get
        # the final integer then scale by the exponent
        if yfloat:
            y_dat_str = '<' + 'f' * pts
        else:
            y_dat_str = '>' + 'B' * 4 * pts
        y_dat_end = y_dat_pos + (4 * pts)

        y_raw = struct.unpack(y_dat_str, data[y_dat_pos:y_dat_end])

        if yfloat:
            self.y = y_raw
            #print "Extracted floating y data"
        else:
            #print "Extracted integer y-data"
            y_int = []
            for i in range(0, len(y_raw), 4):
                y_int.append((
                    y_raw[i + 1] * (256**3) + y_raw[i] * (256**2) +
                    y_raw[i + 3] * (256) + y_raw[i + 2]))
            # fix negative values by casting to np.int32
            self.y_int = np.int32(y_int) / (2**(32 - exp))
            self.y = y_int
        # fix negative values
        # print self.y

        # do stuff if subflgs
        # if 1 subfile changed
        # if 8 if peak table should not be used
        # if 128 if subfile modified by arithmetic
