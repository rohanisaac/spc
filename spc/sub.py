"""
SubFile class: loads each subfile data segment into object

author: Rohan Isaac
"""

from __future__ import division, absolute_import, unicode_literals, print_function

import struct
import numpy as np

from .global_fun import read_subheader


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

    def __init__(self, data, fnpts, fexp, txyxy, tsprec, tmulti):

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
        # choose local vs global exponent depending on tmulti
        if not tmulti:
            exp = fexp
        else:
            exp = self.subexp

        # Make sure it is reasonable, if it out of range zero it
        if not (-128 < exp <= 128):
            exp = 0

        # --------------------------
        # if x_data present
        # --------------------------
        if txyxy:
            x_str = '<' + 'i' * pts
            x_dat_pos = y_dat_pos
            x_dat_end = x_dat_pos + (4 * pts)

            x_raw = np.array(struct.unpack(x_str.encode('utf8'), data[x_dat_pos:x_dat_end]))
            self.x = (2**(exp - 32)) * x_raw

            y_dat_pos = x_dat_end

        # --------------------------
        # extract y_data
        # --------------------------
        y_dat_str = '<'
        if exp == 128:
            # Floating y-values
            y_dat_str += 'f' * pts
            y_dat_end = y_dat_pos + (4 * pts)
            y_raw = np.array(struct.unpack(y_dat_str.encode('utf8'), data[y_dat_pos:y_dat_end]))
            self.y = y_raw
        else:
            # integer format
            # lydata = len(data) - y_dat_pos
            if tsprec:
                # 16 bit
                y_dat_str += 'h' * pts  # short
                y_dat_end = y_dat_pos + (2 * pts)
                y_raw = np.array(struct.unpack(y_dat_str.encode('utf8'), data[y_dat_pos:y_dat_end]))
                self.y = (2**(exp - 16)) * y_raw
            else:
                # 32 bit, using size of subheader to figure out data type
                # actually there is flag for this, use it instead
                # self.tsprec
                y_dat_str += 'i' * pts
                y_dat_end = y_dat_pos + (4 * pts)
                y_raw = np.array(struct.unpack(y_dat_str.encode('utf8'), data[y_dat_pos:y_dat_end]))
                self.y = (2**(exp - 32)) * y_raw


class subFileOld:
    """
    Processes each subfile passed to it, extracts header information and data
    information and places them in data members.

    Used for the old format where the y-values are stored in an odd way

    Data
    ----
    x: x-data (optional)
    y: y-data

    """

    def __init__(self, data, pts, fexp, txyxy):
        # fixed header size
        y_dat_pos = 32

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
            = read_subheader(data[:y_dat_pos])

        # assume it is an integer unless told otherwise
        yfloat = False
        if self.subexp == 128:
            yfloat = True

        # if the sub exp is reasonable, use it
        if self.subexp > 0 and self.subexp < 128:
            exp = self.subexp
        else:
            # or use the global one
            exp = fexp

        # --------------------------
        # if x_data present
        # --------------------------

        if txyxy:
            x_str = 'i' * pts
            x_dat_pos = y_dat_pos
            x_dat_end = x_dat_pos + (4 * pts)

            x_raw = np.array(struct.unpack(x_str.encode('utf8'), data[x_dat_pos:x_dat_end]))
            self.x = (2**(exp - 32)) * x_raw

            y_dat_pos = x_dat_end

        # --------------------------
        # extract y_data
        # --------------------------

        # assuming can't have 2 byte y-values, !! fix maybe
        y_dat_end = y_dat_pos + (4 * pts)
        if yfloat:
            # floats are pretty straigtfoward
            y_dat_str = '<' + 'f' * pts
            y_raw = struct.unpack(y_dat_str.encode('utf8'), data[y_dat_pos:y_dat_end])
            self.y = y_raw
        else:
            # for old format, extract the entire array out as 1 bit unsigned
            # integers, swap 1st and 2nd byte, as well as 3rd and 4th byte to get
            # the final integer then scale by the exponent
            y_dat_str = '>' + 'B' * 4 * pts
            y_raw = struct.unpack(y_dat_str.encode('utf8'), data[y_dat_pos:y_dat_end])

            y_int = []
            for i in range(0, len(y_raw), 4):
                y_int.append((
                    y_raw[i + 1] * (256**3) + y_raw[i] * (256**2) +
                    y_raw[i + 3] * (256) + y_raw[i + 2]))
            # fix negative values by casting to np.int32 (signed int)
            y_int = np.int32(y_int) / (2**(32 - exp))

            self.y = y_int

        # do stuff if subflgs
        # if 1 subfile changed
        # if 8 if peak table should not be used
        # if 128 if subfile modified by arithmetic
