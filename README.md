spc
===

A module for working with .SPC files in Python. SPC is a binary data format to store a variety of spectroscopic data, developed by Thermo Scientific in the '90s. 

Based mainly on the Thermo Scientific SPC File SDK [1]

Dependencies
------------
numpy
matplotlib (for plotting)


Module Organization
-------------------

class File (spc.py)
	output_txt()
	debug_info()
	plot()
	x
class subFile (sub.py)
	y
	
Examples
--------

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


[1] "Thermo Scientific SPC File Format." Thermo Fisher Scientific, Web. 20 July 2014. <http://ftirsearch.com/features/converters/SPCFileFormat.htm>.

