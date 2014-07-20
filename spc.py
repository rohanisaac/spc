""" 
Python script to decode a Thermo Grams *.SPC file format base
@author: Rohan Isaac

Notes
-----
+ Used format specificiton [1]
+ Loads entire file into memory
+ Data uses variable naming as in SPC.H
+ Class variables not in SPC.H prefixed with pr_

To be implemented
-----------------
- Multiple data sets
- Independent x-data
- Old data format

References
----------
[1] Galactic Universal Data Format Specification 9/4/97, SPC.H
http://ftirsearch.com/features/converters/SPCFileFormat.htm


---
Plan for the future
-------------------

-Comletely seperate assigning the data to variables to processing the data
-Loop over the subfile data
-Send each subfile to a new object (subFile)
-Subfile decodes the header and the data for each subfile


* Thus an SPC trace file normally has these components in the following order:
*	SPCHDR		Main header (512 bytes in new format, 224 or 256 in old)
*      [X Values]	Optional FNPTS 32-bit floating X values if TXVALS flag
*	SUBHDR		Subfile Header for 1st subfile (32 bytes)
*	Y Values	FNPTS 32 or 16 bit fixed Y fractions scaled by exponent
*      [SUBHDR	]	Optional Subfile Header for 2nd subfile if TMULTI flag
*      [Y Values]	Optional FNPTS Y values for 2nd subfile if TMULTI flag
*	...		Additional subfiles if TMULTI flag (up to FNSUB total)
*      [Log Info]	Optional LOGSTC and log data if flogoff is non-zero

* However, files with the TXYXYS ftflgs flag set have these components:
*	SPCHDR		Main header (512 bytes in new format)
*	SUBHDR		Subfile Header for 1st subfile (32 bytes)
*	X Values	FNPTS 32-bit floating X values
*	Y Values	FNPTS 32 or 16 bit fixed Y fractions scaled by exponent
*      [SUBHDR	]	Subfile Header for 2nd subfile
*      [X Values]	FNPTS 32-bit floating X values for 2nd subfile
*      [Y Values]	FNPTS Y values for 2nd subfile
*	...		Additional subfiles (up to FNSUB total)
*      [Directory]	Optional FNSUB SSFSTC entries pointed to by FNPTS
*      [Log Info]	Optional LOGSTC and log data if flogoff is non-zero


"""

from __future__ import division
import struct
import numpy as np 
import matplotlib.pyplot as plt

from sub import subFile

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
    
    # Format strings for various parts of the file
    # calculate size of strings using `struct.calcsize(string)`
    head_str = "<cccciddicccci9s9sh32s130s30siicchf48sfifc187s"
    old_head_str = "<ccifffccicccc8sii28s130s30s32s"
    logstc_str = "<iiiii44s" 
    
    # byte positon of various parts of the file
    head_siz = 512
    subhead_siz = 32
    log_siz = 64
    
    subhead1_pos = head_siz + subhead_siz
    
    # ------------------------------------------------------------------------
    # CONSTRUCTOR
    # ------------------------------------------------------------------------
    
    def __init__(self, filename):
        # load file
        with open(filename, "rb") as fin:
            content = fin.read()
            
        # unpack header  
        # -------------
        # use little-endian format with standard sizes 
        # use naming scheme in SPC.H header file
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
            = struct.unpack(self.head_str, content[:self.head_siz])

        # Flag bits
        self.tsprec, \
            self.tcgram, \
            self.tmulti, \
            self.trandm, \
            self.tordrd, \
            self.talabs, \
            self.txyxys, \
            self.txvals = self.flag_bits(self.ftflg)[::-1]

        # fix data types if necessary
        
        self.fnpts = int(self.fnpts)
        self.fexp = ord(self.fexp)
        
        self.ffirst = int(self.ffirst)
        self.flast = int(self.flast)
        
        self.flogoff = int(self.flogoff)
        
        self.fxtype = ord(self.fxtype)
        self.fytype = ord(self.fytype)
        self.fztype = ord(self.fztype)
        
        self.fexper = ord(self.fexper)
        
        # null terminated string
        self.fcmnt = str(self.fcmnt).split('\x00')[0]

        # options
        # -------            
        
        # optional floating point x-values
        if self.txvals: 
            print "Seperate x-values"
            if self.txyxys:
                print "x-data in subfile"
            else:
                x_str = 'i'*self.fnpts
                x_dat_pos = self.head_siz
                x_dat_end = self.head_siz + (4*self.fnpts)
                x_raw = np.array(struct.unpack(x_str, content[x_dat_pos:x_dat_end]))
                self.x = (2**(self.fexp-32))*x_raw
        else:
            print "Generated x-values"
            self.x = np.linspace(self.ffirst,self.flast,num=self.fnpts)
        
        # multiple y values
        if self.tmulti: 
            print "Multiple y-values"
            self.sub = []
            sub_pos = self.head_siz
            if self.txyxys:
                sub_siz = self.subhead_siz + 8*self.fnpts
            else:
                sub_siz = self.subhead_siz + 4*self.fnpts
                
            sub_end = sub_pos + sub_siz
            # to be implemented
            for i in range(self.fnsub):
                self.sub.append(subFile(content[sub_pos:sub_end], self.fnpts, self.fexp, self.txyxys))
                sub_pos = sub_pos + sub_siz
                sub_end = sub_end + sub_siz
        else: # single y values
            print "Single set of y-values"
            y_dat_pos = self.head_siz
            y_dat_pos_end = self.head_siz + self.subhead_siz + (4*self.fnpts)
            # each data point is 4 bytes long
            self.sub = subFile(content[y_dat_pos:y_dat_pos_end],self.fnpts,self.fexp,self.txyxys)
            
        # flog offset to log data offset not zero (bytes)
        if self.flogoff: 
            print "Log data exists"
            log_pos = self.flogoff + self.log_siz
            self.logsizd, \
                self.logsizm, \
                self.logtxto, \
                self.logbins, \
                self.logdsks, \
                self.logspar \
                = struct.unpack(self.logstc_str, content[self.flogoff:log_pos])
                
            #print "log stuff", self.logsizd, self.logsizm
            log_end_pos = log_pos + self.logsizd
            self.log_content = content[log_pos:log_end_pos].split('\r\n')
            print self.log_content
            # split log data into dictionary
            self.log_dict = dict()
            self.log_other = [] # put the rest into a list
            for x in self.log_content:
                if x.find('=') >= 0:
                    key, value = x.split('=')
                    self.log_dict[key] = value
                else:
                    self.log_other.append(x)

        # spacing between data
        self.pr_spacing = (self.flast-self.ffirst)/(self.fnpts-1)
        
        # call functions
        self.set_labels()
        self.set_exp_type()
        

    # ------------------------------------------------------------------------
    # Process other data
    # ------------------------------------------------------------------------
    
    def set_labels(self):
        """ 
        Set the x, y, z axis labels using various information in file content 
        """
        
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
             
        
        if self.fxtype < 30:
            self.pr_xlabel = fxtype_op[self.fxtype]
        else:
            self.pr_xlabel = "Unknown"
            
        if self.fztype < 30:
            self.pr_zlabel = fxtype_op[self.fztype]
        else:
            self.pr_zlabel = "Unknown"            
        
            
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
        
        
        if self.fytype < 27:
            self.pr_ylabel = fytype_op[self.fytype]
        elif self.fytype > 127 and self.fytype < 132:
            self.pr_ylabel = fytype_op2[self.fytype - 128]
        else:
            self.pr_ylabel = "Unknown"   
            
        #--------------------------
        # check if labels are included as text
        #--------------------------    
        
        # split it based on 00 string 
        # format x, y, z
        if self.talabs:
            [self.pr_xlabel, self.pr_ylabel, self.pr_zlabel] =  self.fcatxt.split('\x00')[:3]
 
    def set_exp_type(self):
        """ Set the experiment type """
        
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
             
        self.pr_exp_type = fexper_op[self.fexper]
      
    # ------------------------------------------------------------------------
    # output 
    # ------------------------------------------------------------------------
    def output_txt(self):
        """ Output data as plain text, can feed to file later """
        print self.pr_xlabel, "\t", self.pr_ylabel
        
        if self.txyxys:
            x = self.sub.x
        else:
            x = self.x
        y = self.sub.y
        for i in range(self.fnpts):
            print x[i], "\t", y[i]
           
    def print_metadata(self):
        """ Print out select metadata"""
        print "Scan: ", self.metadict['Comment'], "\n", \
            float(self.metadict['Start']), "to ", \
            float(self.metadict['End']), "; ", \
            float(self.metadict['Increment']), "cm-1;", \
            float(self.metadict['Integration Time']), "s integration time"
       
    def plot(self):
        """ Plots data, and use column headers"""
        if self.tmulti:
            ran = len(self.sub)
            for i in range(ran):
                plt.plot(self.x,self.sub[i].y)
        else:
            # single xy data
            if self.txyxys:
                x = self.sub.x
            else:
                x = self.x
            y = self.sub.y
            
            plt.plot(x,y)
            plt.xlabel(self.pr_xlabel)
            plt.ylabel(self.pr_ylabel)

            
    def debug_info(self):
        """ 
        Interpret flags and header information to debug more about the file 
        format
        """
        
        # Flag bits
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
        
        # spc format version        
        if self.fversn == '\0x4b':
            self.pr_versn = "new LSB 1st"
        elif self.fversn == '\0x4c':
            self.pr_versn = "new MSB 1st"
        elif self.fversn == '\0x4d':
            self.pr_versn = "old format (unsupported)"
        else:
            self.pr_versn = "unknown version"
            
        # subfiles
        if self.fnsub == 1:
            print "Single file only" 
        else:
            print "Multiple subfiles:", self.fnsub
            
            
        print "There are ", self.fnpts, \
            " points between ", self.ffirst, \
            " and ", self.flast, \
            " in steps of ", self.pr_spacing
            
    # ------------------------------------------------------------------------
    # helper functions
    # ------------------------------------------------------------------------

        
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

