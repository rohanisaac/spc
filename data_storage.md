Type of SPC files
-----------------

fversn: Old, New

new
===
Thus an SPC trace file normally has these components in the following order:
	SPCHDR		Main header (512 bytes in new format, 224 or 256 in old)
     [X Values]	Optional FNPTS 32-bit floating X values if TXVALS flag
	SUBHDR		Subfile Header for 1st subfile (32 bytes)
	Y Values	FNPTS 32 or 16 bit fixed Y fractions scaled by exponent
     [SUBHDR	]	Optional Subfile Header for 2nd subfile if TMULTI flag
     [Y Values]	Optional FNPTS Y values for 2nd subfile if TMULTI flag
	...		Additional subfiles if TMULTI flag (up to FNSUB total)
     [Log Info]	Optional LOGSTC and log data if flogoff is non-zero

However, files with the TXYXYS ftflgs flag set have these components:
	SPCHDR		Main header (512 bytes in new format)
	SUBHDR		Subfile Header for 1st subfile (32 bytes)
	X Values	FNPTS 32-bit floating X values
	Y Values	FNPTS 32 or 16 bit fixed Y fractions scaled by exponent
     [SUBHDR	]	Subfile Header for 2nd subfile
     [X Values]	FNPTS 32-bit floating X values for 2nd subfile
     [Y Values]	FNPTS Y values for 2nd subfile
	...		Additional subfiles (up to FNSUB total)
     [Directory]	Optional FNSUB SSFSTC entries pointed to by FNPTS
     [Log Info]	Optional LOGSTC and log data if flogoff is non-zero

txvals: X,Y data pairs

txvals and txyxys:
    may have a directory (given by fnpts)
    each subfile has separate x array then y array,
    subfile header gives number of x,y points rather than fnpts

Storing Data
------------
