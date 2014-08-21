# spc
A module for working with .SPC files in Python. SPC is a binary data format to store a variety of spectroscopic data, developed by Thermo Scientific in the '90s. 

The SPC file format can store either single or multiple y-values, and the x-values can either be given explicitly or even spaced x-values can be generated based on initial and final points as well as number of points. In addition the format can store various log data and parameters, as well as various information such as axis labels and scan type.

Based mainly on the Thermo Scientific SPC File SDK [1]

**Note: Does not work with all SPC formats, may not always give accurate results**

## Features
1. Extracts header information into object members
2. For each subfile, extract subfile data into `subFile` class objects `sub[0]` (, `sub[1]`, `sub[2]`, ...)
3. Extract x and y values into numpy `ndarray`
3. Attempts to interpret x,y, and z labels, as well as scan type
4. Member functions to output data in text, or plot using `matplotlib`

###To Be implemented
1. Multiple y data sets
2. z-values
3. Separate x values

###Dependencies
- numpy
- matplotlib (for plotting)

###Module Organization
- class File (spc.py)
	+ output_txt()
	+ debug_info()
	+ plot()
	+ x
	+ log_data
- class subFile (sub.py)
	+ (optional) x
	+ y
	
## Examples
Load a file:

	# import file to python object
	import spc
	ftir_1 = spc.File('/path/to/ftir.spc')
	
	# extract info from header metadata
	ftir_1.debug_info()
	
	# output file data as columns (tab seperated)
	ftir_1.output_txt()
	
	# plot using matplotlib
	ftir_1.plot()

##References
[1] "Thermo Scientific SPC File Format." Thermo Fisher Scientific, Web. 20 July 2014. <http://ftirsearch.com/features/converters/SPCFileFormat.htm>.


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


