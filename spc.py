""" 
Python script to decode a Thermo Grams *.SPC file format base
@author: Rohan Isaac

Notes
-----
+ Used format specificiton [1]
+ Loads entire file into memory

To be implemented
-----------------
- Multiple data sets
- Independent x-data
- Old data format

References
----------
[1] Galactic Universal Data Format Specification 9/4/97, SPC.H
http://ftirsearch.com/features/converters/SPCFileFormat.htm
"""

# need to functionalize 
from __future__ import division
import struct
import numpy as np 
import binascii as ba
import matplotlib.pyplot as plt

class File:
    """ 
    Stores all the attributes of a spectral file, including:
        - Full raw data
        - Extracted header file data
        - For each subfile
            + sub file header info extracted
            + data for all axes (generated or read)
            
    Examples
    --------
    >>> import spc
    >>> ftir_1 = spc.File('/path/to/ftir.spc')
    """
    
    format_str = "<cccciddicccci9s9sh32s130s30siicchf48sfifc187s"
    subheader_str = "<cchfffiif4s"
    # if need to check size of above string
    # struct.calcsize(format_str)
    
    # byte positon of various parts of the file
    HEAD_POS = 512
    SUBHEAD_POS = 544
    
    def __init__(self, filename):
        # pretty much everything will be in the constructor
        
        #--------------------------
        # load file
        #--------------------------
        with open(filename, "rb") as fin:
            content = fin.read()
            
        #--------------------------
        # unpack header
        #--------------------------
            
        """
         header string format (c: char, i: int, d: double, f:float, 
         10s: 10 character string; sizes: 1,4,8,4,10 respectively )
         
         use little-endian format with standard sizes 
         (hopefully doesn't vary across platforms, should check)
        """
        
        # Unpack header (using naming scheme in SPC.H header file)
        self.ftflg, \
            self.fversn, \
            self.fexper, \
            self.fexp, \
            self.fnpts, \
            self.ffirst, \
            self.flast, \
            self.fnsub, \
            self.fxtype, \
            self.fytype, \
            self.fztype, \
            self.fpost, \
            self.fdate, \
            self.fres, \
            self.fsource, \
            self.fpeakpt, \
            self.fspare, \
            self.fcmnt, \
            self.fcatxt, \
            self.flogoff, \
            self.fmods, \
            self.fprocs, \
            self.flevel, \
            self.fsampin, \
            self.ffactor, \
            self.fmethod, \
            self.fzinc, \
            self.fwplanes, \
            self.fwinc, \
            self.fwtype, \
            self.freserv \
            = struct.unpack(self.format_str, content[:self.HEAD_POS])
            
        #--------------------------
        # Flag bits
        #--------------------------
            
        self.tsprec, \
        self.tcgram, \
        self.tmulti, \
        self.trandm, \
        self.tordrd, \
        self.talabs, \
        self.txyxys, \
        self.txvals = self.flag_bits(self.ftflg)[::-1]
        
        if self.tsprec:
            print "16-bit y data"
        if self.tcgram:
            print "enable fexper"
        if self.tmulti:
            print "multiple traces"
        if self.trandm:
            print "arb time (z) values"
        if self.tordrd:
            print "ordered but uneven subtimes"
        if self.talabs:
            print "use fcatxt axis not fxtype"
        if self.txyxys:
            print "each subfile has own x's"
        if self.txvals:
            print "floating x-value array preceeds y's"
        
        #--------------------------
        # spc format version
        #--------------------------
        
        if self.fversn == ba.unhexlify('4b'):
            print "new LSB 1st"
        elif self.fversn == ba.unhexlify('4c'):
            print "new MSB 1st"
        elif self.fversn == ba.unhexlify('4d'):
            print "old format (unsupported)"
            
            # beginnings of an implementation
            old_format_str = "<ccifffccicccc8sii28s130s30s32s"
            print struct.calcsize(old_format_str)
        else:
            print "unknown version"
            
        #--------------------------
        # experiment type
        #--------------------------
        fexper_op = ["General SPC", \
            "Gas Chromatogram", \
            "General Chromatogram", \
            "HPLC Chromatogram", \
            "FT-IR, FT-NIR, FT-Raman Spectrum or Igram",\
            "NIR Spectrum", \
            "UV-VIS Spectrum", \
            "X-ray Diffraction Spectrum", \
            "Mass Spectrum ", \
            "NMR Spectrum or FID", \
            "Raman Spectrum",\
            "Fluorescence Spectrum", \
            "Atomic Spectrum", \
            "Chromatography Diode Array Spectra"]
             
        EXP_TYPE = fexper_op[ord(self.fexper)]
        print EXP_TYPE
        
        #--------------------------
        # subfiles or not
        #--------------------------
        self.SUBFILES = int(self.fnsub)
        if self.SUBFILES == 1:
            print "Single file only" 
        else:
            print "Multiple subfiles"
            
        #--------------------------
        # units for x,z,w axes
        #--------------------------
        fxtype_op = ["Arbitrary", \
            "Wavenumber (cm-1)", \
            "Micrometers (um)", \
            "Nanometers (nm)", \
            "Seconds ", \
            "Minutes", "Hertz (Hz)", \
            "Kilohertz (KHz)", \
            "Megahertz (MHz) ", \
            "Mass (M/z)", \
            "Parts per million (PPM)", \
            "Days", \
            "Years", \
            "Raman Shift (cm-1)", \
            "eV", \
            "XYZ text labels in fcatxt (old 0x4D version only)", \
            "Diode Number", \
            "Channel", \
            "Degrees", \
            "Temperature (F)",  \
            "Temperature (C)", \
            "Temperature (K)", \
            "Data Points", \
            "Milliseconds (mSec)", \
            "Microseconds (uSec) ", \
            "Nanoseconds (nSec)", \
            "Gigahertz (GHz)", \
            "Centimeters (cm)", \
            "Meters (m)", \
            "Millimeters (mm)", \
            "Hours"]
             
        fxtype_ord = ord(self.fxtype)
        if fxtype_ord < 30:
            self.xlabel = fxtype_op[fxtype_ord]
        else:
            self.xlabel = "Unknown"
        
            
        #--------------------------
        # units y-axis
        #--------------------------
        
        fytype_op = ["Arbitrary Intensity", \
            "Interferogram", \
            "Absorbance", \
            "Kubelka-Monk", \
            "Counts", \
            "Volts", \
            "Degrees", \
            "Milliamps", \
            "Millimeters", \
            "Millivolts", \
            "Log(1/R)", \
            "Percent", \
            "Intensity", \
            "Relative Intensity", \
            "Energy", \
            "", \
            "Decibel", \
            "", \
            "", \
            "Temperature (F)", \
            "Temperature (C)", \
            "Temperature (K)", \
            "Index of Refraction [N]", \
            "Extinction Coeff. [K]", \
            "Real", \
            "Imaginary", \
            "Complex"]
        
        fytype_op2 = ["Transmission", \
            "Reflectance", \
            "Arbitrary or Single Beam with Valley Peaks",  \
            "Emission" ]
        
        fytype_ord = ord(self.fytype)
        if fytype_ord < 27:
            self.ylabel = fytype_op[fytype_ord]
        elif fytype_ord > 127 and fytype_ord < 132:
            self.ylabel = fytype_op2[fytype_ord - 128]
        else:
            self.ylabel = "Unknown"    
             
        #--------------------------
        # spacing between data
        #--------------------------
        self.PTS = int(self.fnpts)
        self.FIRST = int(self.ffirst)
        self.LAST = int(self.flast)
        self.SPACING = (self.LAST-self.FIRST)/(self.PTS-1)
        print "There are ", self.PTS, " points between ", self.FIRST, \
            " and ", self.LAST, " in steps of ", self.SPACING 
        
        #--------------------------
        # file comment
        #--------------------------
        # only need the first part of the string. some test files seem that there
        # is junk after that
        print str(self.fcmnt).split('\x00')[0]
        
        #--------------------------
        # loop over files
        #--------------------------
        
        for i in range(self.SUBFILES):
            print i
        
        
        #--------------------------
        # decode subheader
        #--------------------------
        
        
        print "Size of sub", struct.calcsize(self.subheader_str)
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
            = struct.unpack(self.subheader_str, content[self.HEAD_POS:self.HEAD_POS+32])
            
        # do stuff if subflgs
            # if 1 subfile changed
            # if 8 if peak table should not be used
            # if 128 if subfile modified by arithmetic
        
        #--------------------------
        # decode x,y-data
        #--------------------------
        
        # header + subheader + mumber of data points (int: 4 bytes)
        # ONLY VALID FOR SINGLE SUBFILES !!! need to fix
        self.DATA_POS = 512 + 32 + (self.PTS*4)
        self.EXP = ord(self.fexp)
        self.PTS = int(self.fnpts)
        
        # generate x-values (np.arange can't generate the correct amount of elements)
        self.x_values = np.zeros(self.PTS)
        for i in range(self.PTS):
            self.x_values[i] = self.ffirst + (self.SPACING*i)
            
        # import the y-data and convert it
        self.y_int = np.array(struct.unpack("i"*self.PTS,content[self.SUBHEAD_POS:self.DATA_POS]))
        
        # conversion string
        self.y_values = (2**(self.EXP-32))*self.y_int
        
        # optionally integerize it
        self.y_values_int = self.y_values.astype(int)
            
        
        #--------------------------
        # find column headers
        #--------------------------    
        
        if self.talabs:
            # if supposed to use fcatxt, split it based on 00 string and only use the 
            # first elements to get the x and y labels
            [self.xl, self.yl] =  self.fcatxt.split('\x00')[:2]
        else:
            [self.xl, self.yl] = [self.xlabel,self.ylabel]
        print self.xl, "\t", self.yl
        for i in range(self.PTS):
            print self.x_values[i], "\t", self.y_values_int[i]
            #, y_values[i]
            continue
        
        

        
        # Optional metadata, check if it exists first 
        metastr = '[SCAN PARAM]\r\n'
        metapos = content.find(metastr)
        if metapos != -1:
            metadata = content[metapos+len(metastr):]
            metalst = metadata.split('\r\n')
            keylst = []
            vallst = []
            for x in metalst[1:-1]:
                [key,val] = x.split('=')
                keylst.append(key)
                vallst.append(val)
                continue
            
            self.metadict = dict(zip(keylst,vallst))
            

                
    def print_metadata(self):
        """ Print out all the metadata"""
        print "Scan: ", self.metadict['Comment'], "\n", \
            float(self.metadict['Start']), "to ", \
            float(self.metadict['End']), "; ", \
            float(self.metadict['Increment']), "cm-1;", \
            float(self.metadict['Integration Time']), "s integration time"
    
                
    def plot(self):
        """ Plots data using col headers"""

        plt.plot(self.x_values,self.y_values)
        plt.xlabel(self.xl)
        plt.ylabel(self.yl)


        
    # write better version, perhaps include in main code upate docs on top
    def flag_bits(self, n):
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
    
