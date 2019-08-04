#!/usr/bin/env python

import os

from distutils.core import setup

ver_file = os.path.join('spc', '_version.py')
with open(ver_file) as f:
    exec(f.read())

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
