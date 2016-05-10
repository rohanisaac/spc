"""
Global functions, available to all classes

author: Rohan Isaac
"""
from __future__ import division, absolute_import, unicode_literals, print_function
import struct

# ------------------------------------------------------------------------
# Process subfile data
# ------------------------------------------------------------------------


def read_subheader(subheader):
    """
    Return the subheader as a list

    Parameters
    ----------
    subheader (string):
        32 character string in the subheader format

    Returns
    -------
    list:
        10 item list with the following data members:
        [0] subflgs
        [1] subexp
        [2] subindx
        [3] subtime
        [4] subnext
        [5] subnois
        [6] subnpts
        [7] subscan
        [8] subwlevel
        [9] subresv
    """

    subhead_str = "<cchfffiif4s"
    items = struct.unpack(subhead_str.encode('utf8'), subheader)

    item_cpy = [ord(i) for i in items[:2]]
    item_cpy += items[2:]

    return item_cpy

# ------------------------------------------------------------------------
# Decode a character to boolean array
# ------------------------------------------------------------------------


def flag_bits(n):
    """Return the bits of a byte as a boolean array:

    n (charater):
        8-bit character passed

    Returns
    -------
    list (bool):
        boolean list representing the bits in the byte
        (big endian) ['most sig bit', ... , 'least sig bit' ]

    Example
    -------
    >>> flag_bits('A') # ASCII 65, Binary: 01000001
    [False, True, False, False, False, False, False, True]
    """
    return [x == '1' for x in list('{0:08b}'.format(ord(n)))]
