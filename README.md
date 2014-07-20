# spc

A module for working with .SPC files in Python. SPC is a binary data format to store a variety of spectroscopic data, developed by Thermo Scientific in the '90s. 

Based mainly on the Thermo Scientific SPC File SDK [1]

**Note: Still in development; not stable or accurate for most formats**

###Working

1. Single y-set, generated x-values
2. Log data
3. Basic header information extraction
4. x,y and z labels

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
- class subFile (sub.py)
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

