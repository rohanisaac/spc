"""
spc class: main class that starts loading data from Thermo Grams *.SPC
file

author: Rohan Isaac
"""
# pylint: disable=invalid-name

from __future__ import division, absolute_import, unicode_literals, print_function
import struct
import numpy as np

from .sub import subFile, subFileOld
from .util import read_subheader, flag_bits

class FileFormat:
    # Format string for various parts of the file
    # Calculate size of strings using `struct.calcsize(string)`
    logstc_str = "<iiiii44s"

    # byte position of various parts of the file
    subhead_siz = 32
    log_siz = 64

    def unpack_flag_bits(self):
        # Flag bits (assuming same)
        self.tsprec, \
            self.tcgram, \
            self.tmulti, \
            self.trandm, \
            self.tordrd, \
            self.talabs, \
            self.txyxys, \
            self.txvals = flag_bits(self.tflgs)[::-1]

        if self.txyxys:
            # x values are given
            self.dat_fmt = '-xy'
        elif self.txvals:
            # only one subfile, which contains the x data
            self.dat_fmt = 'x-y'
        else:
            # no x values are given, but they can be generated
            self.dat_fmt = 'gx-y'

    def set_labels(self):
        """
        Set the x, y, z axis labels using various information in file content
        """

        # --------------------------
        # units for x,z,w axes
        # --------------------------
        fxtype_op = ["Arbitrary",
                     "Wavenumber (cm-1)",
                     "Micrometers (um)",
                     "Nanometers (nm)",
                     "Seconds ",
                     "Minutes", "Hertz (Hz)",
                     "Kilohertz (KHz)",
                     "Megahertz (MHz) ",
                     "Mass (M/z)",
                     "Parts per million (PPM)",
                     "Days",
                     "Years",
                     "Raman Shift (cm-1)",
                     "eV",
                     "XYZ text labels in fcatxt (old 0x4D version only)",
                     "Diode Number",
                     "Channel",
                     "Degrees",
                     "Temperature (F)",
                     "Temperature (C)",
                     "Temperature (K)",
                     "Data Points",
                     "Milliseconds (mSec)",
                     "Microseconds (uSec) ",
                     "Nanoseconds (nSec)",
                     "Gigahertz (GHz)",
                     "Centimeters (cm)",
                     "Meters (m)",
                     "Millimeters (mm)",
                     "Hours"]

        if self.xtype < 30:
            self.xlabel = fxtype_op[self.xtype]
        else:
            self.xlabel = "Unknown"

        if self.ztype < 30:
            self.zlabel = fxtype_op[self.ztype]
        else:
            self.zlabel = "Unknown"

        # --------------------------
        # units y-axis
        # --------------------------

        fytype_op = ["Arbitrary Intensity",
                     "Interferogram",
                     "Absorbance",
                     "Kubelka-Munk",
                     "Counts",
                     "Volts",
                     "Degrees",
                     "Milliamps",
                     "Millimeters",
                     "Millivolts",
                     "Log(1/R)",
                     "Percent",
                     "Intensity",
                     "Relative Intensity",
                     "Energy",
                     "",
                     "Decibel",
                     "",
                     "",
                     "Temperature (F)",
                     "Temperature (C)",
                     "Temperature (K)",
                     "Index of Refraction [N]",
                     "Extinction Coeff. [K]",
                     "Real",
                     "Imaginary",
                     "Complex"]

        fytype_op2 = ["Transmission",
                      "Reflectance",
                      "Arbitrary or Single Beam with Valley Peaks",
                      "Emission"]

        if self.ytype < 27:
            self.ylabel = fytype_op[self.ytype]
        elif 127 < self.ytype < 132:
            self.ylabel = fytype_op2[self.ytype - 128]
        else:
            self.ylabel = "Unknown"

        # --------------------------
        # check if labels are included as text
        # --------------------------

        # split it based on 00 string
        # format x, y, z
        if self.talabs:
            ll = self.catxt.split(b'\x00')
            if len(ll) > 2:
                # make sure there are enough items to extract from
                xl, yl, zl = ll[:3]

                # overwrite only if non zero
                if len(xl) > 0:
                    self.xlabel = xl
                if len(yl) > 0:
                    self.ylabel = yl
                if len(zl) > 0:
                    self.zlabel = zl

    def set_exp_type(self):
        """ Sets the experiment type """

        fexper_op = ["General SPC",
                     "Gas Chromatogram",
                     "General Chromatogram",
                     "HPLC Chromatogram",
                     "FT-IR, FT-NIR, FT-Raman Spectrum or Igram",
                     "NIR Spectrum",
                     "UV-VIS Spectrum",
                     "X-ray Diffraction Spectrum",
                     "Mass Spectrum ",
                     "NMR Spectrum or FID",
                     "Raman Spectrum",
                     "Fluorescence Spectrum",
                     "Atomic Spectrum",
                     "Chromatography Diode Array Spectra"]

        self.exp_type = fexper_op[self.exper]


class OldFormat(FileFormat):
    # Format string for the header
    # Calculate size of strings using `struct.calcsize(string)`
    head_str = "<cchfffcchcccc8shh28s130s30s32s"

    # byte position
    head_siz = 256

    def __init__(self, content):
        self.unpack_header(content)
        self.unpack_flag_bits()

        # can it have separate x values ?
        self.x = np.linspace(self.first, self.last, num=self.npts)

        # make a list of subfiles
        self.sub = []

        # already have subheader from main header, retrace steps
        sub_pos = self.head_siz - self.subhead_siz

        # for each subfile
        # in the old format we don't know how many subfiles to expect,
        # just looping till we run out
        i = 0
        while True:
            try:
                # read in subheader
                subhead_lst = read_subheader(content[sub_pos:sub_pos + self.subhead_siz])

                if subhead_lst[6] > 0:
                    # default to subfile points, unless it is zero
                    pts = subhead_lst[6]
                else:
                    pts = self.npts

                # figure out size of subheader
                dat_siz = (4 * pts)
                sub_end = sub_pos + self.subhead_siz + dat_siz

                # read into object, add to list
                # send it pts since we have already figured that out
                self.sub.append(subFileOld(
                    content[sub_pos:sub_end], pts, self.exp, self.txyxys))
                # update next subfile postion, and index
                sub_pos = sub_end

                i += 1
            except:
                # zero indexed, set the total number of subfile
                self.nsub = i + 1
                break

        print('{}({})'.format(self.dat_fmt, self.nsub))

        self.set_labels()

    def unpack_header(self, content):
        self.tflgs, \
            self.versn, \
            self.exp, \
            self.npts, \
            self.first, \
            self.last, \
            self.xtype, \
            self.ytype, \
            self.year, \
            self.month, \
            self.day, \
            self.hour, \
            self.minute, \
            self.res, \
            self.peakpt, \
            self.nscans, \
            self.spare, \
            self.cmnt, \
            self.catxt, \
            self.subh1 = struct.unpack(self.head_str.encode('utf8'),
                                        content[:self.head_siz])

        # fix data types
        self.exp = int(self.exp)
        self.npts = int(self.npts)  # can't have floating num of pts
        self.first = float(self.first)
        self.last = float(self.last)

        # Date information
        # !! to fix !!
        # Year collected (0=no date/time) - MSB 4 bits are Z type

        # extracted as characters, using ord
        self.month = ord(self.month)
        self.day = ord(self.day)
        self.hour = ord(self.hour)
        self.minute = ord(self.minute)

        # number of scans (? subfiles sometimes ?)
        self.nscans = int(self.nscans)

        # null terminated strings
        self.res = self.res.split(b'\x00')[0]
        self.cmnt = self.cmnt.split(b'\x00')[0]

        self.xtype = ord(self.xtype)
        self.ytype = ord(self.ytype)
        # need to find from year apparently
        self.ztype = 0

class NewFormat(FileFormat):
    # Format string for the header
    # Calculate size of strings using `struct.calcsize(string)`
    head_str = "<cccciddicccci9s9sh32s130s30siicchf48sfifc187s"

    # byte position
    head_siz = 512

    subhead1_pos = head_siz + FileFormat.subhead_siz


class NewFormatLSB(NewFormat):

    def __init__(self, content):
        # use naming scheme in SPC.H header file
        self.unpack_header(content)
        self.unpack_flag_bits()

        # TODO use __repr__ instead?
        print('{}({})'.format(self.dat_fmt, self.nsub))

        sub_pos = self.head_siz

        if not self.txyxys:
            # txyxys don't have global x data
            if self.txvals:
                # if global x data is given
                x_dat_pos = self.head_siz
                x_dat_end = self.head_siz + (4 * self.npts)
                self.x = np.array(
                    [struct.unpack_from(
                        'f', content[x_dat_pos:x_dat_end], 4 * i)[0]
                        for i in range(0, self.npts)])
                sub_pos = x_dat_end
            else:
                # otherwise generate them
                self.x = np.linspace(self.first, self.last, num=self.npts)

        # make a list of subfiles
        self.sub = []

        # if subfile directory is given
        if self.dat_fmt == '-xy' and self.npts > 0:
            self.directory = True
            # loop over entries in directory
            for i in range(0, self.nsub):
                ssfposn, ssfsize, ssftime = struct.unpack(
                    '<iif'.encode('utf8'), content[self.npts + (i * 12):self.npts + ((i + 1) * 12)])
                # add sufile, load defaults for npts and exp
                self.sub.append(subFile(content[ssfposn:ssfposn + ssfsize], 0, 0, True, self.tsprec, self.tmulti))

        else:
            # don't have directory, for each subfile
            for i in range(self.nsub):
                # figure out its size
                if self.txyxys:
                    # use points in subfile
                    subhead_lst = read_subheader(content[sub_pos:(sub_pos + 32)])
                    pts = subhead_lst[6]
                    # 4 bytes each for x and y, and 32 for subheader
                    dat_siz = (8 * pts) + 32
                else:
                    # use global points
                    pts = self.npts
                    dat_siz = (4 * pts) + 32

                sub_end = sub_pos + dat_siz
                # read into object, add to list
                self.sub.append(subFile(content[sub_pos:sub_end],
                                        self.npts, self.exp, self.txyxys, self.tsprec, self.tmulti))
                # update positions
                sub_pos = sub_end

        # if log data exists
        # flog offset to log data offset not zero (bytes)
        if self.logoff:
            log_head_end = self.logoff + self.log_siz
            self.logsizd, \
                self.logsizm, \
                self.logtxto, \
                self.logbins, \
                self.logdsks, \
                self.logspar \
                = struct.unpack(FileFormat.logstc_str.encode('utf8'),
                                content[self.logoff:log_head_end])
            log_pos = self.logoff + self.logtxto

            log_end_pos = log_pos + self.logsizd

            # line endings: get rid of any '\r' and then split on '\n'
            self.log_content = content[log_pos:log_end_pos].replace(b'\r', b'').split(b'\n')

            # split log data into dictionary based on =
            self.log_dict = dict()
            self.log_other = []  # put the rest into a list
            for x in self.log_content:
                if x.find(b'=') >= 0:
                    # stop it from breaking if there is more than 1 =
                    key, value = x.split(b'=')[:2]
                    self.log_dict[key] = value
                else:
                    self.log_other.append(x)

        # call functions
        self.set_labels()
        self.set_exp_type()

    def unpack_header(self, content):
        # use little-endian format with standard sizes
        # use naming scheme in SPC.H header file
        self.tflgs, \
            self.versn, \
            self.exper, \
            self.exp, \
            self.npts, \
            self.first, \
            self.last, \
            self.nsub, \
            self.xtype, \
            self.ytype, \
            self.ztype, \
            self.post, \
            self.date, \
            self.res, \
            self.source, \
            self.peakpt, \
            self.spare, \
            self.cmnt, \
            self.catxt, \
            self.logoff, \
            self.mods, \
            self.procs, \
            self.level, \
            self.sampin, \
            self.factor, \
            self.method, \
            self.zinc, \
            self.wplanes, \
            self.winc, \
            self.wtype, \
            self.reserv \
            = struct.unpack(self.head_str.encode('utf8'), content[:self.head_siz])

        # fix data types if necessary
        self.npts = int(self.npts)
        self.exp = ord(self.exp)

        self.first = float(self.first)
        self.last = float(self.last)

        # spacing between data
        self.spacing = (self.last - self.first) / (self.npts - 1)

        self.logoff = int(self.logoff)  # byte; should be int

        self.xtype = ord(self.xtype)
        self.ytype = ord(self.ytype)
        self.ztype = ord(self.ztype)

        self.exper = ord(self.exper)
        self.cmnt = str(self.cmnt)

        # Convert date time to appropriate format
        d = self.date
        self.year = d >> 20
        self.month = (d >> 16) % (2**4)
        self.day = (d >> 11) % (2**5)
        self.hour = (d >> 6) % (2**5)
        self.minute = d % (2**6)

        # null terminated string, replace null characters with spaces
        # split and join to remove multiple spaces
        try:
            self.cmnt = ' '.join((self.cmnt.replace('\x00', ' ')).split())
        except:
            pass

        # figure out type of file
        self.dat_multi = self.nsub > 1

class NewFormatMSB(NewFormat):
    def __init__(self, content):
        print("New MSB 1st, yet to be implemented")
        pass  # To be implemented

class ShimadzuFormat(FileFormat):
    def __init__(self, content):
        print("Highly experimental format, may not work ")
        raw_data = content[10240:]  # data starts here (maybe every time)
        # spacing between y and x data is atleast 0 bytes
        s_32 = chr(int('0', 2)) * 32
        s_8 = chr(int('0', 2)) * 8  # zero double
        dat_len = raw_data.find(s_32)
        for i in range(dat_len, len(raw_data), 8):
            # find first non zero double
            if raw_data[i:i + 8] != s_8:
                break
        dat_siz = int(dat_len / 8)
        self.y = struct.unpack(('<' + dat_siz * 'd').encode('utf8'), raw_data[:dat_len])
        self.x = struct.unpack(('<' + dat_siz * 'd').encode('utf8'), raw_data[i:i + dat_len])

class File:
    """
    Starts loading the data from a .SPC spectral file using data from the
    header. Stores all the attributes of a spectral file:

    Data
    ----
    content: Full raw data
    sub[i]: sub file object for each subfileFor each subfile
        sub[i].y: y data for each subfile
    x: x-data, global, or for the first subheader

    Examples
    --------
    >>> import spc
    >>> ftir_1 = spc.File('/path/to/ftir.spc')
    """

    # ------------------------------------------------------------------------
    # CONSTRUCTOR
    # ------------------------------------------------------------------------

    def __init__(self, filename):
        # load entire into memory temporarly
        with open(filename, "rb") as fin:
            content = fin.read()
            # print "Read raw data"

        self.length = len(content)
        # extract first two bytes to determine file type version
        # TODO remove self.tflg
        self.tflg, self.versn = struct.unpack('<cc'.encode('utf8'), content[:2])

        # --------------------------------------------
        # NEW FORMAT (LSB)
        # --------------------------------------------
        if self.versn == b'\x4b':
            # format: new LSB 1st
            self.format = NewFormatLSB(content)

        # --------------------------------------------
        # NEW FORMAT (MSB)
        # --------------------------------------------
        elif self.versn == b'\x4c':
            # new MSB 1st
            self.format = NewFormatMSB(content)

        # --------------------------------------------
        # OLD FORMAT
        # --------------------------------------------
        elif self.versn == b'\x4d':
            # old format
            self.format = OldFormat(content)

        # --------------------------------------------
        # SHIMADZU
        # --------------------------------------------
        elif self.versn == b'\xcf':
            self.format = ShimadzuFormat(content)

        else:
            print("File type %s not supported yet. Please add issue. "
                  % hex(ord(self.versn)))
            self.content = content

    # ------------------------------------------------------------------------
    # output
    # ------------------------------------------------------------------------
    def data_txt(self, delimiter='\t', newline='\n'):
        """ Returns x,y column data as a string variable, can be printed to
        standard output or fed to text file.

        Arguments
        ---------
        delimiter: chr (default='\t')
            delimiter character for column separation
        newline: chr (default='\n')
            newline character, may want to use '\r\n' for Windows based output

        Example
        -------
        >>> f.data_txt(newline='\r\n')

        """

        dat = ''
        if self.format.nsub == 1:
            if self.format.dat_fmt.endswith('-xy'):
                x = self.format.sub[0].x
            else:
                x = self.format.x
            y = self.format.sub[0].y

            for x1, y1 in zip(x, y):
                dat += '{}{}{}{}'.format(x1, delimiter, y1, newline)
        else:
            if not self.format.dat_fmt.endswith('-xy'):
                # does not have separate x data
                for i in range(len(self.format.x)):
                    dat += '{}'.format(self.format.x[i])
                    for s in self.format.sub:
                        dat += '{}{}'.format(delimiter, s.y[i])
                    dat += newline
            else:
                # txyxy format, return one long xy file with subfiles
                # separated by blank lines
                for i in self.format.sub:
                    for x1, y1 in zip(i.x, i.y):
                        dat += '{}{}{}{}'.format(x1, delimiter, y1, newline)
                    dat += newline
        return dat

    # Writes out data to a stream (significantly faster than appending to a string)
    def stream_data_txt(self, stream, delimiter='\t', newline='\n'):
        if self.format.nsub == 1:
            if self.format.dat_fmt.endswith('-xy'):
                x = self.format.sub[0].x
            else:
                x = self.format.x
            y = self.sub[0].y

            for x1, y1 in zip(x, y):
                stream.write('{}{}{}{}'.format(x1, delimiter, y1, newline))
        else:
            if not self.format.dat_fmt.endswith('-xy'):
                # does not have separate x data
                for i in range(len(self.format.x)):
                    stream.write('{}'.format(self.format.x[i]))
                    for s in self.format.sub:
                        stream.write('{}{}'.format(delimiter, s.y[i]))
                    stream.write(newline)
            else:
                # txyxy format, return one long xy file with subfiles
                # separated by blank lines
                for i in self.format.sub:
                    for x1, y1 in zip(i.x, i.y):
                        stream.write('{}{}{}{}'.format(x1, delimiter, y1, newline))
                    stream.write(newline)

    def write_file(self, path, delimiter='\t', newline='\n'):
        """ Output x,y data to text file tab seperated

        Arguments
        ---------
        path: str
            full path to output file including extension
        delimiter: chr (default='\t')
            delimiter character for column separation
        newline: chr (default='\n')
            newline character, may want to use '\r\n' for Windows based output

        Example
        -------
        >>> f.writefile('/Users/home/output.txt', delimiter=',')

        """
        with open(path, 'w') as f:
            self.stream_data_txt(f, delimiter, newline)

    def print_metadata(self):
        """ Print out select metadata"""
        print("Scan: ", self.format.log_dict['Comment'], "\n",
              float(self.format.log_dict['Start']), "to ",
              float(self.format.log_dict['End']), "; ",
              float(self.format.log_dict['Increment']), "cm-1;",
              float(self.format.log_dict['Integration Time']), "s integration time")

    def plot(self):
        """ Plots data, and use column headers, returns figure object plotted

        Requires matplotlib installed

        Example
        -------
        >>> f.plot()

        """
        import matplotlib.pyplot as plt
        if self.format.dat_fmt.endswith('-xy'):
            for s in self.format.sub:
                plt.plot(s.x, s.y)
        else:
            x = self.format.x
            for s in self.format.sub:
                plt.plot(x, s.y)
        plt.xlabel(self.format.xlabel)
        plt.ylabel(self.format.ylabel)
        return plt.gcf()

    def debug_info(self):
        """
        Interpret flags and header information to debug more about the file
        format

        Example
        -------

        >>> f.debug_info()
        """
        print("\nDEBUG INFO\nFlags:\n")
        # Flag bits
        if self.format.tsprec:
            print("16-bit y data")
        if self.format.tcgram:
            print("enable fexper")
        if self.format.tmulti:
            print("multiple traces")
        if self.format.trandm:
            print("arb time (z) values")
        if self.format.tordrd:
            print("ordered but uneven subtimes")
        if self.format.talabs:
            print("use fcatxt axis not fxtype")
        if self.format.txyxys:
            print("each subfile has own x's")
        if self.format.txvals:
            print("floating x-value array preceeds y's")

        print('----\n')
        # spc format version
        if self.format.versn == chr(0x4b):
            self.format.pr_versn = "new LSB 1st"
        elif self.format.versn == chr(0x4c):
            self.format.pr_versn = "new MSB 1st"
        elif self.format.versn == chr(0x4d):
            self.format.pr_versn = "old format"
        else:
            self.format.pr_versn = "unknown version"

        print("Version:", self.format.pr_versn)

        # subfiles
        if self.format.nsub == 1:
            print("Single file only")
        else:
            print("Multiple subfiles:", self.format.nsub)

        # multiple y values
        if self.format.tmulti:
            print("Multiple y-values")
        else:
            print("Single set of y-values")

        # print "There are ", self.npts, \
        #    " points between ", self.first, \
        #    " and ", self.last, \
        #    " in steps of ", self.pr_spacing
