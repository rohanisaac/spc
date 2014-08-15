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

