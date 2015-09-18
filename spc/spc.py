""" 
spc class: main class that starts loading data from Thermo Grams *.SPC
file

@author: Rohan Isaac
"""

from __future__ import division
import struct
import numpy as np 
import matplotlib.pyplot as plt

from sub import subFile
from global_fun import read_subheader, flag_bits

class File:
    """ 
    Starts loading the data from a .SPC spectral file using data from the 
    header. Stores all the attributes of a spectral file:
    
    Data
    ----
    content: Full raw data
    sub[i]: sub file object for each subfileFor each subfile
        sub[i].y
        
    Examples
    --------
    >>> import spc
    >>> ftir_1 = spc.File('/path/to/ftir.spc')
    """
    
    # Format strings for various parts of the file
    # calculate size of strings using `struct.calcsize(string)`
    head_str = "<cccciddicccci9s9sh32s130s30siicchf48sfifc187s"
    old_head_str = "<cchfffcchcccc8shh28s130s30s32s"
    logstc_str = "<iiiii44s" 
    
    # byte positon of various parts of the file
    head_siz = 512
    old_head_siz = 256
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
            print "Read raw data"
            
            
        # extract first two bytes to determine file type version
        
        ftflg, fversn = struct.unpack('<cc',content[:2])
        
        if fversn == 'K': # new LSB 1st
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
                self.txvals = flag_bits(self.ftflg)[::-1]

            # fix data types if necessary
            
            self.fnpts = int(self.fnpts) # #of points should be int
            self.fexp = ord(self.fexp)
            
            self.ffirst = float(self.ffirst)
            self.flast = float(self.flast)
            
            self.flogoff = int(self.flogoff) # byte; should be int
            
            self.fxtype = ord(self.fxtype)
            self.fytype = ord(self.fytype)
            self.fztype = ord(self.fztype)
            
            self.fexper = ord(self.fexper)
            
            # Convert date time to appropriate format
            d = self.fdate
            self.year = d >> 20
            self.month = (d >> 16) % (2**4)
            self.day = (d >> 11) % (2**5)
            self.hour = (d >> 6) % (2**5)
            self.minute = d % (2**6)
            
            # null terminated string
            self.fcmnt = str(self.fcmnt).split('\x00')[0]
            
            print "\nHEADER"

            # options
            # -------    

            sub_pos = self.head_siz
            
            # optional floating point x-values
            if self.txvals: 
                #print "Seperate x-values"
                
                if self.txyxys:
                    print "x-data in subfile"
                else:
                    x_dat_pos = self.head_siz
                    x_dat_end = self.head_siz + (4 * self.fnpts)
                    self.x = np.array([struct.unpack_from('f', content[x_dat_pos:x_dat_end], 4 * i)[0]
                                       for i in range(0, self.fnpts)])
                    sub_pos = x_dat_end
                    print "Read global x-data"
            else:
                print "Generated x-values"
                self.x = np.linspace(self.ffirst,self.flast,num=self.fnpts)
            
            # make a list of subfiles          
            self.sub = []
            
            # for each subfile
            for i in range(self.fnsub):
                print "\nSUBFILE", i, "\n----------"
                #print "start pos", sub_pos
                
                # figure out its size
                subhead_lst = read_subheader(content[sub_pos:(sub_pos+32)])
                #print subhead_lst
                if subhead_lst[6] > 0:
                    pts = subhead_lst[6]
                    print "Using subfile points"
                else:
                    pts = self.fnpts
                    print "Using global subpoints"
                    
                # if xvalues already set, should use that number of points
                # only necessary for f_xy.spc
                if self.fnpts > 0:
                    pts = self.fnpts
                    print "Using global subpoints"
                    
                #print "Points in subfile", pts
                    
                if self.txyxys:
                    dat_siz = (8*pts) + 32
                else:
                    dat_siz = (4*pts) + 32
                    
                #print "Data size", dat_siz
                    
                sub_end = sub_pos + dat_siz
                #print "sub_end", sub_end
                # read into object, add to list
                self.sub.append(subFile(content[sub_pos:sub_end], self.fnpts, self.fexp, self.txyxys))
                # print self.sub[i].y
                # update positions
                sub_pos = sub_end
                
            # flog offset to log data offset not zero (bytes)
            #print "log data position" , self.flogoff
            if self.flogoff: 
                print "Log data exists"
                log_head_end = self.flogoff + self.log_siz
                self.logsizd, \
                    self.logsizm, \
                    self.logtxto, \
                    self.logbins, \
                    self.logdsks, \
                    self.logspar \
                    = struct.unpack(self.logstc_str, content[self.flogoff:log_head_end])
                log_pos = self.flogoff + self.logtxto
                print "Offset to text", self.logtxto
                #print "log stuff", self.logsizd, self.logsizm
                log_end_pos = log_pos + self.logsizd
                self.log_content = content[log_pos:log_end_pos].split('\r\n')
                
                #print self.log_content
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
            print "Boo beep new version LSB"
            
        elif fversn == 'L': # new MSB 1st
            pass # To be implemented
            print "New version MSB"
            
        elif fversn == 'M': # old format
            self.oftflgs, \
                self.oversn, \
                self.oexp, \
                self.onpts, \
                self.ofirst, \
                self.olast, \
                self.oxtype, \
                self.oytype, \
                self.oyear, \
                self.omonth, \
                self.oday, \
                self.ohour, \
                self.ominute, \
                self.ores, \
                self.opeakpt, \
                self.onscans, \
                self.ospare, \
                self.ocmnt, \
                self.ocatxt, \
                self.osubh1 = struct.unpack(self.old_head_str, content[:self.old_head_siz])
            print "Old Version"

        
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
            "Kubelka-Munk", \
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
            xl, yl, zl = self.fcatxt.split('\x00')[:3]
            
            # overwrite only if non zero
            if len(xl) > 0:
                self.pr_xlabel = xl
            if len(yl) > 0:
                self.pr_ylabel = yl
            if len(zl) > 0:
                self.pr_zlabel = zl 
 
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
    def data_txt(self):
        """ Returns x,y column data as a string variable, can be printed to
        standard output or fed to text file."""
        dat = self.pr_xlabel + "\t" + self.pr_ylabel + "\n"
        
        if self.txyxys:
            x = self.sub.x
        else:
            x = self.x
            
        for i in range(self.fnpts):
            dat = dat + str(x[i]) + "\t" 
            for j in range(self.fnsub):
                dat = dat + str(self.sub[j].y[i]) + "\t" 
            dat = dat + "\n"
            
        return dat
            
    def write_file(self, path):
        """ Output x,y data to text file tab seperated, with column headers
        Arguments
        ---------
        path: full path to output file including extension
        """
        f = open(path, 'w')
        f.write(self.data_txt())
        
        
    def print_metadata(self):
        """ Print out select metadata"""
        print "Scan: ", self.log_dict['Comment'], "\n", \
            float(self.log_dict['Start']), "to ", \
            float(self.log_dict['End']), "; ", \
            float(self.log_dict['Increment']), "cm-1;", \
            float(self.log_dict['Integration Time']), "s integration time"
       
    def plot(self):
        """ Plots data, and use column headers"""
        for i in range(self.fnsub):
            plt.plot(self.x,self.sub[i].y)
        
        # add labels
        plt.xlabel(self.pr_xlabel)
        plt.ylabel(self.pr_ylabel)

            
    def debug_info(self):
        """ 
        Interpret flags and header information to debug more about the file 
        format
        """
        print "\nDEBUG INFO"
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
            
        print "Version:", self.pr_versn
            
        # subfiles
        if self.fnsub == 1:
            print "Single file only" 
        else:
            print "Multiple subfiles:", self.fnsub
            
        # multiple y values
        if self.tmulti: 
            print "Multiple y-values"
        else:
            print "Single set of y-values"
            
            
        #print "There are ", self.fnpts, \
        #    " points between ", self.ffirst, \
        #    " and ", self.flast, \
        #    " in steps of ", self.pr_spacing
            


