#!/usr/bin/env python

from distutils.core import setup

__author__ = "Rohan Isaac"
__author_email__ = "rohan_isaac@yahoo.com"
__version__ = "0.4.0"
__license__ = "GPLv3"

setup(name='spc',
      version=__version__,
      description=__doc__,
      author=__author__,
      author_email=__author_email__,
      url='https://github.com/rohanisaac/spc',
      packages=['spc'],
      install_requires=['numpy'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Chemistry',
        ],
      )
